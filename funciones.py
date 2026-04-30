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
