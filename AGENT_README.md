# Agent Configuration & Shadow Branch Guide

This repository uses a **Shadow Branch Strategy** to isolate AI agent configuration files, prompts, and personal settings from the main project history. This prevents them from being accidentally merged into `master` or shared publicly if desired, while still maintaining version control.

## Ignored Files

The following files and directories are ignored in the main branch (via `.gitignore`) but tracked in the `shadow-agents` branch:

- `.agent/` (Agent configuration and scripts)
- `agents.md` (Main agent context)
- `SKILLS_GUIDE.md` (Guide for agent skills)
- `sample-prompts/` (Collection of prompts)
- `.cursor/` (Cursor IDE rules and settings)
- `AGENT_README.md` (This file)

## Workflow

### 1. Saving Changes

When you update any of the files listed above, you must manually save them to the shadow branch. They are ignored by normal git commands.

Run the save script:

```bash
./.agent/scripts/save-agents.sh
```

This script will:
1.  Stash any pending changes in your current branch.
2.  Switch to the `shadow-agents` branch in a temporary worktree.
3.  Commit the current state of the ignored files.
4.  Push the commit to the shadow branch history.

### 2. Restoring Files

If you switch machines, clone the repo afresh, or accidentally delete these files, you can restore them from the shadow branch.

Run the restore script:

```bash
./.agent/scripts/restore-agents.sh
```

This script will checkout the latest version of the ignored files from `shadow-agents` into your current directory.

## Maintenance

The `shadow-agents` branch is an orphan branch that only strictly tracks these specific files. It does not share history with `master` or other feature branches.
