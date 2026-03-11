import streamlit as st
from google.cloud import bigquery

@st.cache_resource
def get_client():
    return bigquery.Client.from_service_account_info(st.secrets["google"])

