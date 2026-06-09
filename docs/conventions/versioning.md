# Versioning

We follow [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

| Change                            | Bump  | Example         |
| --------------------------------- | ----- | --------------- |
| Breaking change                   | Major | `1.0.0 → 2.0.0` |
| New feature (backward compatible) | Minor | `1.0.0 → 1.1.0` |
| Bug fix or small improvement      | Patch | `1.0.0 → 1.0.1` |

## Releasing

1. Ensure `main` is in a releasable state.
2. Push a tag matching the version:

   ```bash
   git tag v1.2.3
   git push origin v1.2.3
   ```

3. CI publishes the GitHub Release automatically.

## Pre-releases

Use suffixes for pre-release identifiers: `1.0.0-alpha.1`, `1.0.0-rc.2`.
