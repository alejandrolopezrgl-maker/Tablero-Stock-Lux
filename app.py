import os
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Tablero Operativo Lux", layout="wide")

DATA_DIR = "."

@st.cache_data
def listar_archivos(directorio):
    if not os.path.exists(directorio):
        return []
    return [f for f in os.listdir(directorio) if f.endswith((".xlsx", ".xls"))]

archivos = listar_archivos(DATA_DIR)

st.sidebar.title("Navegación y Filtros")

if not archivos:
    st.error(f"No se encontraron archivos en la carpeta '{DATA_DIR}/'. Asegúrate de copiarlos allí.")
    st.stop()

# Clasificación de archivos según nombre
categorias = {
    "Lubricantes": [f for f in archivos if "Lubricantes" in f],
    "Repuestos": [f for f in archivos if "Repuestos" in f],
    "Cuadros V, D, O, M": [f for f in archivos if "Cuadro" in f]
}

tipo_vista = st.sidebar.selectbox("Línea de Análisis", list(categorias.keys()))
archivos_tipo = categorias[tipo_vista]

# Identificar sucursal a partir del nombre de archivo
sucursales_disp = []
for f in archivos_tipo:
    for suc in ["Jujuy", "Salta", "Las Lajitas", "Tartagal"]:
        if suc in f and suc not in sucursales_disp:
            sucursales_disp.append(suc)

sucursal_sel = st.sidebar.multiselect(
    "Seleccionar Sucursal(es)", 
    options=sucursales_disp, 
    default=sucursales_disp
)

st.title(f"Tablero de Control - {tipo_vista}")

def cargar_datos(archivos_filtrados):
    frames = []
    for f in archivos_filtrados:
        ruta = os.path.join(DATA_DIR, f)
        # Extraer sucursal del nombre de archivo
        sucursal = "General"
        for s in ["Jujuy", "Salta", "Las Lajitas", "Tartagal"]:
            if s in f:
                sucursal = s
                break
        try:
            excel = pd.ExcelFile(ruta)
            # Lee la primera pestaña por defecto
            df = pd.read_excel(excel, sheet_name=excel.sheet_names[0])
            df["Sucursal"] = sucursal
            df["Archivo_Origen"] = f
            frames.append(df)
        except Exception as e:
            st.warning(f"Error al leer {f}: {e}")
    if frames:
        return pd.concat(frames, ignore_index=True)
    return pd.DataFrame()

# Filtrar archivos por sucursales seleccionadas
archivos_a_cargar = [
    f for f in archivos_tipo 
    if any(suc in f for suc in sucursal_sel)
]

if archivos_a_cargar:
    df_consolidado = cargar_datos(archivos_a_cargar)

    if not df_consolidado.empty:
        # Métricas rápidas
        cols_num = df_consolidado.select_dtypes(include=["number"]).columns.tolist()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Registros", f"{len(df_consolidado):,}")
        col1.caption(f"Archivos procesados: {len(archivos_a_cargar)}")

        if cols_num:
            # Selector de métrica principal para KPI y gráficos
            col_metrica = st.sidebar.selectbox("Columna Métrica a Graficar", cols_num)
            
            total_val = df_consolidado[col_metrica].sum()
            prom_val = df_consolidado[col_metrica].mean()
            col2.metric(f"Total {col_metrica}", f"{total_val:,.2f}")
            col3.metric(f"Promedio {col_metrica}", f"{prom_val:,.2f}")

            # Gráfico de barras por sucursal
            st.subheader(f"Distribución de {col_metrica} por Sucursal")
            resumen_suc = df_consolidado.groupby("Sucursal")[col_metrica].sum().reset_index()
            fig = px.bar(
                resumen_suc, 
                x="Sucursal", 
                y=col_metrica, 
                color="Sucursal",
                text_auto=True,
                title=f"{col_metrica} consolidado por Sucursal"
            )
            st.plotly_chart(fig, use_container_width=True)

        st.subheader("Vista Detallada de Datos")
        st.dataframe(df_consolidado, use_container_width=True)
    else:
        st.info("No se pudieron cargar datos de los archivos seleccionados.")
else:
    st.info("Selecciona al menos una sucursal para visualizar información.")
