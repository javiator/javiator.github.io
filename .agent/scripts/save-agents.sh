#!/bin/bash
# save-agents.sh
# Safely commits agent/config files to the shadow-agents branch using a temporary worktree.

BRANCH="shadow-agents"
WT_DIR=".shadow-worktree"
FILES=".agent agents.md SKILLS_GUIDE.md sample-prompts .cursor AGENT_README.md"

# Ensure clean slate
if [ -d "$WT_DIR" ]; then
    echo "Removing stale worktree..."
    git worktree remove -f $WT_DIR
fi

# Create/Connect to branch in worktree
if ! git show-ref --verify --quiet refs/heads/$BRANCH; then
    echo "Initializing orphan branch $BRANCH..."
    # Create a detached worktree first to set up the orphan branch
    git worktree add --detach $WT_DIR
    cd $WT_DIR
    git checkout --orphan $BRANCH
    git rm -rf .
    cd ..
else
    echo "Updating existing branch $BRANCH..."
    git worktree add $WT_DIR $BRANCH
fi

# Clean potentially deleted files from index in the worktree
cd $WT_DIR
# Only remove files that we are managing? No, remove EVERYTHING then re-add what we have.
# This ensures that if we deleted a file locally, it gets deleted in the shadow branch too.
# But shadow branch might contain ONLY these files? YES.
git rm -rf . --ignore-unmatch
cd ..

# Copy files (handling existence)
echo "Copying files to shadow worktree..."
for f in $FILES; do
    if [ -e "$f" ]; then
        # Use cp -r to preserve structure
        cp -r "$f" "$WT_DIR/"
    fi
done

# Commit
cd $WT_DIR
git add .
if git diff --staged --quiet; then
    echo "No changes to save."
else
    git commit -m "Agent Snapshot: $(date)"
    echo "Changes saved to $BRANCH."
fi
cd ..

# Cleanup
git worktree remove -f $WT_DIR
