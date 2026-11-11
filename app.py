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
    st.caption("Evolución intermensual del capital inmovilizado y rotación VDOM a nivel consolidado y por sucursal.")

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
        fig_wat.update_layout(yaxis_range=[2800, 3050], yaxis_title="Millones de Pesos")
        st.plotly_chart(fig_wat, use_container_width=True)

    st.write("#### Tabla Comparativa de Indicadores Clave")
    df_comp_tabla = pd.DataFrame([
        {"Indicador": "Stock Total Reposición", "Septiembre": f"${stock_tot_sep:,.2f} M", "Octubre": f"${stock_tot_oct:,.2f} M", "Variación": f"{diff_total:+,.2f} M", "Impacto": "Estable (+0,2%)"},
        {"Indicador": "Stock Vivo (Saludable)", "Septiembre": f"${vivo_sep:,.2f} M (60,0%)", "Octubre": f"${vivo_oct:,.2f} M (61,0%)", "Variación": f"{diff_vivo:+,.2f} M", "Impacto": "Positivo (+1,0 p.p.)"},
        {"Indicador": "Stock Durmiente / Obsoleto", "Septiembre": f"${dur_obs_sep:,.2f} M (10,4%)", "Octubre": f"${dur_obs_oct:,.2f} M (10,3%)", "Variación": f"{diff_dur_obs:+,.2f} M", "Impacto": "Favorable (-$1,95 M)"},
        {"Indicador": "Stock Muerto (Inmovilizado)", "Septiembre": f"${muerto_sep:,.2f} M (29,6%)", "Octubre": f"${muerto_oct:,.2f} M (28,7%)", "Variación": f"{diff_muerto:+,.2f} M", "Impacto": "Muy Favorable (-$24,14 M)"},
        {"Indicador": "Total de Códigos / Ítems", "Septiembre": f"{items_tot_sep:,}", "Octubre": f"{items_tot_oct:,}", "Variación": "+20 ítems", "Impacto": "Ampliación de stock vivo"}
    ])
    st.dataframe(df_comp_tabla, use_container_width=True)

# ==========================================
# 3. LUX SALTA
# ==========================================
with tabs[2]:
    st.subheader("🔴 Lux Salta - Análisis Operativo Octubre 2026")
    cs1, cs2, cs3, cs4 = st.columns(4)
    cs1.metric("Stock Reposición", "$1.651,41 M", "3.640 ítems")
    cs2.metric("Stock Vivo", "$1.036,28 M", "62,8% del total")
    cs3.metric("Stock Muerto", "$424,73 M", "25,7% del total")
    cs4.metric("Venta Neta Total", "$613,34 M", "Margen s/Cto: 37,8%")

    st.markdown("---")
    st.write("#### Facturación y Rendimiento Comercial de Posventa")
    df_salta_vtas = pd.DataFrame([
        {"Línea": "Repuestos Mostrador / Flotilleros", "Venta_Neta": 281.66, "Costo": 210.54, "Utilidad": 71.11, "Margen_Cto": "33,8%"},
        {"Línea": "Repuestos Taller", "Venta_Neta": 331.69, "Costo": 234.41, "Utilidad": 97.28, "Margen_Cto": "41,5%"},
        {"Línea": "Mano de Obra Taller", "Venta_Neta": 256.72, "Costo": 58.03, "Utilidad": 198.69, "Margen_Cto": "342,4%"},
        {"Línea": "Lubricantes Taller", "Venta_Neta": 83.77, "Costo": 53.26, "Utilidad": 30.50, "Margen_Cto": "57,3%"}
    ])
    st.dataframe(df_salta_vtas.style.format({"Venta_Neta": "${:,.2f} M", "Costo": "${:,.2f} M", "Utilidad": "${:,.2f} M"}), use_container_width=True)

# ==========================================
# 4. LUX JUJUY
# ==========================================
with tabs[3]:
    st.subheader("🟢 Lux Jujuy - Análisis Operativo Octubre 2026")
    cj1, cj2, cj3, cj4 = st.columns(4)
    cj1.metric("Stock Reposición", "$948,88 M", "3.380 ítems")
    cj2.metric("Stock Vivo", "$532,41 M", "56,1% del total")
    cj3.metric("Stock Muerto", "$325,51 M", "34,3% del total")
    cj4.metric("Venta Neta Total", "$421,34 M", "Margen s/Cto: 38,2%")

    st.markdown("---")
    st.write("#### Facturación y Rendimiento Comercial de Posventa")
    df_jujuy_vtas = pd.DataFrame([
        {"Línea": "Repuestos Mostrador / Flotilleros", "Venta_Neta": 145.19, "Costo": 108.81, "Utilidad": 36.38, "Margen_Cto": "33,4%"},
        {"Línea": "Repuestos Taller", "Venta_Neta": 276.15, "Costo": 196.03, "Utilidad": 80.12, "Margen_Cto": "40,9%"},
        {"Línea": "Mano de Obra Taller", "Venta_Neta": 109.02, "Costo": 24.93, "Utilidad": 84.08, "Margen_Cto": "337,2%"},
        {"Línea": "Lubricantes Taller", "Venta_Neta": 45.73, "Costo": 29.35, "Utilidad": 16.37, "Margen_Cto": "55,8%"}
    ])
    st.dataframe(df_jujuy_vtas.style.format({"Venta_Neta": "${:,.2f} M", "Costo": "${:,.2f} M", "Utilidad": "${:,.2f} M"}), use_container_width=True)

