import streamlit as st

st.set_page_config(page_title='Saas Analytics Dashboard', layout="wide")

from utils.theme import load_css, kpi_card
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from google.cloud import bigquery
from utils.bigquery import get_client
from utils.navigation import show_navigation

client = get_client()

st.title("Saas Analytics Dashboard")
st.markdown("Overview de la performance business de AWS Business Services")
st.logo(image="AWS-Logo.png", size='large')

# Chargement du thème
load_css()

st.sidebar.title("Navigation")
show_navigation()

# Import dataset
query_sales = """
SELECT *
FROM `sam-dafs-16.dbt_splassmann.mart_sales_summary`
ORDER BY year, month
"""

query_customers = """
SELECT *
FROM `sam-dafs-16.dbt_splassmann.mart_customer_summary`
"""

geo_query = """
SELECT region, revenue
FROM `sam-dafs-16.dbt_splassmann.mart_geo_summary`
"""

query_customers = """
SELECT *
FROM `sam-dafs-16.dbt_splassmann.mart_customer_summary`
"""

products_query = """
SELECT *
FROM `sam-dafs-16.dbt_splassmann.mart_product_summary`
ORDER BY product
"""

@st.cache_data
def load_data(query):
    return client.query(query).to_dataframe()

sales = load_data(query_sales)
customers = load_data(query_customers)
geo = load_data(geo_query)
customers = load_data(query_customers)
products = load_data(products_query)

# KPI principaux
col1, col2, col3, col4 = st.columns(4)

total_revenue = sales["revenue_month"].sum()
total_orders = sales["total_orders"].sum()
active_customers = sales["active_customers"].sum()
avg_order_value = sales["avg_order_value"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card(
        "💰 Revenu total",
        f"{total_revenue:,.0f} €"
    )

with col2:
    kpi_card(
        "📦 Commandes",
        f"{total_orders:,}"
    )

with col3:
    kpi_card(
        "👥 Clients Actifs",
        f"{active_customers:,}"
    )

with col4:
    kpi_card(
        "🛒 Commande moyenne",
        f"{avg_order_value:,.0f} €"
    )

# Evolution du revenu
sales["date"] = pd.to_datetime(
    sales["year"].astype(str) + "-" + sales["month"].astype(str)
)

fig_revenue = px.line(
    sales,
    x="month_date",
    y="revenue_month",
    title="Revenu mensuel",
    labels={
        "revenue_month":"Revenu mensuel",
        "month_date":"Période"
    }
)
fig_revenue.update_xaxes(dtick="M1", tickformat="%m-%Y")

st.plotly_chart(fig_revenue, use_container_width=True)
st.info("Nos ventes sont en croissance depuis 2020, avec des chutes à chaque début d'année. Action commerciale à prévoir sur Q4 pour anticiper N+1")

# Nouveaux clients
fig_customers = px.bar(
    sales,
    x="month_date",
    y="new_customers",
    title="Nouveaux clients par mois",
    labels={
        "month_date":"Période",
        "new_customers":"Nouveaux clients"
    }
)

st.plotly_chart(fig_customers, use_container_width=True)
st.warning("⚠️ Pas de nouveaux clients en acquisition depuis Octobre 2020.")

# Revenu par région
geo = geo.groupby("region", as_index=False)["revenue"].max()
fig_geo = px.bar(
    geo,
    x="region",
    y="revenue",
    title="Revenu par région"
)
st.plotly_chart(fig_geo, use_container_width=True)


# Revenu par produit
fig = px.treemap(
    products,
    path=["product"],
    values="product_sales",
    title="Revenu par produit"
)

st.plotly_chart(fig, use_container_width=True)

