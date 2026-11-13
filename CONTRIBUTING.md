# Contributing to SEDS V2

Thanks for helping improve SEDS V2. It is an early-stage prototype, so please describe behavior as observed and distinguish implemented work from plans or hardware-dependent experiments.

## Prerequisites and environment

- Git
- Python 3.11
- macOS or another environment compatible with the installed OpenCV, PyTorch, and Ultralytics packages
- A YOLOv8n weights file for model-inference work (see the Model weights section)

From the repository root, create an isolated environment and install the pinned dependencies:

```bash
python3.11 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The dependency set and model inference have not been validated on Raspberry Pi. See [README setup and status](README.md#setup-macos-python-311).

## Branches and commits

Use a short, descriptive branch name with a type prefix:

- `docs/` for documentation
- `fix/` for bug fixes
- `feat/` for user-facing functionality
- `test/` for test changes
- `chore/` for maintenance

Use a concise commit subject in Conventional Commit style, for example `docs: clarify database schema` or `fix: handle missing image input`. Keep commits focused and explain behavior or migration implications in the body when relevant. These are contribution conventions; the existing history includes earlier module-numbered commit subjects.

## Bugs and feature proposals

Use the GitHub issue templates to report a bug or propose a feature. Include:

- Operating system, Python version, and relevant dependency versions.
- Exact commands and steps to reproduce.
- Expected and observed behavior, with concise error output where useful.
- For feature requests, the problem being addressed and how success could be evaluated.

Do not attach credentials, private data, or large model/database files to an issue. For security-sensitive reports, use GitHub's private vulnerability reporting if it is enabled for the repository.

## Code quality and testing expectations

- Inspect the existing implementation and preserve current behavior unless a change is intentional and explained.
- Keep changes focused, use `pathlib` for filesystem paths, and handle errors in a way that helps diagnose failures.
- Add automated assertions for new behavior as the test suite is improved.
- The current `tests/unit/` and `tests/integration/` files are mostly executable scripts that print output, not pytest tests. Several can write to `database/seds.db`, `captures/`, or `logs/`; inspect a script before running it and use disposable data where possible.
- `pytest` is not currently declared in `requirements.txt`, and no CI workflow is promised. Report exactly what you ran and separate passed, failed, not-run, and hardware-required checks.
- Do not claim Raspberry Pi compatibility or performance without measurements on the target hardware.

## Model weights, generated files, and databases

- Do not commit downloaded model weights by default. The current detector expects `models/yolov8n.pt`; the pinned Ultralytics loader can request this known asset when it is missing and network access is available. See the README for the initialization command. Record the Ultralytics version and the resulting file's SHA-256 checksum when reproducing model-based experiments.
- Review the model's license and distribution terms separately from this repository's MIT license.
- Do not commit local `.env` files, secrets, virtual environments, caches, logs, or SQLite databases.
- Do not overwrite or delete existing database files or tracked sample assets as part of testing. Back up databases before any schema work; schema changes require a migration plan.
- Preserve useful small test fixtures and intentional samples. Generated captures should be identified explicitly rather than excluding the entire `captures/` directory.

## Pull requests

Before opening a pull request, review the diff for unrelated changes and generated files. Explain the user-visible change, the verification performed, and known limitations. Keep documentation and claims consistent with the current implementation.
