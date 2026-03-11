from fastapi import FastAPI
import pandas as pd
import json
from pathlib import Path

app = FastAPI(
    title="Mock HubSpot CRM API",
    description="Simulation d'une API CRM pour ingestion data pipeline",
    version="1.0"
)

DATA_PATH = Path("data")

# -----------------------------
# Helper functions
# -----------------------------

def load_json(filename):
    with open(DATA_PATH / filename, "r") as f:
        return json.load(f)

# -----------------------------
# Root endpoint
# -----------------------------

@app.get("/")
def root():
    return {
        "message": "Mock HubSpot CRM API",
        "endpoints": [
            "/customers",
            "/deals",
            "/products"
        ]
    }

# -----------------------------
# Customers endpoint
# -----------------------------

@app.get("/customers")
def get_customers():
    customers = load_json("customers.json")
    return {
        "total": len(customers),
        "results": customers
    }

# -----------------------------
# Deals endpoint
# -----------------------------

@app.get("/deals")
def get_deals():
    deals = load_json("deals.json")
    return {
        "total": len(deals),
        "results": deals
    }

# -----------------------------
# Products endpoint
# -----------------------------

@app.get("/products")
def get_products():
    products = load_json("products.json")
    return {
        "total": len(products),
        "results": products
    }

# -----------------------------
# Customer by ID
# -----------------------------

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):

    customers = load_json("customers.json")

    for c in customers:
        if c["id"] == customer_id:
            return c

    return {"error": "Customer not found"}

# -----------------------------
# Deals by customer
# -----------------------------

@app.get("/customers/{customer_id}/deals")
def get_customer_deals(customer_id: int):

    deals = load_json("deals.json")

    customer_deals = [
        d for d in deals if d["customer_id"] == customer_id
    ]

    return {
        "customer_id": customer_id,
        "deals": customer_deals
    }