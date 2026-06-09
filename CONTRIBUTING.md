# Contributing

Thanks for your interest in contributing! Here's how to get started.

## Before you start

- For **bug fixes or small changes**, go ahead and open a pull request.
- For **new features or significant changes**, open an issue first to discuss the approach.
- Please read the [Code of Conduct](CODE_OF_CONDUCT.md).

## How to contribute

1. Fork this repository
2. Create a branch: `git checkout -b feat/your-feature-name`
3. Make your changes
4. Push and open a pull request

## Branch names

Use a short prefix that describes the type of change:

| Prefix   | When to use                   |
| -------- | ----------------------------- |
| `feat/`  | New feature                   |
| `fix/`   | Bug fix                       |
| `docs/`  | Documentation only            |
| `chore/` | Maintenance, tooling, cleanup |

## Commit messages

We recommend [Conventional Commits](https://www.conventionalcommits.org/):

```text
feat: add dark mode support
fix: handle empty input correctly
docs: update installation steps
chore: upgrade dependencies
```

Not strictly enforced, but it keeps the history readable and enables automatic release notes.

## Pull request labels

When opening a PR, add a label that matches your change type.
These labels are used by [Release Drafter](https://github.com/release-drafter/release-drafter) to automatically generate release notes and calculate the next version number:

| Label                        | What it means     | Version bump               |
| ---------------------------- | ----------------- | -------------------------- |
| `feature` or `enhancement`   | New feature       | minor (e.g. 1.0.0 → 1.1.0) |
| `fix`, `bug`, or `bugfix`    | Bug fix           | patch (e.g. 1.0.0 → 1.0.1) |
| `chore` or `maintenance`     | Cleanup, refactor | patch                      |
| `docs` or `documentation`    | Docs only         | patch                      |
| `major` or `breaking-change` | Breaking change   | major (e.g. 1.0.0 → 2.0.0) |

## Releasing a new version

When you're ready to ship a release:

1. Push a tag matching `v1.2.3`:

   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. GitHub Actions will automatically publish the GitHub Release from the draft that Release Drafter maintains.

## Versioning

This project follows [Semantic Versioning](https://semver.org/):

- **Major** version → breaking change
- **Minor** version → new feature, backward compatible
- **Patch** version → bug fix or small improvement
