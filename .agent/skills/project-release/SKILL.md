---
name: project-release
description: Automate project releases with documentation updates, professional commit messages, semantic versioning, and git tagging. Use when the user asks to update docs, make a release, commit changes professionally, create version tags, or push updates to remote. Triggers on phrases like "update", "release", "commit like a boss", "version tag", or "push to remote".
---

# Project Release Skill

Streamlines the release process: analyze changes → update docs → commit → tag → push.

## Quick Reference

| Step | Action |
|------|--------|
| 1 | `git diff --stat` - Review changes |
| 2 | Update README.md, CLAUDE.md, RELEASE_NOTES.md |
| 3 | `git add -A` |
| 4 | `git commit -m "<professional message>"` |
| 5 | `git tag -a vX.Y.Z -m "..."` |
| 6 | `git push origin main --tags` |

## Commit Message Format

```
<type>(<scope>): <short summary>

<body with details>

- Bullet points for specifics
```

### Types
| Type | Use For |
|------|---------|
| `feat` | New features |
| `fix` | Bug fixes |
| `docs` | Documentation only |
| `refactor` | Code restructuring |
| `perf` | Performance improvements |
| `chore` | Maintenance tasks |

### Examples

**Feature:**
```
feat(weather): add Open-Meteo weather display

Implement weather screen with current conditions:
- Add WeatherAPI client with 10s timeout
- Show temperature, status, high/low
- Auto-refresh every 10 minutes
```

**Bug fix:**
```
fix(display): resolve freezing during long operation

Add incremental sleeps and garbage collection to prevent
memory exhaustion on extended runs.
```

## Semantic Versioning

Format: `vMAJOR.MINOR.PATCH`

| Change Type | Bump | Example |
|-------------|------|---------|
| Breaking changes | MAJOR | v1.0.0 → v2.0.0 |
| New features | MINOR | v1.0.0 → v1.1.0 |
| Bug fixes | PATCH | v1.0.0 → v1.0.1 |

Check existing: `git tag --list`

## Documentation Updates

### README.md
- Features list
- Usage instructions
- File structure
- Troubleshooting

### CLAUDE.md
- Architecture diagram
- Key components
- Development patterns
- Common tasks

### RELEASE_NOTES.md
```markdown
## [vX.Y.Z] - YYYY-MM-DD

### Added
- New features

### Changed
- Modified behavior

### Fixed
- Bug fixes
```
