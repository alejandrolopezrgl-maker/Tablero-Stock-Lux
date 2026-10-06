import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Autolux - Control de Stock y Ventas", layout="wide")

st.title("Autolux S.A. - Tablero de Control de Inventario y Posventa")
st.caption("Datos correspondientes al cierre contable de Septiembre 2026")

tabs = st.tabs(["Consolidado General", "Lux Salta", "Lux Jujuy", "Lux Las Lajitas", "Lux Tartagal", "Plan VDOM"])

# Datos consolidados del cuadro VDOM (en Millones de ARS - Reposición)
data_vdom = {
    "Sucursal": ["Salta", "Jujuy", "Las Lajitas"],
    "Vivo": [1000.41, 542.62, 165.00],
    "Durmiente": [139.52, 43.58, 8.13],
    "Obsoleto": [54.01, 31.20, 10.17],
    "Muerto": [414.81, 319.89, 55.35],
    "Total_Items": [3608, 3369, 682]
}
df_vdom = pd.DataFrame(data_vdom)
df_vdom["Total_Stock"] = df_vdom["Vivo"] + df_vdom["Durmiente"] + df_vdom["Obsoleto"] + df_vdom["Muerto"]

with tabs[0]:
    st.subheader("Estado General del Stock")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Stock Total", f"${df_vdom['Total_Stock'].sum():,.2f} M")
    c2.metric("Stock Vivo", f"${df_vdom['Vivo'].sum():,.2f} M", f"{(df_vdom['Vivo'].sum()/df_vdom['Total_Stock'].sum())*100:.1f}%")
    c3.metric("Stock Durmiente/Obs.", f"${(df_vdom['Durmiente'].sum() + df_vdom['Obsoleto'].sum()):,.2f} M")
    c4.metric("Stock Muerto", f"${df_vdom['Muerto'].sum():,.2f} M", f"{(df_vdom['Muerto'].sum()/df_vdom['Total_Stock'].sum())*100:.1f}%", delta_color="inverse")

    df_melt = df_vdom.melt(id_vars=["Sucursal"], value_vars=["Vivo", "Durmiente", "Obsoleto", "Muerto"], var_name="Estado", value_name="Monto_M")
    fig = px.bar(df_melt, x="Sucursal", y="Monto_M", color="Estado", title="Composición del Stock por Sucursal (Millones $)", barmode="stack")
    st.plotly_chart(fig, use_container_width=True)

with tabs[5]:
    st.subheader("Plan de Acción sobre Stock Inmovilizado")
    st.markdown("""
    - **Monitoreo de $790M en Stock Muerto:** Establecer campañas de liquidación para el 50% de ítems con más de 12 meses sin movimiento.
    - **Reasignación Inter-sucursal:** Identificar piezas con clasificación 'Muerto' en Las Lajitas o Jujuy que registren demanda periódica en Salta antes de emitir compras a fábrica.
    """)
