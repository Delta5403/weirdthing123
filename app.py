import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="AgroTech Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATOS SIMULADOS ====================

@st.cache_data
def cargar_cultivos():
    return pd.DataFrame({
        'id': [1, 2, 3, 4],
        'nombre': ['Maíz', 'Trigo', 'Soja', 'Arroz'],
        'hectareas': [5.0, 3.5, 2.8, 4.2],
        'fecha_siembra': ['2026-02-01', '2026-02-15', '2026-01-20', '2026-02-10'],
        'estado': ['Crecimiento', 'Germinación', 'Floración', 'Maduración'],
        'progreso': [65, 40, 75, 50],
        'humedad_suelo': [45, 52, 38, 48],
        'temperatura': [28, 26, 30, 27]
    })

@st.cache_data
def cargar_actividades():
    return pd.DataFrame({
        'fecha': pd.date_range('2026-03-20', periods=12, freq='D'),
        'cultivo': np.random.choice(['Maíz', 'Trigo', 'Soja', 'Arroz'], 12),
        'tipo': np.random.choice(['Riego', 'Fertilización', 'Inspección', 'Poda'], 12),
        'cantidad': np.random.randint(5, 100, 12),
        'estado': np.random.choice(['Completado', 'Pendiente', 'En progreso'], 12)
    })

@st.cache_data
def cargar_alertas():
    return [
        {'tipo': 'warning', 'mensaje': '⚠️ Maíz: Riego urgente recomendado', 'cultivo': 'Maíz'},
        {'tipo': 'info', 'mensaje': 'ℹ️ Trigo: Próxima fertilización en 3 días', 'cultivo': 'Trigo'},
        {'tipo': 'danger', 'mensaje': '🔴 Soja: Plagas detectadas', 'cultivo': 'Soja'},
        {'tipo': 'success', 'mensaje': '✅ Arroz: Estado óptimo', 'cultivo': 'Arroz'},
    ]

cultivos_df = cargar_cultivos()
actividades_df = cargar_actividades()
alertas = cargar_alertas()

# ==================== SIDEBAR (MENÚ) ====================

with st.sidebar:
    st.title("🌾 AgroTech")
    st.divider()
    
    pagina = st.radio(
        "Navegación",
        ["📊 Dashboard", "🌱 Cultivos", "📝 Actividades", "📈 Reportes", "⚙️ Configuración"]
    )
    
    st.divider()
    st.write("**Estado del Sistema**")
    col1, col2 = st.columns(2)
    col1.metric("Cultivos", len(cultivos_df))
    col2.metric("Hectáreas", f"{cultivos_df['hectareas'].sum():.1f}")
    
    st.divider()
    st.write(f"*Última actualización: {datetime.now().strftime('%H:%M:%S')}*")

# ==================== PÁGINA: DASHBOARD ====================

