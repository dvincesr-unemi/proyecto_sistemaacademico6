from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
# 1. Importamos HorarioController junto a los demas controladores
from views import EstudianteController, HorarioController, MateriaController, MatriculaController

# Se crea UN solo controlador de cada tipo.
# Inyeccion de dependencias:
# - Horarios se pasa a Materias para asignar franjas de clase.
# - Estudiantes y Materias se pasan a Matriculas (flujo 1 a 1 intacto).
horarios = HorarioController()                # <--- NUEVO CONTROLADOR
estudiantes = EstudianteController()
materias = MateriaController(horarios)        # <--- RECIBE A HORARIOS
matriculas = MatriculaController(estudiantes, materias)


# =====================================================================
# AYUDAS DE PANTALLA
# =====================================================================

def pausa():
    input("\nPresione Enter para continuar...")


def pedir_entero(etiqueta):
    """Devuelve un entero o None si el usuario escribio otra cosa."""
    try:
        return int(input(etiqueta))
    except ValueError:
        return None


def mostrar_resultado(exito, mensaje):
    # Los controladores devuelven la TUPLA (exito, mensaje)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)


def mostrar_lista(objetos, vacio="No hay registros todavia."):
    """Sirve para horarios, estudiantes, materias y matriculas: cada modelo sabe mostrarse."""
    if not objetos:
        imprimir_info(vacio)
        return
    for objeto in objetos:
        print(f"  {objeto}")
    imprimir_info(f"Total: {len(objetos)}")


def mostrar_detalle(objeto):
    # Recorre el DICCIONARIO del objeto: clave y valor a la vez
    for clave, valor in objeto.a_diccionario().items():
        print(f"  {str(clave).replace('_', ' ').capitalize():<16}: {valor}")


# =====================================================================
# MENU DE HORARIOS (NUEVO)
# =====================================================================

def crear_horario():
    imprimir_titulo("CREAR FRANJA HORARIA")
    datos = {
        "dia": input("Dia de la semana (ej. Lunes, Martes): "),
        "hora_inicio": input("Hora de inicio (ej. 07:00): "),
        "hora_fin": input("Hora de fin (ej. 09:00): "),
    }
    mostrar_resultado(*horarios.crear(datos))
    pausa()


def listar_horarios():
    imprimir_titulo("FRANJAS HORARIAS")
    mostrar_lista(horarios.leer(), "Todavia no hay horarios registrados.")
    pausa()


def buscar_horario():
    imprimir_titulo("BUSCAR HORARIO")
    termino = input("Dia o franja de hora: ")
    encontrados = horarios.buscar(termino)
    mostrar_lista(encontrados, f"Ningun horario coincide con '{termino}'.")
    pausa()


def ver_horario():
    imprimir_titulo("VER HORARIO POR ID")
    horario = horarios.obtener(pedir_entero("Id: "))
    if horario is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(horario)
        asignaturas = materias.por_horario(horario.id)
        print(f"\n  Materias dictadas en este horario ({len(asignaturas)}):")
        for m in asignaturas:
            print(f"    - [{m.codigo}] {m.nombre}")
    pausa()


