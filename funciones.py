from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from bson import ObjectId, Decimal128
from datetime import datetime
import sys
 
 
# ──────────────────────────────────────────────
#  CONEXIÓN A MONGODB
# ──────────────────────────────────────────────
 
def conectar():
    """Establece la conexión con MongoDB y retorna la colección."""
    try:
        cliente = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=3000)
        cliente.admin.command("ping")
        db = cliente["videojuegosDB"]
        coleccion = db["juegos"]
        print("Conexión a MongoDB establecida correctamente.\n")
        return coleccion
    except ConnectionFailure:
        print(" Error: No se puede conectar a MongoDB.")
        sys.exit(1)
 
 

# ──────────────────────────────────────────────
#  UTILIDADES
# ──────────────────────────────────────────────
 
def separador(titulo=""):
    ancho = 60
    if titulo:
        print(f"\n{'─' * 5} {titulo} {'─' * (ancho - len(titulo) - 7)}")
    else:
        print("─" * ancho)
 
 
def imprimir_juego(juego, campos=None):
    """Imprime un documento de forma legible."""
    if campos:
        for campo in campos:
            partes = campo.split(".")
            valor = juego
            try:
                for p in partes:
                    valor = valor[p]
                print(f"  {campo}: {valor}")
            except (KeyError, TypeError):
                pass
    else:
        print(f"  Título     : {juego.get('titulo', 'N/A')}")
        print(f"  Año        : {juego.get('año', 'N/A')}")
        print(f"  Género     : {', '.join(juego.get('genero', []))}")
        print(f"  Plataforma : {', '.join(juego.get('plataforma', []))}")
        print(f"  Precio     : {juego.get('precio', 'N/A')} €")
        print(f"  Disponible : {'Sí' if juego.get('disponible') else 'No'}")
        desarrollador = juego.get('desarrollador', {})
        print(f"  Desarrollador: {desarrollador.get('nombre', 'N/A')} ({desarrollador.get('pais', 'N/A')})")
        valoraciones = juego.get('valoraciones', {})
        print(f"  Nota       : {valoraciones.get('nota', 'N/A')}")
    print()

 
# ──────────────────────────────────────────────
# MENÚ INSERCIÓN
# ──────────────────────────────────────────────

def menu_insercion(col):
    separador("INSERCIÓN DE DOCUMENTOS")
    print("1. Insertar un juego (manual)")
    print("2. Insertar varios juegos (manual)")
    print("0. Volver")

    opcion = input("\nElige una opción: ").strip()

    if opcion == "1":
        insertar_uno(col)
    elif opcion == "2":
        insertar_varios(col)
    elif opcion == "0":
        return
    else:
        print("Opción no válida")


# ──────────────────────────────────────────────
# INSERTAR UNO 
# ──────────────────────────────────────────────

def insertar_uno(col):
    print("\n--- INSERTAR JUEGO ---")

    titulo = input("Título: ").strip()
    año = int(input("Año: ").strip())

    generos = input("Géneros (coma): ").split(",")
    generos = [g.strip() for g in generos]

    plataformas = input("Plataformas (coma): ").split(",")
    plataformas = [p.strip() for p in plataformas]

    disponible = input("¿Disponible? (s/n): ").lower() == "s"

    fecha = datetime.strptime(
        input("Fecha (YYYY-MM-DD): ").strip(),
        "%Y-%m-%d"
    )

    precio = Decimal128(input("Precio: ").strip())

    dev_nombre = input("Desarrollador nombre: ")
    dev_pais = input("Desarrollador país: ")

    nota = int(input("Nota general: "))

    usuarios = input("Valoraciones usuarios (ej 10,9,8): ").split(",")
    usuarios = [int(u.strip()) for u in usuarios]

    ventas_eu = float(input("Ventas Europa: "))
    ventas_am = float(input("Ventas América: "))
    ventas_jp = float(input("Ventas Japón: "))

    metacritic = int(input("Metacritic: "))
    ign = float(input("IGN: "))

    documento = {
        "titulo": titulo,
        "año": año,
        "genero": generos,
        "plataforma": plataformas,
        "disponible": disponible,
        "fecha_lanzamiento": fecha,
        "precio": precio,
        "desarrollador": {
            "nombre": dev_nombre,
            "pais": dev_pais
        },
        "valoraciones": {
            "nota": nota,
            "usuarios": usuarios
        },
        "ventas": {
            "europa": ventas_eu,
            "america": ventas_am,
            "japon": ventas_jp
        },
        "reseñas": {
            "criticos": {
                "metacritic": metacritic,
                "ign": ign
            },
            "usuarios_detalle": []
        },
        "comentarios": None
    }

    resultado = col.insert_one(documento)
    print(f"\n✔ Insertado con _id: {resultado.inserted_id}")


