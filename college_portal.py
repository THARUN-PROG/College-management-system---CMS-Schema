import mysql.connector as mysql

# Database has been connected
db = mysql.connect(host="localhost",user="root",password="",database="college")

command_handler = db.cursor(buffered=True)


def staff_session():
     while 1:
        print("")
        print("Staff's Menu")
        print("1. Mark Student Register")
        print("2. View the Register")
        print("3. Generate and Managing the class schedules")
        print("4. Apply for Leave - Leave Maintenance")
        print("5. Logout")

        user_option = input(str("Module : "))
        if user_option == "1":
            print("")
            print("Mark Student Attendance")
            command_handler.execute("SELECT username FROM users WHERE privilege = 'student'")
            records = command_handler.fetchall()
            date = input(str("Date : DD/MM/YYYY : "))
            # When the record is returned as a tuple, by replacing it is going to return only the name and none of the other stuff that we don't need it dosn't do it
            for record in records:
                record = str(record).replace("'","")
                record=str(record).replace(",","")
                record=str(record).replace("(","")
                record=str(record).replace(")","")
                # Present | Absent | Late
                status = input(str("Status for " + str(record) + " P/A/L : "))
                query_vals = (str(record),date,status)
                command_handler.execute("INSERT INTO attendance (username,date,status) VALUES (%s,%s,%s)", query_vals)
                db.commit()  #Save and refresh all the changes
                print(record + " Marked as " + status)
        
        elif user_option == "2":
            print("")
            print("Viewing all student registers")
            command_handler.execute("SELECT username, date, status FROM attendance")
            records = command_handler.fetchall()
            print("Showcasing all registers")  #It displays the attendance data
            for record in records:
                print(record)

        elif user_option == "5":
            break  #I return to my main loop from main function - main menu

        else:
            print("No Valid Module Selected")




def student_session(username):
    while 1:
        print("")
        print("Student's Menu")
        print("")
        print("1. View Register")
        print("2. Download the Register")
        print("3. Logout")

        user_option = input(str("Module : "))
        if user_option == "1":
            print("Showcasing Register")
            query_vals = (str(username))   #When I pass the values into query, I have multiple ones, I have used variable - query_values 
            command_handler.execute("SELECT date, username, status FROM attendance WHERE username = %s", query_vals)
            records = command_handler.fetchall() #I captured all the info into a variable - records 
            #For loop to display the records
            for record in records:
                print(record)







# This function is going to execute only when the username and password provided by admin is correct
#I have used while loop because admin should be able to access this menu on and on again unless admin logged out
def admin_session():
    # print("Login Success, Welcome Admin")
    while 1:
        print("")
        print("Admin Menu")
        print("1. Register new Student")
        print("2. Register new Staff")
        print("3. Delete existing Student")
        print("4. Delete existing Staff")
        print("5. Logout")

        user_option = input(str("Module : "))
        if user_option == "1":
            print("")
            print("Register New Student")
            # The username that the admin wants to give the new student
            username = input(str("Student username : "))
            password = input(str("Student password : "))
            # The above info I get from here admin and store in Database
            # And I save these values in variable query_vals
            query_vals = (username,password)
            command_handler.execute("INSERT INTO users (username,password,privilege) VALUES (%s,%s, 'student')",query_vals)
            db.commit() #To save all the changes to DB
            print(username + " has been registered as a student")


        elif user_option == "2":
            print("")
            print("Register New Staff")
            # The username that the admin wants to give the new staff
            username = input(str("Staff username : "))
            password = input(str("Staff password : "))
            # The above info I get from here admin and store in Database
            # And I save these values in variable query_vals
            query_vals = (username,password)
            command_handler.execute("INSERT INTO users (username,password,privilege) VALUES (%s,%s, 'staff')",query_vals)
            db.commit() #To save all the changes to DB
            print(username + " has been registered as a staff/faculty")


        elif user_option == "3":
            print("")
            print("Delete Existing Student Account")
            username = input(str("Student username : "))
            query_vals = (username,"student") #If any particular student has a same username I kept to delete it
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s ",query_vals)
            db.commit() #To save all the changes of the deletions

            #Data Validation - It gives how many rows affected, If no rows it gives zero - If no rows are affected then No user with the username provided, that means there was no records have been deleted
            # And no user with that username existed, For finding that the user with that username actually existed or not
            if command_handler.rowcount < 1:
                print("User not found")  #Because that user does not exist that's why no rows affected
            else:
                print(username + " has been deleted")


        elif user_option == "4":
            print("")
            print("Delete Existing Staff Account")
            username = input(str("Staff username : "))
            query_vals = (username,"staff") 
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s ",query_vals)
            db.commit() #To save all the changes of the deletions

            #Data Validation 
            if command_handler.rowcount < 1:
                print("User not found") 
            else:
                print(username + " has been deleted")

        elif user_option == "5":
            break

        #For Validation
        else:
            print("No Valid Module Selected")



def auth_student():
    print("")
    print("Student's Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    query_vals = (username, password, "student")
    command_handler.execute("SELECT username FROM users WHERE username = %s AND password = %s AND privilege = %s", query_vals)
    # username = command_handler.fetchone() #It is going to b one result because I dont have multiple people with the same user name
    #Fetches the username selected 
    #How much rows or results are returned from query
    if command_handler.rowcount <= 0:
         #If there is no results
         print("Invalid Login Credentials")
    else:
         #There was a result that is returned
         student_session(username)






def auth_staff():
    print("")
    print("Staff's Login")
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    query_vals = (username, password)
    #To run a query I had a object called command_handler
    command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s AND privilege = 'staff'", query_vals)
    db.commit()
    if command_handler.rowcount <= 0:
        print("Login not recognized")
    else:
        staff_session()


 
def auth_admin():
    print("")
    print("Admin Login")  #Title
    print("")
    username = input(str("Username : "))
    password = input(str("Password : "))
    if username == "admin":
        if password == "pass":
            admin_session()
        else:
            print("Incorrect Password !")
    else:
        print("Login details are not Recognized, It is Incorrect Credentials")



def main():
    while 1:
        print("Welcome to my College management Portal")
        print("")
        print("1. Login as Student")
        print("2. Login as Staff")
        print("3. Login as Admin")

        user_option = input(str("Login Module : "))
        if user_option == "1":
            auth_student()
            # print("Student Login")
        elif user_option == "2":
            auth_staff()
            # print("Staff Login")
        elif user_option == "3":
            auth_admin()
            # print("Admin Login")
        else:
            print("No valid Login Module was Selected")

main()
 
