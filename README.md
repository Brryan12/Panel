# Cafe Map Visualizer

## Ejecutar programa

### Opción 1: Con virtual environment activado
```bash
# Activar entorno virtual
source .venv/bin/activate

# Ejecutar aplicación
python -m panel serve panel_app_simple.py --show --autoreload
```

### Opción 2: Comando simplificado (si panel está en PATH)
```bash
panel serve panel_app_simple.py --show --autoreload
```

## Acceder a la aplicación
- La aplicación se ejecuta en: `http://localhost:5006/panel_app_simple`
- Se abrirá automáticamente en tu navegador con `--show`

### Instalar Git LFS
- git lfs install

### Trackear archivos grandes (ejemplo para GeoJSON)
- git lfs track "*.geojson"
- git lfs track "Data/*.geojson"

### Agregar el archivo .gitattributes
- git add .gitattributes

