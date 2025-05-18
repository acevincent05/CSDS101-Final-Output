# Gamitin, Ace Vincent A. 
# CSDS101 Final Output - Applying Relations 

import mysql.connector # ito po ay para magamit ang MySQL sa program
from mysql.connector import errorcode # ito po ay para makapag-handle ng errors sa SQL database
import os # ito po ay para magkaroon ng access sa operating system functionalities, tulad po ng pag clear ng screen ng console

class Blood_Donation_DB: # ito po yung class na kailangan para magfunction yung buong program
    def __init__(self, user: str, password: str, host: str, database: str): # ito po ay para ma-initialize yung class
        self.user = user # ito po ay para ma-initialize at ma-encapsulate yung user ng MySQL database
        self.password = password # ito po ay para ma-initialize at ma-encapsulate yung password ng MySQL database
        self.host = host # ito po ay para ma-initialize at ma-encapsulate yung host ng MySQL database
        self.database = database # ito po ay para ma-initialize at ma-encapsulate yung schema ng MySQL database

    @property
    def get_user(self):
        return self.user
    
    @get_user.setter
    def set_user(self, user):
        self.user = user

    @property
    def get_password(self):
        return self.password

    @get_password.setter
    def set_password(self, password):
        self.password = password
    
    @property
    def get_host(self):
        return self.host
    
    @get_host.setter
    def set_host(self, host):
        self.host = host

    @property
    def get_database(self):
        return self.database
    
    @get_database.setter
    def set_database(self, database):
        self.database = database

    def connect(self): # ito po ay para magconnect sa MySQL 
        try: # ito po ay para sa tingnan kung succesful ang connection sa database
            con = mysql.connector.connect(user=self.user, # ito po ay para magamit ang nakuhang "user" sa class initialization
                                        password=self.password,  # ito po ay para magamit ang nakuhang "password" sa class initialization
                                        host=self.host, # ito po ay para magamit ang nakuhang "host" sa class initialization
                                        database=self.database) # ito po ay para magamit ang nakuhang "database" sa class initialization
            print('Connection successful') # ito po ay para malaman na successful ang pag-connect sa database
            return con # ito po ay para ibalik ang naging successful connection sa connect function
        except mysql.connector.Error as err: # ito po ay saluhin ng ang error sa pag-connect sa database
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR: # ito po ay para i-handle ang maling input ng credentials sa database
                print("Something is wrong with your user name or password") # ito po para sabihin na may mali sa user or password 
            elif err.errno == errorcode.ER_BAD_DB_ERROR: # ito po ay para i-handle ang pag connect sa non-existent database
                print("Database does not exist") # ito po para sabihin na wala sa SQL yung database
            else: # ito po ay para masalo ang iba pang errors
                print(err) # ito po ay para ibigay ang specific error na meron sa SQL database

    def connection_cursor(self): # ito po ay para i-call ang  connect method at cursor 
        connected = self.connect()  # ito po ay para ilagay ang connect method sa "connected" variable
        cursor = connected.cursor() # ito po ay para ilagay magamit na ang cursor
        return connected, cursor # ito po ay para  na ibigay sa connection_cursor(self) function ang cursor

    def display_donors(self):
        try:
            connection, cursor = self.connection_cursor()

            query = '''
                    SELECT 
                        d.DonorID,
                        di.Name,
                        bt.BloodType
                    FROM 
                        Donors d
                    JOIN 
                        DonorInfo di ON d.DonorID = di.DonorID
                    JOIN 
                        BloodTypes bt ON d.BloodTypeID = bt.BloodTypeID
                    ORDER BY 
                        d.DonorID;
                    '''
            cursor.execute(query)

            # retrieves all rows
            rows = cursor.fetchall()

            print(f"{'Donor ID':<10} | {'Name':<15} | {'Blood Type':<5}") 
            print("-" * 60)

            # print each rows
            for row in rows:
                print(f"{row[0]:<10} | {row[1]:<15} | {row[2]:<5} ")  

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def donors_info(self):
        try:
            connection, cursor = self.connection_cursor()

            query = '''
                    SELECT 
                        d.DonorID,
                        di.Name,
                        di.Age,
                        DATE_FORMAT(di.DateOfBirth, '%m-%d-%Y') AS DateOfBirth,
                        di.FirstTimeDonor
                    FROM 
                        Donors d
                    JOIN 
                        DonorInfo di ON d.DonorID = di.DonorID
                    ORDER BY 
                        d.DonorID;
                    '''
            cursor.execute(query)

            # retrieves all rows
            rows = cursor.fetchall()

            print(f"{'Donor ID':<10} | {'Name':<20} | {'Age':<3} | {'Birth Date':<10} | {'First Time Donor':<6}") 
            print("-" * 75)

            # print each rows
            for row in rows:
                print(f"{row[0]:<10} | {row[1]:<20} | {row[2]:<3} | {row[3]:<10} | {row[4]:<6}")  

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()  

    def blood_types(self):
        try:
            connection, cursor = self.connection_cursor()

            query = '''
                    SELECT * FROM BloodTypes;
                    '''
            cursor.execute(query)

            # retrieves all rows
            rows = cursor.fetchall()

            print(f"{'Blood ID':<10} | {'Blood Type':<10}") 
            print("-" * 50)

            # print each rows
            for row in rows:
                print(f"{row[0]:<10} | {row[1]:<10}")  

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()  

    def add_donation(self, donor_id, name, blood_type_id, age, date_birth, first_time):
        try:
            connection, cursor = self.connection_cursor()

            # Insert into Donors
            donor_query = '''
                INSERT INTO Donors (DonorID, Name, BloodTypeID)
                VALUES (%s, %s, %s)
            '''
            cursor.execute(donor_query, (donor_id, name, blood_type_id))

            # Insert into DonorInfo
            donor_info_query = '''
                INSERT INTO DonorInfo (DonorID, Name, Age, DateOfBirth, FirstTimeDonor)
                VALUES (%s, %s, %s, %s, %s)
            '''
            cursor.execute(donor_info_query, (donor_id, name, age, date_birth, first_time))
            connection.commit()

            print("Donation data added successfully.") 

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()  


    def update_donation(self, donor_id, name, blood_type_id, age, date_birth, first_time):
        try:
            connection, cursor = self.connection_cursor()

            # Insert into Donors
            donor_query = '''
                UPDATE Donors
                SET Name = %s, BloodTypeID = %s
                WHERE DonorID = %s
            '''
            cursor.execute(donor_query, (name, blood_type_id, donor_id))

            # Update DonorInfo table
            donor_info_query = '''
                UPDATE DonorInfo
                SET Name = %s, Age = %s, DateOfBirth = %s, FirstTimeDonor = %s
                WHERE DonorID = %s
            '''
            cursor.execute(donor_info_query, (name, age, date_birth, first_time, donor_id))
            connection.commit()

            print("Donation data updated successfully.") 

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close() 

    def delete_donation(self, donor_id):
        try:
            connection, cursor = self.connection_cursor()

            # Delete from DonorInfo first due to foreign key constraints
            cursor.execute('DELETE FROM DonorInfo WHERE DonorID = %s', (donor_id,))
        
            # Then delete from Donors
            cursor.execute('DELETE FROM Donors WHERE DonorID = %s', (donor_id,))

            connection.commit()

            print("Donation data updated successfully.") 

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close() 

