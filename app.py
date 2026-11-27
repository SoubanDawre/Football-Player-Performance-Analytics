from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Football Performance Analytics", page_icon="⚽", layout="wide")

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "football_players.csv"

METRIC_LABELS = {
    "goals": "Goals",
    "assists": "Assists",
    "rating": "Rating",
    "xg_per90": "Expected goals / 90",
    "xa_per90": "Expected assists / 90",
    "clean_sheets": "Clean sheets",
    "minutes": "Minutes played",
}

@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {
        "player", "nationality", "club", "position", "age", "matches",
        "starts", "minutes", "goals", "assists", "clean_sheets",
        "xg_per90", "xa_per90", "rating"
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(sorted(missing))}")
    numeric = required.intersection(df.select_dtypes(include="number").columns)
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

try:
    data = load_data(DATA_PATH)
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()

st.title("⚽ Football Player Performance Analytics")
st.caption("Explore player statistics, compare profiles, and discover performance patterns.")
st.warning(
    "Demo dataset notice: the included records are fictional and generated for demonstration. "
    "They do not describe real players, clubs, or official performance."
)

with st.sidebar:
    st.header("Filters")
    clubs = sorted(data["club"].dropna().unique().tolist())
    positions = sorted(data["position"].dropna().unique().tolist())
    selected_clubs = st.multiselect("Club", clubs, default=clubs)
    selected_positions = st.multiselect("Position", positions, default=positions)
    min_age, max_age = int(data["age"].min()), int(data["age"].max())
    age_range = st.slider("Age range", min_age, max_age, (min_age, max_age))
    search = st.text_input("Search player", placeholder="Enter a player name")

filtered = data[
    data["club"].isin(selected_clubs)
    & data["position"].isin(selected_positions)
    & data["age"].between(age_range[0], age_range[1])
]
if search.strip():
    filtered = filtered[filtered["player"].str.contains(search.strip(), case=False, na=False)]

if filtered.empty:
    st.info("No players match these filters. Try changing your selections.")
    st.stop()

total_goals = int(filtered["goals"].sum())
total_assists = int(filtered["assists"].sum())
avg_rating = filtered["rating"].mean()
total_players = len(filtered)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Players", f"{total_players}")
m2.metric("Goals", f"{total_goals}")
m3.metric("Assists", f"{total_assists}")
m4.metric("Average rating", f"{avg_rating:.2f}" if pd.notna(avg_rating) else "N/A")

overview_tab, compare_tab, rankings_tab, data_tab = st.tabs(
    ["📊 Overview", "🆚 Player comparison", "🏆 Rankings", "📄 Data"]
)

with overview_tab:
    left, right = st.columns(2)
    with left:
        goals_by_club = filtered.groupby("club", as_index=False)["goals"].sum().sort_values("goals", ascending=False)
        fig = px.bar(goals_by_club, x="club", y="goals", color="club",
                     title="Goals by club", labels={"club": "Club", "goals": "Goals"})
        fig.update_layout(showlegend=False, xaxis_title=None)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        position_counts = filtered["position"].value_counts().rename_axis("position").reset_index(name="players")
        fig = px.pie(position_counts, names="position", values="players", hole=0.48,
                     title="Player distribution by position")
        st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)
    with left:
        fig = px.scatter(
            filtered, x="xg_per90", y="goals", size="minutes", color="position",
            hover_name="player", hover_data=["club", "assists", "rating"],
            title="Goals vs expected goals per 90",
            labels={"xg_per90": "Expected goals / 90", "goals": "Goals", "minutes": "Minutes"}
        )
        st.plotly_chart(fig, use_container_width=True)
    with right:
        metric = st.selectbox("Metric for position analysis", ["goals", "assists", "rating", "xg_per90", "xa_per90"])
        position_metric = filtered.groupby("position", as_index=False)[metric].mean()
        fig = px.bar(position_metric, x="position", y=metric, color="position",
                     title=f"Average {METRIC_LABELS[metric]} by position")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

with compare_tab:
    player_names = sorted(filtered["player"].unique().tolist())
    if len(player_names) < 2:
        st.info("Select at least two players using the filters to compare them.")
    else:
        c1, c2 = st.columns(2)
        p1 = c1.selectbox("First player", player_names, index=0, key="compare_p1")
        p2 = c2.selectbox("Second player", player_names, index=1, key="compare_p2")
        if p1 == p2:
            st.info("Choose two different players.")
        else:
            pair = filtered.set_index("player").loc[[p1, p2]].reset_index()
            radar_metrics = ["goals", "assists", "rating", "xg_per90", "xa_per90", "clean_sheets"]
            # Normalize each metric to 0–100 so unlike units can be compared visually.
            normalized = pair[["player"] + radar_metrics].copy()
            for metric in radar_metrics:
                maximum = filtered[metric].max()
                normalized[metric] = (pair[metric] / maximum * 100) if maximum and pd.notna(maximum) else 0
            long = normalized.melt(id_vars="player", var_name="metric", value_name="normalized_value")
            fig = px.line_polar(long, r="normalized_value", theta="metric", color="player",
                                line_close=True, range_r=[0, 100], title="Normalized performance comparison")
            st.plotly_chart(fig, use_container_width=True)
            display_cols = ["player", "club", "position", "age", "matches", "minutes", "goals", "assists", "rating"]
            st.dataframe(pair[display_cols].set_index("player"), use_container_width=True)

with rankings_tab:
    metric = st.selectbox("Rank players by", list(METRIC_LABELS), format_func=lambda x: METRIC_LABELS[x])
    ascending = st.checkbox("Show lowest first", value=False)
    top_n = st.slider("Number of players", 5, min(20, max(5, len(filtered))), min(10, max(5, len(filtered))))
    ranked = filtered.sort_values(metric, ascending=ascending).head(top_n)
    fig = px.bar(ranked.sort_values(metric), x=metric, y="player", orientation="h",
                 color="position", hover_data=["club", "age"], title=f"Player ranking: {METRIC_LABELS[metric]}")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(ranked[["player", "club", "position", metric]].reset_index(drop=True), use_container_width=True)

with data_tab:
    st.subheader("Filtered player records")
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download filtered data (CSV)", csv, "filtered_football_players.csv", "text/csv")

st.divider()
st.caption("Built with Python, Pandas, Streamlit and Plotly • Demo analytics project")
