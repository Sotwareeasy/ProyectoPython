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
        id_usuario = pedir_campo_obligatorio(msg.CAMPO_ID)
        if any(u["id"] == id_usuario for u in datos["usuarios"]):
            print(msg.ERR_ID_DUPLICADO_USUARIO)
        else:
            break

    nombres   = pedir_campo_obligatorio(msg.CAMPO_NOMBRES)
    apellidos = pedir_campo_obligatorio(msg.CAMPO_APELLIDOS)
    telefono  = pedir_campo_obligatorio(
        msg.CAMPO_TELEFONO,
        es_telefono_valido,
        msg.ERR_TELEFONO_INVALIDO
    )

    # E-mail único y válido
    while True:
        email = pedir_campo_obligatorio(
            msg.CAMPO_EMAIL,
            es_email_valido,
            msg.ERR_EMAIL_INVALIDO
        )
        if any(u["email"] == email for u in datos["usuarios"]):
            print(msg.ERR_EMAIL_DUPLICADO)
        else:
            break

    direccion = pedir_campo_obligatorio(msg.CAMPO_DIRECCION)
    rol       = pedir_campo_obligatorio(
        msg.CAMPO_ROL,
        rol_valido,
        msg.ERR_ROL_INVALIDO
    ).lower()
    password  = pedir_campo_obligatorio(msg.CAMPO_PASSWORD)

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
    print(msg.OK_USUARIO_REGISTRADO)


# ── Listar ────────────────────────────────────────────────────

def listar_usuarios() -> None:
    imprimir_encabezado("Listado de Usuarios")
    datos = cargar_datos()
    if not datos["usuarios"]:
        print(msg.ERR_NO_HAY_USUARIOS)
        return
    imprimir_tabla_usuarios(datos["usuarios"])


# ── Actualizar ────────────────────────────────────────────────

def actualizar_usuario() -> None:
    imprimir_encabezado("Actualizar Usuario")
    datos = cargar_datos()

    id_buscar = input("  Ingrese el ID del usuario a actualizar: ").strip()
    usuario = next((u for u in datos["usuarios"] if u["id"] == id_buscar), None)
    if not usuario:
        print(msg.ERR_USUARIO_NO_ENCONTRADO)
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

    actualizar_campo("nombres",   msg.CAMPO_NOMBRES)
    actualizar_campo("apellidos", msg.CAMPO_APELLIDOS)
    actualizar_campo("telefono",  msg.CAMPO_TELEFONO,  es_telefono_valido, msg.ERR_TELEFONO_INVALIDO)
    actualizar_campo("email",     msg.CAMPO_EMAIL,     es_email_valido,    msg.ERR_EMAIL_INVALIDO)
    actualizar_campo("direccion", msg.CAMPO_DIRECCION)
    actualizar_campo("rol",       msg.CAMPO_ROL,       rol_valido,         msg.ERR_ROL_INVALIDO)
    actualizar_campo("password",  msg.CAMPO_PASSWORD)

    guardar_datos(datos)
    print(msg.OK_USUARIO_ACTUALIZADO)


# ── Eliminar ──────────────────────────────────────────────────

def eliminar_usuario() -> None:
    imprimir_encabezado("Eliminar Usuario")
    datos = cargar_datos()

    id_buscar = input("  Ingrese el ID del usuario a eliminar: ").strip()
    usuario = next((u for u in datos["usuarios"] if u["id"] == id_buscar), None)
    if not usuario:
        print(msg.ERR_USUARIO_NO_ENCONTRADO)
        return

    # Proteger al administrador principal
    if usuario["id"] == "0000":
        print(msg.ERR_NO_PUEDE_ELIMINAR_ADMIN)
        return

    _imprimir_ficha_usuario(usuario)

    if confirmar(msg.CONFIRMAR_ELIMINAR):
        datos["usuarios"] = [u for u in datos["usuarios"] if u["id"] != id_buscar]
        guardar_datos(datos)
        print(msg.OK_USUARIO_ELIMINADO)
    else:
        print(msg.OK_OPERACION_CANCELADA)

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