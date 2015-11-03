# -*- coding: UTF-8 -*-


class ValidateName():
    @staticmethod
    def valid_gender(gender_string):
        return gender_string.upper() == "F" or gender_string.upper() == "M"
    @staticmethod
    def validate_name(name_string):
        name = name_string.split()
        return name_string.isalpha() and len(name) > 1