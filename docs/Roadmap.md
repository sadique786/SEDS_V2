# SEDS V2 Roadmap

This roadmap separates the current code foundation from proposed work. Planned items are not implemented merely because a package, configuration flag, directory, or historical commit mentions them.

## Current foundation

The repository contains these components, with the integration limitations described in the linked documentation:

- YAML configuration loading and file logging.
- A `DetectionEvent` data model and mock detector.
- YOLO image-inference code using a local/Ultralytics-resolved YOLOv8n weights path.
- A confidence and target-class rules component.
- SQLite database manager and analytics queries.
- Event ID generation (identifier generation only).
- JSON evidence metadata writer (not connected to the detection service).
- Streamlit home metrics, detection history, and confidence histogram pages.

This is prototype foundation code, not a complete autonomous monitoring service. See [Architecture](Architecture.md), [Detection Pipeline](DetectionPipeline.md), and [Database](Database.md).

## Short-term priorities

1. **Fresh-database schema correction:** Define a safe approach for the missing `event_id` column, inspect existing databases, preserve all rows, and implement a versioned migration before changing schema behavior.
2. **Automated test suite:** Introduce pytest-based assertions with isolated temporary databases/capture directories. Convert existing module-level scripts carefully and avoid destructive test side effects.
3. **Detection pipeline orchestration:** Add a clear caller/application flow that applies rules before persistence and handles errors. Keep this a scoped software change; the current entry point is initialization only.
4. **Evidence integration:** Decide how image files and metadata are written and referenced, then integrate with persistence without claiming that behavior before it is implemented and tested.
5. **Reproducible installation and dependency cleanup:** Verify Python/platform support, separate direct and development dependencies, review unused pins, and document model version/checksum handling.

These are priorities, not completed work. Database changes require a migration plan; dependency changes require separate review and verification.

## Future development (planned)

### Raspberry Pi deployment

Validate Raspberry Pi 4B 8 GB setup, dependency wheels, CPU inference, memory/thermal behavior, camera support, storage retention, and reliability. Deployment and performance remain unvalidated.

### Camera capture

Implement camera acquisition and frame handling. Current `CameraManager` only loads a still image path with OpenCV.

### Video processing — separate branch

Develop video ingestion and frame inference on a separate branch after agreeing on resource constraints and test data. Video processing is not part of the current feature set.

### Tracking and event aggregation

Add object tracking and explicit event aggregation policies. `EventManager` currently generates an ID only; no temporal/spatial grouping exists.

### Alerts

Implement and test selected alert integrations with secure credential storage, delivery failure handling, cooldowns, and user configuration. Current YAML flags do not represent functioning alert delivery.

### Active learning

Design a reviewed process for selecting uncertain/representative detections, human annotation, dataset versioning, and model evaluation. The `active_learning/` directory is currently empty.

### Cloud integration

Define synchronization, authentication, offline behavior, conflict handling, privacy, and retention before implementing cloud logging. The `cloud/` package is currently a placeholder.
