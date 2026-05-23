from modules import messages as msg
from modules.utils import cargar_datos, imprimir_encabezado
from modules import crud_contactos as cc
from modules import crud_usuarios   as cu

MAX_INTENTOS = 3

# ── Login ─────────────────────────────────────────────────────

def iniciar_sesion() -> dict | None:
    """
    Muestra la pantalla de login y retorna el usuario autenticado
    o None si se superan los intentos máximos.
    """
    imprimir_encabezado("")
    print(msg.LOGIN_BIENVENIDA)
    print()

    intentos = 0
    while intentos < MAX_INTENTOS:
        email    = input(msg.LOGIN_USUARIO).strip().lower()
        password = input(msg.LOGIN_PASSWORD).strip()

        datos = cargar_datos()
        usuario = next(
            (u for u in datos["usuarios"]
        if u["email"].lower() == email and u["password"] == password),
            None
        )

        if usuario:
            print(msg.LOGIN_EXITOSO.format(usuario["nombres"]))
            return usuario

        intentos += 1
        restantes = MAX_INTENTOS - intentos
        print(msg.LOGIN_FALLIDO)
        if restantes > 0:
            print(f"  Intentos restantes: {restantes}")

    print(msg.LOGIN_BLOQUEADO)
    return None


# ── Menú de Contactos ─────────────────────────────────────────

def menu_contactos() -> None:
    while True:
        print(msg.MENU_CONTACTOS)
        opcion = input(msg.OPCION_SELECCIONAR).strip()

        if opcion == "1":
            cc.registrar_contacto()
        elif opcion == "2":
            cc.listar_contactos()
        elif opcion == "3":
            cc.buscar_contacto()
        elif opcion == "4":
            cc.actualizar_contacto()
        elif opcion == "5":
            cc.eliminar_contacto()
        elif opcion == "6":
            break
        else:
            print(msg.OPCION_INVALIDA)

        input("\n  Presione Enter para continuar...")


# ── Menú de Usuarios (solo admin) ─────────────────────────────

def menu_usuarios() -> None:
    while True:
        print(msg.MENU_USUARIOS)
        opcion = input(msg.OPCION_SELECCIONAR).strip()

        if opcion == "1":
            cu.registrar_usuario()
        elif opcion == "2":
            cu.listar_usuarios()
        elif opcion == "3":
            cu.actualizar_usuario()
        elif opcion == "4":
            cu.eliminar_usuario()
        elif opcion == "5":
            break
        else:
            print(msg.OPCION_INVALIDA)

        input("\n  Presione Enter para continuar...")

# ── Menú Principal ────────────────────────────────────────────

def menu_principal(usuario: dict) -> None:
    """
    Muestra el menú principal adaptado al rol del usuario.
    Administrador: contactos + usuarios.
    Operario: solo contactos.
    """
    es_admin = usuario.get("rol", "").lower() == "admin"

    while True:
        imprimir_encabezado(f"  Sesión: {usuario['nombres']} {usuario['apellidos']}  |  Rol: {usuario['rol']}")

        if es_admin:
            print(msg.MENU_PRINCIPAL_ADMIN)
            opcion = input(msg.OPCION_SELECCIONAR).strip()
            if opcion == "1":
                menu_contactos()
            elif opcion == "2":
                menu_usuarios()
            elif opcion == "3":
                print("\n  Sesión cerrada. Hasta pronto.\n")
                break
            else:
                print(msg.OPCION_INVALIDA)
        else:
            print(msg.MENU_PRINCIPAL_OPERARIO)
            opcion = input(msg.OPCION_SELECCIONAR).strip()
            if opcion == "1":
                menu_contactos()
            elif opcion == "2":
                print("\n  Sesión cerrada. Hasta pronto.\n")
                break
            else:
                print(msg.OPCION_INVALIDA)