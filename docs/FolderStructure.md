# Repository Folder Structure

This guide reflects files currently present in the repository. Directory names do not imply that the corresponding capability is implemented.

```text
.
├── AGENTS.md
├── README.md
├── active_learning/      # empty placeholder directory
├── app/                  # startup, event model, logging
├── alerts/               # placeholder package
├── captures/             # tracked sample metadata/image artifacts
├── cloud/                # placeholder package
├── config/               # YAML settings and loader
├── dashboard/            # Streamlit pages
├── database/             # SQLite manager and analytics queries
├── decision/             # confidence/class rules and event ID creation
├── detection/            # mock, YOLO, image loading, persistence service
├── docs/                 # project documentation
├── models/               # local model artifact may be ignored by Git
├── storage/              # JSON evidence metadata writer
├── test_images/          # tracked sample image
├── tests/                # manual scripts, grouped by purpose
├── tracking/             # placeholder package
├── requirements.txt      # pinned Python environment packages
├── scripts/              # empty; no tracked implementation scripts
└── yolov8n.pt            # tracked root model path in repository history
```

## Production and runtime code

- `app/main.py` initializes the logger, YAML config, and database. It does not run detection.
- `app/models.py` defines `DetectionEvent`.
- `app/utils/logger.py` configures the `SEDS` file logger under `logs/`.
- `config/config_manager.py` loads YAML; `config/config.yaml` contains threshold/class and future-feature flags.
- `detection/yolo_detector.py` performs image inference with `models/yolov8n.pt` in the current worktree.
- `detection/mock_detector.py` produces a fixed example event.
- `detection/camera_manager.py` loads an image via OpenCV; it is not a live camera manager.
- `detection/detection_service.py` inserts detections into SQLite and logs them. It does not invoke rules or evidence storage.
- `decision/rules_engine.py` filters a supplied class/confidence pair; `decision/event_manager.py` generates IDs only.
- `database/database_manager.py` initializes and accesses `database/seds.db`; `database/analytics_manager.py` supplies dashboard queries.
- `storage/evidence_manager.py` writes JSON metadata. It does not save image bytes.
- `dashboard/Home.py`, `dashboard/pages/History.py`, and `dashboard/pages/Analytics.py` implement the Streamlit UI.

## Tests and development scripts

`tests/unit/` and `tests/integration/` contain scripts that execute at module level and print output. Several write to local data. They are not pytest tests with assertions. `tests/hardware/` and `tests/performance/` currently contain only package initializers, not test cases. `scripts/` is present locally but has no tracked implementation file.

## Data and model artifacts

- `test_images/elephant.jpg` is the inference/image-loading sample.
- `captures/` contains tracked example artifacts. Runtime output may also be written there.
- `database/seds.db` and `logs/` are runtime data locations and are ignored by Git.
- Root `yolov8n.pt` is tracked, but the current detector path points to `models/yolov8n.pt`. The latter exists locally in this checkout but is ignored by the current ignore rules and may not be present after cloning.

## Empty or placeholder areas

At the time of inspection, `active_learning/` and `scripts/` had no tracked source files. `alerts/`, `cloud/`, and `tracking/` contained only `__init__.py`. These folders indicate intended areas only.
