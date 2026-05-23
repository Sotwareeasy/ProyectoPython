import sys
import os

# Asegurar que el directorio raíz del proyecto esté en el path
sys.path.insert(0, os.path.dirname(__file__))

from modules.core import iniciar_sesion, menu_principal


def main() -> None:
    usuario = iniciar_sesion()
    if usuario:
        menu_principal(usuario)

if __name__ == "__main__":
    main()