import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.append(str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px

from database.analytics_manager import (
    AnalyticsManager
)

analytics = AnalyticsManager()

confidences = analytics.confidence_distribution()

df = pd.DataFrame(
    {
        "Confidence": confidences
    }
)

st.title(
    "Analytics"
)

fig = px.histogram(
    df,
    x="Confidence",
    nbins=10,
    title="Confidence Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
