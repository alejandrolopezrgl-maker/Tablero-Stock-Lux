import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Autolux - Control de Stock y Posventa", 
    layout="wide",
    page_icon="📦"
)

st.title("📦 Autolux S.A. - Tablero de Control de Stock y Posventa")
st.caption("Cierre Oficial Septiembre 2026 (Datos consolidados SIAC al 30/09/2026)")

# --- PALETA DE COLORES POR SUCURSAL ---
COLORES_SUC = {
    "Lux Salta": "#e63946",        # Rojo
    "Lux Jujuy": "#2a9d8f",        # Verde
    "Lux Las Lajitas": "#e9c46a",  # Amarillo
    "Lux Tartagal": "#1d3557"      # Azul
}

# --- DATOS OFICIALES VDOM (Costo Reposición en $ Millones) ---
df_vdom = pd.DataFrame([
    {"Sucursal": "Lux Salta", "Vivo": 1000.41, "Durmiente": 139.52, "Obsoleto": 54.01, "Muerto": 414.81, "Items": 3608},
    {"Sucursal": "Lux Jujuy", "Vivo": 542.62, "Durmiente": 43.58, "Obsoleto": 31.20, "Muerto": 319.89, "Items": 3369},
    {"Sucursal": "Lux Las Lajitas", "Vivo": 165.00, "Durmiente": 8.13, "Obsoleto": 10.17, "Muerto": 55.35, "Items": 682},
    {"Sucursal": "Lux Tartagal", "Vivo": 98.40, "Durmiente": 11.20, "Obsoleto": 7.30, "Muerto": 28.10, "Items": 520},
])
df_vdom["Total_Stock"] = df_vdom["Vivo"] + df_vdom["Durmiente"] + df_vdom["Obsoleto"] + df_vdom["Muerto"]
df_vdom["Pct_Vivo"] = (df_vdom["Vivo"] / df_vdom["Total_Stock"]) * 100
df_vdom["Pct_Muerto"] = (df_vdom["Muerto"] / df_vdom["Total_Stock"]) * 100

# --- VENTAS Y TALLER SEPTIEMBRE 2026 ---
df_ventas = pd.DataFrame([
    {"Sucursal": "Lux Salta", "Mostrador": 236.28, "Taller_Repuestos": 328.59, "Mano_Obra": 145.20, "Lubricantes": 88.74, "Margen_Rep": 26.5},
    {"Sucursal": "Lux Jujuy", "Mostrador": 176.21, "Taller_Repuestos": 220.78, "Mano_Obra": 98.19, "Lubricantes": 50.94, "Margen_Rep": 28.0},
    {"Sucursal": "Lux Las Lajitas", "Mostrador": 13.80, "Taller_Repuestos": 78.60, "Mano_Obra": 22.10, "Lubricantes": 12.50, "Margen_Rep": 26.6},
    {"Sucursal": "Lux Tartagal", "Mostrador": 15.20, "Taller_Repuestos": 64.68, "Mano_Obra": 44.68, "Lubricantes": 18.40, "Margen_Rep": 27.2},
])

# NAVEGACIÓN
tabs = st.tabs([
    "📊 Consolidado General", 
    "🔴 Lux Salta", 
    "🟢 Lux Jujuy", 
    "🟡 Lux Las Lajitas", 
    "🔵 Lux Tartagal",
    "🎯 Plan Táctico VDOM"
])

# ==========================================
# 1. CONSOLIDADO GENERAL
# ==========================================
with tabs[0]:
    st.subheader("Visión Consolidada de las 4 Sucursales")
    
    tot_stock = df_vdom["Total_Stock"].sum()
    tot_vivo = df_vdom["Vivo"].sum()
    tot_durm = df_vdom["Durmiente"].sum() + df_vdom["Obsoleto"].sum()
    tot_muerto = df_vdom["Muerto"].sum()
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Stock Total Reposición", f"${tot_stock:,.2f} M", f"{df_vdom['Items'].sum():,} ítems")
    c2.metric("Stock Vivo (Saludable)", f"${tot_vivo:,.2f} M", f"{(tot_vivo/tot_stock)*100:.1f}%")
    c3.metric("Stock Durmiente / Obsoleto", f"${tot_durm:,.2f} M", f"{(tot_durm/tot_stock)*100:.1f}%")
    c4.metric("Stock Muerto (Inmovilizado)", f"${tot_muerto:,.2f} M", f"{(tot_muerto/tot_stock)*100:.1f}%", delta_color="inverse")
    
    st.markdown("---")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.write("#### Stock Total por Sucursal ($ Millones)")
        fig_bar = px.bar(
            df_vdom, 
            x="Sucursal", 
            y="Total_Stock", 
            color="Sucursal",
            color_discrete_map=COLORES_SUC,
            text_auto=".1f"
        )
        fig_bar.update_traces(width=0.45)
        fig_bar.update_layout(bargap=0.4, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_g2:
        st.write("#### Proporción de Stock Vivo vs. Muerto (%)")
        fig_stack = go.Figure()
        fig_stack.add_trace(go.Bar(name='Stock Vivo %', x=df_vdom['Sucursal'], y=df_vdom['Pct_Vivo'], marker_color='#2ecc71', width=0.45))
        fig_stack.add_trace(go.Bar(name='Stock Muerto %', x=df_vdom['Sucursal'], y=df_vdom['Pct_Muerto'], marker_color='#e74c3c', width=0.45))
        fig_stack.update_layout(barmode='stack', bargap=0.4)
        st.plotly_chart(fig_stack, use_container_width=True)

    st.write("#### Resumen Comparativo de Inventario y Ventas")
    df_comparativo = df_vdom.merge(df_ventas, on="Sucursal")
    st.dataframe(
        df_comparativo[[
            "Sucursal", "Total_Stock", "Vivo", "Durmiente", "Obsoleto", "Muerto", 
            "Items", "Mostrador", "Taller_Repuestos", "Margen_Rep"
        ]], 
        use_container_width=True
    )

# ==========================================
# 2. LUX SALTA
# ==========================================
with tabs[1]:
    st.subheader("🔴 Lux Salta - Casa Central")
    col1, col2, col3, col4 = st.columns(
