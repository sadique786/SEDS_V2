from dataclasses import dataclass
from uuid import uuid4


@dataclass
class DetectionEvent:

    timestamp: str

    object_class: str

    confidence: float

    image_path: str

    event_id: str = ""
