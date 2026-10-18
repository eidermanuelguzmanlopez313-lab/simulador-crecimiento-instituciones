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
    ["📊 1. Simulador Global (Galindo Martín)", "☕ 2. Simulador Interactivo Eje Cafetero"]
)

# ==========================================
# SECCIÓN 1: SIMULADOR GLOBAL (GALINDO MARTÍN)
# ==========================================
if seccion == "📊 1. Simulador Global (Galindo Martín)":
    st.title("📊 Simulador Global: Instituciones, Políticas y Desempeño Macroeconómico")
    st.markdown("""
    Esta herramienta replica de forma **totalmente interactiva** las relaciones del artículo de **Galindo Martín**. 
    Mueve los controles en la barra lateral o cambia el tipo de política pública para observar el recálculo en tiempo real de la nube de puntos y la línea de tendencia econométrica.
    """)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🎛️ Parametrización Institucional Global")
    
    # Sliders con alta sensibilidad
    rule_of_law = st.sidebar.slider("Estado de Derecho (Rule of Law)", min_value=-2.5, max_value=2.5, value=0.0, step=0.1)
    control_corrupcion = st.sidebar.slider("Control de la Corrupción", min_value=-4.0, max_value=16.0, value=2.0, step=0.5)
    derechos_politicos = st.sidebar.slider("Derechos Políticos y Civiles (DP)", min_value=1.0, max_value=7.0, value=3.0, step=0.2)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🏛️ Escenario de Política Pública")
    tipo_politica = st.sidebar.selectbox(
        "Simular Tipo de Política / Reforma:",
        [
            "1. Política Estándar / Sin Reforma (Base)",
            "2. Reforma de Fortalecimiento Institucional (+ Eficiencia Burocrática)",
            "3. Captura Institucional / Grupos de Interés (Dixit)"
        ]
    )

    # Definición de choques directos y visibles
    if tipo_politica == "2. Reforma de Fortalecimiento Institucional (+ Eficiencia Burocrática)":
        bono_pib = 2.0
        bono_inversion = 6.0
        bono_tea = 4.0
        nota_politica = "✨ **Efecto de Reforma Positiva:** Una reforma pro-transparencia y seguridad jurídica desplaza visiblemente la inversión y el PIB hacia arriba."
    elif tipo_politica == "3. Captura Institucional / Grupos de Interés (Dixit)":
        bono_pib = -2.0
        bono_inversion = -7.0
        bono_tea = -3.5
        nota_politica = "⚠️ **Efecto de Captura por Grupos de Presión:** La incertidumbre y la búsqueda de rentas reducen sustancialmente la inversión privada y el crecimiento."
    else:
        bono_pib = 0.0
        bono_inversion = 0.0
        bono_tea = 0.0
        nota_politica = "ℹ️ **Escenario Base:** Muestra la dispersión estándar según los valores institucionales seleccionados en los sliders."

    # Generación estocástica vinculada DIRECTAMENTE a los sliders del usuario
    np.random.seed(42)
    n_paises = 50
    
    # Sensibilidad reactiva
    dp_vec = np.clip(np.random.normal(derechos_politicos, 0.8, n_paises), 1, 7)
    corr_vec = np.random.normal(control_corrupcion, 1.5, n_paises)
    rule_vec = np.random.normal(rule_of_law, 0.5, n_paises)

    # Las variables dependientes reaccionan fuerte a los sliders
    pib_simulado = 1.0 + (0.8 * dp_vec) + (1.2 * rule_vec) + bono_pib + np.random.normal(0, 0.6, n_paises)
    inversion_simulada = 12.0 + (1.2 * corr_vec) + (2.5 * rule_vec) + bono_inversion + np.random.normal(0, 2.5, n_paises)
    tea_simulado = 3.0 + (1.5 * dp_vec) + (0.8 * corr_vec) + bono_tea + np.random.normal(0, 1.5, n_paises)

    df_global = pd.DataFrame({
        'Rule of Law': rule_vec,
        'Control Corrupción': corr_vec,
        'Derechos Políticos': dp_vec,
        'Crecimiento del PIB (%)': pib_simulado,
        'Inversión Privada (% del PIB)': inversion_simulada,
        'Actividad Emprendedora (TEA %)': tea_simulado
    })

    st.info(nota_politica)

    # Pestañas con límites de ejes fijos para notar el movimiento instantáneo
    tab1, tab2, tab3 = st.tabs(["📈 PIB vs Derechos Políticos", "💰 Inversión vs Corrupción", "🚀 Emprendimiento y Entorno"])

    with tab1:
        st.subheader("Crecimiento del PIB vs. Derechos Políticos (Replicación Gráfico 5)")
        fig1 = px.scatter(
            df_global, x='Derechos Políticos', y='Crecimiento del PIB (%)', 
            trendline="ols", color='Rule of Law', color_continuous_scale='Viridis',
            range_x=[0, 8], range_y=[-3, 12],
            title="Impacto de los Derechos Políticos en el Crecimiento del PIB"
        )
        st.plotly_chart(fig1, use_container_width=True)

    with tab2:
        st.subheader("Inversión Privada vs. Control de Corrupción (Replicación Gráfico 6)")
        fig2 = px.scatter(
            df_global, x='Control Corrupción', y='Inversión Privada (% del PIB)', 
            trendline="ols", color='Rule of Law', color_continuous_scale='Plasma',
            range_x=[-6, 18], range_y=[0, 45],
            title="Relación entre Control de la Corrupción e Inversión Privada"
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        st.subheader("Actividad Emprendedora (TEA) vs. Derechos Políticos (Replicación Gráfico 7)")
        fig3 = px.scatter(
            df_global, x='Derechos Políticos', y='Actividad Emprendedora (TEA %)', 
            trendline="ols", color='Control Corrupción', color_continuous_scale='Cividis',
            range_x=[0, 8], range_y=[-2, 22],
            title="Entorno Institucional y Fomento al Emprendimiento (Schumpeter)"
        )
        st.plotly_chart(fig3, use_container_width=True)

# ==========================================
# SECCIÓN 2: SIMULADOR INTERACTIVO EJE CAFETERO
# ==========================================
elif seccion == "☕ 2. Simulador Interactivo Eje Cafetero":
    st.title("☕ Simulador de Apertura y PTF en el Eje Cafetero (1985-2005)")
    st.markdown("""
    Modifica los parámetros de **apertura comercial (Índice de Transabilidad)** y **soporte institucional** en la barra lateral 
    para simular cómo se habrían comportado los coeficientes de la Productividad Total de los Factores (PTF) en Caldas, Quindío y Risaralda bajo diferentes escenarios de política.
    """)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🎛️ Controles del Eje Cafetero")
    
    ajuste_apertura = st.sidebar.slider(
        "Nivel de Choque de Apertura", min_value=0.5, max_value=2.0, value=1.0, step=0.1,
        help="Multiplica el impacto de la apertura comercial en la región."
    )
    soporte_institucional = st.sidebar.slider(
        "Políticas de Apoyo Institucional / Infraestructura", min_value=-0.05, max_value=0.10, value=0.0, step=0.01,
        help="Simula el efecto sumando un bono institucional positivo a los departamentos."
    )

    # Coeficientes base ajustados interactivamente
    val_caldas = (-0.0888 * ajuste_apertura) + soporte_institucional
    val_quindio = (-0.0787 * ajuste_apertura) + soporte_institucional
    val_risaralda = (0.1370 * ajuste_apertura) + soporte_institucional

    df_eje_dinamico = pd.DataFrame({
        'Departamento': ['Caldas', 'Quindío', 'Risaralda'],
        'Impacto en la PTF (Coeficiente)': [val_caldas, val_quindio, val_risaralda],
        'Resultado': [
            'Favorable' if val_caldas >= 0 else 'Desfavorable (Desindustrialización)',
            'Favorable' if val_quindio >= 0 else 'Desfavorable (Caída de PTF)',
            'Favorable' if val_risaralda >= 0 else 'Desfavorable'
        ]
    })

    fig_eje = px.bar(
        df_eje_dinamico, 
        x='Departamento', 
        y='Impacto en la PTF (Coeficiente)',
        color='Resultado',
        color_discrete_map={
            'Desfavorable (Desindustrialización)': '#EF553B',
            'Desfavorable (Caída de PTF)': '#EF553B',
            'Desfavorable': '#EF553B',
            'Favorable': '#00CC96'
        },
        text='Impacto en la PTF (Coeficiente)',
        title="Simulación Dinámica: Efecto del Índice de Transabilidad sobre la PTF Regional",
        range_y=[-0.25, 0.30]
    )
    
    fig_eje.update_traces(texttemplate='%{text:.4f}', textposition='outside')
    fig_eje.add_hline(y=0, line_dash="dash", line_color="black")
    
    st.plotly_chart(fig_eje, use_container_width=True)

    st.markdown("### 💡 Diagnóstico del Escenario Simulado:")
    if val_caldas < 0 and val_quindio < 0:
        st.warning("""
        ⚠️ **Escenario de Vulnerabilidad:** Con estos niveles de apertura sin un amortiguador institucional fuerte, 
        Caldas y Quindío continúan mostrando coeficientes negativos, reflejando problemas de desindustrialización y pérdida de productividad.
        """)
    else:
        st.success("""
        ✨ **Escenario de Convergencia:** Al sumar apoyo institucional e infraestructura, se logra revertir el impacto negativo inicial, 
        permitiendo que toda la región del Eje Cafetero absorba de forma positiva los choques de la apertura comercial.
        """)
