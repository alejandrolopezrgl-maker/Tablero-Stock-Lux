import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Autolux - Control de Stock y Posventa", 
    layout="wide",
    page_icon="📦"
)

# Encabezado principal
st.title("📦 Autolux S.A. - Tablero de Control de Stock y Posventa")
st.caption("Cierre Oficial Octubre 2026 (Consolidado SIAC & Control de Gestión Grupo Cenoa)")

# --- NAVEGACIÓN POR PESTAÑAS ---
tabs = st.tabs([
    "📊 Consolidado General",
    "🔄 Comparativo Mes Pasado (Oct vs Sep)",
    "🔴 Lux Salta",
    "🟢 Lux Jujuy",
    "🟡 Lux Las Lajitas",
    "🔵 Lux Tartagal",
    "🎯 Plan Táctico VDOM"
])

# ==========================================
# DATOS MAESTROS OCTUBRE Y SEPTIEMBRE
# ==========================================
# Consolidado Octubre
stock_tot_oct = 2955.33
items_tot_oct = 8324
vivo_oct = 1802.46
dur_obs_oct = 305.26
muerto_oct = 847.61

# Consolidado Septiembre
stock_tot_sep = 2949.69
items_tot_sep = 8304
vivo_sep = 1770.73
dur_obs_sep = 307.21
muerto_sep = 871.75

# Detalle por Sucursales Octubre
df_sucursales = pd.DataFrame([
    {
        "Sucursal": "Lux Salta", 
        "Stock_Total": 1651.41, 
        "Items": 3640, 
        "Vivo": 1036.28, 
        "Durmiente": 125.68, 
        "Obsoleto": 64.72, 
        "Muerto": 424.73,
        "Vta_Repuestos": 613.34,
        "Vta_ManoObra": 256.72,
        "Vta_Lubricantes": 83.77,
        "Margen_Cto": 37.8
    },
    {
        "Sucursal": "Lux Jujuy", 
        "Stock_Total": 948.88, 
        "Items": 3380, 
        "Vivo": 532.41, 
        "Durmiente": 66.98, 
        "Obsoleto": 23.99, 
        "Muerto": 325.51,
        "Vta_Repuestos": 421.34,
        "Vta_ManoObra": 109.02,
        "Vta_Lubricantes": 45.73,
        "Margen_Cto": 38.2
    },
    {
        "Sucursal": "Lux Las Lajitas", 
        "Stock_Total": 236.04, 
        "Items": 683, 
        "Vivo": 161.28, 
        "Durmiente": 5.41, 
        "Obsoleto": 6.28, 
        "Muerto": 63.07,
        "Vta_Repuestos": 62.29,
        "Vta_ManoObra": 40.22,
        "Vta_Lubricantes": 14.72,
        "Margen_Cto": 36.5
    },
    {
        "Sucursal": "Lux Tartagal", 
        "Stock_Total": 119.00, 
        "Items": 621, 
        "Vivo": 72.49, 
        "Durmiente": 7.19, 
        "Obsoleto": 5.02, 
        "Muerto": 34.30,
        "Vta_Repuestos": 96.73,
        "Vta_ManoObra": 25.10,
        "Vta_Lubricantes": 12.30,
        "Margen_Cto": 40.1
    }
])

