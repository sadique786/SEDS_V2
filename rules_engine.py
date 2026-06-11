from config.config_manager import ConfigManager


class RulesEngine:

    def __init__(self):

        self.config = ConfigManager()

        self.threshold = self.config.get(
            "detection",
            "confidence_threshold"
        )

        self.target_classes = self.config.get(
            "detection",
            "target_classes"
        )

    def validate_detection(
        self,
        object_class,
        confidence
    ):

        if object_class not in self.target_classes:
            return False

        return confidence >= self.threshold
