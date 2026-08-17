# Contributing to claude-bordcomputer-sounds

Issues and pull requests are welcome. Keep hook behavior predictable and avoid turning optional audio feedback into a dependency for the underlying workflow.

## Ground rules

- Keep changes focused and explain which hook or playback path they affect.
- Preserve failure isolation: missing sounds or players should not make the calling workflow fail.
- Be explicit about synchronous behavior and timeouts; do not describe a blocking playback call as non-blocking.
- Only contribute audio you have the right to redistribute. The repository intentionally does not ship third-party copyrighted clips.
- Do not commit credentials, private workflow data, or other material you do not have permission to publish.
- CI should pass before a PR is merged.

## Commit identity

The maintainer uses a GitHub noreply address for personal OPSEC. Contributors may use the Git identity and privacy settings appropriate for them; no particular email format is required by this project.

## License

Code contributions are accepted under GPL-3.0-or-later unless a file states otherwise. See [LICENSE](LICENSE).
