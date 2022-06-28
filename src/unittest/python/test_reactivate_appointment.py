"""Tests for cancel_appointment method"""
import unittest
from unittest import TestCase
from freezegun import freeze_time
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH, JSON_FILES_RF3_PATH, JSON_FILES_RF2_PATH
from uc3m_care import AppointmentsJsonStore
from uc3m_care import PatientsJsonStore

param_list_nok = [("REV 1",
                   "Node1_Deleted.json",
                   "JSON Decode Error - Wrong JSON Format"),
                    ("REV 5",
                     "Node2_Deleted.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 6",
                     "Node2_Duplicated.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 7",
                     "Node3_Deleted.json",
                     "JSON Decode Error - Wrong type"),

                    ("REV 9",
                     "Node4_Deleted.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 10",
                     "Node4_Duplicated.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 11",
                     "Node5_Modified.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 12",
                     "Node6_Deleted.json",
                     "JSON Decode Error - Wrong JSON Format"),
                    ("REV 14",
                     "Node14_Duplicated.json",
                     "JSON Decode Error - Wrong JSON Format"),
                ]


class TestCancelAppointment(TestCase):
    """test class for open_door"""
    # pylint: disable=no-member

    @freeze_time("2022-03-08")
    def setUp(self) -> None:
        """Removing the Stores and creating required AccessRequest for testing"""
        # first af all, i introduce all value tha I need for the structural testing
        # remove the old storeKeys
        #print("Setup")
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        my_manager.get_vaccine_date(file_test, "2022-03-18")


    @freeze_time("2022-03-17")
    def test_parametrized_cases_tests(self):
        """Casos no validos de equivalencia, no estan todos, he incluido algunos"""
        my_file_cancel = JSON_FILES_PATH + "cancel_files/" + "cancel_temporal.json"
        my_manager = VaccineManager()
        my_manager.cancel_appointment(my_file_cancel)
        for test_id, file_test, result in param_list_nok:
            file_name = JSON_FILES_PATH + "CasosPrueba/" + file_test
            print("Param:" + test_id + "-")
            with self.assertRaises(VaccineManagementException) as c_m:
                my_manager.reactivate_appointment(file_name)
            self.assertEqual(c_m.exception.message, result)

    @freeze_time("2022-03-17")
    def test_reactivate_normal_ok(self):
        """Caso valido 1, correcto"""
        my_file_re = JSON_FILES_RF3_PATH + "Valid_Case_1.json"
        my_file_cancel = JSON_FILES_PATH + "cancel_files/" + "cancel_temporal.json"

        my_manager = VaccineManager()
        #primero cancelamos
        my_manager.cancel_appointment(my_file_cancel)
        #reactivamos despues
        result = my_manager.reactivate_appointment(my_file_re)
        self.assertEqual("5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c", result)
        keys_store = AppointmentsJsonStore()
        reactivate_key = keys_store.find_item(
            "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertEqual(reactivate_key["_VaccinationAppointment__cancelled"], "active")

    #cita newdate no valida

    @freeze_time("2022-03-17")
    def test_reactivate_newdate_ok(self):
        """Caso valido 2, no corregido, no entiendo el fallo, lee mal el json cuando tiene bien el formato"""
        my_file_re = JSON_FILES_RF3_PATH + "Valid_Case_2.json"
        my_file_cancel = JSON_FILES_PATH + "cancel_files/" + "cancel_temporal.json"

        my_manager = VaccineManager()
        # primero cancelamos
        my_manager.cancel_appointment(my_file_cancel)
        # reactivamos despues
        result = my_manager.reactivate_appointment(my_file_re)

        self.assertEqual("5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c", result)
        keys_store = AppointmentsJsonStore()
        reactivate_key = keys_store.find_item(
            "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertEqual(reactivate_key["_VaccinationAppointment__cancelled"], "active")

    @freeze_time("2022-03-17")
    def test_reactivate_cita_sin_cancelar(self):
        """Caso valido de reactivacion de cita no cancelada, correcto"""
        my_file_re = JSON_FILES_RF3_PATH + "Valid_Case_1.json"
        my_manager = VaccineManager()
        # primero cancelamos
        # reactivamos despues
        result = my_manager.reactivate_appointment(my_file_re)
        self.assertEqual("5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c", result)
        keys_store = AppointmentsJsonStore()
        reactivate_key = keys_store.find_item(
            "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        self.assertEqual(reactivate_key["_VaccinationAppointment__cancelled"], "active")

    @freeze_time("2022-03-17")
    def test_reactivate_final_no_ok(self):
        """Caso no valido reactivar cita con cancelacion final, correcto"""
        my_file_re = JSON_FILES_RF3_PATH + "Valid_Case_1.json"
        my_file_cancel = JSON_FILES_PATH + "cancel_files/" + "cancel_final.json"

        my_manager = VaccineManager()
        # primero cancelamos
        my_manager.cancel_appointment(my_file_cancel)
        # reactivamos despues
        with self.assertRaises(VaccineManagementException) as c_m:
            result = my_manager.reactivate_appointment(my_file_re)
        self.assertEqual(c_m.exception.message, "Vaccine not temporally cancelled")

    @freeze_time("2022-03-17")
    def test_reactivate_citapasada(self):
        """Caso no valido reactivar cita pasada, no correcto, no encuentra el archivo"""
        my_file_re = JSON_FILES_RF3_PATH + "citapasada.json"
        my_file_cancel = JSON_FILES_PATH + "cancel_files/" + "cancel_temporal.json"

        my_manager = VaccineManager()
        # primero cancelamos
        my_manager.cancel_appointment(my_file_cancel)
        # reactivamos despues
        with self.assertRaises(VaccineManagementException) as c_m:
            result = my_manager.reactivate_appointment(my_file_re)
        self.assertEqual(c_m.exception.message, "Vaccine not temporally cancelled")


