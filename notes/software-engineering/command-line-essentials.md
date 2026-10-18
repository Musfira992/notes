---
title: "Command Line Essentials"
date: 2026-08-20
source: https://www.musfirajamil.com/primers/command-line-basics-command-line-essentials
---

# Command Line Essentials

_A beginner reference for navigating, managing, viewing, and searching files from the terminal, with bioinformatics examples._

File management is one of the first things you'll do in the command line, whether
you're organizing scripts, moving sequencing data, or setting up analysis
folders. These commands help you navigate and manipulate files efficiently.

## Quick reference

| Command | Description |
| --- | --- |
| `pwd` | Show current directory path |
| `ls` | List files and directories |
| `cd` | Change directory |
| `touch` | Create empty files |
| `mkdir` | Create directories |
| `cp` | Copy files or directories |
| `mv` | Move or rename files or directories |
| `rm` | Remove files or directories |
| `cat` | View or concatenate files |
| `grep` | Search for a text pattern within a file or output |
| `head` and `tail` | View the top and bottom of a file |
| `less` | View a file one page at a time |
| `man` | Show a command's manual |

## General structure of a Linux command

**1. The command: the "what"**

The command is the name of the program or tool you want to run. It represents
the action you want to take.

- **Examples:** `ls` (list files), `rm` (remove), or `mkdir` (make directory).

**2. Options: the "how"**

Options (also called flags) modify how the command behaves. They allow you to
tweak the output or the intensity of the action. They usually start with a single
dash (`-`) for the short form or two dashes (`--`) for full words.

- **Example:** `ls -l`. Here, `-l` tells the computer to show the list in "long"
  format, giving you extra details like file size and modification date.

Use `man [command]` (manual) or `[command] --help` to find every available option
for a given command.

**3. Arguments: the "target"**

The argument is the subject of your command. It tells the program what it should
act on, such as a specific file, a folder, or a path.

- **Example:** `mkdir Projects`. Here, `mkdir` is the command, and `Projects` is
  the argument: the name of the folder you want to create.

Some commands require at least one argument (e.g. `mkdir Projects`), while others
don't need any at all (e.g. `cd`).

**Cancelling a command:** press `Ctrl + C` to cancel a running command.


## File and directory navigation

### 1. `pwd`: print working directory

Displays the full path of your current location.

```bash
pwd
# /home/user/projects/genomics
```

**Important consideration:** this is especially useful when writing scripts or
running pipelines, so you always know where files are being read from or saved to.

### 2. `ls`: list files and directories

Lists the files and folders in the current directory.

```bash
ls [options]
```

Common useful options:

- `ls -l`: long format, including permissions, size, owner, and modification date
- `ls -a`: shows hidden files (files starting with `.`)
- `ls -lh`: human-readable file sizes (KB, MB, GB)

**Important consideration:** hidden files (like `.bashrc` or `.config`) often
store system or environment settings, so `ls -a` is useful when troubleshooting
or configuring tools.

### 3. `cd`: change directory

Moves you between folders.

```bash
cd [directory_path]
```

Basic navigation:

- `cd ~`: goes to your home directory (the base folder for your user)
- `cd /`: moves to the root directory (the very top of the entire system)
- `cd ..`: moves one level up
- `cd -`: takes you back to the directory you were just in (like a "back" button)

**Relative vs. absolute paths:**

- `cd folder_name`: moves down into a folder inside your current location
- `cd ../..`: moves up two levels at once
- `cd ~/Desktop/Project`: jumps directly to a specific folder, regardless of
  where you are starting from

**Important consideration:** most bioinformatics workflows involve moving through
nested folders (raw data → processed data → results), so mastering `cd` is
essential for not getting "lost" in directory structures.


## File management

### 4. `touch`: create empty files

Creates a new empty file.

```bash
touch [file_name]
```

**Best practices for naming files and folders.** Follow these conventions to
avoid data loss and syntax errors:

- **Stick to lowercase:** most shell commands are lowercase, so you won't have to
  keep toggling Caps Lock. This also avoids confusion on case-insensitive systems
  like Windows and (by default) macOS, where `File.txt` and `file.txt` are the same item.
- **Limit your characters:** stick to letters, numbers, underscores (`_`), and
  hyphens (`-`).
- **Avoid spaces:** spaces need "escaping" in the terminal, which makes commands
  clunky. Use an underscore or hyphen instead (e.g. `my_project` instead of
  `my project`).
