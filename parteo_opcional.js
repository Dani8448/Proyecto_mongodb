// ============================================================
//  PARTE OPCIONAL - DISEÑO RELACIONAL Y TRANSFORMACIÓN
//  A MODELO DOCUMENTAL EN MONGODB
// ============================================================

/*
  ESQUEMA RELACIONAL ORIGINAL
  ═══════════════════════════

  TABLA: desarrolladores
    - id_desarrollador (PK)
    - nombre
    - pais
    - año_fundacion

  TABLA: videojuegos
    - id_juego (PK)
    - titulo
    - año
    - precio
    - disponible
    - id_desarrollador (FK → desarrolladores)

  TABLA: generos
    - id_genero (PK)
    - nombre_genero

  TABLA: videojuego_genero  ← relación N:M
    - id_juego (FK → videojuegos)
    - id_genero (FK → generos)

  RELACIONES:
    - 1:N  → Un desarrollador puede tener muchos videojuegos
    - N:M  → Un videojuego puede tener varios géneros,
              y un género puede pertenecer a varios videojuegos

  TRANSFORMACIÓN A MONGODB
  ════════════════════════
  - La relación 1:N (desarrollador → videojuegos) se resuelve
    con un DOCUMENTO EMBEBIDO: campo "desarrollador" dentro de cada juego.
  - La relación N:M (videojuegos ↔ géneros) se resuelve
    con un ARRAY: campo "genero" dentro de cada juego.
  - Se añade una colección separada "desarrolladores" para
    demostrar el uso de REFERENCIAS.
*/

use videojuegosDB


// ────────────────────────────────────────────
// COLECCIÓN AUXILIAR: desarrolladores
// (Demuestra el uso de referencias)
// ────────────────────────────────────────────

db.desarrolladores.drop()

db.desarrolladores.insertMany([
  {
    "_id": ObjectId("771f1a2b3c4d5e6f78900001"),
    "nombre": "Nintendo",
    "pais": "Japón",
    "año_fundacion": 1889,
    "web": "https://www.nintendo.com"
  },
  {
    "_id": ObjectId("771f1a2b3c4d5e6f78900002"),
    "nombre": "Rockstar",
    "pais": "EEUU",
    "año_fundacion": 1998,
    "web": "https://www.rockstargames.com"
  },
  {
    "_id": ObjectId("771f1a2b3c4d5e6f78900003"),
    "nombre": "FromSoftware",
    "pais": "Japón",
    "año_fundacion": 1986,
    "web": "https://www.fromsoftware.jp"
  },
  {
    "_id": ObjectId("771f1a2b3c4d5e6f78900004"),
    "nombre": "CD Projekt",
    "pais": "Polonia",
    "año_fundacion": 1994,
    "web": "https://www.cdprojekt.com"
  },
  {
    "_id": ObjectId("771f1a2b3c4d5e6f78900005"),
    "nombre": "Ubisoft",
    "pais": "Francia",
    "año_fundacion": 1986,
    "web": "https://www.ubisoft.com"
  }
])

// ────────────────────────────────────────────
// COLECCIÓN: juegos_relacional
// (Modelo documental con embebido + array + referencia)
// ────────────────────────────────────────────

db.juegos_relacional.drop()

db.juegos_relacional.insertOne({
  "titulo": "The Legend of Zelda: Ocarina of Time",
  "año": 1998,
  // ARRAY → relación N:M con géneros (embebido)
  "genero": ["Action", "Adventure", "RPG"],
  "plataforma": ["Nintendo 64", "GameCube", "3DS"],
  "disponible": true,
  "fecha_lanzamiento": new Date("1998-11-21T00:00:00Z"),
  "precio": NumberDecimal("39.99"),
  // REFERENCIA → relación 1:N con desarrolladores
  "id_desarrollador": ObjectId("771f1a2b3c4d5e6f78900001"),
  // DOCUMENTO EMBEBIDO → datos detallados del desarrollador (desnormalización)
  "desarrollador": {
    "nombre": "Nintendo",
    "pais": "Japón",
    "año_fundacion": 1889
  },
  "valoraciones": { "nota": 99, "usuarios": [10, 10, 10, 10] },
  "ventas": { "europa": 6.0, "america": 8.0, "japon": 4.0 },
  "reseñas": {
    "criticos": { "metacritic": 99, "ign": 10 },
    "usuarios_detalle": [
      { "usuario": "user1", "puntuacion": 10 },
      { "usuario": "user2", "puntuacion": 10 }
    ]
  },
  "ultima_actualizacion": new Timestamp(1713446500, 1),
  "comentarios": null
})

