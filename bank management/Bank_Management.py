import mysql.connector

# SETTING UP MYSQL - CHANGE PASSWORD WHILE USING
con = mysql.connector.connect(
  host="localhost",
  user="root",
  password="DiboraneB2H6",
  database="techsoc_bankmanagement"
)
mycursor = con.cursor()


def new_acc():                 # This function creates new bank account
    try:                       # Try - except is used to handle errors
        global customer_num    # Changes in variable wwill be global

        # User Inputs for new account
        name = input(" ENTER YOUR NAME ")
        phone = input(" ENTER CONTACT  NUMBER ")
        address = input(" ENTER ADDRESS ")
        city = input(" ENTER CITY NAME ")
        pincode = int(input(" ENTER PINCODE(NUMBER) "))
        new_pass = input(" CREATE YOUR PASSWORD (CASE SENSETIVE) ")
        confirm_pass = input(" CONFIRM YOUR PASSWORD ")

        # password confirmation
        if new_pass == confirm_pass:
            print(" Password matched ")

            # Mysql commands for Bew row in personal_details Table
            query = "INSERT INTO personal_details (Name, contactnumber, Address, city, Pincode, Password) VALUES(%s,%s,%s,%s,%s,%s)"
            val = (name.upper(), phone, address.upper(), city.upper(), str(pincode), new_pass)
            mycursor.execute(query, val)
            con.commit()

            # Fetching assigned Consumer_id (It is auto incremental)
            req = "SELECT Consumer_id FROM techsoc_bankmanagement.personal_details WHERE (contactnumber) = %s and Name = %s"
            val = (phone, name.upper())
            mycursor.execute(req, val)
            res = mycursor.fetchall()
            for i in res[-1]:
                customer_num = i
            query2 = " INSERT INTO balance (Consumer_id) VALUES (%s)"
            val2 = (customer_num,)
            mycursor.execute(query2, val2)
            con.commit()
            print(" OPERATION SUCCESSFUL ")
            print(" Your Customer_id is ", customer_num)

        else:
            print(" PASSWORDS DID NOT MATCH ")                           # Incase passwords do not match
    except:
        print("  UNEXPECTED ERROR . CODE 001")      # Incase of unexpected errors


def login():
    # This function lets user log into their account

    try:                                                        # Try - except method for exception handling
        global customer_num                                     # Declaring global variable
        c_no = int(input(" ENTER CONSUMER NUMBER "))
        passwrd = input(" ENTER PASSWORD ")

        # Mysql command to extract password from Consumer_id from records
        query = "SELECT Password from techsoc_bankmanagement.personal_details WHERE Consumer_id = %s"
        val = (c_no,)
        mycursor.execute(query, val)
        result = mycursor.fetchone()

        # Matching two passwords
        for i in result:
            if i == passwrd:
                customer_num = c_no
                print(" Logged in sucessfully . IDENTITY CONFIRMED ")
            else:
                print(" Wrong password . IDENTITY UNCONFIRMED ")
    except:
        # Incase of unforeseen errors
        print("  UNEXPECTED ERROR . KINDLY CHECK THE SUBMITTING DATA . CODE 002")


def logout():
    # This function helps user in logging out
    global customer_num            # Declararion of global variable
    customer_num = 0
    print("  LOGGED OUT SUCCESSFULLY")


def trans_mod(x,y):
    # This program modifies transaction_history table
    try:
        query = "INSERT INTO techsoc_bankmanagement.transaction_history (Consumer_id,Effect) VALUES(%s,%s)"
        val = (x, y)
        mycursor.execute(query, val)
        con.commit()
    except:
        print("  ERROR ENCOUNTERED . CODE 004")

def balance(x,y):
    # This function is for updating balance table
    try:
        query = "UPDATE balance SET Balance = Balance + %s WHERE Consumer_id = %s"
        val = (y, x)
        mycursor.execute(query, val)
        con.commit()
    except:
        print("  ERROR ENCOUNTERED . CODE 005 .")


def cash_transaction():
    # This function is for cash transactions
    global customer_num          # it is unique primary key used in dbms
    try:
        req = "SELECT Balance from techsoc_bankmanagement.balance WHERE Consumer_id = %s"
        mycursor.execute(req, (customer_num,))
        status = 0  # Variable to store present bank balance
        for i in mycursor.fetchone():
            status = i
        print(" Your current balance is RS ", status)
        print(" 1 - DEPOSIT \n 2 - WITHDRAW \n 3-EXIT ")
        ch = int(input("Choose what to do"))

        # Program for Money deposit
        if ch == 1:
            amt = int(input(" Amount deposited "))
            trans_mod(customer_num, amt)
            balance(customer_num, amt)

        # Program for money withdrawl
        elif ch == 2:
            amt = int(input(" Enter amount to withdraw "))
            if amt < status:
                amt *= (-1)
                trans_mod(customer_num, amt)
                balance(customer_num, amt)
            else:
                print(" NOT ENOUGH BALANCE TO WITHDRAW")
        else:
            pass
    except:
        print("  ERROR ENCOUNTERED . KINDLY CHECK THE SUBMTTED DATA . CODE 006")


def balance_enquiry():
    # This function is for balance enquiry
    global customer_num
    try:
        # Mysql comman for balance extraction using Consumer_id
        req = "SELECT Balance from techsoc_bankmanagement.balance WHERE Consumer_id = %s"
        mycursor.execute(req, (customer_num,))
        status = 0  # Variable to store present bank balance
        for i in mycursor.fetchone():
            status = int(i)
        print("  Your current balance is RS ", status)
    except:
        print("  ERROR ENCOUNTRERED . CODE 007 ")

