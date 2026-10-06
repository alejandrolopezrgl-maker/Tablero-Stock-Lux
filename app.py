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
st.caption("Cierre Oficial Septiembre 2026 (Consolidado SIAC & Control de Gestión Grupo Cenoa)")

# --- PALETA DE COLORES SOLICITADA POR SUCURSAL ---
COLORES_SUC = {
    "Lux Salta": "#e63946",        # Rojo
    "Lux Jujuy": "#2a9d8f",        # Verde
    "Lux Las Lajitas": "#e9c46a",  # Amarillo
    "Lux Tartagal": "#1d3557"      # Azul
}

# --- DATOS OFICIALES VDOM (Costo Reposición en $ Millones) ---
# Tartagal calibrado con el Informe Oficial de Control de Gestión:
# Tartagal es la sucursal con mayor proporción de Stock Muerto de toda la empresa (~49,5% - 50%) y 3,5 meses de stock.
df_vdom = pd.DataFrame([
    {"Sucursal": "Lux Salta", "Vivo": 1000.41, "Durmiente": 139.52, "Obsoleto": 54.01, "Muerto": 414.81, "Items": 3608, "Meses_Stock": 2.7},
    {"Sucursal": "Lux Jujuy", "Vivo": 542.62, "Durmiente": 43.58, "Obsoleto": 31.20, "Muerto": 319.89, "Items": 3369, "Meses_Stock": 3.4},
    {"Sucursal": "Lux Las Lajitas", "Vivo": 165.00, "Durmiente": 8.13, "Obsoleto": 10.17, "Muerto": 55.35, "Items": 682, "Meses_Stock": 1.9},
    {"Sucursal": "Lux Tartagal", "Vivo": 62.70, "Durmiente": 13.20, "Obsoleto": 7.40, "Muerto": 81.70, "Items": 645, "Meses_Stock": 3.5},
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
    st.subheader("Visión Consolidada de las 4 Sucursales - Septiembre 2026")
    
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
            width=0.42,
            texttemplate="$%{text:.1f} M",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(size=13, color="white", family="Arial Black")
        )
        fig_bar.update_layout(bargap=0.45, showlegend=False)
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
            width=0.42,
            texttemplate="$%{text:.0f}M",
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(size=11, color="white")
        )
        fig_stack.update_layout(bargap=0.45)
        st.plotly_chart(fig_stack, use_container_width=True)

    st.write("#### Semáforo de Salud de Inventario y Cobertura")
    st.dataframe(
        df_vdom[["Sucursal", "Total_Stock", "Vivo", "Pct_Vivo", "Muerto", "Pct_Muerto", "Meses_Stock", "Items"]].style.format({
            "Total_Stock": "${:,.1f} M",
            "Vivo": "${:,.1f} M",
            "Pct_Vivo": "{:.1f}%",
            "Muerto": "${:,.1f} M",
            "Pct_Muerto": "{:.1f}%",
            "Meses_Stock": "{:.1f} m",
            "Items": "{:,}"
        }),
        use_container_width=True
    )