db.juegos_relacional.insertMany([
  {
    "titulo": "Grand Theft Auto V",
    "año": 2013,
    "genero": ["Action", "Adventure", "Open World"],
    "plataforma": ["PS3", "Xbox 360", "PS4", "Xbox One", "PC", "PS5"],
    "disponible": true,
    "fecha_lanzamiento": new Date("2013-09-17T00:00:00Z"),
    "precio": NumberDecimal("29.99"),
    "id_desarrollador": ObjectId("771f1a2b3c4d5e6f78900002"),
    "desarrollador": { "nombre": "Rockstar", "pais": "EEUU", "año_fundacion": 1998 },
    "valoraciones": { "nota": 97, "usuarios": [10, 10, 9, 10] },
    "ventas": { "europa": 20.0, "america": 30.0, "japon": 2.0 },
    "reseñas": {
      "criticos": { "metacritic": 97, "ign": 10 },
      "usuarios_detalle": [
        { "usuario": "user1", "puntuacion": 10 },
        { "usuario": "user2", "puntuacion": 10 }
      ]
    },
    "ultima_actualizacion": new Timestamp(1713446501, 1),
    "comentarios": null
  },
  {
    "titulo": "Sekiro: Shadows Die Twice",
    "año": 2019,
    "genero": ["Action", "RPG"],
    "plataforma": ["PC", "PS4", "Xbox"],
    "disponible": true,
    "fecha_lanzamiento": new Date("2019-03-22T00:00:00Z"),
    "precio": NumberDecimal("59.99"),
    "id_desarrollador": ObjectId("771f1a2b3c4d5e6f78900003"),
    "desarrollador": { "nombre": "FromSoftware", "pais": "Japón", "año_fundacion": 1986 },
    "valoraciones": { "nota": 90, "usuarios": [10, 9, 9, 10] },
    "ventas": { "europa": 3.0, "america": 4.5, "japon": 1.5 },
    "reseñas": {
      "criticos": { "metacritic": 90, "ign": 9.5 },
      "usuarios_detalle": [
        { "usuario": "user1", "puntuacion": 10 },
        { "usuario": "user2", "puntuacion": 9 }
      ]
    },
    "ultima_actualizacion": new Timestamp(1713446502, 1),
    "comentarios": null
  },
  {
    "titulo": "The Witcher 3: Wild Hunt",
    "año": 2015,
    "genero": ["RPG", "Open World", "Adventure"],
    "plataforma": ["PC", "PS4", "Xbox", "Nintendo Switch"],
    "disponible": true,
    "fecha_lanzamiento": new Date("2015-05-19T00:00:00Z"),
    "precio": NumberDecimal("39.99"),
    "id_desarrollador": ObjectId("771f1a2b3c4d5e6f78900004"),
    "desarrollador": { "nombre": "CD Projekt", "pais": "Polonia", "año_fundacion": 1994 },
    "valoraciones": { "nota": 93, "usuarios": [10, 9, 10, 9] },
    "ventas": { "europa": 6.5, "america": 7.5, "japon": 1.0 },
    "reseñas": {
      "criticos": { "metacritic": 93, "ign": 9.3 },
      "usuarios_detalle": [
        { "usuario": "user1", "puntuacion": 10 },
        { "usuario": "user2", "puntuacion": 9 }
      ]
    },
    "ultima_actualizacion": new Timestamp(1713446503, 1),
    "comentarios": null
  },
  {
    "titulo": "Assassin's Creed Origins",
    "año": 2017,
    "genero": ["Action", "Adventure", "RPG"],
    "plataforma": ["PC", "PS4", "Xbox"],
    "disponible": true,
    "fecha_lanzamiento": new Date("2017-10-27T00:00:00Z"),
    "precio": NumberDecimal("39.99"),
    "id_desarrollador": ObjectId("771f1a2b3c4d5e6f78900005"),
    "desarrollador": { "nombre": "Ubisoft", "pais": "Francia", "año_fundacion": 1986 },
    "valoraciones": { "nota": 81, "usuarios": [8, 8, 9, 8] },
    "ventas": { "europa": 4.0, "america": 5.0, "japon": 0.4 },
    "reseñas": {
      "criticos": { "metacritic": 81, "ign": 8.2 },
      "usuarios_detalle": [
        { "usuario": "user1", "puntuacion": 8 },
        { "usuario": "user2", "puntuacion": 8 }
      ]
    },
    "ultima_actualizacion": new Timestamp(1713446504, 1),
    "comentarios": null
  }
])


// ────────────────────────────────────────────
// ELIMINACIONES
// ────────────────────────────────────────────

// deleteOne: eliminar el desarrollador con nombre "EA Sports" si existe
db.desarrolladores.deleteOne({ "nombre": "EA Sports" })

