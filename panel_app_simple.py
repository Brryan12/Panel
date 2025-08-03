import os
from pathlib import Path

# IMPORTANTE: Configurar variables de entorno ANTES de importar geopandas
os.environ['OGR_GEOJSON_MAX_OBJ_SIZE'] = '0'  # Remover límite de tamaño
os.environ['GDAL_DISABLE_READDIR_ON_OPEN'] = 'EMPTY_DIR'
os.environ['CPL_DEBUG'] = 'OFF'  # Desactivar debug de GDAL
os.environ['GDAL_MAX_DATASET_POOL_SIZE'] = '1000'

import panel as pn
import geopandas as gpd
import folium
from folium import plugins

# Configuración más simple de Panel
pn.extension()

# Configuración del título
APP_TITLE = "Cafe Map Visualizer"
APP_SUBTITLE = "Dashboard con Panel y Folium"

def load_geojson_data():
    """Carga los datos GeoJSON"""
    geojson_path = 'Data/cober_arborea_2021_dissolve_4326.geojson'
    try:
        print(f"Cargando archivo: {geojson_path}")
        if os.path.exists(geojson_path):
            gdf = gpd.read_file(geojson_path)
            print(f"Datos cargados exitosamente: {len(gdf)} geometrías")
            return gdf
        else:
            print(f"Archivo no encontrado: {geojson_path}")
            return None
    except Exception as e:
        print(f"Error cargando datos: {e}")
        return None

def create_folium_map(gdf):
    """Crea un mapa usando Folium"""
    if gdf is None:
        return None
    
    try:
        # Calcular el centro del mapa
        bounds = gdf.total_bounds
        center_lat = (bounds[1] + bounds[3]) / 2
        center_lon = (bounds[0] + bounds[2]) / 2
        
        # Crear mapa base
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=8,
            tiles='CartoDB positron'
        )
        
        # Agregar las geometrías al mapa
        folium.GeoJson(
            gdf.to_json(),
            style_function=lambda feature: {
                'fillColor': 'lightblue',
                'color': 'blue',
                'weight': 1,
                'fillOpacity': 1,
            }
        ).add_to(m)
        
        return m
    except Exception as e:
        print(f"Error creando mapa: {e}")
        return None

def create_info_text(gdf):
    """Crea el texto informativo"""
    if gdf is not None:
        # Calcular área
        gdf_projected = gdf.to_crs('EPSG:5367')
        area_km2 = gdf_projected.geometry.area.sum() / 1_000_000
        
        info_text = f"""
        # Información del Dataset
        
        - **Número de geometrías:** {len(gdf)}
        - **Sistema de coordenadas:** {gdf.crs}
        - **Área total:** {area_km2:.2f} km²
        - **Archivo:** cober_arborea_2021_dissolve_4326.geojson
        """
    else:
        info_text = "# Error: No hay datos disponibles"
    
    return info_text

def create_dashboard():
    """Crea el dashboard completo"""
    print("Inicializando dashboard...")
    
    # Cargar datos
    gdf = load_geojson_data()
    
    # Crear componentes
    if gdf is not None:
        # Crear mapa
        folium_map = create_folium_map(gdf)
        if folium_map is not None:
            # Convertir el mapa de Folium a HTML
            map_html = folium_map._repr_html_()
            map_pane = pn.pane.HTML(map_html, width=800, height=600)
        else:
            map_pane = pn.pane.HTML("<h3>Error: No se pudo crear el mapa</h3>")
    else:
        map_pane = pn.pane.HTML("<h3>Error: No se pudieron cargar los datos</h3>")
    
    # Crear panel de información
    info_text = create_info_text(gdf)
    info_pane = pn.pane.Markdown(info_text)
    
    # Header
    header = pn.pane.HTML(f"""
    <div style="background-color: #2F4F4F; padding: 20px; color: white; text-align: center;">
        <h1>{APP_TITLE}</h1>
        <h3>{APP_SUBTITLE}</h3>
    </div>
    """, sizing_mode='stretch_width')
    
    # Layout principal
    layout = pn.Column(
        header,
        pn.Row(
            pn.Column(info_pane, width=300),
            map_pane,
            sizing_mode='stretch_width'
        ),
        sizing_mode='stretch_width'
    )
    
    return layout

# Crear la aplicación
app = create_dashboard()
app.servable()
