import pandas as pd
import streamlit as st

from revenue_recovery import (
    calculate_recovery_priority,
    calculate_recovery_metrics,
)


st.set_page_config(
    page_title="AI Revenue Recovery",
    page_icon="💰",
    layout="wide",
)


st.title("💰 AI Revenue Recovery")
st.subheader("Identify and prioritize lost revenue opportunities")


# Load data
df = pd.read_csv("data/sample_revenue_data.csv")


# Run recovery engine
df = calculate_recovery_priority(df)

metrics = calculate_recovery_metrics(df)


# KPI section
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Overdue Revenue",
        f"${metrics['total_overdue_revenue']:,.0f}",
    )

with col2:
    st.metric(
        "High-Priority Revenue",
        f"${metrics['high_priority_revenue']:,.0f}",
    )

with col3:
    st.metric(
        "Estimated Recoverable Revenue",
        f"${metrics['estimated_recovery']:,.0f}",
    )


st.divider()


# Recovery opportunities
st.subheader("🚨 Recovery Opportunities")

overdue_df = df[df["is_overdue"]].copy()

overdue_df = overdue_df.sort_values(
    by="recovery_score",
    ascending=False,
)


st.dataframe(
    overdue_df[
        [
            "customer_id",
            "customer_name",
            "invoice_amount",
            "days_overdue",
            "recovery_score",
            "priority",
        ]
    ],
    use_container_width=True,
)


st.divider()


# Full dataset
st.subheader("📊 Customer Revenue Data")

st.dataframe(
    df,
    use_container_width=True,
)