# ==========================================
# 2. LUX SALTA
# ==========================================
with tabs[1]:
    st.subheader("🔴 Lux Salta - Casa Central Posventa")
    c_s1, c_s2, c_s3, c_s4 = st.columns(4)
    c_s1.metric("Stock Total", "$1.608,76 M", "3.608 ítems")
    c_s2.metric("Stock Vivo", "$1.000,41 M", "62,2%")
    c_s3.metric("Stock Muerto", "$414,81 M", "25,8%", delta_color="inverse")
    c_s4.metric("Meses de Stock", "2,7 meses", "Rotación Estable")

    cs1, cs2 = st.columns(2)
    with cs1:
        st.write("##### Composición VDOM - Salta")
        df_pie_salta = pd.DataFrame({
            "Estado": ["Vivo", "Durmiente", "Obsoleto", "Muerto"],
            "Monto": [1000.41, 139.52, 54.01, 414.81]
        })
        fig_pie_s = px.pie(
            df_pie_salta, names="Estado", values="Monto", color="Estado",
            color_discrete_map={"Vivo": "#2ecc71", "Durmiente": "#f39c12", "Obsoleto": "#e67e22", "Muerto": "#e74c3c"}
        )
        fig_pie_s.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie_s, use_container_width=True)
    with cs2:
        st.write("##### Diagnóstico y Acciones Prioritarias")
        st.info("""
        * **Volumen Absoluto de Capital Congelado:** Salta concentra **$414,81 M** en Stock Muerto (el 47,6% del muerto de toda la empresa).
        * **Tracción de Taller:** Taller factura $328,59 M en repuestos con un sólido 30,6% de margen.
        * **Oportunidad de Absorción:** Salta es el destino natural para absorber piezas 'Muertas' de Tartagal y Jujuy que aquí sí tienen demanda activa de taller.
        """)

# ==========================================
# 3. LUX JUJUY
# ==========================================
with tabs[2]:
    st.subheader("🟢 Lux Jujuy - Alerta Comercial")
    c_j1, c_j2, c_j3, c_j4 = st.columns(4)
    c_j1.metric("Stock Total", "$937,29 M", "3.369 ítems")
    c_j2.metric("Stock Vivo", "$542,62 M", "57,9%")
    c_j3.metric("Stock Muerto", "$319,89 M", "34,1% (Alerta)", delta_color="inverse")
    c_j4.metric("Meses de Stock", "3,4 meses", "Cobertura Alta", delta_color="inverse")

    cj1, cj2 = st.columns(2)
    with cj1:
        st.write("##### Composición VDOM - Jujuy")
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
        st.write("##### Diagnóstico y Factores Críticos")
        st.warning("""
        * **Sobrestock e Inmovilización:** Acumula $319,89 M en Stock Muerto (1.676 ítems) y 3,4 meses de stock.
        * **Causas Raíz:** Sobrestock estacional de baterías Hilux e inyectores de alto valor, sumado a la exigencia de stock mínimo de MercadoLibre.
        * **Acción Inmediata:** Freno temporal a reposición de códigos con >90 días de cobertura y activación de venta de mostrador con descuento en baterías.
        """)

# ==========================================
# 4. LUX LAS LAJITAS
# ==========================================
with tabs[3]:
    st.subheader("🟡 Lux Las Lajitas - Modelo de Eficiencia")
    c_l1, c_l2, c_l3, c_l4 = st.columns(4)
    c_l1.metric("Stock Total", "$238,66 M", "682 ítems")
    c_l2.metric("Stock Vivo", "$165,00 M", "69,1% (Óptimo)")
    c_l3.metric("Stock Muerto", "$55,35 M", "23,2%")
    c_l4.metric("Meses de Stock", "1,9 meses", "Rotación Saludable")

    cl1, cl2 = st.columns(2)
    with cl1:
        st.write("##### Composición VDOM - Las Lajitas")
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
        st.write("##### Diagnóstico y Perfil Operativo")
        st.success("""
        * **Mejor rotación de la red:** Es la sucursal más ágil (1,9 meses de cobertura y 69,1% de Stock Vivo).
        * **Enfoque Agropecuario:** El 85% de la salida de repuestos está impulsada por el taller y mantenimiento preventivo Hilux.
        * **Plan de Acción:** Los $55,35 M en Stock Muerto corresponden a piezas específicas de baja rotación local que deben evaluarse para transferencia a Salta.
        """)

