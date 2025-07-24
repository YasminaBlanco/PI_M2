import streamlit as st
import pandas as pd
import pg8000.dbapi
import os
from dotenv import load_dotenv
import altair as alt

# Cargar variables de entorno
load_dotenv()

# Obtener las credenciales de la base de datos
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

# --- Configuración de la Página Streamlit ---
st.set_page_config(layout="wide", page_title="Análisis de KPIs de Productos 📈")

# --- Funciones de Carga de Datos ---
@st.cache_data(ttl=600) # Cachea los datos por 10 minutos (600 segundos)
def get_data_from_db():
    """
    Establece conexión con la base de datos PostgreSQL y carga
    los datos del modelo rpt_analisis_productos_kpis.
    """
    conn = None
    try:
        with st.spinner("Cargando datos del almacén de datos..."): # Agrega un spinner de carga
            conn = pg8000.dbapi.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                port=int(DB_PORT)
            )

            query = """
            SELECT
                producto_id,
                nombre_producto,
                nombre_categoria,
                mes_orden,
                ingresos_totales,
                crecimiento_porcentual_ventas,
                veces_agregado_al_carrito,
                cantidad_total_agregada_carrito,
                rank_ingresos_totales,
                rank_crecimiento_ventas,
                rank_veces_agregado_carrito
            FROM
                rpt_analisis_productos_kpis
            ORDER BY
                mes_orden DESC, ingresos_totales DESC;
            """
            df = pd.read_sql_query(query, conn)
            
            # Asegurarse de que 'mes_orden' sea de tipo datetime para facilitar filtros
            df['mes_orden'] = pd.to_datetime(df['mes_orden'])
            
            # Asegurarse de que 'crecimiento_porcentual_ventas' sea numérico.
            # Los errores pueden aparecer como NaN o strings si hay problemas en la DB.
            df['crecimiento_porcentual_ventas'] = pd.to_numeric(df['crecimiento_porcentual_ventas'], errors='coerce')
            
            return df
    except Exception as e:
        st.error(f"⚠️ Error al conectar o consultar la base de datos: {e}")
        st.warning("No se pudieron cargar los datos del modelo `rpt_analisis_productos_kpis`. Asegúrate de que dbt se ejecutó correctamente y las credenciales son válidas.")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()

# --- Título Principal y Descripción ---
st.title("📊 Análisis Estratégico de KPIs de Productos")
st.markdown("""
Bienvenido al panel de control de rendimiento de productos. Aquí podrás explorar métricas clave como ingresos, crecimiento en ventas e intención de compra, para identificar oportunidades y tomar decisiones informadas.
""")

# Botón para recargar datos
col_reload, _ = st.columns([0.2, 0.8])
with col_reload:
    if st.button('🔄 Recargar Datos del Dashboard', help="Haz clic para actualizar los datos desde la base de datos."):
        st.cache_data.clear() # Limpia la caché de la función get_data_from_db
        st.rerun() # Fuerza a Streamlit a volver a ejecutar la aplicación desde cero

# --- Cargar Datos ---
df = get_data_from_db()

