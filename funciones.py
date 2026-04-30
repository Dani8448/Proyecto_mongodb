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
 
 
