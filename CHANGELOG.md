# Changelog

Notable project changes are recorded here. This file reflects verified repository history and current source; it does not imply a production-ready release.

## Unreleased

- Added the open-source documentation and contributor guidance for the SEDS V2 alpha prototype.
- The current codebase includes YOLOv8 image-inference code, a mock detector, configurable class/confidence rules, SQLite persistence and analytics components, JSON evidence metadata writing, and a basic Streamlit dashboard. These pieces are not fully integrated into a reliable end-to-end service.
- Known limitations remain: the database table creation omits `event_id` although insertion expects it; the application entry point only initializes components; and tests are mostly side-effecting scripts rather than an automated pytest suite.
- Raspberry Pi deployment, video processing, tracking, cloud synchronization, and live alerting are not validated or complete capabilities.

## SEDS V2 alpha baseline

The Git history leading to the `SEDS_V2_alpha` commit records work on YOLOv8 integration, a detection/rules pipeline, event ID generation, evidence metadata storage, analytics, and Streamlit dashboard pages. Current source confirms the corresponding component files exist, with the integration and limitations described above. No semantic release number or release date is assigned here.