if not df.empty:
    # --- Sidebar para Filtros ---
    st.sidebar.header("🔍 Filtros de Análisis")

    # Filtro por Mes
    available_months = sorted(df['mes_orden'].unique(), reverse=True)
    
    # Establecer el mes más reciente como valor por defecto
    default_month_index = 0
    if len(available_months) > 0:
        pass # default_month_index ya es 0

    selected_month = st.sidebar.selectbox(
        "Selecciona el Mes de Análisis",
        available_months,
        index=default_month_index,
        format_func=lambda x: x.strftime('%B %Y') # Formato más amigable: Enero 2024
    )

    # Filtro por Categoría
    available_categories = ['Todas las Categorías'] + sorted(df['nombre_categoria'].unique().tolist())
    selected_category = st.sidebar.selectbox(
        "Filtrar por Categoría de Producto",
        available_categories
    )

    # Filtrar el DataFrame por el mes y categoría seleccionados
    df_filtered_by_month = df[df['mes_orden'] == selected_month].copy()
    if selected_category != 'Todas las Categorías':
        df_filtered_by_month = df_filtered_by_month[df_filtered_by_month['nombre_categoria'] == selected_category].copy()


    # Asegurarse de que el DataFrame filtrado no esté vacío antes de continuar
    if df_filtered_by_month.empty:
        st.info(f"No hay datos disponibles para el mes de **{selected_month.strftime('%B %Y')}** y categoría **{selected_category}**. Por favor, ajusta tus filtros.")
    else:
        st.markdown(f"### Datos para **{selected_month.strftime('%B %Y')}** {f'en la categoría **{selected_category}**' if selected_category != 'Todas las Categorías' else ''}")
        st.markdown("---")

        # --- Resumen de Datos ---
        st.header("📋 Resumen de Datos (Top Productos por Ingresos)")
        st.markdown("Tabla resumen de los productos con mayor rendimiento en el periodo seleccionado.")
        
        # Ordenar y mostrar el top 20 por ingresos
        df_top_20_ingresos = df_filtered_by_month.sort_values(by='ingresos_totales', ascending=False).head(20)
        st.dataframe(df_top_20_ingresos.style.format({
            'ingresos_totales': "${:,.2f}",
            'crecimiento_porcentual_ventas': "{:,.2f}%",
            'veces_agregado_al_carrito': "{:,.0f}",
            'cantidad_total_agregada_carrito': "{:,.0f}"
        }), use_container_width=True)

        st.markdown("---")
        st.header("📈 Visualizaciones Clave y Análisis Profundo")

        # --- PREGUNTA 1: ¿Qué producto genera más ingresos totales? ---
        st.subheader("1. 💰 Productos con Mayores Ingresos Totales")
        st.markdown("Identifica los productos que son los pilares de tus ingresos. Un alto ingreso puede indicar popularidad, buen precio o alta demanda.")
        
        if not df_filtered_by_month.empty:
            top_ingresos_product = df_filtered_by_month.sort_values(by='ingresos_totales', ascending=False).iloc[0]
            col1, col2 = st.columns(2)
            with col1:
                st.metric(
                    label=f"Producto Líder en Ingresos",
                    value=f"{top_ingresos_product['nombre_producto']}",
                    delta=f"${top_ingresos_product['ingresos_totales']:,.2f}"
                )
            with col2:
                st.metric(
                    label=f"Categoría del Producto Líder",
                    value=f"{top_ingresos_product['nombre_categoria']}"
                )
            
            # Gráfico de barras de ingresos por producto (Top N para claridad)
            chart_ingresos = alt.Chart(df_top_20_ingresos).mark_bar(color='#4CAF50').encode(
                x=alt.X('ingresos_totales', title='Ingresos Totales ($)', axis=alt.Axis(format='$,.0f')),
                y=alt.Y('nombre_producto', sort='-x', title='Producto'),
                tooltip=[
                    alt.Tooltip('nombre_producto', title='Producto'),
                    alt.Tooltip('nombre_categoria', title='Categoría'),
                    alt.Tooltip('ingresos_totales', title='Ingresos', format='$,.2f')
                ]
            ).properties(
                title=f'Top 20 Productos por Ingresos en {selected_month.strftime("%B %Y")}'
            ).interactive()
            st.altair_chart(chart_ingresos, use_container_width=True)
        else:
            st.info("No hay datos de ingresos disponibles para mostrar.")

        st.markdown("---")

        # --- PREGUNTA 2: ¿Qué productos están creciendo más rápidamente en ventas? ---
        st.subheader("2. 🚀 Productos con Mayor Crecimiento en Ventas")
        st.markdown("Descubre qué productos están ganando tracción. Un alto crecimiento puede señalar tendencias emergentes o campañas exitosas.")
        
        # Filtrar para productos con crecimiento real (no nulo ni infinito) y ordenar
        df_crecimiento = df_filtered_by_month[
            df_filtered_by_month['crecimiento_porcentual_ventas'].notna() & 
            (df_filtered_by_month['crecimiento_porcentual_ventas'] != float('inf')) &
            (df_filtered_by_month['crecimiento_porcentual_ventas'] != float('-inf'))
        ].sort_values(by='crecimiento_porcentual_ventas', ascending=False).head(10)
        
        if not df_crecimiento.empty:
            top_crecimiento_product = df_crecimiento.iloc[0]
            st.metric(
                label=f"Producto con mayor crecimiento",
                value=f"{top_crecimiento_product['nombre_producto']}",
                delta=f"{top_crecimiento_product['crecimiento_porcentual_ventas']:,.2f}%"
            )

            st.markdown("#### Tabla de Crecimiento de Ventas (Top 10)")
            st.markdown("Esta tabla muestra los productos con el mayor crecimiento porcentual en el mes seleccionado. El formato condicional te ayuda a identificar rápidamente los de mayor rendimiento.")
            
            def color_crecimiento(val):
                if val > 0:
                    return 'background-color: #006602'
                elif val < 0:
                    return 'background-color: #cd0000'
                else:
                    return 'background-color: #F0F0F0'

            # Crear la tabla con formato condicional
            st.dataframe(
                df_crecimiento[[
                    'nombre_producto',
                    'nombre_categoria',
                    'crecimiento_porcentual_ventas', 
                    'ingresos_totales' # Añadimos ingresos para contexto
                ]].style.format({
                    'crecimiento_porcentual_ventas': "{:,.2f}%",
                    'ingresos_totales': "${:,.2f}"
                }).applymap(color_crecimiento, subset=['crecimiento_porcentual_ventas']),
                use_container_width=True
            )
            
            st.markdown("""
            **Análisis:** Los productos con un crecimiento porcentual más alto son vitales para identificar nuevas tendencias y el éxito de estrategias recientes.
            Un crecimiento negativo (rojo) indica una disminución en las ventas (crecimiento).""")

        else:
            st.info("No hay datos de crecimiento disponibles para mostrar en este mes o categoría.")

        st.markdown("---")

        # --- PREGUNTA 3: ¿Qué producto muestra mayor intención de compra? ---
        st.subheader("3. 🛒 Productos con Mayor Intención de Compra")
        st.markdown("Comprende qué productos captan más la atención de los usuarios, incluso si aún no se han convertido en ventas. Esto puede indicar interés no concretado o productos para futuras campañas.")
        
        if not df_filtered_by_month.empty:
            top_intencion_product = df_filtered_by_month.sort_values(by='cantidad_total_agregada_carrito', ascending=False).iloc[0]
            st.metric(
                label=f"Producto más agregado al carrito",
                value=f"{top_intencion_product['nombre_producto']}",
                delta=f"{top_intencion_product['cantidad_total_agregada_carrito']:,.0f} veces"
            )

            chart_intencion = alt.Chart(df_filtered_by_month.sort_values(by='cantidad_total_agregada_carrito', ascending=False).head(20)).mark_bar(color='#2196F3').encode(
                x=alt.X('cantidad_total_agregada_carrito', title='Cantidad Agregada al Carrito'),
                y=alt.Y('nombre_producto', sort='-x', title='Producto'),
                tooltip=[
                    alt.Tooltip('nombre_producto', title='Producto'),
                    alt.Tooltip('nombre_categoria', title='Categoría'),
                    alt.Tooltip('cantidad_total_agregada_carrito', title='Veces en Carrito', format=',.0f')
                ]
            ).properties(
                title=f'Top 20 Productos por Cantidad Agregada al Carrito en {selected_month.strftime("%B %Y")}'
            ).interactive()
            st.altair_chart(chart_intencion, use_container_width=True)
        else:
            st.info("No hay datos de intención de compra disponibles para mostrar.")
            
        st.markdown("---")

        # --- PREGUNTA 4: ¿Los productos más agregados al carrito también son los que más ingresos generan? ---
        st.subheader("4. 🎯 Correlación: Ingresos vs. Intención de Compra")
        st.markdown("Este gráfico de dispersión te ayuda a visualizar la relación entre la popularidad (intención de compra) y el éxito en ventas (ingresos).")
        
        chart_scatter = alt.Chart(df_filtered_by_month).mark_circle(size=80, opacity=0.7).encode(
            x=alt.X('cantidad_total_agregada_carrito', title='Cantidad Agregada al Carrito', axis=alt.Axis(format=',.0f')),
            y=alt.Y('ingresos_totales', title='Ingresos Totales ($)', axis=alt.Axis(format='$,.0f')),
            tooltip=[
                alt.Tooltip('nombre_producto', title='Producto'),
                alt.Tooltip('nombre_categoria', title='Categoría'),
                alt.Tooltip('ingresos_totales', title='Ingresos', format='$,.2f'),
                alt.Tooltip('cantidad_total_agregada_carrito', title='Veces en Carrito', format=',.0f')
            ],
            color=alt.Color('nombre_categoria', title='Categoría', legend=alt.Legend(orient="bottom", columns=2)), # Color por categoría
            size=alt.Size('ingresos_totales', legend=None) # Tamaño del círculo por ingresos
        ).properties(
            title=f'Ingresos vs. Cantidad Agregada al Carrito en {selected_month.strftime("%B %Y")}'
        ).interactive()
        st.altair_chart(chart_scatter, use_container_width=True)

        st.markdown("""
        **Interpretación del gráfico de dispersión:**
        * **Arriba a la derecha:** Productos de alto valor y alta intención (¡tus estrellas!).
        * **Abajo a la derecha:** Alta intención, pero bajos ingresos (posibles carritos abandonados, productos de bajo precio o problemas de conversión).
        * **Arriba a la izquierda:** Bajos carritos, pero altos ingresos (productos de nicho, alta gama, o compras impulsivas).
        * **Abajo a la izquierda:** Bajo rendimiento en ambos (posibles productos a revisar o descontinuar).
        """)

        st.markdown("---")

        # --- PREGUNTA 5: ¿Qué producto creció más y se convirtió en el top en ingresos? ---
        st.subheader("5. 🏆 Productos Estrella: Alto Crecimiento y Alto Rendimiento")
        st.markdown("Identifica los productos que no solo generan muchos ingresos, sino que también están creciendo rápidamente. Estos son candidatos ideales para inversión y promoción.")
        
        df_high_growth_high_revenue = df_filtered_by_month[
            df_filtered_by_month['crecimiento_porcentual_ventas'].notna() &
            (df_filtered_by_month['crecimiento_porcentual_ventas'] != float('inf')) &
            (df_filtered_by_month['crecimiento_porcentual_ventas'] != float('-inf'))
        ].sort_values(by=['rank_crecimiento_ventas', 'rank_ingresos_totales']).head(10)

        if not df_high_growth_high_revenue.empty:
            st.dataframe(df_high_growth_high_revenue[[
                'nombre_producto',
                'nombre_categoria',
                'ingresos_totales',
                'crecimiento_porcentual_ventas',
                'rank_ingresos_totales',
                'rank_crecimiento_ventas'
            ]].style.format({
                'ingresos_totales': "${:,.2f}",
                'crecimiento_porcentual_ventas': "{:,.2f}%"
            }), use_container_width=True)
            st.markdown("""
            Esta tabla muestra productos que tienen un **buen ranking tanto en crecimiento como en ingresos** para el mes seleccionado.
            Un `rank` más bajo (ej. 1, 2, 3) indica una mejor posición.
            """)
        else:
            st.info("No hay productos con datos de crecimiento y/o ingresos para analizar en conjunto en este mes o categoría.")

        st.markdown("---")

        # --- PREGUNTA 6: ¿Cuál es el producto con alta tasa de crecimiento y alta intención (carrito)? ---
        st.subheader("6. 💡 Productos con Potencial: Alto Crecimiento y Alta Intención de Compra")
        st.markdown("Descubre productos que están ganando popularidad y que los usuarios están explorando activamente. Son fuertes candidatos para convertirse en los próximos éxitos de ventas.")

        df_high_growth_high_intencion = df_filtered_by_month[
            df_filtered_by_month['crecimiento_porcentual_ventas'].notna() &
            (df_filtered_by_month['crecimiento_porcentual_ventas'] != float('inf')) &
            (df_filtered_by_month['crecimiento_porcentual_ventas'] != float('-inf'))
        ].sort_values(by=['rank_crecimiento_ventas', 'rank_veces_agregado_carrito']).head(10)

        if not df_high_growth_high_intencion.empty:
            st.dataframe(df_high_growth_high_intencion[[
                'nombre_producto',
                'nombre_categoria',
                'crecimiento_porcentual_ventas',
                'cantidad_total_agregada_carrito',
                'rank_crecimiento_ventas',
                'rank_veces_agregado_carrito'
            ]].style.format({
                'crecimiento_porcentual_ventas': "{:,.2f}%",
                'cantidad_total_agregada_carrito': "{:,.0f}"
            }), use_container_width=True)
            st.markdown("""
            Esta tabla destaca productos que tienen un **alto crecimiento en ventas y una gran cantidad de veces que son agregados al carrito** en el mes seleccionado.
            Son candidatos ideales para estrategias de marketing o para monitorear su conversión a venta.
            """)
        else:
            st.info("No hay productos con datos de crecimiento y/o intención de compra para analizar en conjunto en este mes o categoría.")

else:
    st.error("❌ No hay datos disponibles para mostrar. Por favor, verifica tu conexión a la base de datos y asegúrate de que dbt se haya ejecutado correctamente para generar el modelo `rpt_analisis_productos_kpis`.")
    st.markdown("""
    **Pasos para solucionar:**
    1.  Asegúrate de que tus variables de entorno (`DB_HOST`, `DB_NAME`, etc.) estén configuradas correctamente.
    2.  Verifica que tu base de datos PostgreSQL esté en funcionamiento y sea accesible.
    3.  Ejecuta `dbt run --full-refresh` en tu terminal para reconstruir todos los modelos.
    4.  Si el problema persiste, revisa los logs de tu aplicación Streamlit para errores detallados.
    """)
st.markdown("---")