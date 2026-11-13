# Raspberry Pi Deployment Guide

## Validation status

**Actual Raspberry Pi 4B deployment and inference performance have not been validated.** This guide is a preparation plan, not a tested deployment recipe. Commands below are documented examples and have not been executed on Raspberry Pi hardware. Dependency compatibility, camera access, memory use, thermal behavior, and inference speed all require hardware validation.

## Target hardware

The stated target is a **Raspberry Pi 4 Model B with 8 GB RAM**. A deployment evaluation should also have:

- A reliable power supply and adequate cooling for sustained CPU inference.
- Raspberry Pi OS on a quality microSD card or other supported boot storage, with free space for the OS, Python environment, model, database, logs, and evidence.
- Optional compatible camera hardware and the correct CSI cable, or a supported USB camera.
- Local network access during installation and when Ultralytics must download missing model weights.

These are planning requirements; no specific storage capacity, cooling configuration, camera model, or runtime measurement has been validated by this project.

## Raspberry Pi OS and first setup

Install a current 64-bit Raspberry Pi OS image using Raspberry Pi Imager, complete first-boot setup, and apply OS updates. The exact menus and camera commands vary by OS release. Confirm the OS and architecture first:

```bash
uname -a
cat /etc/os-release
python3 --version
```

The following update command is **documented but unverified for this project**:

```bash
sudo apt update
sudo apt full-upgrade
```

Restart after OS updates if requested. Do not treat this as a project-specific hardware validation.

## Python environment and dependencies

The development target is Python 3.11, but the Python version supplied by the installed Raspberry Pi OS may differ. Confirm Python availability and package wheel support before proceeding. The commands below are a **documented setup proposal, not Raspberry Pi-verified commands**:

```bash
sudo apt install python3-venv python3-pip
git clone https://github.com/sadique786/SEDS_V2.git
cd SEDS_V2
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The checked-in `requirements.txt` pins a full package set including PyTorch, torchvision, Ultralytics, OpenCV, Streamlit, and scientific Python packages. Compatibility of those exact pins and wheel availability on Raspberry Pi OS is unknown. Do not silently substitute versions and claim parity; first record the selected Python/OS versions and validate the installed dependency set. A Raspberry Pi-specific dependency lock or installation procedure is future work.

## Model weights

`YOLODetector` expects `models/yolov8n.pt`. With the pinned Ultralytics package, initializing the detector can request this known model asset if it is missing and network access is available:

```bash
python -c "from detection.yolo_detector import YOLODetector; YOLODetector()"
```

This command is **documented but not executed on Raspberry Pi**. It may download a multi-megabyte binary. Record the Ultralytics version and SHA-256 checksum used for an experiment. Model licensing/distribution terms are separate from the repository's MIT license. Do not commit downloaded weights by default.

## Camera setup

The current `CameraManager.load_image(path)` calls `cv2.imread(path)` for an existing image file. It does not initialize the CSI camera stack, open a USB camera, capture frames, or handle a failed image read. A camera model must first be supported by the Raspberry Pi OS camera stack and be independently verified at the OS level using documentation for that OS release.

Camera capture support and frame handoff to the detector are **planned and hardware-unverified**. Do not interpret a successful OS camera preview as evidence that SEDS can consume the camera.

## Configuration and paths

`config/config.yaml` currently sets a confidence threshold of `0.85` and target class `elephant`. `RulesEngine` reads these values only when explicitly called. `DetectionService` does not apply the rules itself. Other YAML flags for tracking, Telegram, email, SMS, cooldown, image storage, and video storage do not correspond to complete functioning integrations.

Configuration, database, logs, and model paths are relative to the process working directory. Run project commands from the repository root. Do not place secrets in the tracked config; no Raspberry Pi secret-management setup exists.

## Current limitations and required validation

- `app/main.py` initializes config, logging, and SQLite; it is not a complete detection or camera launcher.
- The database initializer creates a five-column table while insert code expects `event_id` as a sixth column. Fresh-database inference persistence is therefore blocked until a safe schema correction/migration is made.
- The service does not connect rules filtering or evidence metadata/image storage.
- No video processing, object tracking, real-time alerting, cloud synchronization, or startup service is implemented.
- The dashboard's empty-database home metric may fail, and its history page expects six fields.
- No CPU inference, memory, temperature, storage-wear, camera, or uptime results exist for the Pi 4B.

Before considering deployment, validate the OS/Python/dependency combination, model load, image inference, schema migration and persistence, camera acquisition, dashboard behavior, resource use over sustained runs, and recovery after power/network interruption. A systemd service, retention policy, backup approach, and operational alerting plan are also future work.
