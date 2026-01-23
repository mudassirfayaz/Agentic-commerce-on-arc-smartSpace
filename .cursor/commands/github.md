---
name: /github
id: github
category: Git
description: Display repository structure, flow, and automatically handle GitHub operations (pull, push, commit, status).
---

**Guardrails**
- Always check git status before making changes to avoid conflicts.
- Never force push to main/master branches unless explicitly requested.
- Ask for confirmation before committing changes if there are many untracked or modified files.
- Preserve the repository structure and avoid destructive operations.

**Repository Information**
When called, first display:
1. **Current Status**: Run `git status` to show working directory state
2. **Branch Information**: Run `git branch -a` to show all local and remote branches
3. **Remote Configuration**: Run `git remote -v` to show remote repositories
4. **Repository Structure**: Display the main directory structure (backend/, frontend/, openspec/, etc.)
5. **Recent Commits**: Run `git log --oneline -10` to show recent commit history

**Automatic Workflow**
Execute these steps in order:

1. **Pull Latest Changes**
   - Run `git fetch origin` to fetch latest changes from remote
   - Check if current branch is behind: `git status`
   - If behind, run `git pull origin <current-branch>` to update local branch
   - If there are conflicts, report them and wait for resolution

2. **Stage Changes**
   - Check what needs to be staged: `git status`
   - For modified/deleted files: `git add -u` (stages all modified and deleted files)
   - For untracked files: Ask user which files to add, or use `git add .` if explicitly requested
   - Show staged changes: `git status`

3. **Commit Changes** (if there are staged changes)
   - If no commit message provided, generate a descriptive one based on `git diff --cached --stat`
   - Run `git commit -m "<message>"` with an appropriate message
   - Format: Use conventional commits format when possible (feat:, fix:, docs:, refactor:, etc.)

4. **Push Changes** (if there are commits to push)
   - Check if branch is ahead: `git status`
   - If ahead, run `git push origin <current-branch>`
   - If push fails, report the error and suggest solutions

**Repository Structure Overview**
Display the main structure:
```
├── backend/          # Backend API and services
│   ├── agentic/      # Agentic system components
│   ├── src/          # Source code
│   └── tests/        # Backend tests
├── frontend/         # Frontend React application
│   ├── src/          # Source code
│   └── public/       # Static assets
├── openspec/         # OpenSpec documentation and changes
│   ├── changes/      # Change proposals and implementations
│   └── specs/        # Specification documents
└── .cursor/          # Cursor IDE configuration
```

**Common Operations**

- **Sync with Remote**: Pull latest, merge if needed, push local changes
- **Create Branch**: `git checkout -b <branch-name>` (ask for branch name)
- **Switch Branch**: `git checkout <branch-name>` (list available branches first)
- **View Diffs**: `git diff` for unstaged, `git diff --cached` for staged
- **View Log**: `git log --oneline --graph -20` for visual history
- **Checkout File**: `git checkout -- <file>` to discard changes (ask for confirmation)

**Error Handling**
- If pull fails due to conflicts: Report conflicts, show conflicted files, wait for resolution
- If push fails: Check if branch exists remotely, suggest creating upstream branch if needed
- If authentication fails: Suggest checking credentials or SSH keys
- If repository is not initialized: Report and suggest `git init`

**Reference**
- Current remote: `https://github.com/mudassirfayaz/Agentic-commerce-on-arc-smartSpace.git`
- Default branch: `main`
- Use `git status` frequently to keep track of repository state
- Use `git log --oneline --graph --all` to visualize branch structure

