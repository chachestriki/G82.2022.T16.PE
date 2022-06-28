"""Tests for cancel_appointment method"""
import unittest
from unittest import TestCase
from freezegun import freeze_time
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH, JSON_FILES_RF3_PATH, JSON_FILES_RF2_PATH
from uc3m_care import AppointmentsJsonStore
from uc3m_care import PatientsJsonStore


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
    def test_reactivate_temporal_ok(self):
        """path: regex ok , key is found , key is not expired, guest"""
        my_file_re = JSON_FILES_RF3_PATH + "Valid_Case_1.json"
        my_file_cancel = JSON_FILES_PATH + "cancel_files/" + "cancel_temporal.json"

        my_manager = VaccineManager()
        #primero cancelamos
        my_manager.cancel_appointment(my_file_cancel)
        #reactivamos despues
        result = my_manager.reactivate_appointment(my_file_re)
        self.assertEqual("5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c", result)

