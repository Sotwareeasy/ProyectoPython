import modules.messages as msg
import modules.crud_contactos as cc
import modules.crud_user  as cu
from modules.utils import cargar_datos, imprimir_encabezado

MAX_INTENTOS = 3

# ── Login ─────────────────────────────────────────────────────

def iniciar_sesion() -> dict | None:
    """
    Muestra la pantalla de login y retorna el usuario autenticado
    o None si se superan los intentos máximos.
    """
    imprimir_encabezado("")
    print(msg.login_bienvenida)
    print()

    intentos = 0
    while intentos < MAX_INTENTOS:
        email    = input(msg.login_user).strip().lower()
        password = input(msg.login_password).strip()

        datos = cargar_datos()
        usuario = next(
            (u for u in datos["usuarios"]
        if u["email"].lower() == email and u["password"] == password),
            None
        )

        if usuario:
            print(msg.login_exitoso.format(usuario["nombres"]))
            return usuario

        intentos += 1
        restantes = MAX_INTENTOS - intentos
        print(msg.login_fail)
        if restantes > 0:
            print(f"  Intentos restantes: {restantes}")

    print(msg.login_block)
    return None


# ── Menú de Contactos ─────────────────────────────────────────

def menu_contactos() -> None:
    while True:
        print(msg.menu_contact)
        opcion = input(msg.select_option).strip()

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
            print(msg.invalid_option)

        input("\n  Presione Enter para continuar...")


# ── Menú de Usuarios (solo admin) ─────────────────────────────

def menu_usuarios() -> None:
    while True:
        print(msg.menu_user)
        opcion = input(msg.select_option).strip()

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
            print(msg.invalid_option)

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
            print(msg.menu_admin)
            opcion = input(msg.select_option).strip()
            if opcion == "1":
                menu_contactos()
            elif opcion == "2":
                menu_usuarios()
            elif opcion == "3":
                print("\n  Sesión cerrada. Hasta pronto.\n")
                break
            else:
                print(msg.invalid_option)
        else:
            print(msg.menu_operario)
            opcion = input(msg.select_option).strip()
            if opcion == "1":
                menu_contactos()
            elif opcion == "2":
                print("\n  Sesión cerrada. Hasta pronto.\n")
                break
            else:
                print(msg.invalid_option)