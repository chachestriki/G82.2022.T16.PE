"""Module """

from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.data.vaccination_appointment import VaccinationAppointment

class VaccineManager:
    """Class for providing the methods for managing the vaccination process"""

    # pylint: disable=invalid-name
    class __VaccineManager:
        def __init__(self):
            pass

        #pylint: disable=too-many-arguments
        # pylint: disable=no-self-use
        def request_vaccination_id (self, patient_id,
                                    name_surname,
                                    registration_type,
                                    phone_number,
                                    age):
            """Register the patinent into the patients file"""
            my_patient = VaccinePatientRegister(patient_id,
                                                    name_surname,
                                                    registration_type,
                                                    phone_number,
                                                    age)

            my_patient.save_patient()
            return my_patient.patient_sys_id

        def get_vaccine_date (self, input_file, date):
            """Gets an appointment for a registered patient"""
            my_sign= VaccinationAppointment.create_appointment_from_json_file(input_file, date)
            #save the date in store_date.json
            my_sign.save_appointment()
            return my_sign.date_signature

        def vaccine_patient(self, date_signature):
            """Register the vaccination of the patient"""
            appointment = VaccinationAppointment.get_appointment_from_date_signature(date_signature)
            return appointment.register_vaccination()

        def cancel_appointment(self, input_file):
            """Cancel de appointment received in the input file"""
            appointment = VaccinationAppointment.cancel_appointnmet_from_cancel_file(input_file)
            return appointment.date_signature

        def reactivate_appointment(self, input_file):
            """Reactivate the cancelled dates and can change its date"""
            appointment = VaccinationAppointment.reactivate_appointment_from_json_file(input_file)

    instance = None

    def __new__ ( cls ):
        if not VaccineManager.instance:
            VaccineManager.instance = VaccineManager.__VaccineManager()
        return VaccineManager.instance

    def __getattr__ ( self, nombre ):
        return getattr(self.instance, nombre)

    def __setattr__ ( self, nombre, valor ):
        return setattr(self.instance, nombre, valor)



    """[6:37 p. m., 26/6/2022] Diego Informática: A ver, no te quiero pasar código por si acaso al guiarte con mi código al profesor le parece que nos hemos copiado, pero básicamente tienes que hacer las comprobaciones que te dice el enunciado. Primero, tienes que comprobar si la cita se ha cancelado de tipo Final, porque entonces tienes que lanzar excepción. Si no lo es, tienes que mirar si la reactivacnón es Normal o NewDate, y seguir el enunciado en lo que dice de cada caso. Y al final, tienes que hacer un update (como en el cancel) para que los cambios que has hecho sobre la cita se guarden en el fichero de citas
[6:38 p. m., 26/6/2022] Diego Informática: Es mucho texto, pero básicamente es seguir lo que te dice el enunciado
como accedo al json para ver si pone final o temporal

Mira el método is_active del vaccination apppintment, y mira como lo usa el método cancel. Yo he hecho lo mismo, pero en vez de comprobar si esta activo, compruebo si pone final tengo dos métodos para la reactivacion dentro del vaccination appointment, uno que es igual que el metodo cancel_appointment_from_cancel_file pero cambiando los nombres de todo lo que se usa para reactivar en vez de cancelar, y tengo otro que es el reactivate, que es el que he modificado a partir del cancel. Mira como hace las cosas el método cancel, y haz las que necesites de la misma forma pero en el reactivate
 En plan, mira como accede a los parámetros el metodo cancel. Por eso digo que si analizas como funciona el cancel, el reactivate es muy simple de hacer"""
