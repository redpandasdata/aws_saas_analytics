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
st.title("Customer Analytics")
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
customers_query = """
SELECT *
FROM `sam-dafs-16.dbt_splassmann.mart_customer_summary`
"""
sales_query = """
SELECT *
FROM `sam-dafs-16.dbt_splassmann.mart_sales_summary`
ORDER BY year, month
"""

customers = load_data(customers_query)
sales = load_data(sales_query)

# Créer une colonne date pour les graphiques temporels
sales["month_date"] = pd.to_datetime(
    sales["year"].astype(str) + "-" + sales["month"].astype(str) + "-01"
)

# -----------------------------
# Sidebar filtres
# -----------------------------
st.sidebar.header("Filtres clients")

selected_customer = st.sidebar.multiselect(
    "Client", options=customers["customer_name"].unique()
)

selected_segment = st.sidebar.multiselect(
    "Segment", options=customers["segment"].unique()
)

selected_industry = st.sidebar.multiselect(
    "Industrie", options=customers["industry"].unique()
)

# Appliquer les filtres
filtered_customers = customers.copy()

if selected_customer:
    filtered_customers = filtered_customers[filtered_customers["customer_name"].isin(selected_customer)]
if selected_segment:
    filtered_customers = filtered_customers[filtered_customers["segment"].isin(selected_segment)]
if selected_industry:
    filtered_customers = filtered_customers[filtered_customers["industry"].isin(selected_industry)]

# -----------------------------
# KPI clients
# -----------------------------
# Détecter les bonnes colonnes pour le calcul
ltv_col = "ltv" if "ltv" in filtered_customers.columns else "total_sales"
orders_col = "total_orders" if "total_orders" in filtered_customers.columns else None

total_customers = filtered_customers["customer_name"].nunique()
total_revenue = filtered_customers[ltv_col].sum()
avg_customer_value = filtered_customers[ltv_col].mean()
avg_orders = filtered_customers[orders_col].mean() if orders_col else 0

col1, col2, col3= st.columns(3)
col1.metric("Total Clients", f"{total_customers:,}")
col2.metric("Revenu clients", f"{total_revenue:,.0f} €")
col3.metric("Valeur moyenne client", f"{avg_customer_value:,.0f} €")

# -----------------------------
# Graphiques clients
# -----------------------------
# Distribution valeur client
fig_ltv = px.histogram(
    filtered_customers,
    x=ltv_col,
    nbins=30,
    title="Distribution de la valeur client",
    labels={
        "ltv":"Life Time Value",
        "count":"Quantité"
    }
)
fig_ltv.add_vline(
    x=customers["ltv"].mean(),
    line_dash="dash",
    annotation_text=f"Moyenne LTV : {customers["ltv"].mean().round()}"
)
st.plotly_chart(fig_ltv, use_container_width=True)
st.info("**Customer Lifetime Value (LTV):** Revenu total généré par un client pendant toute la durée de sa relation avec l'entreprise. Par exemple : 2 clients ont généré un revenu total compris entre 700 et 750 € sur toute leur durée de vie." )

# Top 10 clients par revenu
top_customers = filtered_customers.sort_values(
    ltv_col, ascending=False
).head(10)
fig_top = px.bar(
    top_customers,
    x="customer_name",
    y=ltv_col,
    title="Top 10 clients par revenu"
)
st.plotly_chart(fig_top, use_container_width=True)

# -----------------------------
# Tableau client
# -----------------------------
st.subheader("Détails clients")
st.dataframe(
    filtered_customers.sort_values(ltv_col, ascending=False),
    use_container_width=True
)