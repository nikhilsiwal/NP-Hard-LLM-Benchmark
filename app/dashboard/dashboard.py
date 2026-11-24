
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px

from app.database.experiment_db import get_all_experiments


# Page setup
st.set_page_config(
    page_title="NP-Hard LLM Benchmark",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 NP-Hard Problem with LLM Benchmarking")
st.caption("AI-powered performance evaluation of NP-hard problems")

# Load data
experiments = get_all_experiments()

if not experiments:
    st.warning("No experiments found.")
    st.stop()

df = pd.DataFrame(experiments)

gemini_df = df[df["provider"] == "gemini"].copy()

if gemini_df.empty:
    st.warning("No Gemini experiments found.")
    st.stop()

# Latest experiment for each problem
latest_df = (
    gemini_df.sort_values("id")
    .drop_duplicates("problem_name", keep="last")
    .copy()
)

# Readable names
problem_names = {
    "tsp": "Travelling Salesman",
    "knapsack": "0/1 Knapsack",
    "graph_coloring": "Graph Coloring",
    "three_sat": "3-SAT",
    "subset_sum": "Subset Sum"
}

latest_df["display_name"] = latest_df["problem_name"].map(
    lambda x: problem_names.get(x, x)
)

# Sidebar
st.sidebar.title("⚙️ Dashboard Controls")

available_problems = latest_df["display_name"].tolist()

selected_problems = st.sidebar.multiselect(
    "Select Problems",
    options=available_problems,
    default=available_problems
)

if st.sidebar.button("🔄 Refresh Dashboard"):
    st.rerun()

filtered_df = latest_df[
    latest_df["display_name"].isin(selected_problems)
].copy()

if filtered_df.empty:
    st.info("Select at least one problem from the sidebar.")
    st.stop()

# Overview
st.header("📊 Performance Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Problems Benchmarked",
    filtered_df["problem_name"].nunique()
)

col2.metric(
    "Valid Solutions",
    int(filtered_df["validity"].sum())
)

col3.metric(
    "Average Exact-Match Accuracy",
    f"{filtered_df['accuracy'].mean() * 100:.1f}%"
)

col4.metric(
    "Average Latency",
    f"{filtered_df['latency'].mean():.2f} sec"
)

st.divider()

# Latest results
st.header("📋 Latest Gemini Results")

display_df = filtered_df[
    [
        "display_name",
        "solution",
        "validity",
        "accuracy",
        "optimality_gap",
        "latency",
        "id"
    ]
].copy()

display_df.columns = [
    "Problem",
    "Gemini Solution",
    "Valid",
    "Exact-Match Accuracy",
    "Optimality Gap (%)",
    "Latency (seconds)",
    "Experiment ID"
]

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# Accuracy chart
st.header("📈 Accuracy Comparison")

accuracy_df = filtered_df.copy()
accuracy_df["accuracy_percent"] = accuracy_df["accuracy"] * 100

fig_accuracy = px.bar(
    accuracy_df,
    x="display_name",
    y="accuracy_percent",
    color="display_name",
    text="accuracy_percent",
    title="Exact-Match Accuracy by Problem",
    labels={
        "display_name": "NP-Hard Problem",
        "accuracy_percent": "Accuracy (%)"
    }
)

fig_accuracy.update_layout(
    yaxis_range=[0, 100],
    showlegend=False
)

st.plotly_chart(fig_accuracy, use_container_width=True)

# Latency chart
st.header("⏱️ Response Time Comparison")

fig_latency = px.bar(
    filtered_df,
    x="display_name",
    y="latency",
    color="display_name",
    text="latency",
    title="Gemini Response Time",
    labels={
        "display_name": "NP-Hard Problem",
        "latency": "Latency (seconds)"
    }
)

fig_latency.update_layout(showlegend=False)

st.plotly_chart(fig_latency, use_container_width=True)

# Optimality gap
st.header("🎯 Optimality Gap Comparison")

gap_df = filtered_df.dropna(subset=["optimality_gap"])

fig_gap = px.bar(
    gap_df,
    x="display_name",
    y="optimality_gap",
    color="display_name",
    text="optimality_gap",
    title="Optimality Gap by Problem",
    labels={
        "display_name": "NP-Hard Problem",
        "optimality_gap": "Optimality Gap (%)"
    }
)

fig_gap.update_layout(showlegend=False)

st.plotly_chart(fig_gap, use_container_width=True)

st.divider()

# Experiment history
st.header("🗂️ Experiment History")

history_df = df.sort_values("id", ascending=False).copy()

st.dataframe(
    history_df,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Note: Exact-match accuracy measures whether the objective value "
    "matches the reference optimum. A valid near-optimal solution "
    "may still have 0% exact-match accuracy."
)