def trans_history():                        #This gives trANSACTION history to user
    global customer_num
    try:
        query = "SELECT * FROM techsoc_bankmanagement.transaction_history WHERE Consumer_id = %s"
        val = (customer_num,)
        mycursor.execute(query, val)
        print("  TRANSACTION_ID  EFFECT    TRANSACTION TIME     INFO")
        for i in mycursor.fetchall():
            print(i[0], "              ", i[2], "     ", i[3] , "     ",i[4])
    except:
        print("  ERROR ENCOUNTERED . CODE 008")


def bank_transaction():
    # This is for account to account transfers
    try:
        global customer_num
        req = "SELECT Balance from techsoc_bankmanagement.balance WHERE Consumer_id = %s"
        mycursor.execute(req, (customer_num,))
        status = 0  # Variable to store present bank balance
        for i in mycursor.fetchone():
            status = int(i)
        print("  Your current balance is RS ", status)
        recieve_num1 = int(input("Account number of reciever "))
        recieve_amt1 = int(input(" Amount to transfer "))
        recieve_num2 = int(input(" Account number of reciever "))
        recieve_amt2 = int(input(" Amount to transfer "))
        if (recieve_amt1, recieve_num1) == (recieve_amt2, recieve_num2):
            if status > recieve_amt1 and recieve_amt1 > 0:
                balance(customer_num, (-1) * recieve_amt1)
                balance(recieve_num1, recieve_amt1)
                query = "INSERT INTO techsoc_bankmanagement.transaction_history (Consumer_id,Effect,Info) VALUES(%s,%s,%s)"
                str_sender = "SENT TO" + str(recieve_num1)
                val = (customer_num, (-1) * recieve_amt1, str_sender)
                mycursor.execute(query, val)
                con.commit()
                str_recieve = "SENT FROM" + str(customer_num)
                query = "INSERT INTO techsoc_bankmanagement.transaction_history (Consumer_id,Effect,Info) VALUES(%s,%s,%s)"
                val = (recieve_num1, recieve_amt1, str_recieve)
                mycursor.execute(query, val)
                con.commit()
                print(" OPERATION COMPLETED SUCCESSFULLY ")
            else:
                print(" INSUFFICIENT BALANCE ")
        else:
            print(" DETAILS DOES NOT MATCH ")
    except:
        print("  ERROR ENCOUNTERED . CODE 009")


def update():
    # THIS CHANGES DETAILS LIKE CONTACT NUM, ADDRESS ,PASSWORD
    global customer_num
    try:
        print(" WHAT TO UPDATE? ")
        ch = int(input(" 1 - CONTACT NUMBER \n 2 - ADDRESS \n 3-PASSWORD \n 0 - EXIT "))
        if ch == 1:
            print(" PLEASE CONFIRM YOUR IDENTITY ")
            login()
            new_num = input(" NEW NUMBER ")
            query = "UPDATE personal_details SET contactnumber = %s WHERE Consumer_id = %s"
            val = (new_num, customer_num)
            mycursor.execute(query, val)
            con.commit()
            print(" DATA UPDATED SUCCESSFULLY ")
        elif ch == 2:
            print(" PLEASE CONFIRM YOUR IDENTITY ")
            login()
            new_add = input(" NEW ADDRESS ")
            new_city = input(" NEW CITY ")
            new_pin = int(input(" NEW PINCODE "))
            query = "UPDATE techsoc_bankmanagement.personal_details SET Address = %s,city = %s , pincode = %s WHERE Consumer_id = %s"
            val = (new_add.upper(), new_city.upper(), str(new_pin), customer_num)
            mycursor.execute(query, val)
            con.commit()
            print(" DATA UPDATED SUCCESSFULLY ")

        elif ch == 3:
            print("  PLEASE CONFIRM YOUR IDENTITY")
            login()
            new_pass1 = input(" NEW PASSWORD")
            new_pass2 = input(" CONFIRM NEW PASSWORD")
            if new_pass2 == new_pass1:
                query = "UPDATE personal_details SET Password = %s WHERE Consumer_id = %s"
                val = (new_pass1, customer_num)
                mycursor.execute(query, val)
                con.commit()
                print(" DATA UPDATED SUCCESSFULLY")
            else:
                print(" PASSWORDS DO NOT MATCH")
        else:
            pass
    except:
        print("ERROR ENCOUNTERED . CODE 010")


customer_num = 0
while True:
    if customer_num == 0:
        print(" 1 - LOGIN \n 2 - CREATE ACCOUNT \n 0 - EXIT")
        ch = int(input(" WHAT TASK TO PERFORM"))
        if ch == 1:
            login()
        elif ch ==2:
            new_acc()
        else:
            break
    else:
        print("1-CASH TRANSACTION\n2-BALANCE ENQUIRY\n3-TRANSACTION RECORD\n4-BANK TRANSACTION\n5-UPDATE DETAILS\n0-LOGOUT")
        opr = int(input(" WHAT TASK TO PERFORM "))
        if opr == 1:
            cash_transaction()
        elif opr == 2:
            balance_enquiry()
        elif opr == 3:
            trans_history()
        elif opr == 4:
            bank_transaction()
        elif opr == 5:
            update()
        else:
            logout()

print( " THANK YOU ")

"""
FUNCTIONS

new_acc()  creating new user account   001
login()    Login into existing account 002
logout()   Loggig out
trans_mod(x,y)   this adds new row in transaction table 004
balance(x,y)     this is for adding or reducing balance 005
cash_transaction() this is for feature like atm where cash to digital value occur 006
balance_enquiry()  this shows current balance to user 007
trans_history()    this shows transactio history to user ( self means cash trans) 008
bank_transaction() this acts like upi/cheque where no cash involved   009
update()            this updates user informaton  010


"""