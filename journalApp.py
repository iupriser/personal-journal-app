# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 04:22:37 2019
@author: Deepak
"""

import sys
import hashlib
import getpass
import os
from datetime import datetime

def read_file(file_name):
    user_names = []
    passwords = []
    number_of_accounts = 0
    try:
        file_conn = open(file_name)
        # readlines() - entire file as list of strings,
        # where each item in the list represent one line of the file
        data = file_conn.readlines() 
        for line in data:
            user_names, pswd = line.split(',')
            passwords.append(pswd[:-1])  #pswd[:-1] It slices the string to omit the last character
            number_of_accounts = number_of_accounts + 1
    except:
        sys.exit('There was a problem reading the file')
        
    file_conn.close()
    
    return user_names, passwords, number_of_accounts

def list_entries(path):
    print('\n')
    f1 = open(str(path) + '\\list_record','r')
    print(f1.read())
    print('\nWant to read any of the entry?\n')
    print('type the serial number of entry to read that entry,\nor type 0 to skip reading entry')
    counter = 0
    serial = int(input())
    f1.seek(0,0)
    if serial == 0:
        pass
    else:
        data = f1.readlines()
        for line in data:
            title, timeStamp = line.split('\t')
            if counter + 1 == serial:
                f2 = open((str(path) + '\\record_' + str(timeStamp))[:-1],'r')
                print(f2.read())
                f2.close()
            else:
                counter = counter + 1
    f1.close()
    

def create_journal(path):
    path = str(path + "\\record_" + str(datetime.now().strftime("%d %b %Y %I %M %p")))
    f2 = open(path , 'w+')
    time_of_creation = str(datetime.now().strftime("%d %b %Y %I %M %p"))
    title = input("What's the title of your entry? - ")
    f2.write("\n\n" + title + "\t\t" + time_of_creation + "\n\n")
    print('Write till your heart\'s content \n')
    para = []
    while True:
        line = input()
        if line:
            para.append(line)
        else:
            break
    text = '\n'.join(para)
    f2.write(text)
    f3 = open(str(os.getcwd()) + "\\list_record", 'a+')
    f3.write(title + "\t" + time_of_creation + "\n")    
    #f2.seek(0,0)
    f2.close()
    f3.close()
    
def journal_management(user):
    print('\n\t\t\tWelcome to Journal Management Program\n')
    os.chdir("C:\\Users\\deepak\\Desktop\\JournalApp\\user_data\\" + str(user))
    path = os.getcwd()
    choice = int(input('1.view all previous entries\n2.create a new entry\n\n'))
    
    if choice == 1 :
        list_entries(path)
    elif choice == 2 :
        create_journal(path)
    else :
        sys.exit('Wrong choice entered, exiting...')

def signup(number_of_accounts):
    if number_of_accounts != 10:
        f = open(sys.argv[1], 'a+')
        user = input('Please enter a user name: ')
        password = hashlib.sha224((getpass.getpass('Please enter password :')).encode()).hexdigest()
        f.write(user)
        f.write(",")
        f.write(str(password))
        f.write("\n")
        f.close()
        pathToRecord = "C:\\Users\\deepak\\Desktop\\JournalApp\\user_data\\" + str(user)
        os.makedirs(pathToRecord)
        f = open(str(pathToRecord)+'\\list_record', 'w+')
        f.close()
        print('\nNew user registerd \n')
        journal_management(user)
    else:
        print('Maximum number of user reached (10 users)')

def login(user_names, passwords, number_of_accounts):
    pass_try = 0
    x = 3
    user = input('\nPlease enter username:')
    
    if user not in user_names:
        sys.exit('Unknown username, terminiting...\n')
        
    while pass_try < x:
        user_input = hashlib.sha224((getpass.getpass('Please enter password :')).encode()).hexdigest()
        if user_input != passwords[user_names.index(user)]:
           pass_try += 1
           print('Incorrect password, ' + str(x-pass_try) + 'more attempts left\n')
        else:
            pass_try = x +1
    
    if pass_try == x:
        sys.exit('Incorrect password, terminiting...\n')
        
    print('User logged in!\n')
    print('Welcome ' + user + '\t\t\t\t\t' + str((datetime.now().strftime("%d %b %Y %I %M %p"))) + '\n\n\n')
    journal_management(user) #send current account
    
def main(argv):
    if len(argv) != 1:
        sys.exit('Usage: user_pass.py <file_name>')
    
    user_name, passwords, number_of_accounts = read_file(sys.argv[1])
    
    print('\t\t\tLOGIN/SIGNUP\n')
    
    flag = int(input('press 1 for LOGIN, 2 for SIGNUP : \t'))
    if flag == 1:
        login(user_name, passwords, number_of_accounts)
        
    elif flag == 2:
        signup(number_of_accounts)
    else:
        sys.exit('Incorrect input, terminiting\n')
    
    print('\n\nThankyou for using Journal Application, Hope you enjoyed writing!!!\n')
    #change path to parent directory
    os.chdir('..\\..')
    
if __name__ == "__main__":
    main(sys.argv[1:])