import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Global Migration Dashboard",
    layout="wide"
)

st.title("Global Migration Flows")

# -----------------------------
# Dataset description + question
# -----------------------------
st.markdown(
    """
### Dataset description
This dataset contains international migration stock data for the year 2020.  
Each row represents the number of people born in one country (**Origin**) who are living in another country (**Destination**).

**Source:** United Nations International Migrant Stock dataset (cleaned and reformatted for this project).

### Question
For a selected origin country:
- Which destination countries host the largest migrant populations?
- Is migration concentrated in a few destinations or spread across many countries?
"""
)

# -----------------------------
# Load and clean data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/migration_2020_clean.csv")

    df["Origin"] = df["Origin"].astype(str).str.strip()
    df["Destination"] = df["Destination"].astype(str).str.strip()
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

    df = df.dropna(subset=["Origin", "Destination", "Value"])
    df = df[df["Value"] >= 0]

    return df

df = load_data()

with st.expander("Preview of the data"):
    st.dataframe(df.head(15), width="stretch")

# -----------------------------
# Sidebar controls (interaction)
# -----------------------------
st.sidebar.header("Filters")

origin_countries = sorted(df["Origin"].unique())
selected_origin = st.sidebar.selectbox(
    "Select origin country",
    origin_countries,
    index=origin_countries.index("Eritrea") if "Eritrea" in origin_countries else 0
)

top_n = st.sidebar.slider(
    "Number of top destinations",
    min_value=5,
    max_value=25,
    value=10
)

filtered_df = df[df["Origin"] == selected_origin].copy()

if filtered_df.empty:
    st.error("No data available for the selected origin.")
    st.stop()

# -----------------------------
# Summary metrics
# -----------------------------
total_abroad = int(filtered_df["Value"].sum())
num_destinations = filtered_df["Destination"].nunique()

c1, c2, c3 = st.columns(3)
c1.metric("Origin country", selected_origin)
c2.metric("Total migrants abroad", f"{total_abroad:,}")
c3.metric("Destination countries", num_destinations)

st.divider()

# -----------------------------
# Visualization 1: World map
# -----------------------------
st.subheader("Map: Global distribution of migrants")

fig_map = px.choropleth(
    filtered_df,
    locations="Destination",
    locationmode="country names",
    color="Value",
    hover_name="Destination",
    hover_data={"Value": ":,0f"},
    color_continuous_scale="Viridis"
)

fig_map.update_layout(
    title=f"Migrants from {selected_origin} by destination",
    height=520,
    margin=dict(l=0, r=0, t=60, b=0),
    coloraxis_colorbar=dict(title="People")
)

st.plotly_chart(fig_map, width="stretch")

# -----------------------------
# Visualization 2: Ranked destinations (light + animated)
# -----------------------------
st.subheader("Ranking: Top destination countries")

top_destinations = (
    filtered_df.sort_values("Value", ascending=False)
    .head(top_n)
    .sort_values("Value", ascending=True)
)

fig_bar = px.bar(
    top_destinations,
    x="Value",
    y="Destination",
    orientation="h",
    text="Value",
    color="Value",
    color_continuous_scale=px.colors.sequential.Tealgrn,
    labels={
        "Value": "Number of people",
        "Destination": "Destination country"
    }
)

fig_bar.update_traces(
    texttemplate="%{text:,}",
    textposition="outside"
)

fig_bar.update_layout(
    title=f"Top {top_n} destinations for migrants from {selected_origin}",
    height=520,
    margin=dict(l=160, r=30, t=60, b=40),
    xaxis_title="Number of people",
    yaxis_title="",
    transition_duration=700,
    coloraxis_showscale=False,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig_bar, width="stretch")

# -----------------------------
# Visualization 3: Sankey flow (movement-focused)
# -----------------------------
st.subheader("Flow view: Origin → destinations")

top_flows = (
    filtered_df.sort_values("Value", ascending=False)
    .head(top_n)
)

labels = [selected_origin] + top_flows["Destination"].tolist()
source = [0] * len(top_flows)
target = list(range(1, len(top_flows) + 1))
values = top_flows["Value"].astype(int).tolist()

fig_sankey = go.Figure(
    data=[
        go.Sankey(
            arrangement="snap",
            node=dict(
                label=labels,
                pad=20,
                thickness=18,
                color=["#B8E1DD"] + ["#E6C7E8"] * len(top_flows)
            ),
            link=dict(
                source=source,
                target=target,
                value=values,
                color="rgba(150,200,220,0.45)"
            )
        )
    ]
)

fig_sankey.update_layout(
    title=f"Migration flow from {selected_origin} to top {top_n} destinations",
    height=520,
    margin=dict(l=20, r=20, t=60, b=20),
    paper_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig_sankey, width="stretch")

# -----------------------------
# Interpretation
# -----------------------------
st.markdown(
    """
### Interpretation
- Most migrants from the selected country go to only a few destinations, not everywhere.
- This means migration is concentrated in certain countries.
- The map shows where migrants are located in the world.
- The flow diagram helps show migration as movement from one country to many others.
"""
)