if pagina == "📊 Dashboard":
    st.title("📊 Dashboard Principal")
    st.write("Bienvenido a tu sistema de gestión agrícola inteligente")
    
    # Métricas principales
    st.subheader("📈 Métricas Clave")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Cultivos Activos",
            value=len(cultivos_df),
            delta="+1 esta semana"
        )
    
    with col2:
        st.metric(
            label="Hectáreas Totales",
            value=f"{cultivos_df['hectareas'].sum():.1f}",
            delta="+0.5 ha"
        )
    
    with col3:
        st.metric(
            label="Actividades Mes",
            value=len(actividades_df),
            delta="+5 completadas"
        )
    
    with col4:
        promedio_progreso = cultivos_df['progreso'].mean()
        st.metric(
            label="Progreso Promedio",
            value=f"{promedio_progreso:.0f}%",
            delta="+5%"
        )
    
    # Alertas
    st.subheader("🚨 Alertas Importantes")
    col1, col2 = st.columns(2)
    
    for i, alerta in enumerate(alertas):
        if i % 2 == 0:
            col = col1
        else:
            col = col2
        
        if alerta['tipo'] == 'warning':
            col.warning(alerta['mensaje'])
        elif alerta['tipo'] == 'danger':
            col.error(alerta['mensaje'])
        elif alerta['tipo'] == 'info':
            col.info(alerta['mensaje'])
        else:
            col.success(alerta['mensaje'])
    
    st.divider()
    
    # Gráficos
    st.subheader("📊 Análisis Visual")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Hectáreas por Cultivo**")
        fig1 = px.bar(
            cultivos_df,
            x='nombre',
            y='hectareas',
            color='nombre',
            title="Distribución de Hectáreas",
            labels={'nombre': 'Cultivo', 'hectareas': 'Hectáreas'}
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.write("**Progreso de Cultivos**")
        fig2 = px.bar(
            cultivos_df,
            x='nombre',
            y='progreso',
            color='progreso',
            title="Progreso de Cosecha (%)",
            labels={'nombre': 'Cultivo', 'progreso': 'Progreso (%)'},
            color_continuous_scale="Viridis"
        )
        fig2.update_yaxes(range=[0, 100])
        st.plotly_chart(fig2, use_container_width=True)
    
    # Tabla resumen
    st.subheader("📋 Estado de Cultivos")
    
    tabla_display = cultivos_df[['nombre', 'hectareas', 'estado', 'progreso', 'humedad_suelo', 'temperatura']].copy()
    tabla_display.columns = ['Cultivo', 'Hectáreas', 'Estado', 'Progreso (%)', 'Humedad (%)', 'Temp (°C)']
    tabla_display['Progreso (%)'] = tabla_display['Progreso (%)'].astype(str) + '%'
    tabla_display['Humedad (%)'] = tabla_display['Humedad (%)'].astype(str) + '%'
    tabla_display['Temp (°C)'] = tabla_display['Temp (°C)'].astype(str) + '°'
    
    st.dataframe(tabla_display, use_container_width=True, hide_index=True)
    
    # Gráfico de línea - Actividades
    st.subheader("📈 Actividades por Día")
    actividades_por_dia = actividades_df.groupby(actividades_df['fecha'].dt.date).size().reset_index()
    actividades_por_dia.columns = ['Fecha', 'Cantidad']
    
    fig3 = px.line(
        actividades_por_dia,
        x='Fecha',
        y='Cantidad',
        markers=True,
        title="Tendencia de Actividades",
        labels={'Fecha': 'Fecha', 'Cantidad': 'Número de Actividades'}
    )
    st.plotly_chart(fig3, use_container_width=True)

# ==================== PÁGINA: CULTIVOS ====================

elif pagina == "🌱 Cultivos":
    st.title("🌱 Gestión de Cultivos")
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Ver Cultivos", "Agregar Cultivo", "Editar Cultivo"])
    
    # TAB 1: Ver Cultivos
    with tab1:
        st.subheader("Lista de Cultivos")
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            filtro_estado = st.multiselect(
                "Filtrar por estado",
                cultivos_df['estado'].unique(),
                default=cultivos_df['estado'].unique()
            )
        with col2:
            filtro_progreso = st.slider("Progreso mínimo (%)", 0, 100, 0)
        
        # Aplicar filtros
        cultivos_filtrados = cultivos_df[
            (cultivos_df['estado'].isin(filtro_estado)) &
            (cultivos_df['progreso'] >= filtro_progreso)
        ]
        
        # Mostrar cultivos en tarjetas
        cols = st.columns(2)
        for idx, (i, cultivo) in enumerate(cultivos_filtrados.iterrows()):
            col = cols[idx % 2]
            
            with col:
                st.write(f"### {cultivo['nombre']}")
                st.write(f"📍 Hectáreas: {cultivo['hectareas']} ha")
                st.write(f"🌱 Estado: {cultivo['estado']}")
                st.write(f"📊 Progreso: {cultivo['progreso']}%")
                
                # Barra de progreso
                st.progress(cultivo['progreso'] / 100)
                
                col_btn1, col_btn2, col_btn3 = st.columns(3)
                with col_btn1:
                    st.button("✏️ Editar", key=f"edit_{cultivo['id']}")
                with col_btn2:
                    st.button("📊 Ver Detalles", key=f"ver_{cultivo['id']}")
                with col_btn3:
                    st.button("🗑️ Eliminar", key=f"del_{cultivo['id']}")
                
                st.divider()
    
    # TAB 2: Agregar Cultivo
    with tab2:
        st.subheader("Agregar Nuevo Cultivo")
        
        with st.form("form_nuevo_cultivo"):
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input("Nombre del cultivo")
                hectareas = st.number_input("Hectáreas", min_value=0.1, max_value=1000.0, step=0.1)
            
            with col2:
                estado = st.selectbox("Estado inicial", ["Siembra", "Germinación", "Crecimiento", "Floración", "Maduración"])
                fecha_siembra = st.date_input("Fecha de siembra")
            
            submitted = st.form_submit_button("✅ Agregar Cultivo", use_container_width=True)
            
            if submitted:
                if nombre:
                    st.success(f"✅ Cultivo '{nombre}' agregado exitosamente")
                else:
                    st.error("⚠️ Por favor completa todos los campos")
    
    # TAB 3: Editar Cultivo
    with tab3:
        st.subheader("Editar Cultivo")
        
        cultivo_seleccionado = st.selectbox(
            "Selecciona cultivo a editar",
            cultivos_df['nombre'].tolist()
        )
        
        cultivo = cultivos_df[cultivos_df['nombre'] == cultivo_seleccionado].iloc[0]
        
        with st.form("form_editar_cultivo"):
            col1, col2 = st.columns(2)
            
            with col1:
                nombre = st.text_input("Nombre", value=cultivo['nombre'])
                hectareas = st.number_input("Hectáreas", value=cultivo['hectareas'], step=0.1)
            
            with col2:
                estado = st.selectbox("Estado", 
                    ["Siembra", "Germinación", "Crecimiento", "Floración", "Maduración"],
                    index=["Siembra", "Germinación", "Crecimiento", "Floración", "Maduración"].index(cultivo['estado'])
                )
                progreso = st.slider("Progreso (%)", 0, 100, cultivo['progreso'])
            
            submitted = st.form_submit_button("✅ Actualizar", use_container_width=True)
            
            if submitted:
                st.success(f"✅ Cultivo actualizado correctamente")

# ==================== PÁGINA: ACTIVIDADES ====================

elif pagina == "📝 Actividades":
    st.title("📝 Gestión de Actividades")
    
    tab1, tab2 = st.tabs(["Historial", "Registrar Actividad"])
    
    # TAB 1: Historial
    with tab1:
        st.subheader("Historial de Actividades")
        
        # Filtros
        col1, col2 = st.columns(2)
        
        with col1:
            filtro_tipo = st.multiselect(
                "Tipo de actividad",
                actividades_df['tipo'].unique(),
                default=actividades_df['tipo'].unique()
            )
        
        with col2:
            filtro_cultivo = st.multiselect(
                "Cultivo",
                actividades_df['cultivo'].unique(),
                default=actividades_df['cultivo'].unique()
            )
        
        # Aplicar filtros
        actividades_filtradas = actividades_df[
            (actividades_df['tipo'].isin(filtro_tipo)) &
            (actividades_df['cultivo'].isin(filtro_cultivo))
        ].sort_values('fecha', ascending=False)
        
        # Tabla
        tabla_act = actividades_filtradas[['fecha', 'cultivo', 'tipo', 'cantidad', 'estado']].copy()
        tabla_act.columns = ['Fecha', 'Cultivo', 'Tipo', 'Cantidad', 'Estado']
        tabla_act['Fecha'] = tabla_act['Fecha'].astype(str)
        
        st.dataframe(tabla_act, use_container_width=True, hide_index=True)
        
        # Estadísticas
        st.subheader("📊 Estadísticas")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Actividades", len(actividades_filtradas))
        
        with col2:
            completadas = len(actividades_filtradas[actividades_filtradas['estado'] == 'Completado'])
            st.metric("Completadas", completadas)
        
        with col3:
            pendientes = len(actividades_filtradas[actividades_filtradas['estado'] == 'Pendiente'])
            st.metric("Pendientes", pendientes)
    
    # TAB 2: Registrar Actividad
    with tab2:
        st.subheader("Registrar Nueva Actividad")
        
        with st.form("form_actividad"):
            col1, col2 = st.columns(2)
            
            with col1:
                cultivo = st.selectbox("Cultivo", cultivos_df['nombre'].tolist())
                tipo = st.selectbox("Tipo de Actividad", 
                    ["Riego", "Fertilización", "Inspección", "Poda", "Cosecha", "Otros"])
            
            with col2:
                cantidad = st.number_input("Cantidad", min_value=0.0, step=0.1)
                fecha = st.date_input("Fecha")
            
            descripcion = st.text_area("Descripción (opcional)")
            
            submitted = st.form_submit_button("✅ Registrar Actividad", use_container_width=True)
            
            if submitted:
                st.success(f"✅ Actividad '{tipo}' registrada para '{cultivo}'")

# ==================== PÁGINA: REPORTES ====================

elif pagina == "📈 Reportes":
    st.title("📈 Reportes y Análisis")
    
    tab1, tab2, tab3 = st.tabs(["Producción", "Recursos", "Comparativas"])
    
    # TAB 1: Producción
    with tab1:
        st.subheader("Análisis de Producción")
        
        # Generar datos de ejemplo
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Marzo']
        produccion_maiz = [100, 110, 120, 135, 150, 160]
        
        df_produccion = pd.DataFrame({
            'Mes': meses,
            'Maíz': produccion_maiz
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(df_produccion, x='Mes', y='Maíz', markers=True, 
                         title="Producción de Maíz",
                         labels={'Maíz': 'Toneladas'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Proyección de Cosecha**")
            fig = px.bar(cultivos_df, x='nombre', y='progreso',
                        title="Progreso hacia Cosecha",
                        color='progreso',
                        color_continuous_scale="Greens")
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 2: Recursos
    with tab2:
        st.subheader("Uso de Recursos")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Consumo de Agua (mm)**")
            fig = px.bar(cultivos_df, x='nombre', y='humedad_suelo',
                        title="Humedad del Suelo",
                        color='humedad_suelo',
                        color_continuous_scale="Blues")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Temperatura Promedio**")
            fig = px.bar(cultivos_df, x='nombre', y='temperatura',
                        title="Temperatura por Cultivo",
                        color='temperatura',
                        color_continuous_scale="Reds")
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 3: Comparativas
    with tab3:
        st.subheader("Análisis Comparativo")
        
        st.write("**Comparativa de Cultivos**")
        
        # Crear datos para comparar
        comparativa = cultivos_df[['nombre', 'hectareas', 'progreso', 'humedad_suelo', 'temperatura']].copy()
        
        fig = go.Figure(data=[
            go.Scatterpolar(
                r=comparativa['progreso'],
                theta=comparativa['nombre'],
                fill='toself',
                name='Progreso (%)'
            )
        ])
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            title="Radar de Progreso de Cultivos"
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ==================== PÁGINA: CONFIGURACIÓN ====================

elif pagina == "⚙️ Configuración":
    st.title("⚙️ Configuración")
    
    tab1, tab2, tab3 = st.tabs(["Perfil", "Notificaciones", "Sistema"])
    
    # TAB 1: Perfil
    with tab1:
        st.subheader("Mi Perfil")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nombre_usuario = st.text_input("Nombre", "José García")
            email = st.text_input("Email", "jose@agrotech.com")
        
        with col2:
            ubicacion = st.text_input("Ubicación", "Córdoba, Argentina")
            telefono = st.text_input("Teléfono", "+54 351 123 4567")
        
        if st.button("💾 Guardar Cambios"):
            st.success("✅ Perfil actualizado correctamente")
    
    # TAB 2: Notificaciones
    with tab2:
        st.subheader("Preferencias de Notificaciones")
        
        st.toggle("📧 Notificaciones por Email", value=True)
        st.toggle("📱 Notificaciones en Aplicación", value=True)
        st.toggle("⚠️ Alertas de Riego", value=True)
        st.toggle("🌡️ Alertas de Temperatura", value=True)
        st.toggle("🦗 Alertas de Plagas", value=True)
        
        if st.button("💾 Guardar Preferencias"):
            st.success("✅ Preferencias guardadas")
    
    # TAB 3: Sistema
    with tab3:
        st.subheader("Información del Sistema")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Versión**: 1.0.0")
            st.write("**Estado**: ✅ Operativo")
            st.write("**Última actualización**: 2026-03-30")
        
        with col2:
            st.write("**Base de datos**: ✅ Conectado")
            st.write("**API**: ✅ Operativo")
            st.write("**Almacenamiento**: 45% utilizado")
        
        st.divider()
        
        if st.button("🔄 Sincronizar Datos"):
            st.info("🔄 Sincronizando datos...")
            st.success("✅ Datos sincronizados correctamente")

# ==================== FOOTER ====================

st.divider()
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.caption("🌾 AgroTech 2026")

with col2:
    st.caption("Made with ❤️ by AgroTech Team")

with col3:
    st.caption("© Todos los derechos reservados")