from funciones import *

def menu_principal(col):
    while True:
        separador()
        print("  GESTIÓN DE VIDEOJUEGOS - MongoDB")
        separador()
        print("  1. Inserción de documentos")
        print("  2. Eliminación de documentos")
        print("  3. Actualización de documentos")
        print("  4. Consultas")
        print("  0. Salir")
        separador()

        opcion = input("  Elige una opción: ").strip()

        if opcion == "1":
            menu_insercion(col)
        elif opcion == "2":
            menu_eliminacion(col)
        elif opcion == "3":
            menu_actualizacion(col)
        elif opcion == "4":
            menu_consultas(col)
        elif opcion == "0":
            print("\nHasta luego.\n")
            break
        else:
            print("Opción no válida.")

        input("\nPulsa ENTER para continuar...")


if __name__ == "__main__":
    coleccion = conectar()
    menu_principal(coleccion)