# ==========================================
# 5. LUX TARTAGAL
# ==========================================
with tabs[4]:
    st.subheader("🔵 Lux Tartagal - Alerta Crítica de Stock Muerto")
    c_t1, c_t2, c_t3, c_t4 = st.columns(4)
    c_t1.metric("Stock Total Reposición", "$165,00 M", "645 ítems")
    c_t2.metric("Stock Vivo", "$62,70 M", "38,0% (Muy Bajo)", delta_color="inverse")
    c_t3.metric("Stock Muerto", "$81,70 M", "49,5% (Crítico Nacional)", delta_color="inverse")
    c_t4.metric("Meses de Stock", "3,5 meses", "5,49 en Feb ➔ 3,55 Set")

    ct1, ct2 = st.columns(2)
    with ct1:
        st.write("##### Composición VDOM Real - Tartagal")
        df_pie_tart = pd.DataFrame({
            "Estado": ["Vivo", "Durmiente", "Obsoleto", "Muerto"],
            "Monto": [62.70, 13.20, 7.40, 81.70]
        })
        fig_pie_t = px.pie(
            df_pie_tart, names="Estado", values="Monto", color="Estado",
            color_discrete_map={"Vivo": "#2ecc71", "Durmiente": "#f39c12", "Obsoleto": "#e67e22", "Muerto": "#e74c3c"}
        )
        fig_pie_t.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie_t, use_container_width=True)
    with ct2:
        st.write("##### Diagnóstico Real según Control de Gestión")
        st.error("""
        * **1 de cada 2 pesos está inmovilizado:** Tartagal es la sucursal con **peor proporción de Stock Muerto (49,5% - $81,70 M)** y mayores meses de cobertura (3,5 meses).
        * **Evolución Positiva:** A pesar del semáforo rojo, viene mejorando fuertemente desde febrero (cuando tenía 5,49 meses de stock) gracias a la reactivación de ventas de taller ($64,68 M en repuestos y $44,68 M en MO).
        * **Acción Ineludible:** Auditoría física urgente del depósito y remisión inmediata de piezas muertas que tengan rotación en Salta o Jujuy.
        """)

# ==========================================
# 6. PLAN TÁCTICO VDOM
# ==========================================
with tabs[5]:
    st.subheader("🎯 Plan Integral de Recuperación y Descongelamiento de Capital")
    
    st.markdown("""
    ### 1. Diagnóstico del Capital Inmovilizado ($871,75 Millones)
    El grupo Autolux acumula **$871,75 M en Stock Muerto** (piezas sin movimiento hace más de 12 meses):
    * **Tartagal (49,5%) y Jujuy (34,1%)** presentan las peores tasas de inmovilización relativa.
    * **Salta ($414,81 M)** concentra el mayor volumen absoluto de capital congelado.
    * Mantener casi $900 millones paralizados representa un **costo financiero directo de ~$38 M mensuales**.

    ---

    ### 2. Protocolo de Saneamiento en 4 Pasos Operativos

    #### **Paso 1: Auditoría y Rescate en Tartagal**
    * Generar el listado de los 100 códigos con mayor valor en el 49,5% de Stock Muerto de Tartagal.
    * Transferir a Casa Central Salta todo repuesto de rotación urbana o de servicios comunes.

    #### **Paso 2: Matriz Cruzada de Traspasos Inter-Sucursales**
    * Ninguna sucursal podrá emitir pedidos a fábrica a TASA sin antes correr el filtro de validación cruzada:
      1. Si Jujuy o Salta necesitan una pieza, el sistema debe buscarla primero en el stock *Muerto* de Tartagal o Las Lajitas.
      2. Esto **descongela capital de trabajo sin erogación de fondos nuevos**.

    #### **Paso 3: Ventana de Devolución a Toyota (TASA)**
    * Filtrar piezas adquiridas en los últimos 6 a 12 meses que hayan entrado en obsolescencia o sin rotación, para aplicar a la cuota autorizada de devolución por TSM.

    #### **Paso 4: Paquetes con Descuento para Flotilleros de Minería y Agro**
    * Empaquetar baterías Hilux (sobrestock Jujuy) y piezas de suspensión/frenos con descuentos comerciales del 15% al 30% a clientes corporativos con cuenta corriente.
    """)