// deleteMany: eliminar juegos con nota inferior a 82
db.juegos_relacional.deleteMany({ "valoraciones.nota": { $lt: 82 } })


// ────────────────────────────────────────────
// ACTUALIZACIONES
// ────────────────────────────────────────────

// updateOne: actualizar el año de fundación de FromSoftware
db.desarrolladores.updateOne(
  { "nombre": "FromSoftware" },
  { $set: { "año_fundacion": 1986 } }
)

// updateMany: añadir campo "destacado" a todos los juegos con nota >= 93
db.juegos_relacional.updateMany(
  { "valoraciones.nota": { $gte: 93 } },
  { $set: { "destacado": true } }
)

// replaceOne: reemplazar el documento de Ubisoft en desarrolladores
db.desarrolladores.replaceOne(
  { "nombre": "Ubisoft" },
  {
    "nombre": "Ubisoft",
    "pais": "Francia",
    "año_fundacion": 1986,
    "web": "https://www.ubisoft.com",
    "empleados": 20000,
    "cotiza_bolsa": true
  }
)


// ════════════════════════════════════════════
// CONSULTAS SOBRE juegos_relacional
// ════════════════════════════════════════════

// ── SIMPLES ──

// 1. Juegos lanzados en 2015
db.juegos_relacional.find(
  { "año": 2015 },
  { "titulo": 1, "año": 1, "_id": 0 }
)

// 2. Juegos disponibles con precio menor a 40€
db.juegos_relacional.find(
  { "disponible": true, "precio": { $lt: NumberDecimal("40.00") } },
  { "titulo": 1, "precio": 1, "_id": 0 }
).sort({ "precio": 1 })

// 3. Top 3 juegos por nota de Metacritic
db.juegos_relacional.find(
  {},
  { "titulo": 1, "reseñas.criticos.metacritic": 1, "_id": 0 }
).sort({ "reseñas.criticos.metacritic": -1 }).limit(3)

// 4. Juegos marcados como destacados
db.juegos_relacional.find(
  { "destacado": true },
  { "titulo": 1, "valoraciones.nota": 1, "_id": 0 }
)

// 5. Juegos entre 2010 y 2020 ordenados por año descendente
db.juegos_relacional.find(
  { "año": { $gte: 2010, $lte: 2020 } },
  { "titulo": 1, "año": 1, "_id": 0 }
).sort({ "año": -1 })


// ── ARRAYS ──

// 1. Juegos del género "RPG"
db.juegos_relacional.find(
  { "genero": { $in: ["RPG"] } },
  { "titulo": 1, "genero": 1, "_id": 0 }
)

// 2. Juegos disponibles en PS4 y PC simultáneamente
db.juegos_relacional.find(
  { "plataforma": { $all: ["PS4", "PC"] } },
  { "titulo": 1, "plataforma": 1, "_id": 0 }
)

// 3. Juegos con más de dos plataformas
db.juegos_relacional.find(
  { "plataforma.2": { $exists: true } },
  { "titulo": 1, "plataforma": 1, "_id": 0 }
)


// ── DOCUMENTOS EMBEBIDOS ──

// 1. Juegos de desarrolladores de Japón
db.juegos_relacional.find(
  { "desarrollador.pais": "Japón" },
  { "titulo": 1, "desarrollador": 1, "_id": 0 }
)

// 2. Juegos con ventas en Europa superiores a 5 millones
db.juegos_relacional.find(
  { "ventas.europa": { $gt: 5 } },
  { "titulo": 1, "ventas.europa": 1, "_id": 0 }
).sort({ "ventas.europa": -1 })

// 3. Juegos con nota IGN mayor o igual a 9.5
db.juegos_relacional.find(
  { "reseñas.criticos.ign": { $gte: 9.5 } },
  { "titulo": 1, "reseñas.criticos": 1, "_id": 0 }
)


// ── AGREGACIÓN ──

// Ventas totales globales y nota media por país del desarrollador
db.juegos_relacional.aggregate([
  {
    $group: {
      _id: "$desarrollador.pais",
      total_juegos: { $sum: 1 },
      nota_media: { $avg: "$valoraciones.nota" },
      ventas_totales: {
        $sum: {
          $add: ["$ventas.europa", "$ventas.america", "$ventas.japon"]
        }
      }
    }
  },
  { $sort: { ventas_totales: -1 } },
  {
    $project: {
      pais: "$_id",
      total_juegos: 1,
      nota_media: { $round: ["$nota_media", 1] },
      ventas_totales: { $round: ["$ventas_totales", 1] },
      _id: 0
    }
  }
])