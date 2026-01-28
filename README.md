# Instacart Orders EDA

Análisis exploratorio del comportamiento de compra de los clientes de
**Instacart**, una plataforma de pedidos de víveres a domicilio. El objetivo es
limpiar un conjunto de datos real y extraer patrones de consumo útiles para el
negocio.

## Objetivo del negocio

Entender cómo y cuándo compran los clientes para apoyar decisiones de
operación, inventario y marketing:

> ¿A qué horas y días se concentran los pedidos? ¿Qué productos son los más
> populares y los que más se reordenan?

## Tecnologías

- Python 3.11
- pandas — limpieza y agregación de datos
- Matplotlib / Seaborn — visualización
- Jupyter Notebook
- Git LFS — versionado de los CSV grandes

## Dataset

Cinco tablas de pedidos (separador `;`): pedidos, productos por pedido,
catálogo de productos, pasillos y departamentos. Detalle y notas sobre Git LFS
en [`datasets/README.md`](datasets/README.md).

## Estructura del proyecto

```
instacart-orders-eda/
├── Notebook/
│   └── instacart_orders_eda.ipynb   # análisis exploratorio
├── datasets/                        # CSV de pedidos (Git LFS)
├── instacart_orders_eda.py          # análisis en formato script
├── requirements.txt
├── .gitattributes                   # configuración de Git LFS
├── LICENSE
└── README.md
```

## Proceso de análisis

1. **Carga** de las cinco tablas.
2. **Preprocesamiento:** detección y eliminación de duplicados; tratamiento de
   valores ausentes (productos sin nombre, primeros pedidos sin historial,
   `add_to_cart_order` ausente).
3. **Verificación** de rangos sensatos (hora del día, día de la semana).
4. **Análisis de comportamiento:** pedidos por hora y por día, tiempo entre
   pedidos, número de pedidos por cliente.
5. **Productos:** los 20 más populares, los más reordenados, la proporción de
   reordenación y los productos que se añaden primero al carrito.

## Resultados

- Los pedidos se concentran entre las **10:00 y las 16:00**.
- Los días con más pedidos son **domingo y lunes**.
- Los productos básicos (frutas, lácteos, verduras) dominan tanto en
  popularidad como en reordenación.

## Conclusiones

El comportamiento de compra es muy regular: alta concentración en horas y días
específicos y una fuerte recurrencia de productos básicos. Esto favorece
estrategias de reabastecimiento y recomendaciones de "volver a comprar".

## Cómo ejecutar

```bash
git clone https://github.com/OrlandoCorona/instacart-orders-eda.git
cd instacart-orders-eda
git lfs install && git lfs pull        # descarga los CSV grandes

python -m venv venv
source venv/bin/activate                # En Windows: venv\Scripts\activate
pip install -r requirements.txt

jupyter notebook Notebook/instacart_orders_eda.ipynb
```

> Para reproducir el notebook completo necesitas además `instacart_orders.csv`
> en `datasets/` (ver `datasets/README.md`).

## Trabajo futuro

- Segmentar clientes por frecuencia y tamaño de pedido.
- Construir un sistema de recomendación de "siguiente producto".
- Visualizar la cesta de la compra (análisis de afinidad de productos).
