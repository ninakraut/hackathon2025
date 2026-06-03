# Active Context

This document captures the active state, focus areas, and recent challenges encountered.

## Current Focus
Providing a clean, responsive single-page horizontal dashboard. The user manages the local execution server manually using `uv run flask --app main.py run --debug`.

## Recent Changes
- **Vue.js State Transition**: Moved the form state (tab selection, file drag-and-drop, criteria selections) from old script handlers to a centralized Vue 3 app instance in `main.js`.
- **Delimiters Match**: Set Vue custom delimiters to `[[` and `]]` to coexist alongside Jinja template parsing tags.
- **Removed Deprecated Inputs**: Dropped tender details ("Name" / "Beschreibung") and the text-value input fields from criteria checkboxes, as requested by the user.
- **Widescreen Two-Column Layout**: Left column houses the source/context and right column hosts the criteria list.
- **XML Criteria Catalog Integration**: Replaced the deprecated `criteria.json` with the XML criteria catalog (`2026_06_01_RUB_Merkmale_Nachhaltigkeit.xml`). `main.py` now parses the XML dynamically using BeautifulSoup to construct criteria groups and criteria lists, and `mapping.json` is updated to support the new criteria mappings.

## Next Steps
- Validate error behaviors for non-standard files or offline GUID API requests.