# Detalle Comparativo Intermensual por Sucursal
df_comp_sucursales = pd.DataFrame([
    {
        "Sucursal": "Lux Salta",
        "Stock_Sep": 1638.20,
        "Stock_Oct": 1651.41,
        "Diff_Stock": +13.21,
        "Vivo_Sep": 998.40,
        "Vivo_Oct": 1036.28,
        "Diff_Vivo": +37.88,
        "Muerto_Sep": 441.30,
        "Muerto_Oct": 424.73,
        "Diff_Muerto": -16.57,
        "Items_Sep": 3620,
        "Items_Oct": 3640,
        "Diff_Items": +20,
        "Diagnostico": "Mejora calidad: +$37,9 M en stock vivo y -$16,6 M en muerto."
    },
    {
        "Sucursal": "Lux Jujuy",
        "Stock_Sep": 955.10,
        "Stock_Oct": 948.88,
        "Diff_Stock": -6.22,
        "Vivo_Sep": 541.20,
        "Vivo_Oct": 532.41,
        "Diff_Vivo": -8.79,
        "Muerto_Sep": 320.50,
        "Muerto_Oct": 325.51,
        "Diff_Muerto": +5.01,
        "Items_Sep": 3375,
        "Items_Oct": 3380,
        "Diff_Items": +5,
        "Diagnostico": "Stock muerto alto (34,3%). Prioridad de transferencia a Salta."
    },
    {
        "Sucursal": "Lux Las Lajitas",
        "Stock_Sep": 234.80,
        "Stock_Oct": 236.04,
        "Diff_Stock": +1.24,
        "Vivo_Sep": 158.10,
        "Vivo_Oct": 161.28,
        "Diff_Vivo": +3.18,
        "Muerto_Sep": 64.60,
        "Muerto_Oct": 63.07,
        "Diff_Muerto": -1.53,
        "Items_Sep": 685,
        "Items_Oct": 683,
        "Diff_Items": -2,
        "Diagnostico": "Sucursal más saludable: 68,3% de stock vivo y solo 5% durmiente."
    },
    {
        "Sucursal": "Lux Tartagal",
        "Stock_Sep": 121.59,
        "Stock_Oct": 119.00,
        "Diff_Stock": -2.59,
        "Vivo_Sep": 73.03,
        "Vivo_Oct": 72.49,
        "Diff_Vivo": -0.54,
        "Muerto_Sep": 45.35,
        "Muerto_Oct": 34.30,
        "Diff_Muerto": -11.05,
        "Items_Sep": 624,
        "Items_Oct": 621,
        "Diff_Items": -3,
        "Diagnostico": "Excelente saneamiento: absorción de -$11,0 M en stock muerto (-24,4%)."
    }
])

# ==========================================
# 1. CONSOLIDADO GENERAL (OCTUBRE 2026)
# ==========================================
with tabs[0]:
    st.subheader("Visión Consolidada de las 4 Sucursales - Octubre 2026")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Stock Total Reposición", f"${stock_tot_oct:,.2f} M", f"↑ {items_tot_oct:,} ítems")
    col2.metric("Stock Vivo (Saludable)", f"${vivo_oct:,.2f} M", f"↑ {(vivo_oct/stock_tot_oct)*100:.1f}%")
    col3.metric("Stock Durmiente / Obsoleto", f"${dur_obs_oct:,.2f} M", f"↓ {(dur_obs_oct/stock_tot_oct)*100:.1f}%")
    col4.metric("Stock Muerto (Inmovilizado)", f"${muerto_oct:,.2f} M", f"↓ {(muerto_oct/stock_tot_oct)*100:.1f}%", delta_color="inverse")

    st.markdown("---")

    cg1, cg2 = st.columns(2)
    with cg1:
        st.write("#### Stock Total por Sucursal ($ Millones)")
        fig_suc = px.bar(
            df_sucursales, x="Sucursal", y="Stock_Total", text="Stock_Total",
            color="Sucursal", color_discrete_sequence=["#e63946", "#2a9d8f", "#e9c46a", "#1d3557"]
        )
        fig_suc.update_traces(
            texttemplate="$%{text:,.2f} M", textposition="inside",
            textfont=dict(size=13, color="white", family="Arial Black")
        )
        fig_suc.update_layout(showlegend=False, yaxis_title="Millones de Pesos")
        st.plotly_chart(fig_suc, use_container_width=True)

    with cg2:
        st.write("#### Composición VDOM por Sucursal ($ Millones)")
        df_vdom_bar = pd.DataFrame([
            {"Sucursal": r["Sucursal"], "Categoría": "Vivo", "Monto": r["Vivo"]} for _, r in df_sucursales.iterrows()
        ] + [
            {"Sucursal": r["Sucursal"], "Categoría": "Durmiente/Obs.", "Monto": r["Durmiente"] + r["Obsoleto"]} for _, r in df_sucursales.iterrows()
        ] + [
            {"Sucursal": r["Sucursal"], "Categoría": "Muerto", "Monto": r["Muerto"]} for _, r in df_sucursales.iterrows()
        ])
        fig_comp = px.bar(
            df_vdom_bar, x="Sucursal", y="Monto", color="Categoría", barmode="stack",
            color_discrete_map={"Vivo": "#2ecc71", "Durmiente/Obs.": "#f1c40f", "Muerto": "#e74c3c"}
        )
        fig_comp.update_layout(yaxis_title="Millones de Pesos")
        st.plotly_chart(fig_comp, use_container_width=True)

    st.write("#### Detalle Consolidado por Sucursal")
    st.dataframe(
        df_sucursales[["Sucursal", "Stock_Total", "Items", "Vivo", "Durmiente", "Obsoleto", "Muerto"]].style.format({
            "Stock_Total": "${:,.2f} M",
            "Items": "{:,}",
            "Vivo": "${:,.2f} M",
            "Durmiente": "${:,.2f} M",
            "Obsoleto": "${:,.2f} M",
            "Muerto": "${:,.2f} M",
        }),
        use_container_width=True
    )

