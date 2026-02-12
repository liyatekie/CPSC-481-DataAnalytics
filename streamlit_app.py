import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(layout="wide")

# Dark cinematic style
st.markdown("""
<style>
html, body, [class*="css"]  {
    background-color: #000000;
    color: #ffffff;
}
.big-title {
    font-size: 64px;
    font-weight: 800;
    text-align: center;
    margin-top: 80px;
}
.subtitle {
    font-size: 26px;
    text-align: center;
    opacity: 0.8;
}
.section {
    margin-top: 120px;
}
.center {
    text-align: center;
    font-size: 24px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# INTRO
# --------------------------------------------------
st.markdown("<div class='big-title'>The Eritrean Journey</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>This is not migration. This is survival.</div>", unsafe_allow_html=True)

st.markdown("<div class='section'></div>", unsafe_allow_html=True)

# --------------------------------------------------
# SECTION 1 – SAWA
# --------------------------------------------------
st.markdown("<div class='center'>Where It Begins</div>", unsafe_allow_html=True)

col1, col2 = st.columns([1,2])

with col1:
    st.image("sawa-eritrea-4.jpg", width=350)

with col2:
    st.markdown("""
National service has no defined end.  
For many young Eritreans, the future becomes uncertain.  
Leaving becomes the only option.
""")

st.markdown("<div class='section'></div>", unsafe_allow_html=True)

# --------------------------------------------------
# SECTION 2 – JOURNEY
# --------------------------------------------------
st.markdown("<div class='center'>The Journey Through Libya</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.image("libya-migrants.jpg", width=350)

with col2:
    st.image("boat.jpg", width=350)

st.markdown("""
The path moves through Sudan.  
Through Libya.  
Onto unstable boats.  
Across the Mediterranean Sea.
""")

st.markdown("<div class='section'></div>", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
refugees = pd.read_csv("data/eritrean_refugees_full.csv")
deaths = pd.read_csv("data/mediterranean_deaths_full.csv")
lampedusa = pd.read_csv("data/lampedusa_2013_event.csv")

# --------------------------------------------------
# SECTION 3 – INTERACTIVE DATA
# --------------------------------------------------
st.markdown("<div class='center'>The Numbers</div>", unsafe_allow_html=True)

years = sorted(refugees["Year"].unique())

# SAFE slider (no crash)
year = st.select_slider(
    "Select Year",
    options=years,
    value=years[len(years)//2]
)

refugees_year = refugees[refugees["Year"] == year]
deaths_year = deaths[deaths["Year"] == year]

total_refugees = int(refugees_year["Refugees"].sum())
total_deaths = int(deaths_year["Deaths_Mediterranean"].sum())

col1, col2 = st.columns(2)
col1.metric("Eritreans Living Abroad", f"{total_refugees:,}")
col2.metric("Mediterranean Deaths", f"{total_deaths:,}")

st.markdown("<div class='section'></div>", unsafe_allow_html=True)

# --------------------------------------------------
# GLOBAL DISTRIBUTION MAP
# --------------------------------------------------
st.markdown("<div class='center'>Global Distribution</div>", unsafe_allow_html=True)

fig_map = px.choropleth(
    refugees_year,
    locations="Country_of_Asylum",
    locationmode="country names",
    color="Refugees",
    color_continuous_scale="Reds"
)

fig_map.update_layout(
    paper_bgcolor="black",
    plot_bgcolor="black",
    font_color="white",
    height=600
)

st.plotly_chart(fig_map, width="stretch")

st.markdown("<div class='section'></div>", unsafe_allow_html=True)

# --------------------------------------------------
# DEATH TIMELINE
# --------------------------------------------------
st.markdown("<div class='center'>Mediterranean Deaths Over Time</div>", unsafe_allow_html=True)

fig_line = px.line(
    deaths,
    x="Year",
    y="Deaths_Mediterranean",
    markers=True
)

fig_line.update_layout(
    paper_bgcolor="black",
    plot_bgcolor="black",
    font_color="white",
    height=600
)

st.plotly_chart(fig_line, width="stretch")

st.markdown("<div class='section'></div>", unsafe_allow_html=True)

# --------------------------------------------------
# LAMPEDUSA EVENT
# --------------------------------------------------
st.markdown("<div class='center'>October 3, 2013 — Lampedusa</div>", unsafe_allow_html=True)

st.markdown("""
A boat carrying mostly Eritrean migrants sank near Italy.  
More than 360 people died.
""")

st.dataframe(lampedusa)

st.markdown("<div class='section'></div>", unsafe_allow_html=True)

st.markdown("""
Behind every spike is a life.  
Behind every bar is a family
""")
