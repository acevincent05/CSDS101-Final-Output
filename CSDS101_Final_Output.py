# Gamitin, Ace Vincent A. 
# CSDS101 Final Output - Applying Relations 

import mysql.connector # ito po ay para magamit ang MySQL sa program
from mysql.connector import errorcode # ito po ay para makapag-handle ng errors sa SQL database
import os # ito po ay para magkaroon ng access sa operating system functionalities, tulad po ng pag clear ng screen ng console



def main(): # ito po yung main menu
    while True: # ito po ay para ma-display lagi yung main menu 
        print("\n=== BLOOD DONATION TRACKER ===") # ito po ay para ma-diplay ang title ng program na "BLOOD DONATION TRACKER"
        print("1. Blood Donors") # ito po ay para ma-diplay ang menu option na i-view ang "Blood Donors"
        print("2. Donors' Info") # ito po ay para ma-diplay ang menu option na i-view ang "Donors' Info"
        print("3. Blood Types") # ito po ay para ma-diplay ang menu option na i-view ang "Blood Types"
        print("4. Add Record") # ito po ay para ma-diplay ang menu option na i-view ang "Add Record"
        print("5. Edit Record") # ito po ay para ma-diplay ang menu option na i-view ang "Edit Record"
        print("6. Delete Record") # ito po ay para ma-diplay ang menu option na i-view ang "Delete Record"

        choice = input("Enter your choice: ")

        if choice == '1':
            os.system('cls')

        elif choice == '0':
            print("Exiting program")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__": # ito po ay para i-run yung program directly tuwing bubuksan
    # DB_credentials() # ito po ay para magamit yung class 
    # main() # ito po ay para mag-open yung main menu