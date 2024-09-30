import tkinter.messagebox
from tkinter import *
import pymysql as pm
from PIL import ImageTk, Image
import random
import string
from email.message import EmailMessage
import ssl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import Label, Tk, messagebox

def print_statement():
    return

# Database connection
def get_db_connection():
    return pm.connect(
        host='localhost',
        user='root',  # replace with your MySQL user
        password='',  # replace with your MySQL password
        database='registrations'  # replace with your database name
    )

def add_money(account_number, amount):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            print(f"Attempting to add {amount} to account {account_number}")  # Debugging
            # Add amount to balance, ensuring balance is not NULL
            cursor.execute(
                "UPDATE registrations SET balance = COALESCE(balance, 0) + %s WHERE TRIM(account_number) = TRIM(%s)",
                (amount, account_number)
            )
            connection.commit()

            # Check how many rows were affected
            rows_affected = cursor.rowcount
            print(f"Rows affected: {rows_affected}")
            if rows_affected == 0:
                print("No rows were updated. Check if the account number exists.")
                messagebox.showwarning("Error", "Account number not found.")
            else:
                print("Amount added successfully")
                messagebox.showinfo("Success", "Amount added successfully.")
    except pm.MySQLError as e:
        # Catch SQL errors and print them
        print(f"Error while adding money: {e}")
        messagebox.showerror("Database Error", f"Error while adding money: {e}")
    finally:
        connection.close()



# Function to check balance with debugging
def check_balance(account_number):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            print(f"Checking balance for account number: {account_number}")  # Debugging line
            cursor.execute("SELECT balance FROM registrations WHERE TRIM(account_number) = %s", (account_number,))
            balance = cursor.fetchone()
            if balance:
                print(f"Balance fetched: {balance[0]}")  # Debugging line
                messagebox.showinfo("Balance", f"Your balance is: {balance[0]}")
            else:
                print("Account not found")  # Debugging line
                messagebox.showwarning("Error", "Account not found.")
    finally:
        connection.close()

# Function to withdraw money with debugging
# Function to handle withdrawal (using float)
def withdrawal(account_number, amount):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            print(f"Withdrawing from account number: {account_number}")  # Debugging line
            cursor.execute("SELECT balance FROM registrations WHERE TRIM(account_number) = %s", (account_number,))
            balance = cursor.fetchone()

            if balance:
                current_balance = float(balance[0])  # Convert balance to float
                print(f"Current balance: {current_balance}")  # Debugging line
                if current_balance >= amount:
                    cursor.execute(
                        "UPDATE registrations SET balance = balance - %s WHERE TRIM(account_number) = TRIM(%s)",
                        (amount, account_number)
                    )
                    connection.commit()

                    new_balance = current_balance - amount  # Calculate new balance
                    messagebox.showinfo("Success", f"Withdrawal successful. Your new balance is: {new_balance}")
                else:
                    messagebox.showwarning("Error", "Insufficient balance.")
            else:
                print("Account not found")  # Debugging line
                messagebox.showwarning("Error", "Account not found.")
    finally:
        connection.close()



# Popup window to input the amount
def open_amount_popup(account_number, operation):
    popup = Toplevel()
    popup.title(f"{operation.capitalize()} Money")
    popup.geometry("300x200")

    # Label and Entry for amount
    Label(popup, text="Enter Amount:").pack(pady=10)
    amount_entry = Entry(popup)
    amount_entry.pack(pady=10)

    # Confirm button to process the input
    def confirm_action():
        try:
            amount = float(amount_entry.get())
            if operation == "add":
                add_money(account_number, amount)
            elif operation == "withdraw":
                withdrawal(account_number, amount)
            popup.destroy()  # Close the popup window after confirming
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")

    Button(popup, text="Confirm", command=confirm_action).pack(pady=10)


def home_window(account_number):
    # Clear all widgets in the root window
    for widget in root.winfo_children():
        widget.destroy()

    con = pm.connect(host='localhost', user='root', password='', db='registrations')
    c = con.cursor()

    # Strip spaces from account_number to avoid mismatch due to extra spaces
    account_number = account_number.strip()

    # Debugging: Print the account number and query
    # print(f"Account Number: {account_number}")
    query = 'SELECT name FROM registrations WHERE TRIM(LOWER(account_number)) = LOWER(%s)'
    # print(f"Executing query: {query} with account_number: {account_number}")

    # Execute the query
    c.execute(query, (account_number,))

    # Fetch the result
    re = c.fetchone()


    # If record is found
    if re:
        name = re[0]  # Since we are only selecting 'name', it will be in the first position (index 0)

        # Display labels
        Label(root, text=f"Welcome {name}").place(x=300, y=60)
        Label(root, text=f"Account Number: {account_number}").place(x=250, y=40)
        Label(root, text=f"NAME: {name}!").place(x=300, y=20)

    # Close the connection
    con.close()

    Button(root, text="Add Money", command=lambda: open_amount_popup(account_number, "add")).place(x=250, y=170)

    # Button to withdraw money
    Button(root, text="Withdrawal", command=lambda: open_amount_popup(account_number, "withdraw")).place(x=350, y=170)

    # Button to check balance
    Button(root, text="Check Balance", command=lambda: check_balance(account_number)).place(x=290, y=210)


    Button(root, text="Go Home page", command=show_main_content).place(x=290, y=250)

