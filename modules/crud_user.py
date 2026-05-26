from modules import messages as msg
from modules.utils import (
    cargar_datos, guardar_datos,
    pedir_campo_obligatorio,
    es_email_valido, es_telefono_valido, rol_valido,
    confirmar,
    imprimir_tabla_usuarios,
    imprimir_encabezado,
)


# ── Registrar ─────────────────────────────────────────────────

def registrar_usuario() -> None:
    imprimir_encabezado("Registrar Usuario")
    datos = cargar_datos()

    # ID único
    while True:
        id_usuario = pedir_campo_obligatorio(msg.campo_id)
        if any(u["id"] == id_usuario for u in datos["usuarios"]):
            print(msg.user_duplicated)
        else:
            break

    nombres   = pedir_campo_obligatorio(msg.campo_nombre)
    apellidos = pedir_campo_obligatorio(msg.campo_apellidos)
    telefono  = pedir_campo_obligatorio(
        msg.campo_telefono,
        es_telefono_valido,
        msg.telefono_invalid
    )

    # E-mail único y válido
    while True:
        email = pedir_campo_obligatorio(
            msg.campo_email,
            es_email_valido,
            msg.correo_invalid
        )
        if any(u["email"] == email for u in datos["usuarios"]):
            print(msg.correo_duplicated)
        else:
            break

    direccion = pedir_campo_obligatorio(msg.campo_direccion)
    rol       = pedir_campo_obligatorio(
        msg.campo_rol,
        rol_valido,
        msg.rol_invalid
    ).lower()
    password  = pedir_campo_obligatorio(msg.campo_password)

    nuevo = {
        "id":        id_usuario,
        "nombres":   nombres,
        "apellidos": apellidos,
        "telefono":  telefono,
        "email":     email,
        "direccion": direccion,
        "password":  password,
        "rol":       rol,
    }
    datos["usuarios"].append(nuevo)
    guardar_datos(datos)
    print(msg.user_registred)


# ── Listar ────────────────────────────────────────────────────

def listar_usuarios() -> None:
    imprimir_encabezado("Listado de Usuarios")
    datos = cargar_datos()
    if not datos["usuarios"]:
        print(msg.user_noregistred)
        return
    imprimir_tabla_usuarios(datos["usuarios"])


# ── Actualizar ────────────────────────────────────────────────

def actualizar_usuario() -> None:
    imprimir_encabezado("Actualizar Usuario")
    datos = cargar_datos()

    id_buscar = input("  Ingrese el ID del usuario a actualizar: ").strip()
    usuario = next((u for u in datos["usuarios"] if u["id"] == id_buscar), None)
    if not usuario:
        print(msg.user_nofind)
        return

    _imprimir_ficha_usuario(usuario)
    print("  Ingrese los nuevos valores (deje en blanco para conservar el actual):\n")

    def actualizar_campo(campo, prompt, validador=None, error_msg=""):
        valor = input(prompt).strip()
        if not valor:
            return
        if validador and not validador(valor):
            print(error_msg)
            return
        usuario[campo] = valor

    actualizar_campo("nombres",   msg.campo_nombre)
    actualizar_campo("apellidos", msg.campo_apellidos)
    actualizar_campo("telefono",  msg.campo_telefono,  es_telefono_valido, msg.telefono_invalid)
    actualizar_campo("email",     msg.campo_email,     es_email_valido,    msg.correo_invalid)
    actualizar_campo("direccion", msg.campo_direccion)
    actualizar_campo("rol",       msg.campo_rol,       rol_valido,         msg.rol_invalid)
    actualizar_campo("password",  msg.campo_password)

    guardar_datos(datos)
    print(msg.contact_update)


# ── Eliminar ──────────────────────────────────────────────────

def eliminar_usuario() -> None:
    imprimir_encabezado("Eliminar Usuario")
    datos = cargar_datos()

    id_buscar = input("  Ingrese el ID del usuario a eliminar: ").strip()
    usuario = next((u for u in datos["usuarios"] if u["id"] == id_buscar), None)
    if not usuario:
        print(msg.user_nofind)
        return

    # Proteger al administrador principal
    if usuario["id"] == "0000":
        print(msg.nodelete_admin)
        return

    _imprimir_ficha_usuario(usuario)

    if confirmar(msg.confirm_delete):
        datos["usuarios"] = [u for u in datos["usuarios"] if u["id"] != id_buscar]
        guardar_datos(datos)
        print(msg.user_deleted)
    else:
        print(msg.operacion_cancelada)

# ── Utilidad local ────────────────────────────────────────────

def _imprimir_ficha_usuario(u: dict) -> None:
    print()
    print("  " + "-" * 50)
    print(f"  ID         : {u.get('id','')}")
    print(f"  Nombre     : {u.get('nombres','')} {u.get('apellidos','')}")
    print(f"  Teléfono   : {u.get('telefono','')}")
    print(f"  E-mail     : {u.get('email','')}")
    print(f"  Dirección  : {u.get('direccion','')}")
    print(f"  Rol        : {u.get('rol','')}")
    print("  " + "-" * 50)
    print()