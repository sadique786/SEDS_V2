import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(PROJECT_ROOT))

import streamlit as st
import pandas as pd

from database.analytics_manager import (
    AnalyticsManager
)

analytics = AnalyticsManager()

rows = analytics.get_all_detections()

columns = [
    "ID",
    "Timestamp",
    "Object",
    "Confidence",
    "Image",
    "Event ID"
]

df = pd.DataFrame(
    rows,
    columns=columns
)

st.title(
    "Detection History"
)

st.dataframe(
    df,
    use_container_width=True
)
