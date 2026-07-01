from config.config_manager import ConfigManager


config = ConfigManager()

print(
    config.get(
        "detection",
        "confidence_threshold"
    )
)

print(
    config.get(
        "detection",
        "target_classes"
    )
)
