---
title: "Git Essentials"
date: 2026-09-06
source: https://www.musfirajamil.com/blog/git-essentials
---

# Git Essentials

_The Git daily loop for scientific and data work, status, diff, commit, branch, and safe undo, without drowning in advanced history surgery._

Git is the shared memory of a software or analysis project. For data analysts and bioinformaticians, it is how you recover yesterday's working script, review a colleague's change to a pipeline, and explain exactly which code produced a figure. You do not need every advanced command, a solid essentials kit covers most real work.

## Why Git matters in scientific data work

Analyses evolve. Parameters change. Reviewers ask for a tweak six months later. Git gives you a chronological story of those decisions. Pair it with clear commits and you can reconstruct not only *what* changed, but often *why*.

Keep large raw data out of Git. Version the code, configs, and small metadata; store bulky omics files in appropriate data stores and record accessions or checksums in the repo.

## The daily loop

```
git status
git diff
git add path/to/file
git commit -m "Describe why this change exists"
git push
```

`status` and `diff` are your habits before every commit. Read the diff. Accidental notebook outputs and credentials show up there more often than anyone likes to admit.

## Clone, branch, merge

```
git clone git@example.com:org/project.git
git checkout -b feature/qc-filters
# ... edit ...
git add -p
git commit -m "Tighten CPM filter for low-depth libraries"
git checkout main
git pull
git merge feature/qc-filters
```

Branches let you try ideas without breaking `main`. Name them for intent (`fix/sample-sheet-join`, `docs/readme-setup`). Prefer small branches that are easy to review.

## Write commits for humans

A good commit message completes the sentence "This commit will...". Focus on motivation:

* Good: *Exclude control wells from normalisation cohort*
* Weak: *Update script*

Atomic commits, one logical change each, make reverts and archaeology easier.

## Inspect history without fear

```
git log --oneline -n 20
git log -p -- path/to/file
git blame path/to/file
git show COMMIT
```

`blame` is not about blame, it answers "when did this line arrive?". Combined with `log -p`, it is the fastest way to understand surprising behaviour in a shared pipeline.

## Undo safely

Common, relatively safe moves:

```
git restore file.py # discard unstaged edits to a file
git restore --staged file.py # unstage
git revert COMMIT # add a new commit that undoes a past one
git reset --soft HEAD~1 # undo last commit, keep changes staged
```

Avoid rewriting published history on shared branches (`reset --hard`, force-push) unless the team explicitly agrees. Prefer `revert` for changes already on `main`.

## .gitignore for analysis repos

Ignore the noise: virtualenvs, `__pycache__`, large intermediates, local secrets, and notebook checkpoint folders. Commit an example env file (`.env.example`) instead of real credentials. Never commit API keys or private key files, rotate immediately if you slip.

```
.venv/
__pycache__/
data/raw/
*.h5ad
.env
.ipynb_checkpoints/
```

## Collaboration basics

* Pull before you push.
* Use pull requests for anything non-trivial, review is part of quality control.
* Resolve conflicts calmly: understand both sides, do not simply accept theirs or yours blindly.
* Tag releases when a pipeline version underpins a paper or production dashboard (`v1.2.0`).

## A minimal mental model

1. Working tree, your files now.
2. Staging area, what the next commit will include.
3. Repository history, commits on branches.
4. Remote, the shared copy on the server.

Master moving changes deliberately between those layers and Git stops feeling mystical. Essentials first; rebases and advanced history surgery can wait until the daily loop is second nature.
