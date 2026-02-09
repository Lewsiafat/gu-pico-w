---
description: Update documentation (README.md, CLAUDE.md, RELEASE_NOTES.md), write professional commit, tag version, and push to remote
---

# Update Workflow

Use this workflow when making a release or significant update to the project.

## Step 1: Analyze Changes

Review all uncommitted changes to understand what was modified:

```bash
git diff --stat
git diff
```

Also check recent commits if needed:

```bash
git log --oneline -10
```

## Step 2: Update Documentation

Update the following markdown files based on the changes:

### README.md
- Update features list if new functionality added
- Update usage instructions if behavior changed
- Update file list in "Upload Files" section if new files added
- Update troubleshooting if relevant

### CLAUDE.md
- Update architecture section if files added/removed
- Update key components if APIs changed
- Update development patterns if new patterns introduced
- Update common tasks if workflows changed

### RELEASE_NOTES.md
Create/update with the following format:

```markdown
# Release Notes

## [vX.Y.Z] - YYYY-MM-DD

### Added
- New feature descriptions

### Changed
- Modified behavior descriptions

### Fixed
- Bug fix descriptions

### Removed
- Removed feature descriptions
```

## Step 3: Stage All Changes

// turbo
```bash
git add -A
```

## Step 4: Write Professional Commit Message

Write a commit message following this format:

```
<type>(<scope>): <short summary>

<detailed description of changes>

- Bullet point 1
- Bullet point 2
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`

Example:
```
feat(weather): Add weather display with Open-Meteo integration

Implement weather screen showing current conditions and forecast:

- Add WeatherAPI client with automatic retry and timeout handling
- Add weather screen to GUDisplay with temperature and status
- Implement button B for switching to weather view
- Auto-refresh weather data every 10 minutes
```

```bash
git commit -m "<your professional commit message>"
```

## Step 5: Create Version Tag

Determine version number using semantic versioning:
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

First, check existing tags:

// turbo
```bash
git tag --list
```

Then create a new tag:

```bash
git tag -a vX.Y.Z -m "Version X.Y.Z - <brief description>"
```

## Step 6: Push to Remote with Tags

// turbo
```bash
git push origin main --tags
```

Or if using a different branch:

```bash
git push origin <branch-name> --tags
```

---

## Quick Reference

| Step | Command |
|------|---------|
| Check changes | `git diff --stat` |
| Stage all | `git add -A` |
| Commit | `git commit -m "..."` |
| Tag | `git tag -a vX.Y.Z -m "..."` |
| Push with tags | `git push origin main --tags` |
