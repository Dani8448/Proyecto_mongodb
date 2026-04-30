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
