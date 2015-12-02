# -*- coding: UTF-8 -*-
import os
import time
from validation import Validate
from functions import Event
import csv
from collections import deque
import pydoc
from operator import attrgetter
from constant_variables import *
clear = lambda: os.system('cls')


class EventManager():
    @staticmethod
    def data_in_e(event, validate, input_mess, error_mess):
        valid_input = ""
        while not valid_input:
            clear()
            if event.date_of_event != "":
                print(event)
            valid_input = input(input_mess)
            if validate(valid_input):
                return valid_input.upper()
            else:
                print(error_mess)
                valid_input = ""
                time.sleep(2)

    @staticmethod
    def put_string_in_quotes_if_has_comma(text):
        if ',' in text:
            return '"' + text + '"'
        else:
            return text

    @staticmethod
    def event_id_generator(donations_csv):
        with open(donations_csv, 'r') as f:
            last_line_list = deque(csv.reader(f), 1)[0]
            if last_line_list[0] == "id":
                return 1
            if last_line_list and last_line_list[0].isdigit():
                return int(last_line_list[0]) + 1
            else:
                return -100

    @staticmethod
    def store_donation_data(donation_object):
        id_int = EventManager.event_id_generator("Data/donations.csv")
        donation_sample = ""
        donation_sample += str(id_int) + "," + str(donation_object.date_of_event) + "," + str(donation_object.start_time) +\
                           "," + str(donation_object.end_time) + "," + str(donation_object.zip_code) + "," + \
                           str(donation_object.city) + "," + EventManager.put_string_in_quotes_if_has_comma(donation_object.address) + \
                           "," + str(donation_object.available_beds) + "," + str(donation_object.planned_donor_number) + \
                           "," + str(donation_object.successfull) + "\n"
        with open("Data/donations.csv", "a") as donations:
            donations.writelines(donation_sample)

    @staticmethod
    def print_sorted_donation_list(event_objects, input_string):
        if input_string not in ("4", "7", "8", "9"):
            input_donation_data_pairs = {"1": "date_of_event", "2": "start_time", "3": "end_time", "5": "city", "6": "address"}
            list_to_print = sorted(event_objects, key=attrgetter(input_donation_data_pairs[input_string]))
        elif input_string == "4":
            list_to_print = sorted(event_objects, key=lambda x: int(x.zip_code))
        elif input_string == "7":
            list_to_print = sorted(event_objects, key=lambda x: int(x.available_beds))
        elif input_string == "8":
            list_to_print = sorted(event_objects, key=lambda x: int(x.planned_donor_number))
        elif input_string == "9":
            list_to_print = sorted(event_objects, key=lambda x: int(x.successfull))
        szoveg = ""
        for eve in list_to_print:
            szoveg += "------------------------------\n"
            szoveg += "ID: " + eve.id + "\n"
            szoveg += str(eve)+"\n"
        szoveg += "------------------------------\n"
        pydoc.pager(szoveg)
        input("\n Press (ENTER) to go back")
        clear()

    @staticmethod
    def add_new_donation_event():
        print("Adding new event...\n")
        time.sleep(1)
        clear()
        e1 = Event()
        while True:
            e1.date_of_event = input("Date of Event: ")
            if Validate.validate_date(e1.date_of_event) and e1.registration_in_tendays():
                pass
            else:
                print("\n\t ! The registration should be at least 10 days from now. ! ")
                print("\t   ! Use this format to enter date: 'YYYY.MM.DD' ! \n")
                time.sleep(2)
                clear()
                continue

            e1.start_time = EventManager.data_in_e(e1, Validate.validate_time, "Start Time: ", TIME_ERR)
            e1.end_time = EventManager.data_in_e(e1, Validate.validate_time, "End Time: ", TIME_ERR)
            while not e1.is_starttime_before_endtime():
                print("\n\t ! The starting time should be before the ending time. ! ")
                time.sleep(2)
                clear()
                e1.end_time = ""
                e1.end_time = EventManager.data_in_e(e1, Validate.validate_time, "End Time: ", TIME_ERR)

            e1.zip_code = EventManager.data_in_e(e1, Validate.validate_zipcode, "ZIP code: ", ZIP_ERR)
            e1.city = EventManager.data_in_e(e1, Validate.validate_city_name, "City: ", CITY_ERR)
            e1.address = EventManager.data_in_e(e1, Validate.validate_address, "Address of event: ", ADDRESS_ERR)
            e1.available_beds = EventManager.data_in_e(e1, Validate.validate_positive_int, "Available beds: ", POSINT_ERR)
            e1.planned_donor_number = EventManager.data_in_e(e1, Validate.validate_positive_int, "Planned donor number: ", POSINT_ERR)

            e1.successfull = EventManager.data_in_e(e1, Validate.validate_positive_int, "\n How many successfull donation was on the event?\n > ",POSINT_ERR)

            print("\nThe required functions: \n")

            print("Weekday :", e1.is_weekday())
            e1.duration = e1.calculate_duration()
            print("Duration: {} min  --  {} hours ".format(e1.duration, round(e1.duration/60, 1)))
            print("Maximum donor number:", e1.max_donor_number())
            print("Success rate: {}".format(e1.success_rate()))
            input("\n\n (Press ENTER to go BACK)")
            EventManager.store_donation_data(e1)
            clear()
            break

    @staticmethod
    def delete_donation_event():
        while True:
            try:
                with open("Data/donations.csv", "r") as f:
                    content = []
                    for line in f:
                        content.append(line.strip())
                ids = [content[i].split(',')[0] for i in range(len(content)) if i != 0]
                print(ids, "(0) Cancel")
                user_input = input("Enter donation event's ID number: ")
                if not user_input.isdigit():
                    print("\n\tWrong ID, enter a real value")
                    time.sleep(2)
                    clear()
                    continue
                elif user_input == '0':
                    clear()
                    break
                elif user_input not in ids:
                    print("\n\tID is valid, but there is no entry with this ID yet.")
                    time.sleep(2)
                    clear()
                    continue
                else:
                    print("Deleting entry...")
                    with open("Data/donations.csv", "w") as f:
                        for line in content:
                            if user_input != line.split(",")[0]:
                                f.write(line + "\n")
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
    def list_donation_events():
        with open("Data/donations.csv", "r") as f:
            event_list = list(csv.reader(f))
        del(event_list[0])
        if len(event_list) < 1:
            print("\n No entry found\n")
            input("\n Press (ENTER) to go back")
            clear()
            return None
        else:
            donation_object_list = []
            for i in event_list:
                next_event = Event()
                next_event.id = i[0]
                next_event.date_of_event = i[1]
                next_event.start_time = i[2]
                next_event.end_time = i[3]
                next_event.zip_code = i[4]
                next_event.city = i[5]
                next_event.address = i[6]
                next_event.available_beds = i[7]
                next_event.planned_donor_number = i[8]
                next_event.successfull = i[9]
                donation_object_list.append(next_event)
            #
            # EVENT SORT BY MENU
            #
            print("Please type the criteria by which you would like to sort the list")
            print("\n(1) Date of Event\n(2) Start Time\n(3) End Time\n(4) Zip code\n"
                  "(5) City\n(6) Address\n(7) Available beds\n(8) Planned donor number\n"
                  "(9) Final donor number\n(0) Cancel")
            user_input = input("\n> ")
            clear()

            if user_input == "":
                user_input = "1"
            if user_input.isdigit() and int(user_input) in range(1, 10):
                EventManager.print_sorted_donation_list(donation_object_list, user_input)
                return None
            elif user_input == "0":
                clear()
                return None
            else:
                print("Please choose from the given numbers")
                time.sleep(1)
                clear()

    @staticmethod
    def search_in_donation_events():
        with open("Data/donations.csv", "r") as f:
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
            string_to_search = input("Search for donations: ")
            found_items = []
            for donation in content:
                if string_to_search.capitalize() in donation:
                    found_items.append(donation)
            eventlista = []
            for i in found_items:
                l = i.split(",")
                eventlista.append(Event())
                eventlista[-1].id = l[0]
                eventlista[-1].date_of_event = l[1]
                eventlista[-1].start_time = l[2]
                eventlista[-1].end_time = l[3]
                eventlista[-1].zip_code = l[4]
                eventlista[-1].city = l[5]
                eventlista[-1].address = l[6]
                eventlista[-1].available_beds = l[7]
                eventlista[-1].planned_donor_number = l[8]
                eventlista[-1].successfull = l[9]

            szoveg = ""
            for i in eventlista:
                szoveg += "------------------------------\n"
                szoveg += "ID: " + i.id + "\n"
                szoveg += str(i)+"\n"
            szoveg += "------------------------------\n"
            pydoc.pager(szoveg)
            input("\n Press (ENTER) to go back")
            clear()