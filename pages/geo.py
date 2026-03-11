import pandas as pd
import streamlit as st
import plotly.express as px
from google.cloud import bigquery
from utils.bigquery import get_client
from utils.navigation import show_navigation
from utils.theme import load_css

# Chargement du thème
load_css()
# -----------------------------
# Page config
# -----------------------------
st.title("Geo Analytics")
st.logo(image="AWS-Logo.png", size='large')

st.sidebar.title("Navigation")
show_navigation()

# -----------------------------
# BigQuery Client
# -----------------------------
client = get_client()

@st.cache_data
def load_data(query):
    return client.query(query).to_dataframe()

# -----------------------------
# Import des données
# -----------------------------
geo_query = """
SELECT *
FROM `sam-dafs-16.dbt_splassmann.mart_geo_summary`
"""
geo = load_data(geo_query)

# -----------------------------
# Sidebar filtres
# -----------------------------
st.sidebar.header("Filtres géographiques")
selected_region = st.sidebar.multiselect(
    "Région", options=geo["region"].unique()
)
if selected_region:
    geo = geo[geo["region"].isin(selected_region)]

selected_country = st.sidebar.multiselect(
    "Pays", options=geo["country"].unique()
)
if selected_country:
    geo = geo[geo["country"].isin(selected_country)]

# -----------------------------
# KPI géo
# -----------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Régions", geo["region"].nunique())
col2.metric("Pays", geo["country"].nunique())
col3.metric("Revenu total", f"{geo['revenue'].sum():,.0f} €")
col4.metric("Profit total", f"{geo['profit'].sum():,.0f} €")

# -----------------------------
# Carte mondiale - Revenu par pays
# -----------------------------
st.subheader("Carte mondiale - Revenu par pays")
fig_revenue_map = px.choropleth(
    geo,
    locations="country",        # colonne avec les noms de pays
    locationmode="country names",
    color="revenue",
    hover_name="country",
    color_continuous_scale="Oranges",
    title="Revenu par pays",
)
st.plotly_chart(fig_revenue_map, use_container_width=True)

# Carte mondiale - Profit par pays
st.subheader("Carte mondiale - Profit par pays")
fig_profit_map = px.choropleth(
    geo,
    locations="country",
    locationmode="country names",
    color="profit",
    hover_name="country",
    color_continuous_scale="Blues",
    title="Profit par pays",
)
st.plotly_chart(fig_profit_map, use_container_width=True)

# -----------------------------
# Top régions par revenu
# -----------------------------
top_regions = geo.groupby("region", as_index=False)["revenue"].sum()
top_regions = top_regions.sort_values("revenue", ascending=False).head(10)

st.subheader("Top 10 régions par revenu")
st.bar_chart(top_regions.set_index("region")["revenue"])

# -----------------------------
# Tableau géographique
# -----------------------------
st.subheader("Détails géographiques")
st.dataframe(
    geo.sort_values("revenue", ascending=False),
    use_container_width=True
)