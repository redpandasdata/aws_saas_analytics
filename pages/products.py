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
st.title("Product Analytics")
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
products_query = """
SELECT *
FROM `sam-dafs-16.dbt_splassmann.mart_product_summary`
ORDER BY product
"""
products = load_data(products_query)

# -----------------------------
# Sidebar filtres
# -----------------------------
st.sidebar.header("Filtres produits")

# Pour l'instant, on ne peut filtrer que par produit
selected_product = st.sidebar.multiselect(
    "Produit", options=products["product"].unique()
)

# Appliquer le filtre
filtered_products = products.copy()
if selected_product:
    filtered_products = filtered_products[filtered_products["product"].isin(selected_product)]

# -----------------------------
# KPI produits
# -----------------------------
total_products = filtered_products["product"].nunique()
total_revenue = filtered_products["product_sales"].sum()
avg_revenue_per_product = filtered_products["product_sales"].mean()
total_quantity = filtered_products["product_quantity"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Produits actifs", f"{total_products:,}")
col2.metric("Revenu total", f"{total_revenue:,.0f} €")
col3.metric("Revenu moyen / produit", f"{avg_revenue_per_product:,.0f} €")
col4.metric("Quantité vendue", f"{total_quantity:,}")

# -----------------------------
# Graphiques
# -----------------------------
# Top produits par revenu
top_products = filtered_products.sort_values(
    "product_sales", ascending=False
).head(10)
fig_top_products = px.bar(
    top_products,
    x="product",
    y="product_sales",
    title="Top 10 Produits par Revenu",
    text="product_sales"
)
fig_top_products.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
st.plotly_chart(fig_top_products, use_container_width=True)

# Distribution des ventes
fig_sales_dist = px.histogram(
    filtered_products,
    x="product_sales",
    nbins=30,
    title="Distribution du revenu produit"
)
st.plotly_chart(fig_sales_dist, use_container_width=True)

# -----------------------------
# Tableau produits
# -----------------------------
st.subheader("Détails produits")
st.dataframe(
    filtered_products.sort_values("product_sales", ascending=False),
    use_container_width=True
)

# Revenu par produit
fig = px.treemap(
    products,
    path=["product"],
    values="product_sales",
    title="Revenu par produit"
)

st.plotly_chart(fig, use_container_width=True)