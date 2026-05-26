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
        id_contacto = pedir_campo_obligatorio(msg.campo_id)
        if any(c["id"] == id_contacto for c in datos["contactos"]):
            print(msg.contact_duplicate)
        else:
            break

    nombres   = pedir_campo_obligatorio(msg.campo_nombre)
    apellidos = pedir_campo_obligatorio(msg.campo_apellidos)
    telefono  = pedir_campo_obligatorio(
        msg.campo_telefono,
        es_telefono_valido,
        msg.telefono_invalid
    )
    email = pedir_campo_obligatorio(
        msg.campo_email, 
        es_email_valido,
        msg.correo_invalid
    )
    direccion = pedir_campo_obligatorio(msg.campo_direccion)
    tipo      = pedir_campo_obligatorio(msg.campo_tipo)
    notas     = input(msg.campo_notas).strip()

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
    print(msg.user_registred)


# ── Listar ────────────────────────────────────────────────────

def listar_contactos() -> None:
    imprimir_encabezado("Listado de Contactos")
    datos = cargar_datos()
    if not datos["contactos"]:
        print(msg.contact_noresgistred)
        return
    imprimir_tabla_contactos(datos["contactos"])


# ── Buscar ────────────────────────────────────────────────────

def buscar_contacto() -> None:
    imprimir_encabezado("Buscar Contacto")

    while True:
        print(msg.search_contact)
        opcion = input(msg.select_option).strip()

        if opcion == "1":
            _buscar_por_id()
        elif opcion == "2":
            _buscar_por_nombre()
        elif opcion == "3":
            _buscar_por_tipo()
        elif opcion == "4":
            break
        else:
            print(msg.invalid_option)


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
        print(msg.contact_nofind)
    else:
        imprimir_tabla_contactos(resultado)


# ── Actualizar ────────────────────────────────────────────────

def actualizar_contacto() -> None:
    imprimir_encabezado("Actualizar Contacto")
    datos = cargar_datos()

    id_buscar = input("  Ingrese el ID del contacto a actualizar: ").strip()
    contacto = next((c for c in datos["contactos"] if c["id"] == id_buscar), None)
    if not contacto:
        print(msg.contact_nofind)
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

    actualizar_campo("nombres",   msg.campo_nombre)
    actualizar_campo("apellidos", msg.campo_apellidos)
    actualizar_campo("telefono",  msg.campo_telefono,  es_telefono_valido, msg.telefono_invalid)
    actualizar_campo("email",     msg.campo_email,     es_email_valido,    msg.correo_invalid)
    actualizar_campo("direccion", msg.campo_direccion)
    actualizar_campo("tipo",      msg.campo_tipo)
    actualizar_campo("notas",     msg.campo_notas)

    guardar_datos(datos)
    print(msg.contact_update)


# ── Eliminar ──────────────────────────────────────────────────

def eliminar_contacto() -> None:
    imprimir_encabezado("Eliminar Contacto")
    datos = cargar_datos()

    id_buscar = input("  Ingrese el ID del contacto a eliminar: ").strip()
    contacto = next((c for c in datos["contactos"] if c["id"] == id_buscar), None)
    if not contacto:
        print(msg.contact_noresgistred)
        return

    imprimir_ficha_contacto(contacto)

    if confirmar(msg.confirm_delete):
        datos["contactos"] = [c for c in datos["contactos"] if c["id"] != id_buscar]
        guardar_datos(datos)
        print(msg.contact_deleted)
    else:
        print(msg.operacion_cancelada)