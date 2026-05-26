import json
import re
import os

RUTA_JSON = os.path.join(os.path.dirname(__file__), "..", "data", "Contactos.json")


# ── Persistencia ─────────────────────────────────────────────

def cargar_datos() -> dict:
    """Lee el archivo JSON y retorna el diccionario de datos."""
    with open(RUTA_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_datos(datos: dict) -> None:
    """Sobreescribe el archivo JSON con el diccionario actualizado."""
    with open(RUTA_JSON, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)


# Validaciones

def es_email_valido(email: str) -> bool:
    patron = r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(patron, email))


def es_telefono_valido(telefono: str) -> bool:
    return bool(re.match(r"^[\d\s\+\-\(\)]+$", telefono))


def no_vacio(valor: str) -> bool:
    return valor.strip() != ""


def rol_valido(rol: str) -> bool:
    return rol.strip().lower() in ("admin", "operario")


# ── Entrada de usuario ────────────────────────────────────────

def pedir_campo(prompt: str, validador=None, mensaje_error: str = "") -> str:
    """
    Solicita un campo al usuario, aplicando un validador opcional.
    Repite hasta obtener un valor válido.
    Retorna "" si el usuario deja en blanco (para campos opcionales al actualizar).
    """
    while True:
        valor = input(prompt).strip()
        if validador is None:
            return valor
        if validador(valor):
            return valor
        print(mensaje_error)


def pedir_campo_obligatorio(prompt: str, validador=None, mensaje_error: str = "") -> str:
    """Igual que pedir_campo pero no acepta cadena vacía."""
    from modules.messages import campo_empty
    while True:
        valor = input(prompt).strip()
        if not valor:
            print(campo_empty)
            continue
        if validador is None or validador(valor):
            return valor
        print(mensaje_error)


def confirmar(prompt: str) -> bool:
    """Retorna True si el usuario responde 's' o 'si'."""
    respuesta = input(prompt).strip().lower()
    return respuesta in ("s", "si", "sí")


# ── Tablas en consola ─────────────────────────────────────────

def imprimir_tabla_contactos(contactos: list) -> None:
    """Imprime una tabla formateada de contactos."""
    if not contactos:
        return
    cab = f"  {'ID':<15} {'Nombre completo':<28} {'Teléfono':<15} {'E-mail':<28} {'Tipo':<12}"
    print()
    print("  " + "-" * 100)
    print(cab)
    print("  " + "-" * 100)
    for c in contactos:
        nombre = f"{c.get('nombres','')} {c.get('apellidos','')}".strip()
        print(
            f"  {c.get('id',''):<15} "
            f"{nombre:<28} "
            f"{c.get('telefono',''):<15} "
            f"{c.get('email',''):<28} "
            f"{c.get('tipo',''):<12}"
        )
    print("  " + "-" * 100)
    print(f"  Total: {len(contactos)} contacto(s)")
    print()


def imprimir_ficha_contacto(c: dict) -> None:
    """Imprime los datos completos de un contacto."""
    print()
    print("  " + "-" * 50)
    print(f"  ID          : {c.get('id','')}")
    print(f"  Nombres     : {c.get('nombres','')} {c.get('apellidos','')}")
    print(f"  Teléfono    : {c.get('telefono','')}")
    print(f"  E-mail      : {c.get('email','')}")
    print(f"  Dirección   : {c.get('direccion','')}")
    print(f"  Tipo        : {c.get('tipo','')}")
    print(f"  Notas       : {c.get('notas','')}")
    print("  " + "-" * 50)
    print()


def imprimir_tabla_usuarios(usuarios: list) -> None:
    """Imprime una tabla formateada de usuarios del sistema."""
    if not usuarios:
        return
    cab = f"  {'ID':<10} {'Nombre completo':<28} {'E-mail':<30} {'Rol':<10}"
    print()
    print("  " + "-" * 82)
    print(cab)
    print("  " + "-" * 82)
    for u in usuarios:
        nombre = f"{u.get('nombres','')} {u.get('apellidos','')}".strip()
        print(
            f"  {u.get('id',''):<10} "
            f"{nombre:<28} "
            f"{u.get('email',''):<30} "
            f"{u.get('rol',''):<10}"
        )
    print("  " + "-" * 82)
    print(f"  Total: {len(usuarios)} usuario(s)")
    print()


# ── Encabezado ────────────────────────────────────────────────

def imprimir_encabezado(titulo: str) -> None:
    from modules.messages import separador, app_titulo
    print()
    print("  " + separador)
    print(f"  {app_titulo}")
    if titulo:
        print(f"  {titulo}")
    print("  " + separador)