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

    @property # ito po ay para malaman ang value ng attribute
    def get_user(self): # Ito po ay para kunin ang value ng 'user' property
        return self.user # ito po ay binabalik ang value ng 'user'
    
    @get_user.setter  # ito po ay para palitan ang value ng 'user'
    def set_user(self, user):  # ito ay kumukuha ng bagong value na 'user'
        self.user = user  # ito ay nag-assign  ng bagong value sa property na 'user'

    @property # ito po ay para malaman ang value ng attribute
    def get_password(self): # Ito po ay para kunin ang value ng 'password' property
        return self.password # ito po ay binabalik ang value ng 'password'

    @get_password.setter # ito po ay para palitan ang value ng 'password'
    def set_password(self, password): # ito ay kumukuha ng bagong value na 'password'
        self.password = password # ito po ay binabalik ang value ng 'password'
    
    @property # ito po ay para malaman ang value ng attribute
    def get_host(self): # Ito po ay para kunin ang value ng 'host' property
        return self.host # ito po ay binabalik ang value ng 'host'
    
    @get_host.setter # ito po ay para palitan ang value ng 'host'
    def set_host(self, host): # ito ay kumukuha ng bagong value na 'host'
        self.host = host # ito po ay binabalik ang value ng 'host'

    @property  # ito po ay para malaman ang value ng attribute
    def get_database(self):  # Ito po ay para kunin ang value ng 'database' property
        return self.database  # ito po ay binabalik ang value ng 'database'
    
    @get_database.setter # ito po ay para palitan ang value ng 'database'
    def set_database(self, database): # ito ay kumukuha ng bagong value na 'database'
        self.database = database # ito po ay binabalik ang value ng 'database'

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

    def display_donors(self): # ito po ay class para sa makita ang donors
        try: # ito po ay sa pagcheck kung nagana ng walang error
            connection, cursor = self.connection_cursor() # ito po ay para magconnect sa MySQL

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
                    ''' # ito po ay para sa SQL script na kukunin at ipagjo-join ang DonorInfo at BloodType table, 
                        # dito po nai-apply ang relations kung saan may one-to-many relationship ang mga blood types 
                        # sa kung kaninong donors

            cursor.execute(query) # ito po ay para i-run yung script na nakalagay sa query variable sa MySQL database

            rows = cursor.fetchall() # ito po ay para ma-retrevie lahat ng rows

            print(f"{'Donor ID':<10} | {'Name':<15} | {'Blood Type':<5}")  # ito po ay para madisplay ang headers sa console
            print("-" * 60) # ito po ay lines lang na idi-display para magseparate sa headers

            for row in rows: # ito po ay para sa bawat laman ng rows na nakuha
                print(f"{row[0]:<10} | {row[1]:<15} | {row[2]:<5} ")  # ito po yung magdi-display ng content ng bawat rows na may formatting po

        except mysql.connector.Error as err: # ito po ay sasalo sa magiging kung anumang error sa database 
            print(f"Error: {err}") # ito po ang magsasabi ng error na binibigay ng database 

        finally: # pagkatapos po ng functions, nagkaroon po ng error o hindi, ito po ang mangyayari
            if connection.is_connected(): # ito po ang magche-check kung nakapagconnect nga po ba sa database
                cursor.close() # ito po ang magclo-close ng cursor ng SQL
                connection.close() # tatanggalin na rin po nito ang connections once na matapos po ang lahat

    def donors_info(self): # ito po ang method na kukunin ang info ng donors
        try: # ito po ay sa pagcheck kung nagana ng walang error
            connection, cursor = self.connection_cursor() # ito po ay para magconnect sa MySQL

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
                    ''' # ito po ay SQL script para idisplay ang DonorInfo table na connected din sa Blood types 
           
            cursor.execute(query)# ito po ay para i-run yung script na nakalagay sa query variable sa MySQL database

            rows = cursor.fetchall() # ito po ay para ma-retrevie lahat ng rows

            print(f"{'Donor ID':<10} | {'Name':<20} | {'Age':<3} | {'Birth Date':<10} | {'First Time Donor':<6}") # ito po ay para madisplay ang headers sa console
            print("-" * 75) # ito po ay lines lang na idi-display para magseparate sa headers

            for row in rows: # ito po ay para sa bawat laman ng rows na nakuha
                print(f"{row[0]:<10} | {row[1]:<20} | {row[2]:<3} | {row[3]:<10} | {row[4]:<6}") # ito po yung magdi-display ng content ng bawat rows na may formatting po


        except mysql.connector.Error as err: # ito po ay sasalo sa magiging kung anumang error sa database 
            print(f"Error: {err}") # ito po ang magsasabi ng error na binibigay ng database 

        finally: # pagkatapos po ng functions, nagkaroon po ng error o hindi, ito po ang mangyayari
            if connection.is_connected(): # ito po ang magche-check kung nakapagconnect nga po ba sa database
                cursor.close() # ito po ang magclo-close ng cursor ng SQL
                connection.close() # tatanggalin na rin po nito ang connections once na matapos po ang lahat 

    def blood_types(self): # ito po ang method na kukunin ang blood types
        try: # ito po ay sa pagcheck kung nagana ng walang error
            connection, cursor = self.connection_cursor() # ito po ay para magconnect sa MySQL

            query = '''
                    SELECT * FROM BloodTypes;
                    ''' # ito po ay para idisplay ang contents ng BloodTypes table
            
            cursor.execute(query) # ito po ay para i-run yung script na nakalagay sa query variable sa MySQL database

            rows = cursor.fetchall() # ito po ay para ma-retrevie lahat ng rows

            print(f"{'Blood ID':<10} | {'Blood Type':<10}") # ito po ay para madisplay ang headers sa console
            print("-" * 50) # ito po ay lines lang na idi-display para magseparate sa headers

            for row in rows: # ito po ay para sa bawat laman ng rows na nakuha
                print(f"{row[0]:<10} | {row[1]:<10}")  # ito po yung magdi-display ng content ng bawat rows na may formatting po

        except mysql.connector.Error as err: # ito po ay sasalo sa magiging kung anumang error sa database 
            print(f"Error: {err}") # ito po ang magsasabi ng error na binibigay ng database 

        finally: # pagkatapos po ng functions, nagkaroon po ng error o hindi, ito po ang mangyayari
            if connection.is_connected(): # ito po ang magche-check kung nakapagconnect nga po ba sa database
                cursor.close() # ito po ang magclo-close ng cursor ng SQL
                connection.close() # tatanggalin na rin po nito ang connections once na matapos po ang lahat 

    def add_donation(self, donor_id, name, blood_type_id, age, date_birth, first_time): # ito po ang method na maglalagay ng new donor infos
        try: # ito po ay sa pagcheck kung nagana ng walang error
            connection, cursor = self.connection_cursor() # ito po ay para magconnect sa MySQL

            donor_query = '''
                INSERT INTO Donors (DonorID, Name, BloodTypeID)
                VALUES (%s, %s, %s)
            ''' # ito po ay maglalagay muna sa table ng Donors

            cursor.execute(donor_query, (donor_id, name, blood_type_id)) # ito po ay para i-run yung script na nakalagay sa query variable sa MySQL database

            donor_info_query = '''
                INSERT INTO DonorInfo (DonorID, Name, Age, DateOfBirth, FirstTimeDonor)
                VALUES (%s, %s, %s, %s, %s)
            ''' # ito po ay maglalagay naman sa table ng DonorInfo

            cursor.execute(donor_info_query, (donor_id, name, age, date_birth, first_time)) # ito po ay para i-run yung script na nakalagay sa query variable sa MySQL database
            connection.commit() # ito po ay para gawin ang changes sa database

            print("Donation data added successfully.") # ito po ang magsasabi na nailagay na ang bagong donor

        except mysql.connector.Error as err: # ito po ay sasalo sa magiging kung anumang error sa database 
            print(f"Error: {err}") # ito po ang magsasabi ng error na binibigay ng database 

        finally: # pagkatapos po ng functions, nagkaroon po ng error o hindi, ito po ang mangyayari
            if connection.is_connected(): # ito po ang magche-check kung nakapagconnect nga po ba sa database
                cursor.close() # ito po ang magclo-close ng cursor ng SQL
                connection.close() # tatanggalin na rin po nito ang connections once na matapos po ang lahat 


    def update_donation(self, donor_id, name, blood_type_id, age, date_birth, first_time): # ito po ang method para makapag-edit ng content ng database
        try:
            connection, cursor = self.connection_cursor() # ito po ay para magconnect sa MySQL

            donor_query = '''
                UPDATE Donors
                SET Name = %s, BloodTypeID = %s
                WHERE DonorID = %s
            ''' # ito po yung SQL script na mag-eedit muna sa Donors table sa pamamagitan ng DonorID 

            cursor.execute(donor_query, (name, blood_type_id, donor_id)) # ito po ay para i-run yung script na nakalagay sa query variable sa MySQL database

            donor_info_query = '''
                UPDATE DonorInfo
                SET Name = %s, Age = %s, DateOfBirth = %s, FirstTimeDonor = %s
                WHERE DonorID = %s
            ''' # ito po yung SQL script na mag-eedit naman sa DonorsInfo table sa pamamagitan ng DonorID 

            cursor.execute(donor_info_query, (name, age, date_birth, first_time, donor_id)) # ito po ay para i-run yung script na nakalagay sa query variable sa MySQL database
            connection.commit() # ito po ay para gawin ang changes sa database

            print("Donation data updated successfully.") # ito po ang magsasabi na nailagay na na-edit na ang database

        except mysql.connector.Error as err: # ito po ay sasalo sa magiging kung anumang error sa database 
            print(f"Error: {err}") # ito po ang magsasabi ng error na binibigay ng database 

        finally: # pagkatapos po ng functions, nagkaroon po ng error o hindi, ito po ang mangyayari
            if connection.is_connected(): # ito po ang magche-check kung nakapagconnect nga po ba sa database
                cursor.close() # ito po ang magclo-close ng cursor ng SQL
                connection.close() # tatanggalin na rin po nito ang connections once na matapos po ang lahat 

    def delete_donation(self, donor_id): # ito po ang method para makapag-delete sa database
        try:
            connection, cursor = self.connection_cursor() # ito po ay para magconnect sa MySQL

            cursor.execute('DELETE FROM DonorInfo WHERE DonorID = %s', (donor_id,)) # ito po ay yung magdedelete sa DonorInfo table sa pamamagitan ng DonorID
        
            cursor.execute('DELETE FROM Donors WHERE DonorID = %s', (donor_id,)) # ito po ay yung magdedelete sa Donors table sa pamamagitan ng DonorID

            connection.commit() # ito po ay para gawin ang changes sa database

            print("Donation data deleted successfully.") # ito po ang magsasabi na nailagay na na-delete na ang database

        except mysql.connector.Error as err: # ito po ay sasalo sa magiging kung anumang error sa database 
            print(f"Error: {err}") # ito po ang magsasabi ng error na binibigay ng database 

        finally: # pagkatapos po ng functions, nagkaroon po ng error o hindi, ito po ang mangyayari
            if connection.is_connected(): # ito po ang magche-check kung nakapagconnect nga po ba sa database
                cursor.close() # ito po ang magclo-close ng cursor ng SQL
                connection.close() # tatanggalin na rin po nito ang connections once na matapos po ang lahat 

