"""Contains the class Vaccination Appointment"""
import hashlib
from datetime import datetime

from freezegun import freeze_time

from uc3m_care.data.attribute.attribute_cancellation_type import CancellationType
from uc3m_care.data.attribute.attribute_date_signature import DateSignature
from uc3m_care.data.attribute.attribute_iso_date import AppointmentIsoDate
from uc3m_care.data.attribute.attribute_patient_system_id import PatientSystemId
from uc3m_care.data.attribute.attribute_phone_number import PhoneNumber
from uc3m_care.data.attribute.attribute_reason import Reason
from uc3m_care.data.vaccination_log import VaccinationLog
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.parser.appointment_json_parser import AppointmentJsonParser
from uc3m_care.parser.cancel_json_parser import CancelJsonParser
from uc3m_care.parser.reactivate_json_parser import ReactivateJsonParser
from uc3m_care.storage.appointments_json_store import AppointmentsJsonStore
from uc3m_care.data.attribute.attribute_reactivation_type import ReactivationType

#pylint: disable=too-many-instance-attributes
class VaccinationAppointment():
    """Class representing an appointment  for the vaccination of a patient"""

    def __init__( self, patient_sys_id, patient_phone_number, date ):
        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__patient_sys_id = PatientSystemId(patient_sys_id).value
        patient = VaccinePatientRegister.create_patient_from_patient_system_id(
            self.__patient_sys_id)
        self.__patient_id = patient.patient_id
        self.__phone_number = PhoneNumber(patient_phone_number).value
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        self.__appointment_date = datetime.fromisoformat(AppointmentIsoDate(date).value).timestamp()
        self.__date_signature = self.vaccination_signature
        self.__cancelled="active"
        self.__reason_to_cancel=""

    @property
    def cancelled( self ):
        """revoked property getter"""
        return self.__cancelled

    @cancelled.setter
    def cancelled( self, value ):
        self.__cancelled = CancellationType(value).value

    @property
    def reason( self ):
        """reason property getter"""
        return self.__reason_to_cancel

    @reason.setter
    def reason( self, value ):
        self.__reason_to_cancel = Reason(value).value

    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + self.__alg +",typ:" + self.__type +",patient_sys_id:" + \
               self.__patient_sys_id + ",issuedate:" + self.__issued_at.__str__() + \
               ",vaccinationtiondate:" + self.__appointment_date.__str__() + "}"

    @property
    def patient_id( self ):
        """Property that represents the guid of the patient"""
        return self.__patient_id

    @patient_id.setter
    def patient_id( self, value ):
        self.__patient_id = value

    @property
    def patient_sys_id(self):
        """Property that represents the patient_sys_id of the patient"""
        return self.__patient_sys_id
    @patient_sys_id.setter
    def patient_sys_id(self, value):
        self.__patient_sys_id = value

    @property
    def phone_number( self ):
        """Property that represents the phone number of the patient"""
        return self.__phone_number

    @phone_number.setter
    def phone_number( self, value ):
        self.__phone_number = PhoneNumber(value).value

    @property
    def vaccination_signature( self ):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @property
    def issued_at(self):
        """Returns the issued at value"""
        return self.__issued_at

    @issued_at.setter
    def issued_at( self, value ):
        self.__issued_at = value

    @property
    def appointment_date( self ):
        """Returns the vaccination date"""
        return self.__appointment_date

    @property
    def date_signature(self):
        """Returns the SHA256 """
        return self.__date_signature

    def save_appointment( self ):
        """saves the appointment in the appointments store"""
        appointments_store = AppointmentsJsonStore()
        appointments_store.add_item(self)

    def update_appointment( self ):
        """Updates the info of the appointment in the store"""
        appointments_store = AppointmentsJsonStore()
        appointments_store.update_item(self.__date_signature, self)

    def is_active( self ):
        """returns true if the appointment has not been cancelled"""
        #print(self.__cancelled)
        return self.__cancelled == "active"

    def cancel( self, cancellation_type, reason):
        """cancels the appoinmtent"""
        today = datetime.today().date()
        if self.is_active():
            today = datetime.today().date()
            date_patient = datetime.fromtimestamp(self.__appointment_date).date()
            if today < date_patient:
                self.__cancelled = CancellationType(cancellation_type).value
                self.__reason_to_cancel = Reason(reason).value
                self.update_appointment()
            else:
                raise VaccineManagementException("The appointment cannot be cancelled today")
        else:
            raise VaccineManagementException("Vaccine already cancelled")

    def reactivate( self, reactivation_type, newdate ):
        """reactivate the appoinmtent"""
        today = datetime.today().date()
        #cambiamos formato a timestamph
        newdate = datetime.fromisoformat(newdate).date()
        if self.__cancelled != "Final":
            today = datetime.today().date()
            if reactivation_type == "Normal":
                date_patient = datetime.fromtimestamp(self.__appointment_date).date()
                if today < date_patient:
                    self.__cancelled = "active"
                    self.update_appointment()
                else:
                    raise VaccineManagementException("The appointment cannot be retrieved today")
            else:
                if today < newdate:
                    self.__appointment_date = newdate
                    self.__cancelled = "active"
                    self.update_appointment()
        else:
            raise VaccineManagementException("Vaccine not temporally cancelled")

    @classmethod
    def get_appointment_from_date_signature( cls, date_signature ):
        """returns the vaccination appointment object for the date_signature received"""
        appointments_store = AppointmentsJsonStore()
        appointment_record = appointments_store.find_item(DateSignature(date_signature).value)
        if appointment_record is None:
            raise VaccineManagementException("date_signature is not found")
        freezer = freeze_time(
            datetime.fromtimestamp(appointment_record["_VaccinationAppointment__issued_at"]))
        freezer.start()
        appointment = cls(appointment_record["_VaccinationAppointment__patient_sys_id"],
                          appointment_record["_VaccinationAppointment__phone_number"],
                          datetime.fromtimestamp(
                              appointment_record
                              ["_VaccinationAppointment__appointment_date"]).date().isoformat())
        if appointment_record["_VaccinationAppointment__cancelled"] != "active":
            appointment.cancel(appointment_record["_VaccinationAppointment__cancelled"],
                               appointment_record["_VaccinationAppointment__reason_to_cancel"])
        freezer.stop()
        return appointment

    @classmethod
    def create_appointment_from_json_file( cls, json_file, date ):
        """returns the vaccination appointment for the received input json file"""
        appointment_parser = AppointmentJsonParser(json_file)
        new_appointment = cls(
            appointment_parser.json_content[appointment_parser.PATIENT_SYSTEM_ID_KEY],
            appointment_parser.json_content[appointment_parser.CONTACT_PHONE_NUMBER_KEY],
            date)
        return new_appointment

    @staticmethod
    def cancel_appointnmet_from_cancel_file( cancel_file ):
        """Cancels and appointment from a input file"""
        #print(cancel_file)
        cancel_key = CancelJsonParser(cancel_file).json_content
        #retrieve the appointment
        appointment = VaccinationAppointment.\
            get_appointment_from_date_signature(cancel_key[CancelJsonParser.DATE_SIGNATURE_KEY])
        #cancel the appoinment
        appointment.cancel(cancel_key[CancelJsonParser.CANCELLATION_KEY],
                           cancel_key[CancelJsonParser.REASON_KEY])
        return appointment


    @staticmethod
    def reactivate_appointment_from_json_file(json_file):
        """Check is appointment is cancelled and reactivates"""
        reactivation_key = ReactivateJsonParser(json_file).json_content
        appointment = VaccinationAppointment. \
            get_appointment_from_date_signature(reactivation_key[ReactivateJsonParser.DATE_SIGNATURE_KEY])
        appointment.reactivate(reactivation_key[ReactivateJsonParser.REACTIVATION_KEY], reactivation_key[ReactivateJsonParser.NEW_DATE_KEY])
        return appointment


    def is_valid_today( self ):
        """returns true if today is the appointment's date"""
        if not self.is_active():
            raise VaccineManagementException("The appointment was cancelled")
        today = datetime.today().date()
        date_patient = datetime.fromtimestamp(self.appointment_date).date()
        if date_patient != today:
            raise VaccineManagementException("Today is not the date")

        return True

    def register_vaccination( self ):
        """register the vaccine administration"""
        if self.is_valid_today():
            vaccination_log_entry = VaccinationLog(self.date_signature)
            vaccination_log_entry.save_log_entry()
        return True
