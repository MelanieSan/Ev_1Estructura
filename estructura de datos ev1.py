import datetime
import random

class LimiteClavesException(Exception):
    pass

class Consultorio:
    def __init__(self, rango_clave_paciente=(1000, 9999)):
        self.pacientes = []
        self.citas = []
        self.rango_clave_paciente = rango_clave_paciente

    def generar_folio_cita(self):
        return random.randint(100000, 999999) 

    def generar_clave_paciente(self):
        return random.randint(self.rango_clave_paciente[0], self.rango_clave_paciente[1])

    def registrar_paciente(self):
        while True:
            try:
                primer_apellido = input("Ingrese el primer apellido del paciente: ")
                if not primer_apellido:
                    raise ValueError("Error: El primer apellido es obligatorio.")
                segundo_apellido = input("Ingrese el segundo apellido del paciente (puede omitirse): ")
                nombre = input("Ingrese el nombre del paciente: ")
                if not nombre:
                    raise ValueError("Error: Debe ingresar mínimo un nombre obligatoriamente.")
                fecha_nacimiento = input("Ingrese la fecha de nacimiento del paciente (MM/DD/YYYY): ")
                if not fecha_nacimiento:
                    raise ValueError("Error: Debe ingresar su fecha de nacimiento. Ingrese de nuevo su fecha.")

                clave_paciente = self.generar_clave_paciente()

                paciente = {
                    'clave_paciente': clave_paciente,
                    'primer_apellido': primer_apellido,
                    'segundo_apellido': segundo_apellido,
                    'nombre': nombre,
                    'fecha_nacimiento': fecha_nacimiento
                }
                self.pacientes.append(paciente)
                return clave_paciente
            except LimiteClavesException as e:
                print(e)
                return -1
            except ValueError as e:
                print(e)
                print("Por favor, ingrese los datos nuevamente.\n")

    def programar_cita(self, clave_paciente):
        while True:
            try:
                fecha_cita = input("Ingrese la fecha de la cita (MM/DD/YYYY): ")
                turno_cita = int(input("Ingrese el turno de la cita (1 - mañana, 2 - mediodía, 3 - tarde): "))
                
                if turno_cita not in [1, 2, 3]:
                    raise ValueError("Error al ingresar el dato. Debe ser en el turno 1, 2 o 3.")

                if not self.validar_fecha_cita(fecha_cita):
                    raise ValueError("Error: La fecha de la cita debe ser posterior al día actual y no mayor a 60 días")

                folio_cita = self.generar_folio_cita()
                cita = {
                    'folio_cita': folio_cita,
                    'clave_paciente': clave_paciente,
                    'turno_cita': turno_cita,
                    'fecha_cita': fecha_cita
                }
                self.citas.append(cita)
                return folio_cita
            except ValueError as e:
                print(e)

    def registrar_presentacion(self, folio_cita, clave_paciente):
        while True:
            try:
                peso = float(input("Ingrese el peso del paciente en kilogramos: "))
                estatura = float(input("Ingrese la estatura del paciente en centímetros: "))

                hora_llegada = datetime.datetime.now().strftime('%H:%M:%S')
                presentacion = {
                    'folio_cita': folio_cita,
                    'clave_paciente': clave_paciente,
                    'hora_llegada': hora_llegada,
                    'peso': peso,
                    'estatura': estatura
                }
                return presentacion
            except ValueError:
                print("Error: Ingrese un valor numérico válido para peso y estatura.")

    def validar_fecha_cita(self, fecha_cita):
        fecha_actual = datetime.datetime.now()
        fecha_cita = datetime.datetime.strptime(fecha_cita, '%m/%d/%Y')
        limite_superior = fecha_actual + datetime.timedelta(days=60)
        return fecha_actual < fecha_cita <= limite_superior

consultorio = Consultorio(rango_clave_paciente=(1000, 9999))
clave_paciente = consultorio.registrar_paciente()

if clave_paciente is not None:
    folio_cita = consultorio.programar_cita(clave_paciente)

    if folio_cita is not None:
        presentacion = consultorio.registrar_presentacion(folio_cita, clave_paciente)

        if presentacion is not None:
            print("Presentación del paciente")
            print(presentacion)