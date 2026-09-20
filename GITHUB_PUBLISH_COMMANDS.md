# GitHub Publish Commands

These commands are provided for the maintainer to run manually. This task does
not push anything automatically.

Assumed remote:

```text
https://github.com/duyang1994/ARIS-Research-OS
```

## One-time remote setup

```bash
git remote add origin https://github.com/duyang1994/ARIS-Research-OS.git
```

If a remote named `origin` already exists, use `git remote -v` and adapt.

## Push the main branch

The current local branch may be named `clinical-meta-v0.2`. To publish under
`main`:

```bash
git branch -M main
git push -u origin main
```

## Tag the release

```bash
git tag -a v0.2.0 -m "ARIS Research OS v0.2.0"
git push origin v0.2.0
```

## Before pushing

- Verify `git status` shows the intended release files.
- Verify `python -m pytest tests/governance -q` passes.
- Verify no secrets or private paths are present in tracked files.
- Confirm you are authorized to publish this repository.
