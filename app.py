import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from google.cloud import bigquery

client = bigquery.Client()

query = "SELECT * FROM `sam-dafs-16.dbt_splassmann.mart_customer_summary`"
df = client.query(query).to_dataframe()

display(df.head())