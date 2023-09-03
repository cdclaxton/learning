# Git

```bash
git config --global user.name "<name>"
git config --global user.email "<email address>"

# Initialise a Git repo in current folder
git init

# Show uncommitted changes
git status

git log
git log --oneline
git log --oneline <filename>  # history for the file

# Add a file to a snapshot (state of project) for next commit
# Staging -- files to include in the next commit
git add <file>
git add <folder>

# Delete and stop tracking a file
git rm <file>

# Commit the staged snapshot with a descriptive message
# Commit ID is a SHA-1 checksum of the commit's contents
git commit -m "<commit message>"

# Include all tracked files in staged snapshot and commit
git commit -a -m "<commit message>"

# Add staged changes to the most recent commit (instead of creating a new one)
git commit --amend

# View contents of a previous snapshot
git checkout <commit ID>
git checkout <branch name>  # Go back to current state

# Tag the most recent commit with a version number
git tag -a v.1.0 -m "<commit message>"
git checkout v1.0  # tag is a shortcut to a commit ID (detached HEAD)

# View list of existing tags
git tag

# Remove a commit (doesn't get deleted from git history)
# Specify commit to undo, not the stable commit to return to
git revert <commit ID>

# Changes all tracked files to match the most recent commit
# Permanently undos changes!
git reset --hard

# Remove all untracked files (permanently undos changes!)
git clean -f

# List existing branches (asterisk denotes branch currently checked out)
git branch

# Create a new branch
git branch <name>  # take current working directory and fork it into a new branch
git checkout <name>

# Create a new branch and check it out
git checkout -b <branch name>

# Take snapshots from a given branch and add them to the current branch
# fast-forward merge -- move tip of current branch to match required branch
git merge <branch>

# Force a merge commit when Git would normally do a fast-forward merge
git merge --no-ff <branch>

# Delete a branch (as long as the branch has been merged)
git branch -d <name>
git branch -D <name>  # delete an unmerged branch

# Rebase (be on branch to move)
# Rewrite repository history with brand new commits
git rebase <branch>

# Interactive rebase -- choose how each commit is transferred to the new base
# p, pick = use commit
# r, reword = use commit, but edit commit message
# e, edit = use commit, but stop for amending
# s, squash = use commit, but meld into previous commit
# f, fixup = like squash, but discard commit message
# x, exec = run command using shell
# b, break = stop here
# d, drop = remove commit
# l, label = label current HEAD with a name
# t, reset = reset HEAD to a label
# m, merge
git rebase -i <branch>  

git rebase --continue
git rebase --abort  # abandon rebase to start from scratch


```


