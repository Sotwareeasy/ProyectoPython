import json, os, re
from datetime import datetime
from modules.utils import cargar_datos, imprimir_encabezado

RUTA_REPORTE = os.path.join(os.path.dirname(__file__), "..", "data", "reporte_auditoria_datos.json")

ROLES_PERMITIDOS          = {"admin", "operario"}
TIPOS_CONTACTO_PERMITIDOS = {"cliente", "proveedor", "aliado", "personal", "empleado", "otro"}
CAMPOS_USUARIO            = ["id", "nombres", "apellidos", "telefono", "email", "direccion", "password", "rol"]
CAMPOS_CONTACTO           = ["id", "nombres", "apellidos", "telefono", "email", "tipo"]

# ── Validadores ───────────────────────────────────────────────
_presente  = lambda r, c: c in r and str(r[c]).strip() != ""
_email_ok  = lambda v: bool(re.match(r"^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$", str(v).strip()))
_tel_ok    = lambda v: bool(re.match(r"^[\d\s\+\-\(\)]+$", str(v).strip()))

def _validar(registro, campos, extra_checks):
    errores  = [f"Campo obligatorio ausente o vacío: '{c}'." for c in campos if not _presente(registro, c)]
    errores += [msg for condicion, msg in extra_checks if condicion]
    return errores

def _validar_usuario(u):
    return _validar(u, CAMPOS_USUARIO, [
        (_presente(u, "telefono") and not _tel_ok(u["telefono"]),
            f"Teléfono inválido: '{u.get('telefono')}' (solo dígitos, espacios y +, -, (, ))."),
        (_presente(u, "email") and not _email_ok(u["email"]),
            f"E-mail inválido: '{u.get('email')}' (formato: usuario@dominio.ext)."),
        (_presente(u, "rol") and u["rol"].strip().lower() not in ROLES_PERMITIDOS,
            f"Rol inválido: '{u.get('rol')}'. Permitidos: {sorted(ROLES_PERMITIDOS)}."),
    ])

def _validar_contacto(c):
    return _validar(c, CAMPOS_CONTACTO, [
        (_presente(c, "telefono") and not _tel_ok(c["telefono"]),
            f"Teléfono inválido: '{c.get('telefono')}' (solo dígitos, espacios y +, -, (, ))."),
        (_presente(c, "email") and not _email_ok(c["email"]),
            f"E-mail inválido: '{c.get('email')}' (formato: usuario@dominio.ext)."),
        (_presente(c, "tipo") and c["tipo"].strip().lower() not in TIPOS_CONTACTO_PERMITIDOS,
            f"Tipo inválido: '{c.get('tipo')}'. Permitidos: {sorted(TIPOS_CONTACTO_PERMITIDOS)}."),
    ])

# ── Duplicados ────────────────────────────────────────────────
def _duplicados(lista, clave, normalizar=lambda x: x):
    vistos, dups = set(), []
    for item in lista:
        v = normalizar(str(item.get(clave, "")).strip())
        if v and v in vistos and v not in dups:
            dups.append(v)
        vistos.add(v)
    return dups

def _agregar_error_dup(lista_errores, registros, campo_busqueda, valor_dup, msg_dup, campo_nombre=None):
    for r in registros:
        if str(r.get(campo_busqueda, "")).strip().lower() == valor_dup:
            entrada = next((e for e in lista_errores if e["id"] == r.get("id")), None)
            if entrada:
                if msg_dup not in entrada["errores"]:
                    entrada["errores"].append(msg_dup)
            else:
                base = {"id": r.get("id", "(sin id)"), "errores": [msg_dup]}
                if campo_nombre:
                    base[campo_nombre] = r.get(campo_nombre, "")
                else:
                    base["nombre"] = f"{r.get('nombres','')} {r.get('apellidos','')}".strip()
                lista_errores.append(base)

# ── Función principal ─────────────────────────────────────────
def auditar_datos() -> None:
    imprimir_encabezado("Auditoría de Consistencia de Datos")
    datos     = cargar_datos()
    usuarios  = datos.get("usuarios", [])
    contactos = datos.get("contactos", [])
    print(f"\n  Leyendo agenda.json...  Usuarios: {len(usuarios)}  |  Contactos: {len(contactos)}\n")

    uce = [{"id": u.get("id","(sin id)"), "email": u.get("email","(sin email)"), "errores": e}
        for u in usuarios if (e := _validar_usuario(u))]
    cce = [{"id": c.get("id","(sin id)"), "nombre": f"{c.get('nombres','')} {c.get('apellidos','')}".strip(), "errores": e}
        for c in contactos if (e := _validar_contacto(c))]

    emails_dup = _duplicados(usuarios, "email", str.lower)
    ids_dup    = _duplicados(contactos, "id")

    for ed in emails_dup:
        _agregar_error_dup(uce, usuarios, "email", ed,
            f"E-mail duplicado: '{ed}' aparece en más de un usuario.", "email")
    for id_d in ids_dup:
        _agregar_error_dup(cce, contactos, "id", id_d,
            f"ID duplicado: '{id_d}' aparece en más de un contacto.")

    sin_errores = not uce and not cce
    reporte = {
        "fecha_auditoria":        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "estado_general":         "SIN ERRORES" if sin_errores else "SE ENCONTRARON ERRORES",
        "usuarios_con_errores":   uce,
        "contactos_con_errores":  cce,
        "resumen": {
            "total_usuarios":               len(usuarios),
            "total_contactos":              len(contactos),
            "usuarios_con_errores":         len(uce),
            "contactos_con_errores":        len(cce),
            "usuarios_con_email_duplicado": len(emails_dup),
            "contactos_con_id_duplicado":   len(ids_dup),
        },
    }

    with open(RUTA_REPORTE, "w", encoding="utf-8") as f:
        json.dump(reporte, f, ensure_ascii=False, indent=4)

    sep = "  " + "-" * 52
    print(sep)
    print(f"  {'RESULTADO DE LA AUDITORÍA':^52}")
    print(sep)
    for label, val in [("Fecha", reporte["fecha_auditoria"]), ("Estado", reporte["estado_general"])]:
        print(f"  {label:<28}: {val}")
    print(sep)
    for label, val in [("Total usuarios", len(usuarios)), ("Total contactos", len(contactos)),
                        ("Usuarios con errores", len(uce)), ("Contactos con errores", len(cce)),
                        ("E-mails duplicados (usuarios)", len(emails_dup)),
                        ("IDs duplicados (contactos)", len(ids_dup))]:
        print(f"  {label:<28}: {val}")
    print(sep)

    if sin_errores:
        print("  ✔  No se encontraron inconsistencias en los datos.")
    else:
        for titulo, lista, campo_id in [("USUARIOS", uce, "email"), ("CONTACTOS", cce, "nombre")]:
            if lista:
                print(f"\n  {titulo} CON PROBLEMAS:")
                for item in lista:
                    print(f"    • ID {item['id']} ({item.get(campo_id, '')}):")
                    for e in item["errores"]:
                        print(f"        - {e}")
    print(f"\n  Reporte guardado en: {os.path.abspath(RUTA_REPORTE)}\n")
