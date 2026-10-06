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
            text="Total_Stock"
        )
        fig_bar.update_traces(
            width=0.45,
            texttemplate="$%{text:.1f} M",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(size=14, color="white", family="Arial Black")
        )
        fig_bar.update_layout(bargap=0.4, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_g2:
        st.write("#### Composición VDOM por Sucursal ($ Millones)")
        df_melt = df_vdom.melt(
            id_vars=["Sucursal"], 
            value_vars=["Vivo", "Durmiente", "Obsoleto", "Muerto"], 
            var_name="Clasificación", 
            value_name="Monto_M"
        )
        fig_stack = px.bar(
            df_melt,
            x="Sucursal",
            y="Monto_M",
            color="Clasificación",
            barmode="stack",
            text="Monto_M",
            color_discrete_map={"Vivo": "#2ecc71", "Durmiente": "#f39c12", "Obsoleto": "#e67e22", "Muerto": "#e74c3c"}
        )
        fig_stack.update_traces(
            width=0.45,
            texttemplate="$%{text:.0f}M",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(size=11, color="white")
        )
        fig_stack.update_layout(bargap=0.4)
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
    c_s1, c_s2, c_s3, c_s4 = st.columns(4)
    c_s1.metric("Stock Total", "$1.608,76 M", "3.608 ítems")
    c_s2.metric("Stock Vivo", "$1.000,41 M", "62,2%")
    c_s3.metric("Stock Muerto", "$414,81 M", "25,8%", delta_color="inverse")
    c_s4.metric("Venta Repuestos Neto", "$564,87 M", "Margen: 26,5%")

    cs1, cs2 = st.columns(2)
    with cs1:
        st.write("##### Estado del Inventario Salta")
        df_pie_salta = pd.DataFrame({
            "Estado": ["Vivo", "Durmiente", "Obsoleto", "Muerto"],
            "Monto": [1000.41, 139.52, 54.01, 414.81]
        })
        fig_pie = px.pie(
            df_pie_salta, names="Estado", values="Monto", color="Estado",
            color_discrete_map={"Vivo": "#2ecc71", "Durmiente": "#f39c12", "Obsoleto": "#e67e22", "Muerto": "#e74c3c"}
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    with cs2:
        st.write("##### Diagnóstico Operativo")
        st.info("""
        * **Concentración de Stock Muerto:** Salta representa el **50,6% del stock muerto total** de la compañía ($414,81 M sobre 1.807 ítems).
        * **Tracción de Taller:** El taller absorbe $328,59 M en repuestos con un margen del 30,6%.
        * **Prioridad:** Revisar los 30 repuestos de mayor valor en Stock Muerto para evaluar recompra o absorción interna en servicios.
        """)

# ==========================================
# 3. LUX JUJUY
# ==========================================
with tabs[2]:
    st.subheader("🟢 Lux Jujuy")
    c_j1, c_j2, c_j3, c_j4 = st.columns(4)
    c_j1.metric("Stock Total", "$937,29 M", "3.369 ítems")
    c_j2.metric("Stock Vivo", "$542,62 M", "57,9%")
    c_j3.metric("Stock Muerto", "$319,89 M", "34,1%", delta_color="inverse")
    c_j4.metric("Venta Repuestos Neto", "$396,99 M", "Margen: 28,0%")

    cj1, cj2 = st.columns(2)
    with cj1:
        st.write("##### Estado del Inventario Jujuy")
        df_pie_jujuy = pd.DataFrame({
            "Estado": ["Vivo", "Durmiente", "Obsoleto", "Muerto"],
            "Monto": [542.62, 43.58, 31.20, 319.89]
        })
        fig_pie_j = px.pie(
            df_pie_jujuy, names="Estado", values="Monto", color="Estado",
            color_discrete_map={"Vivo": "#2ecc71", "Durmiente": "#f39c12", "Obsoleto": "#e67e22", "Muerto": "#e74c3c"}
        )
        fig_pie_j.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie_j, use_container_width=True)
    with cj2:
        st.write("##### Diagnóstico Operativo")
        st.warning("""
        * **Mayor índice de inmovilización:** El **34,1%** del inventario está en Stock Muerto (1.676 ítems sin movimiento en > 12 meses).
        * **Excelente Margen:** Registra el margen más alto en mostrador (32,5%) y un global de 28,0%.
        * **Acción Inmediata:** Cruce de ítems sin movimiento con la demanda activa de Salta para transferencias inter-sucursal antes de solicitar pedidos a TASA.
        """)

# ==========================================
# 4. LUX LAS LAJITAS
# ==========================================
with tabs[3]:
    st.subheader("🟡 Lux Las Lajitas")
    c_l1, c_l2, c_l3, c_l4 = st.columns(4)
    c_l1.metric("Stock Total", "$238,66 M", "682 ítems")
    c_l2.metric("Stock Vivo", "$165,00 M", "69,1% (Óptimo)")
    c_l3.metric("Stock Muerto", "$55,35 M", "23,2%", delta_color="inverse")
    c_l4.metric("Venta Repuestos Neto", "$92,41 M", "Margen: 26,6%")

    cl1, cl2 = st.columns(2)
    with cl1:
        st.write("##### Estado del Inventario Las Lajitas")
        df_pie_laj = pd.DataFrame({
            "Estado": ["Vivo", "Durmiente", "Obsoleto", "Muerto"],
            "Monto": [165.00, 8.13, 10.17, 55.35]
        })
        fig_pie_l = px.pie(
            df_pie_laj, names="Estado", values="Monto", color="Estado",
            color_discrete_map={"Vivo": "#2ecc71", "Durmiente": "#f39c12", "Obsoleto": "#e67e22", "Muerto": "#e74c3c"}
        )
        fig_pie_l.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie_l, use_container_width=True)
    with cl2:
        st.write("##### Diagnóstico Operativo")
        st.success("""
        * **Sucursal más ágil:** Posee el índice más alto de Stock Vivo (**69,1%**), reflejando un inventario adaptado a la demanda agropecuaria.
        * **Orientación al Taller:** El 85% de las piezas despachadas salen por órdenes de reparación.
        * **Oportunidad:** Los $55,35 M de Stock Muerto corresponden en su mayoría a piezas pesadas específicas que pueden reubicarse en Salta.
        """)

