import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- CONFIGURACIÓN (DEBE ESTAR AL PRINCIPIO) ---
st.set_page_config(page_title="Tablero Interactivo - Proyecto de Grado", layout="wide")

# --- TÍTULO ---
st.title("📊 Tablero Interactivo - Análisis de Vehículos Varados")

# --- CARGA DE DATOS ---
st.sidebar.header("Cargar Datos")
archivo = st.sidebar.file_uploader("Sube el archivo Excel", type=["xlsx"])

if archivo:
    data = pd.read_excel(archivo)

    # --- LIMPIEZA DE DATOS ---
    data['Capacidad'] = data['Tipologia'].astype(str).str.extract(r'(\d+)')  # Usamos una cadena 'raw' para la expresión regular
    data['Capacidad'] = pd.to_numeric(data['Capacidad'], errors='coerce').astype('Int64')

    data['Tipologia'] = data['Tipologia'].replace(to_replace='BUS', value=1)
    data['Tipologia'] = data['Tipologia'].replace(to_replace='ALIMENTADOR', value=2)

    franja_map = {'a. m.': 0, 'p. m.': 1, 'a.\xa0m.': 0, 'p.\xa0m.': 1}  # Mantenemos el espacio invisible
    data['Franja'] = data['Franja'].replace(franja_map)
    data['Franja'] = pd.to_numeric(data['Franja'], errors='coerce').fillna(1).astype(int)
    data['Franja'] = data['Franja'].replace(-1, 1)

    # --- VISTA PREVIA DE LOS DATOS ---
    st.subheader("Vista previa de los datos")
    st.dataframe(data.head())

    # --- FILTRO POR FRANJA HORARIA ---
    opcion_franja = st.selectbox("Selecciona la Franja Horaria", options=data['Franja'].unique())
    data_filtrada = data[data['Franja'] == opcion_franja]

    # --- GRÁFICO DE CONTEO DE TIPOLOGÍAS ---
    st.subheader("Conteo de Tipologías en la Franja seleccionada")
    fig, ax = plt.subplots()
    sns.countplot(x='Tipologia', data=data_filtrada, ax=ax)
    st.pyplot(fig)

    # --- GRÁFICO DE CAJA Y BIGOTES DE EDAD POR MARCA ---
    st.subheader("📦 Distribución de Edad de la Flota por Marca")

    if 'Marca' in data.columns and 'Edad' in data.columns:
        marcas = data['Marca'].dropna().unique()
        marca_seleccionada = st.selectbox("Selecciona una Marca", marcas)

        datos_marca = data[data['Marca'] == marca_seleccionada]

        fig2, ax2 = plt.subplots()
        sns.boxplot(x='Marca', y='Edad', data=datos_marca, ax=ax2)
        ax2.set_title(f"Distribución de Edad para la Marca {marca_seleccionada}")
        st.pyplot(fig2)
    else:
        st.info("Las columnas 'Marca' y/o 'Edad' no se encuentran en los datos.")

else:
    st.warning("Por favor, sube un archivo Excel con los datos.")