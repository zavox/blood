# -*- coding: UTF-8 -*-
import os
import time
from validation import Validate
from functions import Donor
import csv
import pydoc
from operator import attrgetter
from constant_variables import *
clear = lambda: os.system('cls')


class DonorManager():
    @staticmethod
    def data_in(donor, validate, input_mess, error_mess):
        valid_input = ""
        while not valid_input:
            clear()
            if donor.name != "":
                print(donor)
            valid_input = input(input_mess)
            if validate(valid_input):
                return valid_input.upper()
            else:
                print(error_mess)
                valid_input = ""
                time.sleep(2)

    @staticmethod
    def print_sorted_donor_list(donor_objects, input_string):
        if input_string not in ("2", "13"):
            input_donor_data_pairs = {"1": "name", "3": "gender", "4": "dateofbirth", "5": "lastdonationdate",
                                      "6": "wassick", "7": "uniqueid", "8": "expofid", "9": "bloodtype",
                                      "10": "hemoglobin", "11": "emailaddress", "12": "mobilnumber"}
            list_to_print = sorted(donor_objects, key=attrgetter(input_donor_data_pairs[input_string]))
        elif input_string == "2":
            list_to_print = sorted(donor_objects, key=lambda x: int(x.weight))
        elif input_string == "13":
            list_to_print = sorted(donor_objects, key=lambda x: int(x.age))
        text = ""
        for don in list_to_print:
            text += "------------------------------\n"
            text += don.data_out()+"\n"
        text += "------------------------------\n"
        pydoc.pager(text)
        input("\n Press (ENTER) to go back")
        clear()

    @staticmethod
    def add_new_donor():
        print("Adding new donor...\n")
        time.sleep(1)
        clear()

        donor_sample = Donor()
        donor_sample.name = DonorManager.data_in(donor_sample, Validate.validate_name, "Name: ", NAME_ERR)
        donor_sample.weight = DonorManager.data_in(donor_sample, Validate.validate_positive_int, "Weight (in KG): ", POSINT_ERR)
        donor_sample.gender = DonorManager.data_in(donor_sample, Validate.validate_gender, "Gender (M/F): ", GEND_ERR)
        donor_sample.dateofbirth = DonorManager.data_in(donor_sample, Validate.validate_date, "Date of Birth: ", DATE_ERR)
        donor_sample.lastdonationdate = DonorManager.data_in(donor_sample, Validate.validate_date, "Last Donation: ", DATE_ERR)

        if not donor_sample.is_suitable():
            print("\n\t - It seems your donor is not suitable for the donation. =( - ")
            input("\n\n (Press ENTER to go BACK)")
            clear()
            return None

        donor_sample.wassick = DonorManager.data_in(donor_sample, Validate.validate_sickness, "Was he/she sick in the last month? (Y/N) ", SICK_ERR)
        donor_sample.uniqueid = DonorManager.data_in(donor_sample, Validate.validate_id, "Unique ID: ", ID_ERR)
        donor_sample.bloodtype = DonorManager.data_in(donor_sample, Validate.validate_blood_type, "Blood Type: ", BTYPE_ERR)
        donor_sample.expofid = DonorManager.data_in(donor_sample, Validate.validate_date, "Expiration of ID: ", DATE_ERR)
        donor_sample.emailaddress = DonorManager.data_in(donor_sample, Validate.validate_email, "Email address: ", EMAIL_ERR)
        donor_sample.mobilnumber = DonorManager.data_in(donor_sample, Validate.validate_mobilnumber, "Mobile Number: ", MOBILE_ERR)

        with open("Data/donors.csv", "a") as f:
            f.write(donor_sample.name+",")
            f.write(donor_sample.weight+",")
            f.write(donor_sample.gender+",")
            f.write(donor_sample.dateofbirth+",")
            f.write(donor_sample.lastdonationdate+",")
            f.write(donor_sample.wassick+",")
            f.write(donor_sample.uniqueid+",")
            f.write(donor_sample.expofid+",")
            f.write(donor_sample.bloodtype+",")
            f.write(donor_sample.generate_hemoglobin_level()+",")
            f.write(donor_sample.emailaddress+",")
            f.write(donor_sample.mobilnumber+"\n")

        print("\n - Your donor is added to the csv -\n\n Going back to main menu...")
        time.sleep(2.5)
        clear()

    @staticmethod
    def delete_donor():
        while True:
            try:
                with open("Data/donors.csv", "r") as f:
                    content=[]
                    for line in f:
                        content.append(line.strip())
                ids = [content[i].split(',')[6] for i in range(len(content)) if i != 0]
                print(ids, "(0) Cancel")
                user_input = input("Enter donor's ID or passport number: ").upper()
                if user_input=='0':
                    clear()
                    break
                elif not Validate.validate_id(user_input):
                    print("\n\tWrong ID or Passport number, enter a real value")
                    time.sleep(2)
                    clear()
                    continue
                elif user_input not in ids:
                    print("\n\tID is valid, but there is no entry with this ID yet.")
                    time.sleep(2)
                    clear()
                    continue
                else:
                    print("Deleting entry...")
                    with open("Data/donors.csv", "w") as f:
                        for line in content:
                            if user_input != line.split(",")[6]:
                                f.write(line+"\n")
                    time.sleep(1)
                print("Done!")
                input()
                clear()
                break
            except Exception as e:
                print(e)
                print("\n\t! ! !  Belso Error ! ! ! ")
                input()
                clear()

    @staticmethod
    def list_donors():
        with open("Data/donors.csv", "r") as f:
            donor_list = list(csv.reader(f))
        del(donor_list[0])
        if len(donor_list) < 1:
            print("\n No entry found\n")
            input("\n Press (ENTER) to go back")
            clear()
            return None
        else:
            donor_object_list = []
            for l in donor_list:
                next_donor = Donor()
                next_donor.name = l[0]
                next_donor.weight = l[1]
                next_donor.gender = l[2]
                next_donor.dateofbirth = l[3]
                next_donor.lastdonationdate = l[4]
                next_donor.wassick = l[5]
                next_donor.uniqueid = l[6]
                next_donor.expofid = l[7]
                next_donor.bloodtype = l[8]
                next_donor.hemoglobin = l[9]
                next_donor.emailaddress = l[-2]
                next_donor.mobilnumber = l[-1]
                next_donor.age = next_donor.donor_age()
                donor_object_list.append(next_donor)

            sort_by_input = input("Please choose the criteria by which you would like to sort the list: "
                            "\n\n(ENTER) or (1) by name\n(2) by weight\n(3) by gender\n(4) by birth date"
                            "\n(5) by date of last donation\n(6) by health status in last month"
                            "\n(7) by ID or Passport number\n(8) by expiration date of ID"
                            "\n(9) by blood type\n(10) by hemoglobin\n(11) by e-mail address"
                            "\n(12) by mobile number\n(13) by age\n(0) Cancel\n\n> ")
            clear()

            if sort_by_input == "":
                sort_by_input = "1"
            if sort_by_input.isdigit() and int(sort_by_input) in range(1, 14):
                DonorManager.print_sorted_donor_list(donor_object_list, sort_by_input)
                return None
            elif sort_by_input == "0":
               clear()
               return None

            else:
                print("\n\t\t! ! !  Please choose from the given numbers.  ! ! !\t\t\n ")
                time.sleep(1.5)
                clear()

    @staticmethod
    def search_in_donors():
        with open("Data/donors.csv", "r") as f:
            content = []
            for line in f:
                content.append(line.strip())
        del(content[0])
        if len(content) < 1:
            print("\n No entry found\n")
            input("\n Press (ENTER) to go back")
            clear()
            return None
        else:
            string_to_search = input("Search for donor: ")
            found_items = []
            for donor in content:
                if string_to_search.upper() in donor:
                    found_items.append(donor)
            donor_object_list = []
            for i in found_items:
                l = i.split(",")
                donor_object_list.append(Donor())
                donor_object_list[-1].name = l[0]
                donor_object_list[-1].weight = l[1]
                donor_object_list[-1].dateofbirth = l[3]
                donor_object_list[-1].emailaddress = l[-2]
                donor_object_list[-1].age = donor_object_list[-1].donor_age()
            szoveg = ""
            for i in donor_object_list:
                szoveg += "------------------------------\n"
                szoveg += i.data_out()+"\n"
            szoveg += "------------------------------\n"
            pydoc.pager(szoveg)

            input("\n Press (ENTER) to go back")
            clear()

    @staticmethod
    def change_donor_data(data_input):
        with open('Data/donors.csv', 'r') as f:
            donor_list = list(csv.reader(f))
        del(donor_list[0])

        if data_input in [i[6] for i in donor_list]:
            for i, l in enumerate(donor_list):
                if data_input == l[6]:
                    next_donor = Donor()
                    next_donor.name = l[0]
                    next_donor.weight = l[1]
                    next_donor.gender = l[2]
                    next_donor.dateofbirth = l[3]
                    next_donor.lastdonationdate = l[4]
                    next_donor.wassick = l[5]
                    next_donor.uniqueid = l[6]
                    next_donor.expofid = l[7]
                    next_donor.bloodtype = l[8]
                    next_donor.hemoglobin = l[9]
                    next_donor.emailaddress = l[-2]
                    next_donor.mobilnumber = l[-1]
                    print(next_donor)
                    line_number = i

        else:
            print("Data entry doesn't exist with that ID.")
            time.sleep(1)

        which = input("\nWhich data you want to modify?"
                        "\n\n(1) Name\n(2) Weight\n(3) Gender\n(4) Birth date"
                        "\n(5) Date of last donation\n(6) Health status in last month"
                        "\n(7) ID or Passport number\n(8) Expiration date of ID"
                        "\n(9) Blood type\n(10) Hemoglobin\n(11) E-mail address"
                        "\n(12) Mobile number\n(0) Cancel\n\n> ")
        if which == '0':
            return None
        input_donor_data_pairs = {"1": "name", "2": "weight", "3": "gender", "4": "dateofbirth", "5": "lastdonationdate",
                                  "6": "wassick", "7": "uniqueid", "8": "expofid", "9": "bloodtype",
                                  "10": "hemoglobin", "11": "emailaddress", "12": "mobilnumber"}
        which_donor_data_validation = {"1": Validate.validate_name, "2": Validate.validate_positive_int, "3": Validate.validate_gender, "4": Validate.validate_date, "5": Validate.validate_date,
                                  "6": Validate.validate_sickness, "7": Validate.validate_id, "8": Validate.validate_date, "9": Validate.validate_blood_type,
                                  "10": Validate.validate_positive_int, "11": Validate.validate_email, "12": Validate.validate_mobilnumber}

        new = ""
        while new == "":
            clear()
            print(next_donor)
            new = input("\n{}: ".format(input_donor_data_pairs[which]))
            if which_donor_data_validation[which](new):
                with open("Data/donors.csv", "w") as f:
                    donor_list[line_number][int(which)-1] = new.upper()
                    f.write(DONORS_ELSOSOR)
                    for line in donor_list:
                        for i in range(len(line)):
                            f.write(line[i])
                            if i < len(line)-1:
                                f.write(',')
                        f.write('\n')
                print('\n...Done!')
                time.sleep(1)
                break
            else:
                print("Wrong input")
                new = ""
                time.sleep(1)





