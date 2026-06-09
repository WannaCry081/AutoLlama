# Branching

## Branch Names

| Pattern        | Purpose                       |
| -------------- | ----------------------------- |
| `main`         | Stable, always deployable     |
| `feat/<slug>`  | New features                  |
| `fix/<slug>`   | Bug fixes                     |
| `docs/<slug>`  | Documentation                 |
| `chore/<slug>` | Maintenance, tooling, cleanup |

Keep slugs short and descriptive: `feat/dark-mode`, `fix/null-pointer-login`.

## Rules

- Branch off `main` unless told otherwise.
- Delete branches after they are merged.
- Never commit directly to `main`.