# Assuming you're inside your user_home window setup
    Button(root, text="Print Statement", command=print_statement).place(x=300, y=250)


# HX7368





def login():
    logmail = email_log_entry.get()
    logpass = pass_log_entry.get()
    if logmail == '' or logpass == '':
        tkinter.messagebox.showinfo('error', 'check your fields')
    else:
        con = pm.connect(host='localhost', user='root', password='', db='registrations')
        c = con.cursor()
        uq = 'update registrations set account_number = TRIM(account_number),password = TRIM(password);'
        c.execute(uq)
        c.execute('select * from registrations where account_number = %s AND password = %s;', (logmail, logpass))  # Fix the query
        re = c.fetchone()

        if re is None:  # Corrected comparison
            tkinter.messagebox.showinfo('Error', 'Login failed')
        else:
            tkinter.messagebox.showinfo('Success', 'Login successful')
            home_window(logmail,)

def login_window():
    global email_log_entry
    global pass_log_entry
    for widget in root.winfo_children():
        widget.destroy()

        Label(root, text="Account Number:").place(x=200, y=80)
        Label(root, text="Password:").place(x=200, y=120)

        email_log_entry = Entry(root)
        pass_log_entry = Entry(root)

        email_log_entry.place(x=320, y=80)
        pass_log_entry.place(x=320, y=120)
        Button(root, text="Sign up", command=register_window).place(x=290, y=170)
        Button(root, text="login", command=login).place(x=380, y=170)

def generate_bank_account_number():
    # Generate the first two letters
    first_two_letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    # Generate the remaining four digits
    remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    # Combine letters and digits
    return f"{first_two_letters}{remaining_digits}"



def submit_form():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    password = pass_entry.get().strip()
    contact_number = contact_entry.get().strip()
    address = address_entry.get().strip()

    if name == '' or email == '' or password == '' or contact_number == '' or address == '':
        tkinter.messagebox.showinfo('error', 'check your fields')
    else:
        account_number = generate_bank_account_number()
        print("Generated Bank Account Number:", account_number)
        con = pm.connect(host='localhost', user='root', password='', db='registrations')
        c = con.cursor()
        c.execute(
            "insert into registrations(name,email,password,contact_number,address,account_number)values"
            "(' " + name + " ',' " + email + " ',' " + password + " ',' " + contact_number + " ',' " + address + " ',' " + account_number + " ');")
        con.commit()
        con.close()


        sender = 'farhanareekode@gmail.com'
        pswd = 'fzqz ztcu strr vorm'
        reciver = email
        subject = 'Bank service'

        em = MIMEMultipart()
        em['From'] = sender
        em['To'] = reciver
        em['Subject'] = subject

        html_msg = f"""
            <html>
                    <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                        <h2 style="color: #2c3e50;">Dear {name},</h2>
                        <p><b>Thank you for registering at ATM system committed to 
                        providing you with the best Bank services.</p>
                        <p>Your Account Number:{account_number},</P>
                    </body>
                </html>
        """
        html_part  = MIMEText(html_msg, 'html')
        em.attach(html_part)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smpt:
            smpt.login(sender, pswd)
            smpt.sendmail(sender, reciver, em.as_string())


        tkinter.messagebox.showinfo('Alert', 'Registration completed Check Your Email for get Account number to login')
        login_window()



################## Register Page#####################
def register_window():
    global name_entry
    global email_entry
    global contact_entry
    global address_entry
    global pass_entry
    # Clear the window content first
    for widget in root.winfo_children():
        widget.destroy()
        p = Image.open("/home/muhammed/python_fullstack/24.thinkender/image/bl.jpg")
        p = p.resize((700, 700))
        p = ImageTk.PhotoImage(p)

        pic = Label(root, image=p)
        pic.place(x=0, y=0)
        Label(root, text="Name:").place(x=170, y=120)
        Label(root, text="Email:").place(x=170, y=160)
        Label(root, text="Contact Number:").place(x=170, y=200)
        Label(root, text="Address:").place(x=170, y=240)
        Label(root, text="password:").place(x=170, y=280)

        name_entry = Entry(root)
        email_entry = Entry(root)
        contact_entry = Entry(root)
        address_entry = Entry(root)
        pass_entry = Entry(root)

        name_entry.place(x=330, y=120)
        email_entry.place(x=330, y=160)
        contact_entry.place(x=330, y=200)
        address_entry.place(x=330, y=240)
        pass_entry.place(x=330, y=280)

        Button(root, text="Register", command=submit_form).place(x=250, y=350)
        Button(root, text="Login", command=login_window).place(x=350, y=350)

def show_main_content():
    for widget in root.winfo_children():
        widget.destroy()
    welcome_label = tkinter.Label(root, text="Welcome to Bank ESA", font=("Arial", 24, "bold"), fg="blue")
    welcome_label.pack(pady=20)
    Button(root, text="Sign up", command=register_window).place(x=250, y=350)
    Button(root, text="Login", command=login_window).place(x=350, y=350)


root = Tk()
root.title("ESA Bank")
root.geometry("700x700")
Label(root, text="").place(x=170, y=280)
show_main_content()
root.mainloop()