#!/bin/bash
# restore-agents.sh
# Restores agent/config files from the shadow-agents branch to the current working directory.

BRANCH="shadow-agents"
FILES=".agent agents.md SKILLS_GUIDE.md sample-prompts .cursor AGENT_README.md"

if ! git show-ref --verify --quiet refs/heads/$BRANCH; then
    echo "Error: Branch '$BRANCH' does not exist."
    exit 1
fi

echo "Restoring agent files from $BRANCH..."
# Checkout files from the shadow branch (overwrite local)
# Since these files are/will be ignored in current branch, this is safe and won't conflict with tracked files.
git checkout $BRANCH -- $FILES 2>/dev/null || echo "Some files could not be restored (may not exist in shadow branch yet)."

echo "Done."
