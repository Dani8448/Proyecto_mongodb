#  Práctica MongoDB — Base de Datos de Videojuegos
 
Proyecto de práctica sobre MongoDB con una colección de videojuegos.  
Dataset original basado en [CORGIS](https://corgis-edu.github.io/corgis/datasets/json/video_games/video_games.json), adaptado y ampliado para cubrir todos los tipos de datos y operaciones requeridas.
 
---

```
 
---
 
##  Parte 1 — Creación y gestión de la colección
 
### Tipos de datos utilizados
 
| Tipo MongoDB   | Campo(s)                              |
|----------------|---------------------------------------|
| `String`       | `titulo`, `desarrollador.nombre`, `desarrollador.pais` |
| `Number`       | `año`, `valoraciones.nota`, ventas    |
| `Array`        | `genero`, `plataforma`, `valoraciones.usuarios` |
| `Embedded doc` | `desarrollador`, `ventas`, `reseñas`  |
| `Boolean`      | `disponible`                          |
| `Date`         | `fecha_lanzamiento`                   |
| `Decimal128`   | `precio`                              |
| `Timestamp`    | `ultima_actualizacion`                |
| `Null`         | `comentarios`                         |
| `ObjectId`     | `_id`                                 |
 
### Importación
 
```bash
mongoimport --db videojuegosDB --collection juegos --file data/videojuegos.json --jsonArray
```
 
### Operaciones implementadas 
 
**Inserción**
- `insertOne()` — inserta un único documento
- `insertMany()` — inserta varios documentos
**Eliminación**
- `deleteOne()` — elimina un documento concreto
- `deleteMany()` — elimina todos los documentos que cumplen una condición
**Actualización**
- `updateOne()` — modifica un único documento
- `updateMany()` — modifica varios documentos
- `replaceOne()` — reemplaza completamente un documento
Y las consultas simples.
---
 
##  Parte 2 — Programa Python
 
### Requisitos
 
```bash
pip install pymongo
```
 
Asegúrate de tener MongoDB corriendo en `localhost:27017` con la colección importada.
 
### Ejecución
 
```bash
cd python
python menu.py
```
 
### Menú interactivo
 
```
    GESTIÓN DE VIDEOJUEGOS - MongoDB
  ────────────────────────────────────────────────────────────
  1. Inserción de documentos
  2. Eliminación de documentos
  3. Actualización de documentos
  4. Consultas
  0. Salir
```
 
**Inserción:** `insertOne` (Hollow Knight) y `insertMany` (Stardew Valley, Among Us)  
**Eliminación:** por título (`deleteOne`) o todos los no disponibles (`deleteMany`)  
**Actualización:** precio (`updateOne`), disponibilidad por desarrollador (`updateMany`), reemplazo completo (`replaceOne`)  
**Consultas:** 13 consultas interactivas que cubren simples, arrays, documentos embebidos y agregación
 
---
 
##  Parte Opcional — Esquema relacional y transformación
 
Archivo: `parteo_opcional.js`
 
### Esquema relacional diseñado
 
```
desarrolladores (1) ──── (N) videojuegos
videojuegos    (N) ──── (M) generos
```
 
### Transformación a MongoDB
 
| Relación | Estrategia MongoDB          |
|----------|-----------------------------|
| 1:N (desarrollador → juegos) | **Documento embebido** `desarrollador` dentro de cada juego |
| N:M (juegos ↔ géneros)       | **Array** `genero` dentro de cada juego |
| Referencia explícita         | Campo `id_desarrollador` (ObjectId) apuntando a colección `desarrolladores` |
 
### Operaciones incluidas
 
- **Inserción:** `insertOne`, `insertMany` en colecciones `desarrolladores` y `juegos_relacional`
- **Eliminación:** `deleteOne`, `deleteMany`
- **Actualización:** `updateOne`, `updateMany`, `replaceOne`
- **Consultas simples:** 5 consultas con proyección, `sort` y `limit`
- **Consultas arrays:** 3 consultas con `$in`, `$all` y `$exists`
- **Consultas embebidos:** 3 consultas sobre `desarrollador`, `ventas` y `reseñas`
- **Agregación:** ventas totales y nota media agrupadas por país del desarrollador
---
 
## Tecnologías
 
- **MongoDB** 6+
- **Python** 3.8+ con `pymongo`
- Dataset original: [CORGIS Video Games](https://corgis-edu.github.io/corgis/datasets/json/video_games/)
 
