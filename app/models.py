from dataclasses import dataclass

@dataclass
class DetectionEvent:
	timestamp: str
	object_class: str
	confidence: float
	image_path: str

