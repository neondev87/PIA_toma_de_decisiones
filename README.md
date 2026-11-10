# PIA - Análisis de ventas con pandas

Proyecto integrador de la materia **Análisis de datos para la toma de decisiones** (UANL - FACPYA), Equipo 10.

Analizamos las ventas de unas tiendas minoristas (varias sucursales y productos) usando pandas. Sacamos totales por sucursal y por producto, cómo se comportan las ventas en el tiempo y algunas gráficas para apoyar las conclusiones.

## Archivos

- `DatosPIA.csv`: la base de datos de ventas (fecha, sucursal, producto, cantidad, precio y total).
- `analisis_pia.py`: el script con todo el análisis.

## Cómo correrlo

```
pip install pandas matplotlib
python analisis_pia.py
```

Al correrlo se imprimen los resultados en consola, se guardan en `resultados.txt` y las gráficas quedan en la carpeta `capturas/`.
