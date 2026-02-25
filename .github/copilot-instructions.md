# LyricsGenius Development Guide

## Architecture Overview

Three-layer design for Genius.com API interaction:

1. **Sender** ([lyricsgenius/api/base.py](../lyricsgenius/api/base.py)) - HTTP request handling, retries, authentication headers
2. **API** ([lyricsgenius/api/api.py](../lyricsgenius/api/api.py)) - Direct API methods organized by resource in `api/public_methods/` (album.py, artist.py, song.py, etc.)
3. **Genius** ([lyricsgenius/genius.py](../lyricsgenius/genius.py)) - User-facing search methods + web scraping. Inherits from both `API` and `PublicAPI`

**Critical**: The `lyrics()` method uses BeautifulSoup to scrape HTML, not the API. It searches for `div[data-lyrics-container="true"]` elements. The Genius API provides metadata but not full lyrics.

## Type System

Entities in [lyricsgenius/types/](../lyricsgenius/types/): `Song`, `Artist`, `Album` all extend `BaseEntity`

- `Song(lyrics: str, body: dict)` - lyrics + metadata from API response
- `Artist(body: dict)` - artist metadata with `songs: list[Song]` collection
- `Album(body: dict, tracks: list[Song])` - album metadata with track list

Each entity has `.to_json()`, `.to_text()`, and `.save_lyrics()` methods for export.

## Development Workflow

**Package manager**: Uses `uv` (not pip/poetry)

```bash
uv sync                    # Install dependencies
uv run pytest              # Run tests
uv run mypy                # Type checking
uv build                   # Build distribution
python -m lyricsgenius     # CLI usage
```

**Authentication**: Set `GENIUS_ACCESS_TOKEN` environment variable. All API calls require this. Tests use `get_genius_client()` factory from [tests/__init__.py](../tests/__init__.py) which configures timeout=15, retries=3, sleep_time=1.0.

## Key Patterns & Conventions

**Excluded terms filtering**: `Genius.excluded_terms` contains literal strings (case-insensitive substring matches) to filter non-songs like "(Remix)", "[Instrumental]", "tracklist". Default terms in `Genius.default_terms` include bracketed/parenthesized variations.

**Search flow**: `search_song()`/`search_artist()`/`search_album()` → call `search_all()` → filter results → optionally get full info via direct API call (song(id), artist(id), album(id)) → scrape lyrics if needed → return typed object.

**Section header removal**: `remove_section_headers=True` strips `[Chorus]`, `[Verse 1]`, etc. from lyrics using regex.

**CLI support**: [__main__.py](../lyricsgenius/__main__.py) provides command-line interface. Supports `--format json txt`, `--save`, `--max-songs` options.

## Type Checking

Strict mypy config in [mypy.ini](../mypy.ini): `disallow_untyped_defs`, `disallow_untyped_calls`, etc. All new code must include type hints.

## Testing Considerations

- Live API tests skipped when `GENIUS_ACCESS_TOKEN` missing (see [tests/test_genius_api.py](../tests/test_genius_api.py))
- Mocked fixtures in [tests/fixtures/](../tests/fixtures/) for offline testing
- Web scraping is fragile - Genius.com HTML structure changes break `lyrics()` method