# ──────────────────────────────────────────────
# INSERTAR VARIOS
# ──────────────────────────────────────────────

def insertar_varios(col):
    juegos = []

    n = int(input("\n¿Cuántos juegos quieres insertar?: "))

    for i in range(n):
        print(f"\n--- JUEGO {i+1} ---")

        titulo = input("Título: ")
        año = int(input("Año: "))

        generos = input("Géneros (coma): ").split(",")
        generos = [g.strip() for g in generos]

        plataformas = input("Plataformas (coma): ").split(",")
        plataformas = [p.strip() for p in plataformas]

        disponible = input("¿Disponible? (s/n): ").lower() == "s"

        fecha = datetime.strptime(
            input("Fecha (YYYY-MM-DD): "),
            "%Y-%m-%d"
        )

        precio = Decimal128(input("Precio: "))

        dev_nombre = input("Dev nombre: ")
        dev_pais = input("Dev país: ")

        nota = int(input("Nota: "))

        usuarios = input("Usuarios (ej 10,9,8): ").split(",")
        usuarios = [int(u.strip()) for u in usuarios]

        ventas_eu = float(input("Ventas EU: "))
        ventas_am = float(input("Ventas AM: "))
        ventas_jp = float(input("Ventas JP: "))

        metacritic = int(input("Metacritic: "))
        ign = float(input("IGN: "))

        juegos.append({
            "titulo": titulo,
            "año": año,
            "genero": generos,
            "plataforma": plataformas,
            "disponible": disponible,
            "fecha_lanzamiento": fecha,
            "precio": precio,
            "desarrollador": {
                "nombre": dev_nombre,
                "pais": dev_pais
            },
            "valoraciones": {
                "nota": nota,
                "usuarios": usuarios
            },
            "ventas": {
                "europa": ventas_eu,
                "america": ventas_am,
                "japon": ventas_jp
            },
            "reseñas": {
                "criticos": {
                    "metacritic": metacritic,
                    "ign": ign
                },
                "usuarios_detalle": []
            },
            "comentarios": None
        })

    resultado = col.insert_many(juegos)
    print(f"\n {len(resultado.inserted_ids)} juegos insertados")


# ──────────────────────────────────────────────
#  2. ELIMINACIÓN
# ──────────────────────────────────────────────
 
def menu_eliminacion(col):
    separador("ELIMINACIÓN DE DOCUMENTOS")
    print("1. Eliminar un juego por título (deleteOne)")
    print("2. Eliminar todos los juegos no disponibles (deleteMany)")
    print("0. Volver")
    opcion = input("\nElige una opción: ").strip()
 
    if opcion == "1":
        titulo = input("Introduce el título exacto a eliminar: ").strip()
        resultado = col.delete_one({"titulo": titulo})
        if resultado.deleted_count > 0:
            print(f" Juego '{titulo}' eliminado correctamente.")
        else:
            print(f"  No se encontró ningún juego con el título '{titulo}'.")
 
    elif opcion == "2":
        resultado = col.delete_many({"disponible": False})
        print(f" Se han eliminado {resultado.deleted_count} juego(s) no disponibles.")
 
    elif opcion == "0":
        return
    else:
        print("Opción no válida.")


# ──────────────────────────────────────────────
#  3. ACTUALIZACIÓN
# ──────────────────────────────────────────────
 
def menu_actualizacion(col):
    separador("ACTUALIZACIÓN DE DOCUMENTOS")
    print("1. Actualizar precio de un juego (updateOne)")
    print("2. Marcar disponibles todos los juegos de un desarrollador (updateMany)")
    print("3. Reemplazar documento completo (replaceOne)")
    print("0. Volver")
    opcion = input("\nElige una opción: ").strip()
 
    if opcion == "1":
        titulo = input("Título del juego: ").strip()
        try:
            nuevo_precio = float(input("Nuevo precio (€): ").strip())
        except ValueError:
            print(" Precio no válido.")
            return
        resultado = col.update_one(
            {"titulo": titulo},
            {"$set": {"precio": Decimal128(str(nuevo_precio))}}
        )
        if resultado.matched_count > 0:
            print(f"Precio actualizado para '{titulo}'.")
        else:
            print(f"  No se encontró el juego '{titulo}'.")
 
    elif opcion == "2":
        desarrollador = input("Nombre del desarrollador: ").strip()
        resultado = col.update_many(
            {"desarrollador.nombre": desarrollador},
            {"$set": {"disponible": True}}
        )
        print(f"{resultado.modified_count} juego(s) de '{desarrollador}' actualizados a disponible.")
 
    elif opcion == "3":
        titulo = input("Título del juego a reemplazar: ").strip()
        juego_reemplazado = {
            "titulo": titulo,
            "año": 2024,
            "genero": ["Action", "Adventure"],
            "plataforma": ["PC", "PS5", "Xbox"],
            "disponible": True,
            "fecha_lanzamiento": datetime(2024, 1, 1),
            "precio": Decimal128("69.99"),
            "desarrollador": {"nombre": "Desarrollador Actualizado", "pais": "EEUU"},
            "valoraciones": {"nota": 88, "usuarios": [9, 8, 9, 9]},
            "ventas": {"europa": 1.0, "america": 2.0, "japon": 0.5},
            "reseñas": {
                "criticos": {"metacritic": 88, "ign": 8.8},
                "usuarios_detalle": [
                    {"usuario": "user1", "puntuacion": 9},
                    {"usuario": "user2", "puntuacion": 8}
                ]
            },
            "comentarios": "Documento reemplazado desde Python"
        }
        resultado = col.replace_one({"titulo": titulo}, juego_reemplazado)
        if resultado.matched_count > 0:
            print(f"Documento '{titulo}' reemplazado correctamente.")
        else:
            print(f"  No se encontró el juego '{titulo}'.")
 
    elif opcion == "0":
        return
    else:
        print("Opción no válida.")

