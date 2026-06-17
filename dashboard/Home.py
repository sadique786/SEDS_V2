import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(PROJECT_ROOT))

import streamlit as st

from database.analytics_manager import (
    AnalyticsManager
)

st.set_page_config(
    page_title="SEDS v2",
    layout="wide"
)

analytics = AnalyticsManager()

st.title(
    "🐘 SEDS v2 Dashboard"
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Total Detections",
        analytics.total_detections()
    )

with col2:

    st.metric(
        "Average Confidence",
        round(
            analytics.average_confidence(),
            2
        )
    )