def get_donation_data(): # ito po ay function para hindi ulit ulit yung pagkuha ng required inputs 
    donor_id = input("Enter Donor ID: ") # ito po ay para mag-input ng Donor ID
    name = input("Enter Donor Name: ") # ito po ay para mag-input ng name ng Donor
    blood_type_id = input("Enter Blood Type ID: ") # ito po ay para mag-input ng blood type
    age = int(input("Enter Age: ")) # ito po ay para mag-input ng Age 
    date_birth = input("Enter Date of Birth (YYYY-MM-DD): ") # ito po ay para mag-input ng birth date
    first_time = input("First Time Donor? (Yes/No): ") # ito po ay para mag-input kung first time magdo-donate or hindi
    return donor_id, name, blood_type_id, age, date_birth, first_time # ito po ibabalik ang inputs sa get_donation_data function para gamitin sa iba't ibang methods


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

        choice = input("Enter your choice: ") # ito po ay para makapili ng functions ng program na nakalagay sa menu

        if choice == '1': # ito po ay kung iselect ang "1. Blood Donors"
            os.system('cls') # ito po ay para i-clear and screen ng console

            SQL_Blood_Donation_DB.display_donors() # ito po ay para i-call ang display_donors method 

        if choice == '2': # ito po ay kung iselect ang "2. Donors' Info"
            os.system('cls') # ito po ay para i-clear and screen ng console

            SQL_Blood_Donation_DB.donors_info() # ito po ay para i-call ang donors_info method 

        if choice == '3': # ito po ay kung iselect ang "3. Blood Types"
            os.system('cls') # ito po ay para i-clear and screen ng console

            SQL_Blood_Donation_DB.blood_types() # ito po ay para i-call ang blood_types method 

        if choice == '4': # ito po ay kung iselect ang "4. Add Record"
            os.system('cls') # ito po ay para i-clear and screen ng console

            donor_id, name, blood_type_id, age, date_birth, first_time = get_donation_data() # kukunin po nito ang mga values galing sa get_donation_data function
            SQL_Blood_Donation_DB.add_donation(donor_id, name, blood_type_id, age, date_birth, first_time) # gagamitin na po nito ang values para mag add ng donation data

        if choice == '5': # ito po ay kung iselect ang "5. Edit Record"
            os.system('cls') # ito po ay para i-clear and screen ng console

            donor_id, name, blood_type_id, age, date_birth, first_time = get_donation_data() # kukunin po nito ang mga values galing sa get_donation_data function
            SQL_Blood_Donation_DB.update_donation(donor_id, name, blood_type_id, age, date_birth, first_time) # gagamitin na po nito ang values para mag i-edit ang isang donation data

        if choice == '6': # ito po ay kung iselect ang "6. Delete Record"
            os.system('cls') # ito po ay para i-clear and screen ng console

            donor_id = input("Enter Donor ID: ") # ito po ay para mag-input ng Donor ID na gustong i-delete

            SQL_Blood_Donation_DB.delete_donation(donor_id) # ito po ay para po ay para i-call ang delete_donation method 

        elif choice == '0': # ito po ay kung iclo-close na ang program
            print("Exiting program") # ito po ay magsasabi na nage-exit na ang program
            break # ito po ang mage-exit ng program

if __name__ == "__main__": # ito po ay para i-run yung program directly tuwing bubuksan
    DB_credentials() # ito po ay para magamit yung class 
    main() # ito po ay para mag-open yung main menu