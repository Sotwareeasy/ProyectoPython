## Titulo del programa
app_titulo = "Gestor contactos - ACME Solution"
separador = "="*45
linea = "-"*45

## Mensajes para login
login_bienvenida ="\n Bienvenido, inicie sesion para continuar."
login_user =" Ingrese correo electrónico."
login_password = "Ingrese la contraseña."
login_exitoso = "Bienvenido"
login_fail = "Contraseña o clave inválida"
login_block ="Usuario bloqueado por intentos fallidos"

## Menu para admin
menu_admin = """
Administrador ACME Solutions
1. Contactos
2. Usuarios
3. Auditoria de datos
4. Salir
"""
## Menu de usuario
menu_operario= """
Menu Principal
1. Contactos
2. Salir
"""
##Menu contactos
menu_contact= """
1. Registrar contacto.
2. Listar Contacto.
3. Buscar Contacto.
4. Actualizar contacto.
5. Eliminar contacto.
6. Regresar menu principal.
"""
##Menu usuarios
menu_user= """
1. Registrar Usuario
2. Listar Usuarios
3. Actualizar usuario.
4. Eliminar usuario
5. Regresar al menu principal
"""
##Buscar contacto
search_contact= """
Escoja por que opción desea buscar el contacto:
1. Numero de identificacion
2. Nombre o apellidos
3. Tipo de contacto
4. Regresar al menu anterior
"""

invalid_option = " Opcion inválida, ingrese los datos de nuevo"
select_option = "Seleccione una opción: "

####Campos Contactos
campo_id ="Numero de identificacion : "
campo_nombre =" Nombres: "
campo_apellidos="Apellidos: "
campo_telefono= "Telefono: "
campo_email =" Correo electronico: "
campo_direccion = " Direccion: "
campo_rol= "Rol Admin u Operario: "
campo_password = " Contraseña : "
campo_tipo = "Ingrese el tipo de contacto: "
campo_notas=" Notas ó informacion adicional: "

confirm_delete=" ¿Desea eliminar este contacto: ?"
##Confirmacion de procesos
contact_registred = " Contacto registrado exitosamente"
contact_update = "Contacto actualizado exitosamente"
contact_deleted = "Contacto eliminado"
user_registred= " Usuario registrado exitosamente"
user_update = "Usuario registrado exitosamente"
user_deleted =" Usuario eliminado exitosamente"
operacion_cancelada ="Operacion Cancelada"

####Errores
contact_duplicate = "El numero de identificacion, ya está registrado"
user_duplicated = "Ya existe un usuario con ese numero de identificacion"
correo_duplicated = "El correo ya esta registrado"
correo_invalid = "El correo ingresado es invalido"
telefono_invalid = "El telefono solo puede contener numeros"
campo_empty =" Campo obligatorio"
rol_invalid ="Ingrese un rol valido"
contact_nofind=" No se encontro el contacto"
user_nofind="Usuario no encontrado"
contact_noresgistred= " No hay contactos registrados"
user_noregistred=" No hay usuarios registrados"
action_canceled=" Accion cancelada"
nodelete_admin ="No puede borrar el administrador"