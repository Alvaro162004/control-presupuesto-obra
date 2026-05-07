import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración
st.set_page_config(page_title="Seguimiento de Presupuesto", layout="centered")

# Logo (Opcional: sube un archivo 'logo.png' a tu GitHub)
try:
    st.image("logo.png", width=150)
except:
    st.title("💰 Control de Presupuesto")

st.header("Registro de Albaranes")

# Formulario de entrada
with st.form("form_presupuesto"):
    num_albaran = st.text_input("Número de albarán")
    fecha = st.date_input("Fecha", datetime.now())
    trabajador = st.text_input("Nombre del Trabajador")
    
    partida = st.selectbox("Partida del presupuesto asociada", [
        "Material Eléctrico",
        "Mecanismos y Cuadros",
        "Iluminación",
        "Domótica y Automatismos",
        "Mano de Obra Exterior",
        "Varios / Otros"
    ])
    
    gastos = st.number_input("Gastos de esa partida (€)", min_value=0.0, step=0.01)
    comentarios = st.text_area("Comentarios")
    
    # Nota Extra: Foto del albarán
    foto_albaran = st.camera_input("Capturar foto del albarán")
    
    boton_añadir = st.form_submit_button("Añadir al registro")

# Base de datos temporal
if 'presupuesto' not in st.session_state:
    st.session_state.presupuesto = pd.DataFrame(columns=[
        "Número Albarán", "Fecha", "Trabajador", "Partida", "Gasto (€)", "Comentarios"
    ])

if boton_añadir:
    nuevo_gasto = {
        "Número Albarán": num_albaran,
        "Fecha": fecha.strftime("%d/%m/%Y"),
        "Trabajador": trabajador,
        "Partida": partida,
        "Gasto (€)": gastos,
        "Comentarios": comentarios
    }
    st.session_state.presupuesto = pd.concat([st.session_state.presupuesto, pd.DataFrame([nuevo_gasto])], ignore_index=True)
    st.success("Gasto registrado correctamente")

# Mostrar tabla y descarga
if not st.session_state.presupuesto.empty:
    st.divider()
    st.subheader("Resumen de Gastos")
    st.dataframe(st.session_state.presupuesto)
    
    total = st.session_state.presupuesto["Gasto (€)"].sum()
    st.metric("Gasto Total Acumulado", f"{total:,.2f} €")
    
    # Generar Excel
    nombre_archivo = "seguimiento_presupuesto.xlsx"
    st.session_state.presupuesto.to_excel(nombre_archivo, index=False)
    
    with open(nombre_archivo, "rb") as f:
        st.download_button("📥 Descargar Excel de Gastos", f, file_name=nombre_archivo)
