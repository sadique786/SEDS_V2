# Repository instructions for coding agents

## Project context

SEDS V2 is an existing Python prototype for wildlife detection. Preserve its working components and describe current behavior accurately. Before implementation, inspect the relevant source, tests/scripts, configuration, and current Git status. Do not infer implemented features from directory names or configuration flags.

## Safety and scope

- Keep user changes intact. Inspect `git status` and diffs before editing.
- Do not delete, rename, or overwrite files without explicit authorization.
- Do not rewrite whole modules when a focused change is sufficient.
- Do not alter persisted detection records or change SQLite schema without a migration strategy.
- Do not commit credentials, `.env` files, virtual environments, caches, or unnecessary generated assets.
- Use repository-relative paths and preserve macOS/Raspberry Pi OS portability.
- Do not claim tests, performance, hardware operation, or model behavior unless actually verified. Separate passed, failed, not run, and hardware-required checks.

## Current implementation facts

- `app/main.py` initializes configuration, logging, and SQLite. It is not a complete detection launcher.
- `YOLODetector` performs image inference using a model path currently set to `models/yolov8n.pt` in this checkout.
- `RulesEngine`, `DetectionService`, and `EvidenceManager` are separate. The service does not invoke the rules engine or evidence manager.
- `EventManager` creates an ID; time/space event aggregation is not implemented.
- `EvidenceManager` writes JSON metadata when called. Automatic evidence-image saving is not implemented.
- `DatabaseManager.create_tables()` defines five detection columns, while `insert_detection()` inserts an `event_id` sixth column. Do not hide or silently patch this mismatch in documentation; code fixes need explicit scope and a migration plan.
- Files in `tests/` are primarily manual scripts with side effects, not pytest assertions. Inspect before running.
- Raspberry Pi deployment has not been validated.

## Project commands and verification

Run commands from the repository root unless code explicitly supports another working directory. The documented Python target is 3.11. Do not assume setup or test commands pass just because they are documented. Many current test scripts can write to `database/`, `captures/`, or `logs/`; prefer isolated temporary data when executing them, and do not modify existing user data.

## Documentation conventions

- Label capabilities as implemented, partial, planned, experimental, or hardware-unverified.
- Derive descriptions from current source and configuration.
- Keep relative links valid and Mermaid fenced blocks balanced.
- Do not describe proposed roadmap work as complete.
- The repository's `LICENSE` file states the approved MIT license and copyright notice. Keep documentation consistent with that file.
