---
title: "AI Drug Discovery Made Easy: Your Complete Guide to Chemprop on Databricks"
date: 2026-08-20
source: https://www.musfirajamil.com/blog/chemprop-drug-discovery-on-databricks
---

# AI Drug Discovery Made Easy: Your Complete Guide to Chemprop on Databricks

_Notes on using Chemprop, a directed message-passing graph neural network for molecular property prediction, as a managed workflow on Databricks, from loading pretrained models to training multi-task ADMET regressors._

*These are my notes on a Databricks Community technical blog post, ["AI Drug Discovery Made Easy: Your Complete Guide to Chemprop on Databricks."](https://community.databricks.com/t5/technical-blog/ai-drug-discovery-made-easy-your-complete-guide-to-chemprop-on/ba-p/111750) All credit for the original workflow and code goes to the Databricks authors, see the link for the full walkthrough and runnable notebooks.*

Computational drug discovery got a well-known proof point in 2020, when a graph neural network flagged halicin, a compound already sitting in a screening library, as a candidate antibiotic with a structure unlike anything in existing drug classes. That's the pitch for pairing a chemistry-aware model like Chemprop with a platform like Databricks: search chemical space faster, and do it on infrastructure that also handles the data engineering and deployment side.

### What Chemprop actually models

Chemprop is a directed message-passing neural network (D-MPNN) built specifically for molecules. Instead of hand-engineered chemical descriptors, it treats a molecule as a graph, atoms as nodes, bonds as edges, and runs several rounds of message passing so that information about neighboring atoms and bonds propagates through the structure. The result is a learned molecular fingerprint that feeds into a feed-forward network for the actual prediction task, whether that's a classification (toxic / non-toxic) or a regression (solubility, binding affinity, an ADMET property).

### Why run it on Databricks specifically

The argument isn't that Databricks changes the modeling, it's that it removes friction around everything adjacent to modeling. Unity Catalog gives you a governed, discoverable place to keep datasets and registered models so a chemistry team and a data engineering team aren't passing CSVs around. MLflow handles experiment tracking and model registry, so a trained Chemprop model can be logged, versioned, and served without a bespoke deployment pipeline. For a workflow that moves from raw SMILES strings to a served prediction endpoint, having compute, governance, and serving in one place is the practical win.

### The four workflows the guide walks through

The Databricks post runs these against Unity Catalog data and MLflow's registry. To show what's actually happening underneath, the snippets below are trimmed straight from Chemprop's own [example notebooks](https://github.com/chemprop/chemprop/tree/main/examples) (Chemprop is MIT-licensed), Databricks just wraps this with governed data access and managed serving.

**1. Inference with a pretrained model**, loading an existing Chemprop checkpoint and scoring new molecules for a property like aqueous solubility, with no training step at all.

```
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from lightning import pytorch as pl
from chemprop import data, featurizers, models

chemprop_dir = Path.cwd().parent
checkpoint_path = chemprop_dir / "tests" / "data" / "example_model_v2_regression_mol.ckpt"
mpnn = models.MPNN.load_from_checkpoint(checkpoint_path)

test_path = chemprop_dir / "tests" / "data" / "regression" / "mol" / "mol.csv"
df_test = pd.read_csv(test_path)
smis = df_test["smiles"]

test_data = [data.MoleculeDatapoint.from_smi(smi) for smi in smis]
featurizer = featurizers.SimpleMoleculeMolGraphFeaturizer()
test_dset = data.MoleculeDataset(test_data, featurizer=featurizer)
test_loader = data.build_dataloader(test_dset, shuffle=False)

with torch.inference_mode():
 trainer = pl.Trainer(logger=None, accelerator="cpu", devices=1)
 test_preds = trainer.predict(mpnn, test_loader)

df_test["pred"] = np.concatenate(test_preds, axis=0)
```

**2. Training a single-task classifier**, fine-tuning Chemprop on a labeled dataset for a binary property such as toxicity.

```
from pathlib import Path
import pandas as pd
from lightning import pytorch as pl
from chemprop import data, featurizers, models, nn

input_path = Path.cwd().parent / "tests" / "data" / "classification" / "mol.csv"
target_columns = ["NR-AhR", "NR-ER", "SR-ARE", "SR-MMP"]

df_input = pd.read_csv(input_path)
smis = df_input.loc[:, "smiles"].values
ys = df_input.loc[:, target_columns].values
all_data = [data.MoleculeDatapoint.from_smi(smi, y) for smi, y in zip(smis, ys)]

mols = [d.mol for d in all_data]
train_indices, val_indices, test_indices = data.make_split_indices(mols, "random", (0.8, 0.1, 0.1))
train_data, val_data, test_data = data.split_data_by_indices(all_data, train_indices, val_indices, test_indices)

featurizer = featurizers.SimpleMoleculeMolGraphFeaturizer()
train_dset = data.MoleculeDataset(train_data[0], featurizer)
val_dset = data.MoleculeDataset(val_data[0], featurizer)
test_dset = data.MoleculeDataset(test_data[0], featurizer)

train_loader = data.build_dataloader(train_dset)
val_loader = data.build_dataloader(val_dset, shuffle=False)
test_loader = data.build_dataloader(test_dset, shuffle=False)

mp = nn.BondMessagePassing()
agg = nn.MeanAggregation()
ffn = nn.BinaryClassificationFFN(n_tasks=len(target_columns))
mpnn = models.MPNN(mp, agg, ffn, batch_norm=False)

trainer = pl.Trainer(
 accelerator="cpu", devices=1, max_epochs=20, enable_checkpointing=True,
)
trainer.fit(mpnn, train_loader, val_loader)
results = trainer.test(mpnn, test_loader)
```

**3. Serving via MLflow's registry**, pulling a registered model back out of Unity Catalog/MLflow for inference, which is the pattern you'd actually use once a model is production-bound rather than sitting in a notebook. This part is Databricks/MLflow plumbing rather than Chemprop code, so see the original post for that snippet.

**4. Multi-task ADMET regression**, training one model to predict several absorption/distribution/metabolism/excretion/toxicity endpoints simultaneously, which is closer to how a real drug-candidate triage pipeline would be structured than any single-property demo.

```
from pathlib import Path
import torch
import pandas as pd
from lightning import pytorch as pl
from chemprop import data, models, nn

input_path = Path.cwd().parent / "tests" / "data" / "regression" / "mol_multitask.csv"
target_columns = ["mu", "alpha", "homo", "lumo", "gap", "r2", "zpve", "cv", "u0", "u298", "h298", "g298"]

df_input = pd.read_csv(input_path)
smis = df_input.loc[:, "smiles"].values
ys = df_input.loc[:, target_columns].values
datapoints = [data.MoleculeDatapoint.from_smi(smi, y) for smi, y in zip(smis, ys)]

split_indices = data.make_split_indices(datapoints)
train_data, val_data, test_data = data.split_data_by_indices(datapoints, *split_indices)
train_dset = data.MoleculeDataset(train_data[0])
val_dset = data.MoleculeDataset(val_data[0])
test_dset = data.MoleculeDataset(test_data[0])

output_scaler = train_dset.normalize_targets()
val_dset.normalize_targets(output_scaler)
train_loader = data.build_dataloader(train_dset)
val_loader = data.build_dataloader(val_dset)
test_loader = data.build_dataloader(test_dset)

output_transform = nn.transforms.UnscaleTransform.from_standard_scaler(output_scaler)
ffn = nn.RegressionFFN(n_tasks=len(target_columns), output_transform=output_transform)
chemprop_model = models.MPNN(nn.BondMessagePassing(), nn.MeanAggregation(), ffn)

trainer = pl.Trainer(logger=False, enable_checkpointing=False, max_epochs=1)
trainer.fit(chemprop_model, train_loader, val_loader)

preds = trainer.predict(chemprop_model, test_loader)
preds = torch.concat(preds, axis=1)
```

### Takeaway

The interesting part isn't that Chemprop works, message-passing GNNs for molecular property prediction are well established, it's the integration story: a specialized chemistry model dropped into a general-purpose data platform's governance and serving layer, so the same infrastructure that tracks a churn model can track a toxicity classifier. Worth reading the full post for the actual notebook code and the ADMET multi-task setup in detail.
