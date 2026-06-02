# Technical Context

This document outlines the development environment, tooling, and execution instructions.

## Tech Stack

- **Backend**: Python 3, Flask, BeautifulSoup4 (XML processing), Requests.
- **Frontend**: HTML5, Vanilla CSS, Tailwind CSS (via CDN), Vue.js 3 (via CDN).
- **Environment & Dependency Management**: `uv` package manager, Virtualenv (`.venv`).

## Dev Environment Configuration

- **Workspace File Locations**:
  - Main App Entry: `main.py`
  - Domain XML logic: `aia.py`
  - Root template layout: `templates/index.html`
  - Results template: `templates/result.html`
  - Main JavaScript logic: `static/scripts/main.js`
  - Criteria mappings: `criteria.json`, `mapping.json`, `properties.json`

## Development Commands

### Install dependencies
```bash
uv sync
```

### Run Flask Application (Debug mode enabled)
```bash
uv run flask --app main.py run --debug
```

### Run Flask Application (Normal mode)
```bash
uv run flask --app main.py run
```
Default URL: `http://127.0.0.1:5000/`
