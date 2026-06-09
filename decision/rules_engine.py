from config.config_manager import ConfigManager


class RulesEngine:

    def __init__(self):

        self.config = ConfigManager()

        self.threshold = self.config.get(
            "detection",
            "confidence_threshold"
        )

    def validate_detection(
        self,
        confidence
    ):

        return confidence >= self.threshold
