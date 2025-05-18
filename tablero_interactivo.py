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

if archivo:  # Indent the rest of the code under this condition
    data = pd.read_excel(archivo)

    # --- LIMPIEZA DE DATOS ---
    # Asegúrate de que las operaciones de reemplazo se realicen solo si la columna existe
    if 'Tipologia' in data.columns:
        data['Tipologia'] = data['Tipologia'].replace(to_replace='BUS', value=1)
        data['Tipologia'] = data['Tipologia'].replace(to_replace='ALIMENTADOR', value=2)
    else:
        st.error("La columna 'Tipologia' no existe en los datos.")
        st.stop()  # Detener la ejecución si la columna no existe

    st.subheader("Vista previa de los datos")
    st.dataframe(data.head())

    # --- FILTRO POR MODELO ---
    if 'Modelo' in data.columns:
        modelos = data['Modelo'].dropna().unique()
        modelo_seleccionado = st.selectbox("Selecciona un Modelo", options=modelos)
        data_filtrada = data[data['Modelo'] == modelo_seleccionado]

        # --- CONTEO DE TIPOLOGÍAS PARA EL MODELO SELECCIONADO ---
        st.subheader(f"📌 Conteo de Tipologías para el Modelo: {modelo_seleccionado}")
        fig, ax = plt.subplots()
        sns.countplot(x='Tipologia', data=data_filtrada, ax=ax)
        st.pyplot(fig)
    else:
        st.error("La columna 'Modelo' no existe en los datos.")
        st.stop()

    # --- CANTIDAD DE FLOTA POR MODELO (BARRAS) ---
    st.subheader("🚍 Cantidad de Flota por Modelo (Total)")
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    if 'Modelo' in data.columns:  # Verificar antes de calcular
        conteo_modelos = data['Modelo'].value_counts().sort_values(ascending=False)
        sns.barplot(x=conteo_modelos.index, y=conteo_modelos.values, ax=ax2)
        ax2.set_xlabel("Modelo")
        ax2.set_ylabel("Cantidad de Flota")
        ax2.set_title("Cantidad Total de Flota por Modelo")
        ax2.tick_params(axis='x', rotation=45)
        st.pyplot(fig2)
    else:
        st.error("La columna 'Modelo' no existe en los datos.")
        st.stop()

    # --- GRÁFICO DE CAJA Y BIGOTES DE EDAD POR MARCA ---
    st.subheader("📦 Distribución de Edad de la Flota por Marca")

    if 'Marca' in data.columns and 'Edad' in data.columns:
        marcas = data['Marca'].dropna().unique()
        marca_seleccionada = st.selectbox("Selecciona una Marca", marcas)

        datos_marca = data[data['Marca'] == marca_seleccionada]

        fig3, ax3 = plt.subplots()  # Use a different figure name
        sns.boxplot(x='Marca', y='Edad', data=datos_marca, ax=ax3)
        ax3.set_title(f"Distribución de Edad para la Marca {marca_seleccionada}")
        st.pyplot(fig3)
    else:
        st.info("Las columnas 'Marca' y/o 'Edad' no se encuentran en los datos.")

else:
    st.warning("Por favor, sube un archivo Excel con los datos.")