# Changelog

All notable changes follow [Keep a Changelog](https://keepachangelog.com/) and [SemVer](https://semver.org/).
Released versions are listed under [GitHub Releases](https://github.com/KeilerHirsch/claude-bordcomputer-sounds/releases).

## [Unreleased]

## [1.0.1] - 2026-07-14

### Security
- ECC audit pass (ruff clean, bandit 14 → 0). Added `pyproject.toml [tool.bandit]`
  documenting the accepted audio-shell pattern (the whole tool shells to the OS audio
  player with a fixed list-form argv and no shell, and fails silent so a missing player
  never breaks the hook chain; the played name is validated to `[A-Za-z0-9_-]+`), plus an
  inline `nosec` on the single download next to its existing https guard + MP3 magic-byte
  check. No behaviour change.

## [1.0.0] - 2026-07-13
### Added
- Repository hygiene files (CONTRIBUTING, SECURITY, CODE_OF_CONDUCT, CI) per the KeilerHirsch repo standard.