# ──────────────────────────────────────────────
#  4. CONSULTAS
# ──────────────────────────────────────────────
 
def menu_consultas(col):
    separador("CONSULTAS")
    print("1.  Juegos por año")
    print("2.  Juegos disponibles")
    print("3.  Top 5 juegos por valoración")
    print("4.  Juegos con nota superior a un valor")
    print("5.  Juegos ordenados por precio (ascendente)")
    print("─── Arrays ───────────────────────────────")
    print("6.  Buscar por género")
    print("7.  Juegos en PS4 y PC")
    print("8.  Juegos con alguna puntuación de usuario = 10")
    print("9.  Juegos por desarrollador")
    print("─── Documentos embebidos ─────────────────")
    print("10. Juegos con Metacritic ≥ 90")
    print("11. Juegos con ventas en América > 10M")
    print("─── Agregación ───────────────────────────")
    print("12. Estadísticas por género")
    print("13. Ranking de desarrolladores por ventas")
    print("0.  Volver")
 
    opcion = input("\nElige una consulta: ").strip()
 
    # ── Simples ──
    if opcion == "1":
        try:
            año = int(input("Año a buscar: "))
        except ValueError:
            print(" Año no válido.")
            return
        separador(f"Juegos del año {año}")
        juegos = col.find({"año": año}, {"titulo": 1, "año": 1, "desarrollador.nombre": 1, "_id": 0})
        for j in juegos:
            print(f"  • {j['titulo']} — {j.get('desarrollador', {}).get('nombre', 'N/A')}")
 
    elif opcion == "2":
        separador("Juegos disponibles")
        juegos = col.find({"disponible": True}, {"titulo": 1, "precio": 1, "_id": 0}).sort("titulo", 1)
        for j in juegos:
            print(f"  • {j['titulo']} — {j.get('precio', 'N/A')} €")
 
    elif opcion == "3":
        separador("Top 5 juegos por valoración")
        juegos = col.find({}, {"titulo": 1, "valoraciones.nota": 1, "_id": 0}).sort("valoraciones.nota", -1).limit(5)
        for i, j in enumerate(juegos, 1):
            nota = j.get("valoraciones", {}).get("nota", "N/A")
            print(f"  {i}. {j['titulo']} — Nota: {nota}")
 
    elif opcion == "4":
        try:
            umbral = int(input("Nota mínima (0-100): "))
        except ValueError:
            print(" Valor no válido.")
            return
        separador(f"Juegos con nota > {umbral}")
        juegos = col.find(
            {"valoraciones.nota": {"$gt": umbral}},
            {"titulo": 1, "valoraciones.nota": 1, "_id": 0}
        ).sort("valoraciones.nota", -1)
        for j in juegos:
            nota = j.get("valoraciones", {}).get("nota", "N/A")
            print(f"  • {j['titulo']} — Nota: {nota}")
 
    elif opcion == "5":
        separador("Juegos ordenados por precio (ascendente)")
        juegos = col.find(
            {"disponible": True},
            {"titulo": 1, "precio": 1, "_id": 0}
        ).sort("precio", 1).limit(10)
        for j in juegos:
            print(f"  • {j['titulo']} — {j.get('precio', 'N/A')} €")
 
    # ── Arrays ──
    elif opcion == "6":
        genero = input("Género a buscar (ej: RPG, Action, Racing): ").strip()
        separador(f"Juegos del género '{genero}'")
        juegos = col.find(
            {"genero": {"$in": [genero]}},
            {"titulo": 1, "genero": 1, "_id": 0}
        )
        encontrados = 0
        for j in juegos:
            print(f"  • {j['titulo']} — Géneros: {', '.join(j.get('genero', []))}")
            encontrados += 1
        if encontrados == 0:
            print(f"  No se encontraron juegos del género '{genero}'.")
 
    elif opcion == "7":
        separador("Juegos disponibles en PS4 Y PC")
        juegos = col.find(
            {"plataforma": {"$all": ["PS4", "PC"]}},
            {"titulo": 1, "plataforma": 1, "_id": 0}
        )
        for j in juegos:
            print(f"  • {j['titulo']} — {', '.join(j.get('plataforma', []))}")
 
    elif opcion == "8":
        separador("Juegos con alguna puntuación de usuario = 10")
        juegos = col.find(
            {"valoraciones.usuarios": 10},
            {"titulo": 1, "valoraciones.usuarios": 1, "_id": 0}
        ).limit(8)
        for j in juegos:
            usuarios = j.get("valoraciones", {}).get("usuarios", [])
            print(f"  • {j['titulo']} — Puntuaciones: {usuarios}")
 
    # ── Documentos embebidos ──
    elif opcion == "9":
        desarrollador = input("Nombre del desarrollador: ").strip()
        separador(f"Juegos de '{desarrollador}'")
        juegos = col.find(
            {"desarrollador.nombre": desarrollador},
            {"titulo": 1, "año": 1, "desarrollador": 1, "_id": 0}
        )
        encontrados = 0
        for j in juegos:
            dev = j.get("desarrollador", {})
            print(f"  • {j['titulo']} ({j.get('año', '?')}) — {dev.get('nombre', '')} ({dev.get('pais', '')})")
            encontrados += 1
        if encontrados == 0:
            print(f"  No se encontraron juegos del desarrollador '{desarrollador}'.")
 
    elif opcion == "10":
        separador("Juegos con Metacritic ≥ 90")
        juegos = col.find(
            {"reseñas.criticos.metacritic": {"$gte": 90}},
            {"titulo": 1, "reseñas.criticos.metacritic": 1, "_id": 0}
        ).sort("reseñas.criticos.metacritic", -1)
        for j in juegos:
            meta = j.get("reseñas", {}).get("criticos", {}).get("metacritic", "N/A")
            print(f"  • {j['titulo']} — Metacritic: {meta}")
 
    elif opcion == "11":
        separador("Juegos con ventas en América > 10 millones")
        juegos = col.find(
            {"ventas.america": {"$gt": 10}},
            {"titulo": 1, "ventas": 1, "_id": 0}
        ).sort("ventas.america", -1)
        for j in juegos:
            ventas = j.get("ventas", {})
            print(f"  • {j['titulo']} — América: {ventas.get('america', 0)}M | Europa: {ventas.get('europa', 0)}M | Japón: {ventas.get('japon', 0)}M")
 
    # ── Agregación ──
    elif opcion == "12":
        separador("Estadísticas por género")
        pipeline = [
            {"$unwind": "$genero"},
            {
                "$group": {
                    "_id": "$genero",
                    "total_juegos": {"$sum": 1},
                    "nota_media": {"$avg": "$valoraciones.nota"},
                    "ventas_america": {"$sum": "$ventas.america"}
                }
            },
            {"$sort": {"total_juegos": -1}}
        ]
        resultados = col.aggregate(pipeline)
        print(f"  {'Género':<20} {'Juegos':>7} {'Nota Media':>12} {'Ventas América':>16}")
        print(f"  {'─'*20} {'─'*7} {'─'*12} {'─'*16}")
        for r in resultados:
            nota = round(r.get("nota_media", 0), 1)
            ventas = round(r.get("ventas_america", 0), 1)
            print(f"  {r['_id']:<20} {r['total_juegos']:>7} {nota:>12} {ventas:>14}M")
 
    elif opcion == "13":
        separador("Ranking de desarrolladores por ventas en Europa")
        pipeline = [
            {
                "$group": {
                    "_id": "$desarrollador.nombre",
                    "pais": {"$first": "$desarrollador.pais"},
                    "total_juegos": {"$sum": 1},
                    "ventas_europa": {"$sum": "$ventas.europa"},
                    "nota_media": {"$avg": "$valoraciones.nota"}
                }
            },
            {"$sort": {"ventas_europa": -1}},
            {"$limit": 5}
        ]
        resultados = col.aggregate(pipeline)
        print(f"  {'Desarrollador':<20} {'País':<10} {'Juegos':>7} {'Ventas EU':>12} {'Nota':>6}")
        print(f"  {'─'*20} {'─'*10} {'─'*7} {'─'*12} {'─'*6}")
        for r in resultados:
            nota = round(r.get("nota_media", 0), 1)
            ventas = round(r.get("ventas_europa", 0), 1)
            print(f"  {r['_id']:<20} {r.get('pais', 'N/A'):<10} {r['total_juegos']:>7} {ventas:>10}M {nota:>6}")
 
    elif opcion == "0":
        return
    else:
        print("Opción no válida.")
