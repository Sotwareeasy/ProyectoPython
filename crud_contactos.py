from modules import messages as msg
from modules.utils import (
    cargar_datos, guardar_datos,
    pedir_campo_obligatorio, pedir_campo,
    es_email_valido, es_telefono_valido,
    confirmar,
    imprimir_tabla_contactos, imprimir_ficha_contacto,
    imprimir_encabezado,
)


# ── Registrar ─────────────────────────────────────────────────

def registrar_contacto() -> None:
    imprimir_encabezado("Registrar Contacto")
    datos = cargar_datos()

    # ID
    while True:
        id_contacto = pedir_campo_obligatorio(msg.CAMPO_ID)
        if any(c["id"] == id_contacto for c in datos["contactos"]):
            print(msg.ERR_ID_DUPLICADO_CONTACTO)
        else:
            break

    nombres   = pedir_campo_obligatorio(msg.CAMPO_NOMBRES)
    apellidos = pedir_campo_obligatorio(msg.CAMPO_APELLIDOS)
    telefono  = pedir_campo_obligatorio(
        msg.CAMPO_TELEFONO,
        es_telefono_valido,
        msg.ERR_TELEFONO_INVALIDO
    )
    email = pedir_campo_obligatorio(
        msg.CAMPO_EMAIL,
        es_email_valido,
        msg.ERR_EMAIL_INVALIDO
    )
    direccion = pedir_campo_obligatorio(msg.CAMPO_DIRECCION)
    tipo      = pedir_campo_obligatorio(msg.CAMPO_TIPO)
    notas     = input(msg.CAMPO_NOTAS).strip()

    nuevo = {
        "id":        id_contacto,
        "nombres":   nombres,
        "apellidos": apellidos,
        "telefono":  telefono,
        "email":     email,
        "direccion": direccion,
        "tipo":      tipo,
        "notas":     notas,
    }
    datos["contactos"].append(nuevo)
    guardar_datos(datos)
    print(msg.OK_CONTACTO_REGISTRADO)


# ── Listar ────────────────────────────────────────────────────

def listar_contactos() -> None:
    imprimir_encabezado("Listado de Contactos")
    datos = cargar_datos()
    if not datos["contactos"]:
        print(msg.ERR_NO_HAY_CONTACTOS)
        return
    imprimir_tabla_contactos(datos["contactos"])


# ── Buscar ────────────────────────────────────────────────────

def buscar_contacto() -> None:
    imprimir_encabezado("Buscar Contacto")

    while True:
        print(msg.MENU_BUSCAR_CONTACTO)
        opcion = input(msg.OPCION_SELECCIONAR).strip()

        if opcion == "1":
            _buscar_por_id()
        elif opcion == "2":
            _buscar_por_nombre()
        elif opcion == "3":
            _buscar_por_tipo()
        elif opcion == "4":
            break
        else:
            print(msg.OPCION_INVALIDA)


def _buscar_por_id() -> None:
    termino = input("  Ingrese el ID a buscar: ").strip()
    datos = cargar_datos()
    resultado = [c for c in datos["contactos"] if c["id"] == termino]
    _mostrar_resultados(resultado)


def _buscar_por_nombre() -> None:
    termino = input("  Ingrese nombre o apellido (búsqueda parcial): ").strip().lower()
    datos = cargar_datos()
    resultado = [
        c for c in datos["contactos"]
        if termino in c.get("nombres", "").lower()
        or termino in c.get("apellidos", "").lower()
    ]
    _mostrar_resultados(resultado)


def _buscar_por_tipo() -> None:
    termino = input("  Ingrese el tipo de contacto: ").strip().lower()
    datos = cargar_datos()
    resultado = [
        c for c in datos["contactos"]
        if termino in c.get("tipo", "").lower()
    ]
    _mostrar_resultados(resultado)


def _mostrar_resultados(resultado: list) -> None:
    if not resultado:
        print(msg.ERR_CONTACTO_NO_ENCONTRADO)
    else:
        imprimir_tabla_contactos(resultado)


# ── Actualizar ────────────────────────────────────────────────

def actualizar_contacto() -> None:
    imprimir_encabezado("Actualizar Contacto")
    datos = cargar_datos()

    id_buscar = input("  Ingrese el ID del contacto a actualizar: ").strip()
    contacto = next((c for c in datos["contactos"] if c["id"] == id_buscar), None)
    if not contacto:
        print(msg.ERR_CONTACTO_NO_ENCONTRADO)
        return

    imprimir_ficha_contacto(contacto)
    print("  Ingrese los nuevos valores (deje en blanco para conservar el actual):\n")

    def actualizar_campo(campo, prompt, validador=None, error_msg=""):
        valor = input(prompt).strip()
        if not valor:
            return
        if validador and not validador(valor):
            print(error_msg)
            return
        contacto[campo] = valor

    actualizar_campo("nombres",   msg.CAMPO_NOMBRES)
    actualizar_campo("apellidos", msg.CAMPO_APELLIDOS)
    actualizar_campo("telefono",  msg.CAMPO_TELEFONO,  es_telefono_valido, msg.ERR_TELEFONO_INVALIDO)
    actualizar_campo("email",     msg.CAMPO_EMAIL,     es_email_valido,    msg.ERR_EMAIL_INVALIDO)
    actualizar_campo("direccion", msg.CAMPO_DIRECCION)
    actualizar_campo("tipo",      msg.CAMPO_TIPO)
    actualizar_campo("notas",     msg.CAMPO_NOTAS)

    guardar_datos(datos)
    print(msg.OK_CONTACTO_ACTUALIZADO)


# ── Eliminar ──────────────────────────────────────────────────

def eliminar_contacto() -> None:
    imprimir_encabezado("Eliminar Contacto")
    datos = cargar_datos()

    id_buscar = input("  Ingrese el ID del contacto a eliminar: ").strip()
    contacto = next((c for c in datos["contactos"] if c["id"] == id_buscar), None)
    if not contacto:
        print(msg.ERR_CONTACTO_NO_ENCONTRADO)
        return

    imprimir_ficha_contacto(contacto)

    if confirmar(msg.CONFIRMAR_ELIMINAR):
        datos["contactos"] = [c for c in datos["contactos"] if c["id"] != id_buscar]
        guardar_datos(datos)
        print(msg.OK_CONTACTO_ELIMINADO)
    else:
        print(msg.OK_OPERACION_CANCELADA)