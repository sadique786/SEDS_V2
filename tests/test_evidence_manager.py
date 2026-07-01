from storage.evidence_manager import (
    EvidenceManager
)

manager = EvidenceManager()

metadata = {

    "event_id":
        "EVT-a8805d7e",

    "animals_detected":
        2,

    "max_confidence":
        0.95
}

path = manager.save_metadata(
    "EVT-a8805d7e",
    metadata
)

print(
    f"Saved: {path}"
)
