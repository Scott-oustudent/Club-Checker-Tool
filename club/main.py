from datetime import datetime, timedelta
import sys
import banned
from openpyxl import load_workbook, Workbook
import os

# Check if the id_check_log.xlsx file exists, if not, create it
if not os.path.exists("id_check_log.xlsx"):
    wb = Workbook()
    ws = wb.active
    ws.title = "ID Check Log"
    ws.append(["Name", "Date", "Status"])  # Adding headers
    wb.save("id_check_log.xlsx")

def log_id_check(name, status):
    wb = load_workbook("id_check_log.xlsx")
    ws = wb["ID Check Log"]
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws.append([name, today, status])
    wb.save("id_check_log.xlsx")

def banned_from_club():
    """ This will check to see if a person is banned from the club"""
    are_they_banned = input('What is the name of the person trying to enter the club? ')
    if are_they_banned in banned.banned_people:
        print('Do not allow entry to the club!!!')
        log_id_check(are_they_banned, "Banned")
        return False
    else:
        print('Now lets check their age!')
        return True

def auth_id_type():
    return ['passport', 'driving licence', 'national id card']

def age_check(name):
    """ This will check to see if a person is old enough to enter the club
        and check their ID """
    how_old = int(input('How old is the person trying to enter? '))
    if how_old < 18:
        print('This person is not old enough to enter!!!')
        log_id_check(name, "Too Young")
        return False
    else:
        print('This person is old enough to enter. Let’s check their ID!')
        return True

def id_check(name):
    """ This will check their ID to see if it is valid! """
    valid_ids = auth_id_type()
    id_type = input('What form of ID are you presented with? ')
    if id_type not in valid_ids:
        print('Invalid ID type, please ask for another form of ID or decline entry!')
        log_id_check(name, "Invalid ID")
        return False
    else:
        print('ID type is valid. Let’s check their date of birth!')
        return True

def is_legal_age(birthdate, legal_age=18):
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d").date()
    legal_age_date = birthdate + timedelta(days=legal_age * 365.25)
    today = datetime.now().date()
    return today >= legal_age_date

def dob_check(name):
    day = int(input('What day of the month does the birthdate fall on? '))
    month = int(input('What month does their birthday fall on? '))
    year = int(input('What year were they born? '))
    birthdate = f"{year}-{month:02d}-{day:02d}"  # Format birthdate as YYYY-MM-DD
    if is_legal_age(birthdate):
        print('Allow Entry!!!')
        log_id_check(name, "Allowed")
    else:
        print('Do not allow entry!!!')
        log_id_check(name, "Not of Legal Age")

def nextp():
    answer = 'y'
    while answer == 'y':
        name = input('What is the name of the person trying to enter the club? ')
        if not banned_from_club():
            answer = input("Press 'y' when you are ready to check the next person or press 'n' to leave the program: ")
            continue
        if not age_check(name):
            answer = input("Press 'y' when you are ready to check the next person or press 'n' to leave the program: ")
            continue
        if not id_check(name):
            answer = input("Press 'y' when you are ready to check the next person or press 'n' to leave the program: ")
            continue
        dob_check(name)
        answer = input("Press 'y' when you are ready to check the next person or press 'n' to leave the program: ")

def main_menu():
    while True:
        choice = input("Type 'banned' to manage banned list or 'check' to check IDs, or 'exit' to leave the program: ")
        if choice == 'banned':
            banned.banned_menu()
        elif choice == 'check':
            nextp()
        elif choice == 'exit':
            print('Exiting the program...')
            sys.exit()
        else:
            print('Invalid choice, please try again.')

main_menu()
