# LyricsGenius

Python client for the Genius.com API.

## Releases

The git tag is both the version source and the release trigger. `hatch-vcs`
derives the version from the tag, so **no file in the tree carries a version** —
`pyproject.toml` declares `dynamic = ["version"]` and `uv.lock` has no version
for `lyricsgenius`.

To cut a release:

1. Add an entry for it to `docs/src/release_notes.rst`.
2. `git tag vX.Y.Z && git push origin vX.Y.Z`

Pushing a `v*` tag builds the package, publishes it to PyPI, and creates the
GitHub release. A run that fails partway can simply be re-run.

Rules that follow from this:

- **Never bump a version by hand** in `pyproject.toml`, `uv.lock`, or anywhere
  else. There is nothing to bump.
- **Only tag when `lyricsgenius/` actually changed.** Infrastructure and docs
  commits are not releases; tagging them ships a package identical to the last
  one and burns a version number.
- **Tags are `vX.Y.Z`.** Some tags predating 3.13.0 lack the `v`; don't copy that.
- Builds off a tag get a dev version with a local segment (`+g<sha>`), which
  PyPI rejects. That is deliberate — it stops an untagged tree publishing by
  accident.
- Don't rename `publish.yml` or the `pypi`/`testpypi` environments. Trusted
  publishing is bound to those exact names.

To try a build without releasing, dispatch `publish-to-test-pypi.yml`; off a tag
it publishes a dev version to TestPyPI.

## Development

```sh
uv sync            # install
uv run pytest      # tests
uv run ruff check  # lint
```

Tests that hit the Genius API are skipped unless `GENIUS_ACCESS_TOKEN` is set.
