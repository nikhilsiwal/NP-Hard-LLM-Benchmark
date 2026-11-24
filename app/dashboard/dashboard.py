
import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px

from app.database.experiment_db import get_all_experiments


# PAGE CONFIGURATION

st.set_page_config(
    page_title="NP-Hard LLM Benchmark",
    page_icon="🧠",
    layout="wide"
)

st.title("NP-Hard Problem with LLM Benchmarking")
st.caption("Advanced AI-powered performance evaluation")


# LOAD DATA

experiments = get_all_experiments()

if not experiments:
    st.warning("No experiments found.")
    st.stop()

df = pd.DataFrame(experiments)

# Convert mixed solution lists into JSON strings.
# This prevents Streamlit Arrow serialization errors.
if "solution" in df.columns:
    df["solution"] = df["solution"].apply(
        lambda value: json.dumps(value)
        if isinstance(value, (list, dict))
        else str(value)
    )

if "tokens_used" not in df.columns:
    df["tokens_used"] = None

for column in ["tokens_used", "latency", "accuracy", "optimality_gap"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")


# PROBLEM NAMES

problem_names = {
    "tsp": "Travelling Salesman",
    "knapsack": "0/1 Knapsack",
    "graph_coloring": "Graph Coloring",
    "three_sat": "3-SAT",
    "subset_sum": "Subset Sum"
}

df["display_name"] = df["problem_name"].map(
    lambda x: problem_names.get(x, x)
)


# SIDEBAR FILTERS

st.sidebar.title("Dashboard Controls")

available_providers = sorted(
    df["provider"].dropna().unique().tolist()
)

available_problems = sorted(
    df["display_name"].dropna().unique().tolist()
)

selected_providers = st.sidebar.multiselect(
    "Select LLM Providers",
    options=available_providers,
    default=available_providers
)

selected_problems = st.sidebar.multiselect(
    "Select NP-Hard Problems",
    options=available_problems,
    default=available_problems
)

if st.sidebar.button("Refresh Dashboard"):
    st.rerun()


filtered_df = df[
    df["provider"].isin(selected_providers)
    & df["display_name"].isin(selected_problems)
].copy()

if filtered_df.empty:
    st.info("Select at least one provider and problem.")
    st.stop()


# LATEST EXPERIMENT PER PROVIDER AND PROBLEM

latest_df = (
    filtered_df.sort_values("id")
    .drop_duplicates(
        subset=["problem_name", "provider"],
        keep="last"
    )
    .copy()
)


# PERFORMANCE OVERVIEW

st.header("Performance Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Experiments", len(filtered_df))

col2.metric(
    "Valid Solutions",
    int(filtered_df["validity"].fillna(0).sum())
)

col3.metric(
    "Average Accuracy",
    f"{filtered_df['accuracy'].mean() * 100:.1f}%"
)

col4.metric(
    "Average Latency",
    f"{filtered_df['latency'].mean():.2f} sec"
)

st.divider()


# TOKEN USAGE

st.header("Token Usage Analysis")

token_df = filtered_df.dropna(
    subset=["tokens_used"]
).copy()

token_col1, token_col2, token_col3 = st.columns(3)

if not token_df.empty:

    token_col1.metric(
        "Total Tokens Used",
        f"{int(token_df['tokens_used'].sum()):,}"
    )

    token_col2.metric(
        "Average Tokens",
        f"{token_df['tokens_used'].mean():.1f}"
    )

    token_col3.metric(
        "Experiments with Token Data",
        len(token_df)
    )

    fig_tokens = px.bar(
        token_df,
        x="display_name",
        y="tokens_used",
        color="provider",
        barmode="group",
        text="tokens_used",
        title="Token Usage by Problem and Provider"
    )

    st.plotly_chart(fig_tokens, width="stretch")

else:

    token_col1.metric("Total Tokens Used", "N/A")
    token_col2.metric("Average Tokens", "N/A")
    token_col3.metric("Experiments with Token Data", 0)

    st.info("Token usage data is not available yet.")

st.divider()


# LATEST RESULTS

st.header("Latest Benchmark Results")

display_df = latest_df[
    [
        "display_name",
        "provider",
        "solution",
        "validity",
        "accuracy",
        "optimality_gap",
        "latency",
        "tokens_used",
        "id"
    ]
].copy()

display_df.columns = [
    "Problem",
    "Provider",
    "Solution",
    "Valid",
    "Accuracy",
    "Optimality Gap (%)",
    "Latency (seconds)",
    "Tokens Used",
    "Experiment ID"
]

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)

st.divider()


# ACCURACY COMPARISON

st.header("Accuracy Comparison")

accuracy_df = latest_df.copy()
accuracy_df["accuracy_percent"] = (
    accuracy_df["accuracy"] * 100
)

fig_accuracy = px.bar(
    accuracy_df,
    x="display_name",
    y="accuracy_percent",
    color="provider",
    barmode="group",
    text="accuracy_percent",
    title="Exact-Match Accuracy by Provider",
    labels={
        "display_name": "NP-Hard Problem",
        "accuracy_percent": "Accuracy (%)",
        "provider": "LLM Provider"
    }
)

fig_accuracy.update_layout(yaxis_range=[0, 100])

st.plotly_chart(fig_accuracy, width="stretch")


# LATENCY COMPARISON

st.header("Response Time Comparison")

fig_latency = px.bar(
    latest_df,
    x="display_name",
    y="latency",
    color="provider",
    barmode="group",
    text="latency",
    title="Response Latency by Provider"
)

st.plotly_chart(fig_latency, width="stretch")


# OPTIMALITY GAP

st.header("Optimality Gap Analysis")

gap_df = latest_df.dropna(
    subset=["optimality_gap"]
)

if not gap_df.empty:

    fig_gap = px.bar(
        gap_df,
        x="display_name",
        y="optimality_gap",
        color="provider",
        barmode="group",
        text="optimality_gap",
        title="Optimality Gap by Provider"
    )

    st.plotly_chart(fig_gap, width="stretch")

else:
    st.info("No optimality gap data available.")

st.divider()


# COMPLETE EXPERIMENT HISTORY

st.header("Complete Experiment History")

history_df = filtered_df.sort_values(
    "id",
    ascending=False
)

st.dataframe(
    history_df,
    width="stretch",
    hide_index=True
)


# FOOTER

st.divider()

st.caption(
    "Exact-match accuracy measures whether the objective value "
    "matches the reference optimum. A valid near-optimal solution "
    "may still have 0% exact-match accuracy. Missing token data "
    "is displayed as unavailable, not as zero."
)
