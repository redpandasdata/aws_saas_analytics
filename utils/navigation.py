import streamlit as st

def show_navigation():

    with st.sidebar:
        st.page_link("app.py", label="Overview", icon="📊")
        st.page_link("pages/customers.py", label="Clients", icon="👨‍💼")
        st.page_link("pages/geo.py", label="Géo-analyses", icon="🌍")
        st.page_link("pages/products.py", label="Produits", icon="⚙️")

    st.sidebar.markdown("---")
    st.sidebar.caption("Developped by Samuel P.")