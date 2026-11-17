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

No test reaches the network by default:

- Tests marked `vcr` replay recorded responses from `tests/cassettes/`. To
  record a new cassette or refresh one, set `GENIUS_ACCESS_TOKEN` and run
  `uv run pytest --record-mode=once` (or `rewrite` to replace existing ones).
  Cassettes drop the token, cookies, user agent and most response headers,
  and the recorder refuses lyrics pages and the `/account` endpoint, so real
  lyrics and the token owner's private details never land in the repo.
- Tests marked `live` make real requests and run only with `--live` and
  `GENIUS_ACCESS_TOKEN` set. Use them for lyrics pages and anything private.
- Any other test that reaches the network fails (`--block-network` is on by
  default and lifted only for `--live`).
- Never record a test that writes to Genius (creating annotations, voting).

## Test conventions

- Plain pytest functions; no `unittest.TestCase` and no test classes.
- One test module per unit under test, starting with a one-line module
  docstring.
- Name tests `test_<subject>_<expected behavior>`, e.g.
  `test_lyrics_raises_on_403`.
- Every test and public fixture has a one-line docstring stating the
  behavior it checks or what it provides, in the present tense.
- Fully type annotate tests, fixtures and helpers. Prefix helpers with `_`.
- Shared fixtures (`genius`, `public_api`, `live_genius`) live in
  `tests/conftest.py`; others stay in their module.
- Use plain `assert`, `pytest.raises` with `match=` where the message
  matters, and `pytest.mark.parametrize` with `pytest.param(..., id=...)`
  for case tables.
- Arrange, act and assert are separated by blank lines.
- Fixture data lives in `tests/fixtures/` and uses invented lyrics.

ruff enforces annotations (`ANN`), pytest style (`PT`) and test docstrings
(`D100`, `D103`).
