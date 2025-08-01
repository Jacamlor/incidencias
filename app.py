import streamlit as st
import pandas as pd
import os
from database import init_db, insertar_albaran, obtener_albaranes, ajustar_cantidad_albaran, registrar_incidencia, obtener_incidencias

st.set_page_config(page_title="Incidencias", layout="wide")
st.title("📦 Registro de Incidencias")

# Mostrar conexión
st.info(f"📡 Conectando a: {os.getenv('SUPABASE_URL')}")

init_db()

tabs = st.tabs(["➕ Albarán", "⚠️ Incidencia", "📋 Ver incidencias"])

with tabs[0]:
    st.subheader("Nuevo albarán")
    num = st.text_input("Nº Albarán")
    tienda = st.text_input("Tienda")
    cant = st.number_input("Cantidad", min_value=0)
    if st.button("Guardar albarán"):
        if num and tienda and cant > 0:
            insertar_albaran(num, tienda, cant)
            st.success("Albarán registrado")

with tabs[1]:
    st.subheader("Registrar incidencia")
    albaranes = obtener_albaranes()
    if not albaranes:
        st.warning("No hay albaranes")
    else:
        albaran = st.selectbox("Selecciona albarán", albaranes)
        tienda = st.text_input("Tienda")
        tipo = st.selectbox("Tipo", ["Faltan", "Sobra","Diferencia de talla", "Fallo color", "Fallo transfer", "Otro"])
        estado = st.selectbox("Estado", ["Pendiente", "Resuelto"])
        desc = st.text_area("Descripción")
        ajuste = st.number_input("Cantidad a ajustar", min_value=0)
        modo = st.radio("Tipo de ajuste", ["Sumar", "Restar"])
        if st.button("Registrar incidencia"):
            ajustar_cantidad_albaran(albaran, ajuste, modo)
            registrar_incidencia((albaran, tienda, tipo, desc, estado, ajuste, modo, usuario, pd.Timestamp.now().isoformat()))
            st.success("Incidencia registrada")

with tabs[2]:
    st.subheader("Incidencias registradas")
    data, cols = obtener_incidencias()
    if not data:
        st.info("No hay incidencias")
    else:
        df = pd.DataFrame(data, columns=cols)
        st.dataframe(df, use_container_width=True)
