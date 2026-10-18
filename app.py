import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Instituciones y Crecimiento Económico",
    layout="wide"
)

# --- MENÚ DE NAVEGACIÓN PRINCIPAL EN LA BARRA LATERAL ---
st.sidebar.title("🧭 Menú de Navegación")
seccion = st.sidebar.radio(
    "Selecciona la sección:",
    ["📊 1. Simulador Institucional Global", "☕ 2. Caso Eje Cafetero (Apertura y PTF)"]
)

# ==========================================
# SECCIÓN 1: SIMULADOR INSTITUCIONAL GLOBAL
# ==========================================
if seccion == "📊 1. Simulador Institucional Global":
    st.title("📊 Simulador Interactivo: Instituciones, Inversión y Crecimiento")
    st.markdown("""
    Esta herramienta simula la relación empírica entre las variables institucionales (Estado de derecho, corrupción, derechos políticos) 
    y el desempeño macroeconómico global.
    """)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🎛️ Controles Institucionales")
    
    rule_of_law = st.sidebar.slider("Estado de Derecho (Rule of Law)", min_value=-2.5, max_value=2.5, value=0.0, step=0.1)
    control_corrupcion = st.sidebar.slider("Control de la Corrupción", min_value=-4.0, max_value=16.0, value=2.0, step=0.5)
    derechos_politicos = st.sidebar.slider("Derechos Políticos y Civiles (DP)", min_value=1, max_value=7, value=3, step=1)

    # Simulación estadística de los datos globales
    np.random.seed(42)
    n_paises = 50
    base_rule = np.random.normal(rule_of_law, 0.4, n_paises)
    base_corr = np.random.normal(control_corrupcion, 1.2, n_paises)
    base_dp = np.random.normal(derechos_politicos, 0.8, n_paises)

    pib_simulado = 2.5 + 1.2 * base_rule + 0.8 * base_dp + np.random.normal(0, 0.8, n_paises)
    inversion_simulada = 20 + 3.5 * base_corr + 2.0 * base_rule + np.random.normal(0, 5, n_paises)
    tea_simulado = 5 + 2.8 * base_dp + 1.5 * base_rule + np.random.normal(0, 3, n_paises)

    df_global = pd.DataFrame({
        'Rule of Law': base_rule,
        'Control Corrupción': base_corr,
        'Derechos Políticos': base_dp,
        'PIB (Crecimiento)': pib_simulado,
        'Inversión (% del PIB)': inversion_simulada,
        'Emprendimiento (TEA %)': tea_simulado
    })

    # Pestañas internas solo para la parte global
    tab1, tab2, tab3 = st.tabs(["📈 PIB vs Derechos Políticos", "💰 Inversión vs Corrupción", "🚀 Emprendimiento y Entorno"])

    with tab1:
        st.subheader("Crecimiento del PIB y Derechos Políticos")
        fig1 = px.scatter(df_global, x='Derechos Políticos', y='PIB (Crecimiento)', trendline="ols", color='Rule of Law', color_continuous_scale='Viridis')
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        st.subheader("Inversión Privada y Control de Corrupción")
        fig2 = px.scatter(df_global, x='Control Corrupción', y='Inversión (% del PIB)', trendline="ols", color='Rule of Law', color_continuous_scale='Plasma')
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.subheader("Actividad Emprendedora (TEA) y Derechos Políticos")
        fig3 = px.scatter(df_global, x='Derechos Políticos', y='Emprendimiento (TEA %)', trendline="ols", color='Control Corrupción', color_continuous_scale='Cividis')
        st.plotly_chart(fig3, use_container_width=True)

# ==========================================
# SECCIÓN 2: CASO EJE CAFETERO (APERTURA Y PTF)
# ==========================================
elif seccion == "☕ 2. Caso Eje Cafetero (Apertura y PTF)":
    st.title("☕ Impacto de la Apertura Económica en el Eje Cafetero (1985-2005)")
    st.markdown("""
    Esta sección presenta de forma independiente el modelo econométrico aplicado al Eje Cafetero. 
    Mide cómo el **Índice de Transabilidad (IT)** impactó la **Productividad Total de los Factores (PTF)** en cada departamento.
    """)

    # Datos específicos del estudio universitario
    df_eje = pd.DataFrame({
        'Departamento': ['Caldas', 'Quindío', 'Risaralda'],
        'Impacto en la PTF (Coeficiente)': [-0.0888, -0.0787, 0.1370],
        'Resultado': ['Desfavorable (Desindustrialización)', 'Desfavorable (Caída de PTF)', 'Favorable (Efecto Estímulo)']
    })

    # Gráfica de Barras Independiente y Clara
    fig_eje = px.bar(
        df_eje, 
        x='Departamento', 
        y='Impacto en la PTF (Coeficiente)',
        color='Resultado',
        color_discrete_map={
            'Desfavorable (Desindustrialización)': '#EF553B',
            'Desfavorable (Caída de PTF)': '#EF553B',
            'Favorable (Efecto Estímulo)': '#00CC96'
        },
        text='Impacto en la PTF (Coeficiente)',
        title="Efecto del Índice de Transabilidad sobre la PTF Regional"
    )
    
    fig_eje.update_traces(texttemplate='%{text:.4f}', textposition='outside')
    fig_eje.add_hline(y=0, line_dash="dash", line_color="black")
    
    st.plotly_chart(fig_eje, use_container_width=True)

    st.markdown("### 💡 Análisis del Caso para la Exposición:")
    col1, col2 = st.columns(2)
    with col1:
        st.error("""
        **Caldas y Quindío (Coeficientes Negativos):**
        * La apertura económica de los años 90 se implementó sin una red institucional de apoyo ni infraestructura adecuada.
        * Provocó un impacto desfavorable sobre la productividad industrial y desplazamiento hacia la informalidad.
        """)
    with col2:
        st.success("""
        **Risaralda (Coeficiente Positivo):**
        * Representa la excepción favorable ($+0,1370$).
        * Demuestra que una mejor adaptación local y comercial permitió que la apertura sí estimulara positivamente la PTF y el crecimiento.
        """)
