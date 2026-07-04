import streamlit as st
import pandas as pd
from datetime import datetime
from db import create_reclamo, get_reclamos

st.set_page_config(page_title="GIRU - Reclamos Bancarios", layout="wide")

st.title("🏦 GIRU - Sistema de Pedidos y Reclamos")

menu = st.sidebar.selectbox("Menú", ["Crear Reclamo", "Ver Reclamos"])

# =========================
# FORMULARIO DE RECLAMOS
# =========================
if menu == "Crear Reclamo":
    st.subheader("📩 Registrar nuevo reclamo")

    with st.form("reclamo_form"):
        nombre = st.text_input("Nombre del cliente")
        tipo = st.selectbox("Tipo de problema", [
            "Error en transacción",
            "Problema con tarjeta",
            "App no funciona",
            "Cobro indebido",
            "Otro"
        ])
        descripcion = st.text_area("Describe el problema")
        prioridad = st.selectbox("Prioridad", ["Baja", "Media", "Alta"])

        submit = st.form_submit_button("Enviar reclamo")

        if submit:
            create_reclamo(nombre, tipo, descripcion, prioridad)
            st.success("✅ Reclamo registrado correctamente")

# =========================
# LISTADO DE RECLAMOS
# =========================
if menu == "Ver Reclamos":
    st.subheader("📊 Reclamos registrados")

    data = get_reclamos()

    if len(data) == 0:
        st.info("No hay reclamos aún")
    else:
        df = pd.DataFrame(data, columns=[
            "ID", "Nombre", "Tipo", "Descripción", "Prioridad", "Fecha"
        ])
        st.dataframe(df, use_container_width=True)

        st.metric("Total reclamos", len(df))
