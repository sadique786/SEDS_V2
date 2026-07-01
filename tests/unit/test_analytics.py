from database.analytics_manager import (
    AnalyticsManager
)

analytics = AnalyticsManager()

print()

print(
    "Total Detections:",
    analytics.total_detections()
)

print(
    "Average Confidence:",
    round(
        analytics.average_confidence(),
        2
    )
)
