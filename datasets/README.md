# Datasets

Datos de pedidos de la plataforma de compras Instacart. Los archivos usan
**`;`** como separador.

| Archivo | Descripción | Tamaño |
|---|---|---|
| `instacart_orders.csv` | Pedidos (usuario, hora, día, días desde el pedido previo). | *no incluido* |
| `order_products.csv` | Productos de cada pedido (Git LFS). | ~86 MB |
| `products.csv` | Catálogo de productos (Git LFS). | ~2 MB |
| `aisles.csv` | Pasillos. | pequeño |
| `departments.csv` | Departamentos. | pequeño |

> **Git LFS:** los CSV se versionan con [Git LFS](https://git-lfs.com).
> Tras clonar, ejecuta `git lfs install` y `git lfs pull` para descargar los
> archivos grandes.
>
> **Nota:** `instacart_orders.csv` no se incluye por su tamaño/licencia.
> Colócalo en esta carpeta para reproducir el notebook completo.
