from datetime import datetime, timedelta
import sys
import os
from openpyxl import load_workbook, Workbook

password = 'Brookhouse01!'
log_file = "id_check_log.txt"
banned_file = "banned_list.txt"

# Check if the id_check_log.txt file exists, if not, create it
if not os.path.exists(log_file):
    with open(log_file, 'w') as f:
        f.write("Name,Date,Status\n")  # Adding headers

def log_id_check(name, status):
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, 'a') as f:
        f.write(f"{name},{today},{status}\n")

def read_banned_list():
    if not os.path.exists(banned_file):
        return []
    with open(banned_file, 'r') as f:
        return [line.strip() for line in f]

def write_banned_list(banned_list):
    with open(banned_file, 'w') as f:
        for person in banned_list:
            f.write(f"{person}\n")

def banned_from_club():
    """ This will check to see if a person is banned from the club"""
    banned_people = read_banned_list()
    are_they_banned = input('What is the name of the person trying to enter the club? ')
    if are_they_banned in banned_people:
        print('Do not allow entry to the club!!!')
        log_id_check(are_they_banned, 'Banned')
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
        log_id_check(name, 'Underage')
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
        log_id_check(name, 'Invalid ID')
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
        log_id_check(name, 'Allowed')
    else:
        print('Do not allow entry!!!')
        log_id_check(name, 'Underage')

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
            manage_banned_list()
        elif choice == 'check':
            nextp()
        elif choice == 'exit':
            if password == input('Please enter the password to exit the program: '):
                print('Exiting the program...')
                sys.exit()
            else:
                print('Invalid password, please try again.')
        else:
            print('Invalid choice, please try again.')

def manage_banned_list():
    banned_list = read_banned_list()
    while True:
        action = input("Type 'add' to add a person to the banned list, 'remove' to remove a person, or 'back' to return to the main menu: ")
        if action == 'add':
            name = input('Enter the name of the person to ban: ')
            if name not in banned_list:
                banned_list.append(name)
                write_banned_list(banned_list)
                print(f'{name} has been added to the banned list.')
            else:
                print(f'{name} is already on the banned list.')
        elif action == 'remove':
            name = input('Enter the name of the person to remove from the banned list: ')
            if name in banned_list:
                banned_list.remove(name)
                write_banned_list(banned_list)
                print(f'{name} has been removed from the banned list.')
            else:
                print(f'{name} is not on the banned list.')
        elif action == 'back':
            break
        else:
            print('Invalid choice, please try again.')

main_menu()