# ==========================================
# 5. LUX TARTAGAL
# ==========================================
with tabs[4]:
    st.subheader("🔵 Lux Tartagal")
    c_t1, c_t2, c_t3, c_t4 = st.columns(4)
    c_t1.metric("Stock Estimado", "$145,00 M", "520 ítems")
    c_t2.metric("Stock Vivo", "$98,40 M", "67,9%")
    c_t3.metric("Facturación Taller", "$128,29 M", "Set-2026")
    c_t4.metric("Mano de Obra", "$44,68 M", "275,36 hs facturadas")

    ct1, ct2 = st.columns(2)
    with ct1:
        st.write("##### Composición de Ventas de Taller Tartagal")
        df_tart_vta = pd.DataFrame({
            "Rubro": ["Repuestos en Taller", "Mano de Obra", "Lubricantes", "Otros / Terceros"],
            "Monto": [64.68, 44.68, 18.40, 0.53]
        })
        fig_pie_t = px.pie(
            df_tart_vta, names="Rubro", values="Monto",
            color_discrete_sequence=["#1d3557", "#457b9d", "#a8dadc", "#f1faee"]
        )
        fig_pie_t.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie_t, use_container_width=True)
    with ct2:
        st.write("##### Diagnóstico Operativo")
        st.info("""
        * **Alta intensidad de taller:** Gran volumen de horas de mecánica facturadas (275,36 hs).
        * **Venta de repuestos por servicio:** El taller colocó $64,68 M en repuestos y $18,40 M en lubricantes.
        * **Recomendación:** Incorporar el cuadro de inventario VDOM mensual de Tartagal para monitorear el stock de seguridad local.
        """)

# ==========================================
# 6. PLAN TÁCTICO VDOM
# ==========================================
with tabs[5]:
    st.subheader("🎯 Plan Integral de Recuperación y Descongelamiento de Capital")
    
    st.markdown("""
    ### 1. Diagnóstico del Capital Inmovilizado ($818,15 Millones)
    El inventario de Autolux presenta **$818,15 M en Stock Muerto** a costo de reposición (más de 3.800 ítems sin ventas en 12 meses):
    * **Salta y Jujuy concentran el 90%** de esta inmovilización.
    * Mantener este inventario representa un costo de oportunidad financiero de **~$35 M mensuales**.

    ---

    ### 2. Protocolo de Acción Inmediata (4 Pasos)

    #### **Paso 1: Filtro de Devolución a Toyota Argentina (TASA)**
    * Identificar ítems en Stock Muerto y Obsoleto adquiridos dentro de la ventana de devolución autorizada por TASA.
    * **Objetivo:** Recuperar notas de crédito directas con fábrica para cancelar deuda de compras corrientes.

    #### **Paso 2: Matriz Cruzada de Traspasos Inter-Sucursales**
    * Antes de confirmar el pedido mensual de reposición a fábrica:
      1. El sistema cruza las piezas solicitadas contra los ítems clasificados como *Muerto* en las otras 3 sucursales.
      2. Si Salta necesita un código que está inmovilizado en Jujuy, Tartagal o Las Lajitas, se emite una **transferencia interna**, descongelando capital sin erogación de fondos.

    #### **Paso 3: Campaña Comercial para Flotilleros y Empresas**
    * Armar paquetes con descuentos escalonados (20% al 40%) para clientes corporativos de minería y agro, aplicando a repuestos durmientes de alta rotación histórica (filtros, rodamientos, correas, tensores).

    #### **Paso 4: Saneamiento y Provisión Contable**
    * Para los ítems que superen 24 meses sin rotación y correspondan a modelos discontinuados (Hilux anteriores a 2015, Corolla líneas previas), definir plan de descarte o remate a mayoristas para liberar espacio en estanterías de Casa Central.
    """)
