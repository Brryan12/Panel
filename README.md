# Ejecutar programa  
serve panel_app_simple.py --show --autoreload

### Instalar Git LFS  
git lfs install

### Trackear archivos grandes (ejemplo para GeoJSON)
git lfs track "*.geojson"
git lfs track "Data/*.geojson"

### Agregar el archivo .gitattributes
git add .gitattributes

