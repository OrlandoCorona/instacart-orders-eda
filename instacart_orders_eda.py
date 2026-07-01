"""
Análisis exploratorio de los pedidos de Instacart.

Versión en script del notebook `Notebook/instacart_orders_eda.ipynb`: carga las
cinco tablas de pedidos, elimina duplicados y valores ausentes, y analiza los
patrones de compra (horarios, días, productos más pedidos y reordenados).
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# --- Carga de datos ---
orders = pd.read_csv('datasets/instacart_orders.csv', sep=';')
products = pd.read_csv('datasets/products.csv', sep=';')
aisles = pd.read_csv('datasets/aisles.csv', sep=';')
departments = pd.read_csv('datasets/departments.csv', sep=';')
order_products = pd.read_csv('datasets/order_products.csv', sep=';')
# leer conjuntos de datos en los DataFrames

# mostrar información del DataFrame
print("Información de orders:")
orders.info(show_counts=True)

# mostrar información del DataFrame
print("\nInformación de products:")
products.info(show_counts=True)

# mostrar información del DataFrame
print("\nInformación de aisles:")
aisles.info(show_counts=True)

# mostrar información del DataFrame
print("\nInformación de departments:")
departments.info(show_counts=True)

# mostrar información del DataFrame
print("\nInformación de order_products:")
order_products.info(show_counts=True)

# --- `orders` data frame ---
# Revisa si hay pedidos duplicados
print("Filas duplicadas en orders:", orders.duplicated().sum())

# Basándote en tus hallazgos,
# Verifica todos los pedidos que se hicieron el miércoles a las 2:00 a.m.
wed_2am_orders = orders[(orders['order_dow'] == 3) & (orders['order_hour_of_day'] == 2)]
print("\nPedidos el miércoles a las 2:00 a.m.:")
print(wed_2am_orders)

# Elimina los pedidos duplicados
orders = orders.drop_duplicates()

# Vuelve a verificar si hay filas duplicadas
print("\nFilas duplicadas después de eliminación:", orders.duplicated().sum())

# Vuelve a verificar únicamente si hay IDs duplicados de pedidos
print("IDs de pedidos duplicados:", orders['order_id'].duplicated().sum())

# --- `products` data frame ---
# Verifica si hay filas totalmente duplicadas
print("Filas duplicadas en products:", products.duplicated().sum())

# Revisa únicamente si hay ID de productos duplicados
print("IDs de productos duplicados:", products['product_id'].duplicated().sum())

# Revisa únicamente si hay nombres duplicados de productos (convierte los nombres a letras mayúsculas para compararlos mejor)
products['product_name_upper'] = products['product_name'].str.upper()
print("Nombres de productos duplicados:", products['product_name_upper'].duplicated().sum())

# Revisa si hay nombres duplicados de productos no faltantes
non_missing_products = products[products['product_name'].notnull()]
print("Nombres duplicados de productos no faltantes:", non_missing_products['product_name_upper'].duplicated().sum())
products = products.drop(columns='product_name_upper')

# --- `departments` data frame ---
# Revisa si hay filas totalmente duplicadas
print("Filas duplicadas en departments:", departments.duplicated().sum())

# Revisa únicamente si hay IDs duplicadas de departamentos
print("IDs de departamentos duplicados:", departments['department_id'].duplicated().sum())

# --- `aisles` data frame ---
# Revisa si hay filas totalmente duplicadas
print("Filas duplicadas en aisles:", aisles.duplicated().sum())

# Revisa únicamente si hay IDs duplicadas de pasillos
print("IDs de pasillos duplicados:", aisles['aisle_id'].duplicated().sum())

# --- `order_products` data frame ---
# Revisa si hay filas totalmente duplicadas
print("Filas duplicadas en order_products:", order_products.duplicated().sum())

# Vuelve a verificar si hay cualquier otro duplicado engañoso
duplicates_order_product = order_products.duplicated(subset=['order_id', 'product_id']).sum()
print("Duplicados en order_id y product_id:", duplicates_order_product)

# --- `products` data frame ---
# Encuentra los valores ausentes en la columna 'product_name'
print("Valores ausentes en product_name:", products['product_name'].isnull().sum())

#  ¿Todos los nombres de productos ausentes están relacionados con el pasillo con ID 100?
missing_products = products[products['product_name'].isnull()]
print("Productos ausentes con aisle_id == 100:", (missing_products['aisle_id'] == 100).all())

# ¿Todos los nombres de productos ausentes están relacionados con el departamento con ID 21?
print("Productos ausentes con department_id == 21:", (missing_products['department_id'] == 21).all())

# Usa las tablas department y aisle para revisar los datos del pasillo con ID 100 y el departamento con ID 21.
aisle_100 = aisles[aisles['aisle_id'] == 100]
department_21 = departments[departments['department_id'] == 21]
print("\nPasillo con ID 100:")
print(aisle_100)
print("\nDepartamento con ID 21:")
print(department_21)

# Completa los nombres de productos ausentes con 'Unknown'
products['product_name'] = products['product_name'].fillna('Unknown')
print("\nValores ausentes en product_name después de rellenar:", products['product_name'].isnull().sum())

# --- `orders` data frame ---
# Encuentra los valores ausentes
print("Valores ausentes en orders:")
print(orders.isnull().sum())

# ¿Hay algún valor ausente que no sea el primer pedido del cliente?
missing_days = orders[orders['days_since_prior_order'].isnull()]
print("Valores ausentes en days_since_prior_order donde order_number != 1:", (missing_days['order_number'] != 1).sum())
orders['days_since_prior_order'] = orders['days_since_prior_order'].fillna(0).astype('Int64')
print("\nValores ausentes en orders después de rellenar:")
print(orders.isnull().sum())

# --- `order_products` data frame ---
# Encuentra los valores ausentes
print("Valores ausentes en order_products:")
print(order_products.isnull().sum())

# ¿Cuáles son los valores mínimos y máximos en esta columna?
print("Mínimo en add_to_cart_order:", order_products['add_to_cart_order'].min())
print("Máximo en add_to_cart_order:", order_products['add_to_cart_order'].max())

# Guarda todas las IDs de pedidos que tengan un valor ausente en 'add_to_cart_order'
missing_cart_orders = order_products[order_products['add_to_cart_order'].isnull()]['order_id'].unique()
print("Número de pedidos con add_to_cart_order ausente:", len(missing_cart_orders))

# ¿Todos los pedidos con valores ausentes tienen más de 64 productos?
# Agrupa todos los pedidos con datos ausentes por su ID de pedido.
# Cuenta el número de 'product_id' en cada pedido y revisa el valor mínimo del conteo.
order_sizes = order_products[order_products['order_id'].isin(missing_cart_orders)].groupby('order_id').size()
print("Tamaño mínimo de pedidos con add_to_cart_order ausente:", order_sizes.min())

# Remplaza los valores ausentes en la columna 'add_to_cart? con 999 y convierte la columna al tipo entero.
order_products['add_to_cart_order'] = order_products['add_to_cart_order'].fillna(999).astype('int16')
print("\nValores ausentes en order_products después de rellenar:")
print(order_products.isnull().sum())

# --- [A1] Verifica que los valores sean sensibles ---
print("Rango de order_hour_of_day:", orders['order_hour_of_day'].min(), "-", orders['order_hour_of_day'].max())

print("Rango de order_dow:", orders['order_dow'].min(), "-", orders['order_dow'].max())

# --- [A2] Para cada hora del día, ¿cuántas personas hacen órdenes? ---
hourly_orders = orders['order_hour_of_day'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
plt.bar(hourly_orders.index, hourly_orders.values)
plt.title('Número de Pedidos por Hora del Día')
plt.xlabel('Hora del Día')
plt.ylabel('Número de Pedidos')
plt.xticks(range(24))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# --- [A3] ¿Qué día de la semana compran víveres las personas? ---
dow_orders = orders['order_dow'].value_counts().sort_index()
dow_labels = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']

plt.figure(figsize=(10, 6))
plt.bar(dow_orders.index, dow_orders.values)
plt.title('Número de Pedidos por Día de la Semana')
plt.xlabel('Día de la Semana')
plt.ylabel('Número de Pedidos')
plt.xticks(range(7), dow_labels, rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# --- [A4] ¿Cuánto tiempo esperan las personas hasta hacer otro pedido? Come ---
days_since_prior = orders[orders['days_since_prior_order'] != 0]['days_since_prior_order']

plt.figure(figsize=(10, 6))
plt.hist(days_since_prior, bins=30, edgecolor='black')
plt.title('Distribución del Tiempo Hasta el Próximo Pedido')
plt.xlabel('Días Desde el Pedido Anterior')
plt.ylabel('Frecuencia')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

print("Minimo días:", days_since_prior.min())
print("Maximo días:", days_since_prior.max())

# --- [B1] Diferencia entre miércoles y sábados para  `'order_hour_of_day'`. ---
wed_orders = orders[orders['order_dow'] == 3]['order_hour_of_day']

sat_orders = orders[orders['order_dow'] == 6]['order_hour_of_day']

plt.figure(figsize=(10, 6))
plt.hist(wed_orders, bins=24, alpha=0.5, label='Miércoles', edgecolor='black')
plt.hist(sat_orders, bins=24, alpha=0.5, label='Sábado', edgecolor='black')
plt.title('Distribución de Pedidos por Hora: Miércoles vs Sábado')
plt.xlabel('Hora del Día')
plt.ylabel('Frecuencia')
plt.legend()
plt.xticks(range(24))
plt.grid(axis='y', linestyle='--', alpha=0.7)

plt.show()

# --- [B2] ¿Cuál es la distribución para el número de pedidos por cliente? ---
orders_per_user = orders.groupby('user_id')['order_id'].count()

plt.figure(figsize=(10, 6))
plt.hist(orders_per_user, bins=range(1, orders_per_user.max() + 2), edgecolor='black')
plt.title('Distribución del Número de Pedidos por Cliente')
plt.xlabel('Número de Pedidos')
plt.ylabel('Número de Clientes')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# --- [B3] ¿Cuáles son los 20 productos más populares (muestra su ID y nombr ---
product_counts = order_products.groupby('product_id').size().reset_index(name='count')
product_counts = product_counts.merge(products[['product_id', 'product_name']], on='product_id')
top_20_products = product_counts.sort_values('count', ascending=False).head(20)

print(top_20_products[['product_id', 'product_name', 'count']])

plt.figure(figsize=(12, 8))
sns.barplot(data=top_20_products, x='count', y='product_name')
plt.title('20 Principales Productos Pedidos')
plt.xlabel('Número de Pedidos')
plt.ylabel('Nombre del Producto')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

# --- [C1] ¿Cuántos artículos compran normalmente las personas en un pedido? ---
items_per_order = order_products.groupby('order_id').size()

plt.figure(figsize=(10, 6))
plt.hist(items_per_order, bins=range(1, items_per_order.max() + 2), edgecolor='black')
plt.title('Distribución del Número de Artículos por Pedido')
plt.xlabel('Número de Artículos')
plt.ylabel('Número de Pedidos')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

print("Promedio de artículos por pedido:", items_per_order.mean())
print("Mediana de artículos por pedido:", items_per_order.median())

# --- [C2] ¿Cuáles son los 20 principales artículos que vuelven a pedirse co ---
reordered_products = order_products[order_products['reordered'] == 1]
reordered_counts = reordered_products.groupby('product_id').size().reset_index(name='reordered_count')
reordered_counts = reordered_counts.merge(products[['product_id', 'product_name']], on='product_id')
top_20_reordered = reordered_counts.sort_values('reordered_count', ascending=False).head(20)

print(top_20_reordered[['product_id', 'product_name', 'reordered_count']])

plt.figure(figsize=(12, 8))
sns.barplot(data=top_20_reordered, x='reordered_count', y='product_name')
plt.title('20 Principales Productos Reordenados')
plt.xlabel('Número de Reordenaciones')
plt.ylabel('Nombre del Producto')
plt.grid(axis='x', linestyle='--', alpha=0.7)

plt.show()

# --- [C3] Para cada producto, ¿cuál es la proporción de las veces que se pi ---
product_reorder = order_products.groupby('product_id').agg(
    total_orders=('reordered', 'count'),
    reordered=('reordered', 'sum')
).reset_index()
product_reorder['reorder_ratio'] = product_reorder['reordered'] / product_reorder['total_orders']
product_reorder = product_reorder.merge(products[['product_id', 'product_name']], on='product_id')

print(product_reorder[['product_id', 'product_name', 'reorder_ratio']].head())

# --- [C4] Para cada cliente, ¿qué proporción de sus productos ya los había  ---
user_orders = orders[['order_id', 'user_id']].merge(order_products, on='order_id')
user_reorder = user_orders.groupby('user_id').agg(
    total_items=('reordered', 'count'),
    reordered_items=('reordered', 'sum')
).reset_index()
user_reorder['reorder_ratio'] = user_reorder['reordered_items'] / user_reorder['total_items']

plt.figure(figsize=(10, 6))
plt.hist(user_reorder['reorder_ratio'], bins=30, edgecolor='black')
plt.title('Distribución de la Proporción de Reordenación por Cliente')
plt.xlabel('Proporción de Reordenación')
plt.ylabel('Número de Clientes')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# --- [C5] ¿Cuáles son los 20 principales artículos que las personas ponen p ---
first_added = order_products[order_products['add_to_cart_order'] == 1]
first_added_counts = first_added.groupby('product_id').size().reset_index(name='first_added_count')
first_added_counts = first_added_counts.merge(products[['product_id', 'product_name']], on='product_id')
top_20_first_added = first_added_counts.sort_values('first_added_count', ascending=False).head(20)

print(top_20_first_added[['product_id', 'product_name', 'first_added_count']])

plt.figure(figsize=(12, 8))
sns.barplot(data=top_20_first_added, x='first_added_count', y='product_name')
plt.title('20 Principales Productos Añadidos Primero al Carrito')
plt.xlabel('Número de Veces Añadido Primero')
plt.ylabel('Nombre del Producto')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