- **Use standard extensions:** always include a clear file extension (like `.txt`
  or `.sh`) so both you and the system know what the file is.

### 5. `mkdir`: create directories

Creates new folders.

```bash
mkdir [folder_name]
mkdir -p [directory_path]   # create nested directories
```

**Example:** `mkdir -p project/raw_data/fastq_files`

**Important consideration:** `-p` is short for "parents". It tells the system to
create any missing parent folders in the path. Without it, the command would fail
if `project` or `raw_data` didn't already exist. This is very useful in
bioinformatics, where projects often need deeply nested directories for raw data,
scripts, results, and metadata.

### 6. `cp`: copy files or directories

Copies a file to a new name, or into another folder.

```bash
cp [options] source destination
cp file.txt new_file.txt
cp file.txt /home/user/backup/
```

Common useful options:

- `-r` (recursive): copies an entire folder and all its contents, e.g. `cp -r Projects/ Backup`
- `-i` (interactive): asks before overwriting an existing file, e.g. `cp -i file.txt destination/`
- `-v` (verbose): shows exactly what is being copied, e.g. `cp -v file.txt backup/`

**Important consideration:** always double-check destination paths. Unlike a
graphical interface, the command line will not ask for confirmation in most cases.

### 7. `mv`: move or rename files

Used for both moving and renaming.

```bash
mv oldname.txt newname.txt          # rename
mv file.txt /home/user/Documents/   # move
```

**Important consideration:** `mv` does not make a copy; it *removes the
original*. If the destination already has a file with the same name, it may be
overwritten without warning.

### 8. `rm`: remove files or directories

Deletes files or folders.

```bash
rm [file_name]
```

Common useful options:

- `-r` (recursive): removes a directory and everything in it, including sub-folders
- `-i` (interactive): asks for confirmation before deleting each file

**Critical warning:** deleted files are not sent to a recycle bin. They are
usually gone for good. Use `rm -r` with extreme caution, especially around
important data or project directories.


## Viewing and searching file contents

### 9. `cat`: display and concatenate

Shows the contents of a file, or joins several files together.

```bash
cat [file_name]
cat [file_1] [file_2] [file_3]
```

### 10. `grep`: search for text

Searches for a pattern or text in files or command output.

```bash
grep [options] "pattern" [file_name]
```

Common useful options:

- `-c`: counts matching lines (not individual occurrences)
- `-i`: case-insensitive search
- `-r` (recursive): searches all files in a folder and its sub-folders

In bioinformatics, `grep` is commonly used for counting sequences and finding motifs:

```bash
grep -c ">" sequences.fasta        # count the sequences in a FASTA file
grep "ATCTGACC" sample.fastq       # find reads containing a motif
```

### 11. `head` and `tail`: view the top and bottom of a file

`head` and `tail` are quick sanity checks when working with big files. By
default they show the first and last 10 lines, and they work on multiple files.

```bash
head [options] [file_name]
tail [options] [file_name]
head -n 20 sample_file             # show the first 20 lines
```

### 12. `less`: page-by-page viewer

Like `head` and `tail`, `less` previews large files. It opens one page at a time
and lets you scroll forward and backward.

```bash
less [options] [file_name]
```

**Navigation shortcuts:** space for the next page, `b` for the previous page, and
`q` to quit.


## Glossary

- **Directory / sub-directory:** the technical terms for what most people call
  "folders". A directory is a location where files are stored, and a
  sub-directory is a directory inside another one.
- **Folder / sub-folder:** the graphical terms for directories. In the terminal,
  "folder" and "directory" mean exactly the same thing.

**Directory separator.** Linux and macOS use the forward slash (`/`) to separate
folder names in a path, or a folder from a file.

- **The root directory:** a single `/` at the very start of a path is the top-level
  directory of the entire system.
- **Defining paths:** in `project/raw_data/sample.fastq`, the slashes tell Linux
  that `sample.fastq` is inside `raw_data`, which is inside `project`.
- **Windows** traditionally uses the backslash (`\`) instead.

**Tip:** in the terminal, always use the forward slash. Linux treats a backslash
as an "escape character" (telling the system to ignore the special meaning of the
next character), so a backslash in a path will make your command fail.

**Absolute vs. relative paths**

- **Absolute path:** the full address of a file or folder. It always starts from
  the root (`/`) and works no matter where you are in the terminal.
  Example: `/home/user/project/data.txt`
- **Relative path:** a shortcut based on your current location (`pwd`). If you are
  already in the `project` folder, the relative path to your file is just
  `data.txt`.
