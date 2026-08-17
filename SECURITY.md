# Security Policy

## Reporting a vulnerability

Please report security issues privately through GitHub's vulnerability-reporting / Security Advisory flow when available. If that is not available, open a minimal public issue asking for a private contact path without including exploit details or sensitive data.

## Supported versions

The latest release is the primary supported version. Older releases may not receive security fixes.

## Security scope

Security-relevant areas include command/subprocess invocation, path traversal through sound names or configuration, unsafe handling of hook JSON, download-source validation, and any case where untrusted hook input can cause unintended file access or command execution.

A missing player, inaudible clip, unsupported platform, or hook timeout is normally a reliability/compatibility issue rather than a security vulnerability unless it crosses one of those boundaries.

## Trust boundaries and limits

- Sound names are expected to resolve only inside the local `sounds/` directory.
- Playback uses fixed program invocation without a shell where applicable.
- Hook playback is synchronous in the documented setup; errors are swallowed so optional audio does not fail the calling workflow.
- Third-party copyrighted clips are not shipped in the repository; the download helper and local user-provided sounds are separate from the project license for the code.

Please redact private workflow payloads, paths, usernames, credentials, or other unrelated local data from public reports.
