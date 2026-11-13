# Testing and Validation

## Current test inventory

The files are executable scripts, not a reliable automated test suite. They mostly run work at module import time, print output, and use fixed repository paths; they do not define pytest test functions or assertions.

| File | Apparent purpose | Side effects / caveats |
|---|---|---|
| `tests/unit/test_config.py` | Print configured threshold and target classes. | No assertions. Uses default relative config path. |
| `tests/unit/test_event.py` | Construct and print a `DetectionEvent`. | No assertions. |
| `tests/unit/test_logger.py` | Write sample log messages. | Writes to `logs/application.log`. |
| `tests/unit/test_rules_engine.py` | Exercise rules validation. | Calls `validate_detection` with one argument although the method requires class and confidence; likely raises `TypeError`. |
| `tests/unit/test_database.py` | Insert and print a detection row. | Writes to the local database; fresh source-created schema lacks the `event_id` column required by the insert. |
| `tests/unit/test_analytics.py` | Print count and average confidence. | Reads the local database; `round(None, 2)` can fail when there are no rows. |
| `tests/integration/test_pipeline.py` | Send a mock event to the detection service. | Writes database/log data; affected by the schema mismatch. |
| `tests/integration/test_detection_service.py` | Persist a constructed event. | Writes database/log data; affected by the schema mismatch. |
| `tests/integration/test_ai_pipeline.py` | Run YOLO, apply rules, and persist accepted events. | Requires model/dependencies and may download weights; writes database/log data; its calls should be reviewed before execution. |
| `tests/integration/test_yolo.py` | Run YOLO against `test_images/elephant.jpg`. | Requires model/dependencies and may download weights; no assertions. |
| `tests/integration/test_camera.py` | Load the sample image through OpenCV. | No assertion; can fail if path/image is unavailable, then `.shape` access fails. |
| `tests/integration/test_visualization.py` | Draw an example rectangle and label. | Overwrites the tracked `captures/visualized_elephant.jpg`; do not run against the working copy without protecting that asset. |
| `tests/integration/test_event_aggregation.py` | Reuse one event ID for two events and persist both. | Demonstrates shared IDs, not time/space aggregation; writes to database/log and encounters the schema mismatch on a fresh DB. |
| `tests/integration/test_evidence_manager.py` | Write sample JSON metadata. | Writes a dated file under `captures/`; may create generated files. |
| `tests/hardware/`, `tests/performance/` | Reserved categories. | Contain no substantive test cases at this baseline. |

Printing a value does not compare it with an expected result or fail reliably when behavior is wrong. Module-level scripts can mutate shared developer data merely by being imported. There are no pytest tests currently, and pytest is not declared in `requirements.txt`; no automated suite is claimed to pass.

## Proposed pytest structure

The following is a proposal, not an existing layout or implementation:

```text
tests/
├── unit/
│   ├── test_config_manager.py
│   ├── test_detection_event.py
│   ├── test_rules_engine.py
│   └── test_event_manager.py
├── integration/
│   ├── test_database_manager.py
│   ├── test_detection_service.py
│   ├── test_evidence_manager.py
│   └── test_dashboard_queries.py
├── performance/
└── hardware/
```

Tests should use fixtures and assertions, import code without triggering execution, and report clear expected/actual results. Add pytest as a development dependency only when that suite is introduced through a separately reviewed dependency change.

## Test categories

- **Unit:** configuration lookup, event values, confidence/class rules, event ID format, and isolated helper behavior.
- **Database:** schema initialization, insert/query behavior, aggregate results for empty and populated data, and migration preservation. Use temporary databases and cover the `event_id` mismatch before calling persistence healthy.
- **Integration:** mock/YOLO result flow through explicit rules and persistence, plus metadata writing. Separate tests requiring weights or network from offline tests.
- **Dashboard:** empty and populated state, five/six-column compatibility, metrics, pages, and useful error handling. Streamlit-specific tests require chosen tooling to be added and verified.
- **Performance:** repeatable image-inference timing, memory/temperature observations, and sustained-run behavior, with hardware and model details recorded. No performance baseline currently exists.
- **Hardware:** camera detection/acquisition, OS/Python/dependency compatibility, inference and persistence on the target Pi, and startup/recovery checks. No hardware cases currently exist.

## Test isolation and data safety

- Use a temporary directory (`tmp_path` in a future pytest suite) and a dedicated SQLite file; do not point tests at the developer's `database/seds.db`.
- The current classes hardcode relative paths and do not accept a database path. Safe automated isolation will require a separately scoped code change or controlled temporary working directory.
- Do not delete or recreate an existing database as cleanup. Back it up before schema experiments and preserve all rows.
- Do not run `tests/integration/test_visualization.py` on the working tree without first protecting the tracked capture image; it writes over that file.
- Evidence scripts write under `captures/`; configure a temporary base directory in a future refactor or remove only test-owned files after verifying their exact paths and that they are not tracked.
- A YOLO constructor may download weights. Keep model artifacts outside test outputs, and skip/mark network-dependent inference when the asset is unavailable.
- Avoid importing the current test scripts during collection; their top-level code executes immediately.

## Validation levels and future acceptance criteria

### Software validation

Future software checks should establish repeatable Python 3.11 setup, assertions for unit behavior, fresh-database migration and insert success, empty-database dashboard handling, dashboard query correctness, model loading with a known local checksum, and clean test isolation. Failures should be reported rather than silently skipped.

### Hardware validation

On a Raspberry Pi 4B 8 GB, record OS image/release, Python and dependency versions, model checksum, camera model, input dimensions, CPU-only inference conditions, warm-up policy, repeated latency distribution, peak memory, temperature/throttling, storage growth, and run duration. Verify camera operation and persistence independently. No such measurements have been collected.

### Real-world field validation

Field validation is separate from software and bench hardware checks. It requires an ethically and safely approved deployment, representative day/night/weather/distance data, labeled ground truth, false-positive and missed-detection analysis, alert-delivery measurement, privacy/data-retention review, and an operational response plan. No real-world field trial or accuracy result is claimed.