def actualizar_horario():
    imprimir_titulo("ACTUALIZAR HORARIO")
    id_horario = pedir_entero("Id: ")
    horario = horarios.obtener(id_horario)
    if horario is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Editando: {horario.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("dia", "hora_inicio", "hora_fin"):
        actual = getattr(horario, campo)
        nuevo = input(f"{campo.replace('_', ' ').capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    mostrar_resultado(*horarios.actualizar(id_horario, cambios))
    pausa()


def eliminar_horario():
    imprimir_titulo("ELIMINAR HORARIO")
    id_horario = pedir_entero("Id: ")
    horario = horarios.obtener(id_horario)
    if horario is None:
        imprimir_error("No encontrado")
        return pausa()

    asignaturas = materias.por_horario(id_horario)
    if asignaturas:
        imprimir_info(f"Aviso: Hay {len(asignaturas)} materia(s) usando esta franja horaria.")

    imprimir_info(f"Se eliminara: {horario.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*horarios.eliminar(id_horario))
    else:
        imprimir_info("Operacion cancelada")
    pausa()


# =====================================================================
# MENU DE ESTUDIANTES (INTACTO)
# =====================================================================

def crear_estudiante():
    imprimir_titulo("CREAR ESTUDIANTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "carnet": input("Carnet: "),
        "carrera": input("Carrera: "),
    }
    mostrar_resultado(*estudiantes.crear(datos))
    pausa()


def listar_estudiantes():
    imprimir_titulo("ESTUDIANTES")
    mostrar_lista(estudiantes.leer(), "Todavia no hay estudiantes registrados.")
    pausa()


def buscar_estudiante():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, apellido, email, carnet o carrera: ")
    encontrados = estudiantes.buscar(termino)
    mostrar_lista(encontrados, f"Ningun estudiante coincide con '{termino}'.")
    pausa()


def ver_estudiante():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    estudiante = estudiantes.obtener(pedir_entero("Id: "))
    if estudiante is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(estudiante)
    pausa()


def actualizar_estudiante():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    id_estudiante = pedir_entero("Id: ")
    estudiante = estudiantes.obtener(id_estudiante)
    if estudiante is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Editando: {estudiante.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "apellido", "email", "carnet", "carrera"):
        actual = getattr(estudiante, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    mostrar_resultado(*estudiantes.actualizar(id_estudiante, cambios))
    pausa()


def eliminar_estudiante():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    id_estudiante = pedir_entero("Id: ")
    estudiante = estudiantes.obtener(id_estudiante)
    if estudiante is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Se eliminara: {estudiante.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*estudiantes.eliminar(id_estudiante))
    else:
        imprimir_info("Operacion cancelada")
    pausa()


# =====================================================================
# MENU DE MATERIAS (ADAPTADO CON HORARIOS)
# =====================================================================

def crear_materia():
    imprimir_titulo("CREAR MATERIA")
    
    # Mostramos los horarios disponibles para seleccionar
    imprimir_info("Horarios disponibles:")
    mostrar_lista(horarios.leer(), "No hay franjas registradas (se creara sin horario).")

    datos = {
        "nombre": input("\nNombre: "),
        "codigo": input("Codigo: "),
        "creditos": input("Creditos: "),
        "cupos": input("Cupos iniciales [Enter = 30]: "),
        "horario_id": pedir_entero("Id del horario (0 o vacio si aun no tiene): ") or 0,
    }
    mostrar_resultado(*materias.crear(datos))
    pausa()


def listar_materias():
    imprimir_titulo("MATERIAS")
    mostrar_lista(materias.leer(), "Todavia no hay materias creadas.")
    pausa()


def buscar_materia():
    imprimir_titulo("BUSCAR MATERIA")
    termino = input("Nombre o codigo: ")
    mostrar_lista(materias.buscar(termino), "Sin coincidencias.")
    pausa()


def ver_materia():
    imprimir_titulo("VER MATERIA POR ID")
    materia = materias.obtener(pedir_entero("Id: "))
    if materia is None:
        imprimir_error("No encontrado")
    else:
        mostrar_detalle(materia)
        hr_obj = horarios.obtener(materia.horario_id) if materia.horario_id else None
        info_hr = hr_obj.etiqueta() if hr_obj else "Sin horario asignado"
        print(f"  Franja Asignada : {info_hr}")
    pausa()


def actualizar_materia():
    imprimir_titulo("ACTUALIZAR MATERIA")
    id_materia = pedir_entero("Id: ")
    materia = materias.obtener(id_materia)
    if materia is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Editando: {materia.etiqueta()}")
    print("Deje en blanco lo que no quiera cambiar.\n")

    cambios = {}
    for campo in ("nombre", "codigo", "creditos", "cupos"):
        actual = getattr(materia, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo:
            cambios[campo] = nuevo

    # Opcion para cambiar el horario asociado
    cambio_hr_id = input(f"Horario ID [{materia.horario_id}]: ").strip()
    if cambio_hr_id:
        try:
            cambios["horario_id"] = int(cambio_hr_id)
        except ValueError:
            imprimir_error("El ID de horario debe ser un numero")
            return pausa()

    mostrar_resultado(*materias.actualizar(id_materia, cambios))
    pausa()


def eliminar_materia():
    imprimir_titulo("ELIMINAR MATERIA")
    id_materia = pedir_entero("Id: ")
    materia = materias.obtener(id_materia)
    if materia is None:
        imprimir_error("No encontrado")
        return pausa()

    imprimir_info(f"Se eliminara: {materia.etiqueta()}")
    if confirmar("¿Confirma?"):
        mostrar_resultado(*materias.eliminar(id_materia))
    else:
        imprimir_info("Operacion cancelada")
    pausa()


# =====================================================================
# MENU DE MATRICULAS (TRANSACCIONAL 1 A 1 INTACTO)
# =====================================================================

def registrar_matricula():
    imprimir_titulo("REGISTRAR MATRICULA")
    imprimir_info("Estudiantes:")
    mostrar_lista(estudiantes.leer())
    imprimir_info("Materias:")
    mostrar_lista(materias.leer())

    datos = {
        "estudiante_id": pedir_entero("\nId del estudiante: "),
        "materia_id": pedir_entero("Id de la materia: "),
        "periodo": input("Periodo (ej. 2026-1): "),
    }
    
    if None in (datos["estudiante_id"], datos["materia_id"]):
        imprimir_error("Los IDs deben ser numeros enteros")
        return pausa()

    mostrar_resultado(*matriculas.crear(datos))
    pausa()


def listar_matriculas():
    imprimir_titulo("MATRICULAS ACTIVAS")
    mostrar_lista(matriculas.leer(), "Todavia no hay inscripciones.")
    pausa()


def asentar_calificacion():
    imprimir_titulo("ASENTAR CALIFICACION")
    id_matricula = pedir_entero("Id de la matricula: ")
    if not id_matricula:
        return pausa()
        
    nota = input("Ingrese la nota (0 a 20): ")
    mostrar_resultado(*matriculas.actualizar(id_matricula, {"nota": nota}))
    pausa()


def ver_reporte():
    imprimir_titulo("REPORTE ACADEMICO")
    texto = matriculas.reporte_academico(pedir_entero("Id del estudiante: "))
    if texto is None:
        imprimir_error("El estudiante no existe.")
    else:
        print(texto)
    pausa()


def anular_matricula():
    imprimir_titulo("ANULAR MATRICULA")
    id_matricula = pedir_entero("Id de la matricula: ")
    if id_matricula and confirmar("Se liberara el cupo. ¿Confirma?"):
        mostrar_resultado(*matriculas.eliminar(id_matricula))
    else:
        imprimir_info("Operacion cancelada")
    pausa()


def resumen():
    imprimir_titulo("RESUMEN GENERAL")
    print(f"  Horarios    : {len(horarios.leer())}")
    print(f"  Estudiantes : {len(estudiantes.leer())}")
    print(f"  Carreras    : {', '.join(estudiantes.carreras_registradas()) or '-'}")
    print(f"  Materias    : {len(materias.leer())}")
    
    llenas = [m for m in materias.leer() if not m.hay_cupo()]
    print(f"  Sin cupos   : {', '.join(m.codigo for m in llenas) or 'ninguna'}")
    print(f"  Matriculas  : {len(matriculas.leer())}")
    pausa()


# =====================================================================
# MENUS: DICCIONARIOS tecla -> (texto, funcion)
# =====================================================================

MENU_HORARIOS = {
    "1": ("Crear horario", crear_horario),
    "2": ("Ver todos", listar_horarios),
    "3": ("Buscar", buscar_horario),
    "4": ("Ver por id", ver_horario),
    "5": ("Actualizar", actualizar_horario),
    "6": ("Eliminar", eliminar_horario),
    "0": ("Volver", None),
}

MENU_ESTUDIANTES = {
    "1": ("Crear estudiante", crear_estudiante),
    "2": ("Ver todos", listar_estudiantes),
    "3": ("Buscar", buscar_estudiante),
    "4": ("Ver por id", ver_estudiante),
    "5": ("Actualizar", actualizar_estudiante),
    "6": ("Eliminar", eliminar_estudiante),
    "0": ("Volver", None),
}

MENU_MATERIAS = {
    "1": ("Crear materia", crear_materia),
    "2": ("Ver todas", listar_materias),
    "3": ("Buscar", buscar_materia),
    "4": ("Ver por id", ver_materia),
    "5": ("Actualizar", actualizar_materia),
    "6": ("Eliminar", eliminar_materia),
    "0": ("Volver", None),
}

MENU_MATRICULAS = {
    "1": ("Inscribir estudiante", registrar_matricula),
    "2": ("Ver todas", listar_matriculas),
    "3": ("Asentar calificacion", asentar_calificacion),
    "4": ("Ver reporte academico", ver_reporte),
    "5": ("Anular matricula", anular_matricula),
    "0": ("Volver", None),
}


def ejecutar_menu(titulo, opciones):
    """Un solo bucle para los submenus."""
    while True:
        imprimir_titulo(titulo)
        for tecla, (texto, _funcion) in opciones.items():
            print(f"  {tecla}. {texto}")
        print()

        tecla = input("Opcion: ").strip()
        if tecla not in opciones:
            imprimir_error("Opcion no valida")
            pausa()
            continue

        _texto, funcion = opciones[tecla]
        if funcion is None:
            break
        funcion()


def main():
    while True:
        imprimir_titulo("SISTEMA ACADEMICO")
        print("  1. Estudiantes")
        print("  2. Horarios")       # <--- NUEVA OPCION EN EL MENU
        print("  3. Materias")
        print("  4. Matriculas")
        print("  5. Resumen")
        print("  0. Salir\n")

        tecla = input("Opcion: ").strip()
        if tecla == "1":
            ejecutar_menu("GESTION DE ESTUDIANTES", MENU_ESTUDIANTES)
        elif tecla == "2":
            ejecutar_menu("GESTION DE HORARIOS", MENU_HORARIOS)
        elif tecla == "3":
            ejecutar_menu("GESTION DE MATERIAS", MENU_MATERIAS)
        elif tecla == "4":
            ejecutar_menu("GESTION DE MATRICULAS", MENU_MATRICULAS)
        elif tecla == "5":
            resumen()
        elif tecla == "0":
            imprimir_info("¡Hasta luego! 👋")
            break
        else:
            imprimir_error("Opcion no valida")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")