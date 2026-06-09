# Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```text
<type>: <short summary in present tense, lowercase, no period>
```

## Types

| Type       | When to use                                         |
| ---------- | --------------------------------------------------- |
| `feat`     | New feature                                         |
| `fix`      | Bug fix                                             |
| `docs`     | Documentation only                                  |
| `chore`    | Maintenance, tooling, cleanup                       |
| `test`     | Tests                                               |
| `ci`       | CI/CD changes                                       |
| `refactor` | Code change that doesn't add a feature or fix a bug |

## Examples

```text
feat: add dark mode support
fix: handle empty input on login form
docs: update installation steps
chore: upgrade dependencies
ci: add lint step to pull request workflow
```

## Rules

- Use the imperative mood: "add", not "added" or "adds".
- Keep the summary under 72 characters.
- Reference issues in the body when relevant: `Closes #42`.
