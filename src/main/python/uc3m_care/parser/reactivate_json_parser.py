"""Subclass of JsonParer for parsing inputs of get_vaccine_date"""
from uc3m_care.parser.json_parser import JsonParser

class ReactivateJsonParser(JsonParser):
    """Subclass of JsonParer for parsing inputs of get_vaccine_date"""
    BAD_REACTIVATION_TYPE_ERROR = "Bad label reactivation_type"
    BAD_DATE_SIGNATURE_LABEL_ERROR = "Bad label date_signature"
    DATE_SIGNATURE_KEY = "date_signature"
    REACTIVATION_KEY = "reactivation_type"
    NEW_DATE_KEY = "new_date"
    BAD_REACTIVATION_TYPE_ERROR = "JSON Decode Error - Wrong type"
    BAD_DATE_SIGNATURE_LABEL_ERROR = "JSON Decode Error - Wrong type"
    BAD_NEW_DATE_LABEL_ERROR = "JSON Decode Error - Wrong type"

    _JSON_KEYS = [DATE_SIGNATURE_KEY,
                   REACTIVATION_KEY,
                   NEW_DATE_KEY]
    _ERROR_MESSAGES = [ BAD_DATE_SIGNATURE_LABEL_ERROR,
                        BAD_REACTIVATION_TYPE_ERROR,
                        BAD_NEW_DATE_LABEL_ERROR ]