# ==========================================
# 2. COMPARATIVO MES PASADO (OCT VS SEP)
# ==========================================
with tabs[1]:
    st.subheader("🔄 Comparativo de Gestión: Octubre vs. Septiembre 2026")
    st.caption("Evolución intermensual del capital inmovilizado y rotación VDOM a nivel consolidado y por cada sucursal.")

    diff_total = stock_tot_oct - stock_tot_sep
    diff_vivo = vivo_oct - vivo_sep
    diff_dur_obs = dur_obs_oct - dur_obs_sep
    diff_muerto = muerto_oct - muerto_sep

    cm1, cm2, cm3, cm4 = st.columns(4)
    cm1.metric(
        "Stock Total Reposición", 
        f"${stock_tot_oct:,.2f} M", 
        f"{diff_total:+,.2f} M (+{(diff_total/stock_tot_sep)*100:.1f}%)", 
        delta_color="off"
    )
    cm2.metric(
        "Stock Vivo (Saludable)", 
        f"${vivo_oct:,.2f} M", 
        f"{diff_vivo:+,.2f} M (+1,0 p.p.)", 
        delta_color="normal"
    )
    cm3.metric(
        "Stock Durmiente / Obsoleto", 
        f"${dur_obs_oct:,.2f} M", 
        f"{diff_dur_obs:+,.2f} M (-0,1 p.p.)", 
        delta_color="normal"
    )
    cm4.metric(
        "Stock Muerto (Inmovilizado)", 
        f"${muerto_oct:,.2f} M", 
        f"{diff_muerto:+,.2f} M (-0,9 p.p.)", 
        delta_color="normal"
    )

    st.markdown("---")

    # SECCIÓN 1: CONSOLIDADO
    st.write("### 1. Nivel Consolidado General")
    col_cmp1, col_cmp2 = st.columns(2)
    with col_cmp1:
        st.write("#### Variación del Stock por Categoría VDOM ($ Millones)")
        df_comp_vdom = pd.DataFrame([
            {"Categoría": "Stock Vivo", "Septiembre": vivo_sep, "Octubre": vivo_oct},
            {"Categoría": "Durmiente / Obsoleto", "Septiembre": dur_obs_sep, "Octubre": dur_obs_oct},
            {"Categoría": "Stock Muerto", "Septiembre": muerto_sep, "Octubre": muerto_oct}
        ])
        df_comp_melt = df_comp_vdom.melt(id_vars=["Categoría"], value_vars=["Septiembre", "Octubre"], var_name="Mes", value_name="Monto")
        fig_comp_bar = px.bar(
            df_comp_melt, x="Categoría", y="Monto", color="Mes", barmode="group",
            text="Monto", color_discrete_map={"Septiembre": "#95a5a6", "Octubre": "#3498db"}
        )
        fig_comp_bar.update_traces(texttemplate="$%{text:,.1f} M", textposition="inside")
        fig_comp_bar.update_layout(yaxis_title="Millones de Pesos")
        st.plotly_chart(fig_comp_bar, use_container_width=True)

    with col_cmp2:
        st.write("#### Variación Neta de Capital en Octubre ($ Millones)")
        fig_wat = go.Figure(go.Waterfall(
            name="Variación Capital",
            orientation="v",
            measure=["absolute", "relative", "relative", "relative", "total"],
            x=["Septiembre Base", "Stock Vivo", "Durmiente/Obs.", "Stock Muerto", "Octubre Cierre"],
            textposition="outside",
            text=[f"${stock_tot_sep:,.1f} M", f"{diff_vivo:+,.1f} M", f"{diff_dur_obs:+,.1f} M", f"{diff_muerto:+,.1f} M", f"${stock_tot_oct:,.1f} M"],
            y=[stock_tot_sep, diff_vivo, diff_dur_obs, diff_muerto, 0],
            connector={"line": {"color": "#7f8c8d"}},
            decreasing={"marker": {"color": "#2ecc71"}},
            increasing={"marker": {"color": "#3498db"}},
            totals={"marker": {"color": "#2c3e50"}}
        ))
        fig_wat.update_layout(yaxis_range=[2800, 305
