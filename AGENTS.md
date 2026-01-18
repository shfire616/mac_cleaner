# AGENTS.md

This file guides agentic coding assistants working in this repository.

## Project Snapshot
- App: MacCleaner (macOS disk cleaner)
- Language: Python 3.11
- UI Framework: PyQt6
- Repo layout:
  - `src/main.py` (entry point)
  - `src/ui/` (Qt widgets and styling)
  - `src/core/` (non-UI logic)
- Dependencies: `PyQt6`, `humanize`, `send2trash`

## Build / Lint / Test

### Build (local)
- Install deps:
  - `pip install -r requirements.txt`
  - `pip install pyinstaller dmgbuild`
- Build app bundle:
  - `pyinstaller --name="MacCleaner" --windowed --noconfirm --clean --paths=src src/main.py`
- Build DMG:
  - `dmgbuild -s dmg_settings.py "MacCleaner" dist/MacCleaner.dmg`

### CI build
Defined in `/.github/workflows/build.yml`.
- Builds on tag push `v*` for Intel and Apple Silicon macOS.
- Produces `dist/MacCleaner-<arch>.dmg`.

### Lint
- No lint tooling configured.
- No formatter configured (no `black`, `ruff`, `isort`, etc.).

### Tests
- No test framework configured.
- No test files found.
- No command exists to run a single test.
  - If tests are added later, prefer `pytest path/to/test_file.py::test_name`.

## Code Style Guidelines

### Imports
- Prefer absolute imports from `src`:
  - `from src.core.scanner import ScanWorker`
- Order imports:
  1. Standard library (`os`, `sys`, `traceback`)
  2. Third-party (`PyQt6`, `humanize`, `send2trash`)
  3. Local (`src.ui`, `src.core`)

### Naming
- Classes: `PascalCase` (e.g., `ScanWorker`, `MainWindow`)
- Functions/methods: `snake_case` (e.g., `scan_grouped`, `refresh_stats`)
- Variables/signals: `snake_case` (e.g., `item_found`, `progress_update`)
- Private attributes: single underscore prefix (e.g., `self._is_running`)

### Formatting
- Indentation: 4 spaces.
- Keep function bodies readable and short; prefer helper methods when logic grows.
- Use blank lines to separate logical blocks in long methods.

### Types
- No static typing conventions in place.
- Avoid introducing `typing` unless needed for clarity.

### Error Handling
- Prefer explicit `try/except Exception as e:` with a message.
- When debugging, print the traceback (see `src/main.py`).
- For filesystem access, guard with `try/except` to handle permission errors.
- Avoid empty except blocks in new code.

### File Safety
- NEVER delete user files directly with `os.remove` or `shutil.rmtree`.
- Use `send2trash` to move files to the Trash.

### Paths
- Use `os.path.expanduser("~")` for user paths.
- Avoid hardcoding `/Users/<name>` paths.

## UI / UX Conventions

### Structure
- Keep UI widgets under `src/ui/`.
- `MainWindow` uses a `QStackedWidget` for page navigation.
- Each view typically has a `setup_ui()` method.

### Threading & Responsiveness
- Long-running scans must run in `QThread` subclasses.
- Communicate worker progress via `pyqtSignal`.
- Do NOT update UI directly from background threads.

### Styling
- Global styles live in `src/ui/styles.py`.
- Use QSS for component-specific styling.
- Use `.AppleSystemUIFont` for native macOS look.
- Button styling convention:
  - `QPushButton[class="primary"]` and `QPushButton[class="danger"]` in global styles.
  - Some views override button styles inline for visibility.

## Architectural Patterns
- Core logic goes in `src/core/` (e.g., scanning in `scanner.py`).
- UI widgets should focus on presentation and signals.
- Background worker pattern:
  - Inherit from `QThread`.
  - Implement `run()`.
  - Support cancellation with a `_is_running` flag.

## Safety & UX Defaults
- App leftovers are unchecked by default to reduce accidental deletion.
- Confirm destructive actions with a `QMessageBox`.

## Repo Rules Files
- No Cursor rules found (`.cursor/rules/`, `.cursorrules`).
- No Copilot instructions found (`.github/copilot-instructions.md`).

## References
- Entry point: `src/main.py`
- Styles: `src/ui/styles.py`
- Main window: `src/ui/main_window.py`
- Scanner worker: `src/core/scanner.py`
- Scan view: `src/ui/scan_view.py`
- CI workflow: `.github/workflows/build.yml`

## Agent Checklist (Before Shipping)
- Use existing patterns; minimize refactors.
- Keep UI responsive; move heavy work to threads.
- Use `send2trash` for deletions.
- Avoid adding new tooling unless requested.
- If adding tests, document how to run a single test.

## Notes for Future Expansion
- If linting is added, document formatter + lint rules here.
- If tests are added, document test runner and single-test command here.