def get_donation_data():
    donor_id = input("Enter Donor ID: ")
    name = input("Enter Donor Name: ")
    blood_type_id = input("Enter Blood Type ID: ")
    age = int(input("Enter Age: "))
    date_birth = input("Enter Date of Birth (YYYY-MM-DD): ")
    first_time = input("First Time Donor? (Yes/No): ")
    return donor_id, name, blood_type_id, age, date_birth, first_time


def DB_credentials(): # ito po ay para i-require ang user na ibigay the credentials ng SQL database 
    user = input('Enter user: ') # ito po ay para kunin ang user
    password = input('Enter password: ') # ito po ay para kunin ang password
    host = input('Enter host: ') # ito po ay para kunin ang host
    db_select = input('Enter Database: ') # ito po ay para kunin ang schema 

    global SQL_Blood_Donation_DB # ito po ay para ma-access ang Blood_Donation_DB sa menu
    SQL_Blood_Donation_DB = Blood_Donation_DB('root', 'CS2025EU', 'localhost', 'Blood_Donation')
    #SQL_Blood_Donation_DB = Blood_Donation_DB(user, password, host, db_select) # ito po ay para magamit yung class Blood_Donation_DB 

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

            SQL_Blood_Donation_DB.display_donors()

        if choice == '2':
            os.system('cls')

            SQL_Blood_Donation_DB.donors_info()

        if choice == '3':
            os.system('cls')

            SQL_Blood_Donation_DB.blood_types()

        if choice == '4':
            os.system('cls')

            donor_id, name, blood_type_id, age, date_birth, first_time = get_donation_data()
            SQL_Blood_Donation_DB.add_donation(donor_id, name, blood_type_id, age, date_birth, first_time)

        if choice == '5':
            os.system('cls')

            donor_id, name, blood_type_id, age, date_birth, first_time = get_donation_data()
            SQL_Blood_Donation_DB.update_donation(donor_id, name, blood_type_id, age, date_birth, first_time)

        if choice == '6':
            os.system('cls')

            donor_id = input("Enter Donor ID: ")

            SQL_Blood_Donation_DB.delete_donation(donor_id)

        elif choice == '0':
            print("Exiting program")
            break

if __name__ == "__main__": # ito po ay para i-run yung program directly tuwing bubuksan
    DB_credentials() # ito po ay para magamit yung class 
    main() # ito po ay para mag-open yung main menu