# ==========================================
# 5. LUX LAS LAJITAS
# ==========================================
with tabs[4]:
    st.subheader("🟡 Lux Las Lajitas - Análisis Operativo Octubre 2026")
    cl1, cl2, cl3, cl4 = st.columns(4)
    cl1.metric("Stock Reposición", "$236,04 M", "683 ítems")
    cl2.metric("Stock Vivo", "$161,28 M", "68,3% del total")
    cl3.metric("Stock Muerto", "$63,07 M", "26,7% del total")
    cl4.metric("Venta Neta Total", "$62,29 M", "Margen s/Cto: 36,5%")

    st.markdown("---")
    st.write("#### Facturación y Rendimiento Comercial de Posventa")
    df_lajitas_vtas = pd.DataFrame([
        {"Línea": "Repuestos Mostrador", "Venta_Neta": 15.98, "Costo": 11.60, "Utilidad": 4.38, "Margen_Cto": "37,8%"},
        {"Línea": "Repuestos Taller", "Venta_Neta": 46.31, "Costo": 34.04, "Utilidad": 12.27, "Margen_Cto": "36,0%"},
        {"Línea": "Mano de Obra Taller", "Venta_Neta": 40.22, "Costo": 9.16, "Utilidad": 31.06, "Margen_Cto": "339,0%"},
        {"Línea": "Lubricantes Taller", "Venta_Neta": 14.72, "Costo": 9.36, "Utilidad": 5.36, "Margen_Cto": "57,3%"}
    ])
    st.dataframe(df_lajitas_vtas.style.format({"Venta_Neta": "${:,.2f} M", "Costo": "${:,.2f} M", "Utilidad": "${:,.2f} M"}), use_container_width=True)

# ==========================================
# 6. LUX TARTAGAL
# ==========================================
with tabs[5]:
    st.subheader("🔵 Lux Tartagal - Análisis Operativo Octubre 2026")
    ct1, ct2, ct3, ct4 = st.columns(4)
    ct1.metric("Stock Reposición", "$119,00 M", "621 ítems")
    ct2.metric("Stock Vivo", "$72,49 M", "60,9% del total")
    ct3.metric("Stock Muerto", "$34,30 M", "28,8% del total")
    ct4.metric("Venta Neta Repuestos", "$96,73 M", "Margen s/Cto: 40,1%")

    st.markdown("---")
    st.write("#### Rendimiento de Repuestos en Tartagal")
    df_tart_vtas = pd.DataFrame([
        {"Canal": "Ventas Directas Clientes (Minorista / Cta Cte)", "Venta_Neta": 31.58, "Costo": 22.19, "Utilidad": 9.40, "Margen_Cto": "42,4%"},
        {"Canal": "Flotilleros Toyota (Cta Cte)", "Venta_Neta": 5.89, "Costo": 4.89, "Utilidad": 1.00, "Margen_Cto": "20,5%"},
        {"Canal": "Facturación Taller / Vales", "Venta_Neta": 59.21, "Costo": 41.95, "Utilidad": 17.25, "Margen_Cto": "41,1%"},
        {"Canal": "Total General Tartagal", "Venta_Neta": 96.73, "Costo": 69.07, "Utilidad": 27.66, "Margen_Cto": "40,1%"}
    ])
    st.dataframe(df_tart_vtas.style.format({"Venta_Neta": "${:,.2f} M", "Costo": "${:,.2f} M", "Utilidad": "${:,.2f} M"}), use_container_width=True)

# ==========================================
# 7. PLAN TÁCTICO VDOM
# ==========================================
with tabs[6]:
    st.subheader("🎯 Plan Táctico de Saneamiento y Absorción de Stock (VDOM)")
    st.markdown("""
    ### Diagnóstico y Estrategia de Mitigación
    1. **Plan de Rotación de Stock Muerto ($847,61 M inmovilizados):**
       * En octubre se logró una absorción neta de **-$24,14 M** de stock muerto.
       * Priorizar la transferencia intersucursales de códigos muertos en Jujuy ($325,51 M) que posean demanda activa en Salta.
    2. **Descuentos Escalonados en Mostrador para Stock Durmiente y Obsoleto ($305,26 M):**
       * Aplicar paquetes de mantenimiento preventivo para unidades de más de 5 años con descuentos de hasta el 25% en repuestos obsoletos seleccionados.
    3. **Cumplimiento y Cobertura:**
       * Mantener la reposición diaria estrictamente acotada a la canasta de **Stock Vivo ($1.802,46 M)** para evitar la migración de ítems hacia categorías durmientes.
    """)
