from tkinter import *
import mysql.connector
from tkinter import messagebox
from tkinter import ttk

#Global variable(s) to assist the program
flag=False

#Main GUI for the System
manage=Tk()
manage.title("Bank Management System")
manage.configure(bg="cornflower blue")

#Connecting python to MySQL Server
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)

#Creating a cursor
my_cursor=mydb.cursor()

#Creating a database
db=("Management",)
try:
    my_cursor.execute("CREATE DATABASE IF NOT EXISTS Management;")
except Exception as e:
    print("Something went wrong!",e)
    pass
else:
    print(mydb)

#Connecting to MySQL Server with tuple
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database=db[0]
)

#Creating a cursor again
my_cursor=mydb.cursor()

#Creating Table and its columns
try:
    my_cursor.execute("CREATE TABLE IF NOT EXISTS users(name VARCHAR(255),"
                      "email VARCHAR(255),"
                      "password VARCHAR(255),"
                      "balance INTEGER(10),"
                      "user_id INTEGER AUTO_INCREMENT Primary KEY);")
except Exception as e:
    print("Something went wrong!",e)
    pass
else:
    my_cursor.execute("SHOW TABLES;")
    result=my_cursor.fetchall()
    for row in result:
        print(row)

#Label for Main GUI
heading=Label(manage,text="Bank Management",font=("Times",20,"bold"),bg="cornflower blue")
heading.grid(row=0,column=1)

#Labels for Register Entries
username=Label(manage,text="Username",font=18,bg="cornflower blue")
username.grid(row=1,column=0)
email=Label(manage,text="Email:",font=18,bg="cornflower blue")
email.grid(row=2,column=0)
password=Label(manage,text="Password:",font=18,bg="cornflower blue")
password.grid(row=3,column=0)

#Entries for Registration
Entry_username=Entry(manage,width=25,borderwidth=5)
Entry_username.grid(row=1,column=1)
Entry_email=Entry(manage,width=25,borderwidth=5)
Entry_email.grid(row=2,column=1)
Entry_password=Entry(manage,width=25,borderwidth=5)
Entry_password.grid(row=3,column=1)

def show_records():
    showrec = Tk()
    showrec.title("Records Database")
    iteration = 0

    # Creating a tree view for database
    my_tree = ttk.Treeview(showrec)
    my_tree['columns'] = ("Account No.","Names", "Emails", "Balance")

    # Formatting the columns
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("Account No.", width=100, minwidth=30, anchor=CENTER)
    my_tree.column("Names", width=100, minwidth=25)
    my_tree.column("Emails", width=150, minwidth=25)
    my_tree.column("Balance", width=120, minwidth=25, anchor=CENTER)

    # Headings of Tree columns
    my_tree.heading("#0", text="")
    my_tree.heading("Account No.", text="Account No.")
    my_tree.heading("Names", text="Names")
    my_tree.heading("Emails", text="Emails")
    my_tree.heading("Balance", text="Balance")

    # Adding data into the tree
    my_cursor.execute("SELECT name,email,balance,user_id FROM Management.users;")
    result = my_cursor.fetchall()
    for row in result:
        if(row[2]==None):
            my_tree.insert(parent='', index='end', iid=iteration, text="",
                           values=(row[3], row[0], row[1], "N/A"))
            iteration = iteration + 1
        else:
            my_tree.insert(parent='', index='end', iid=iteration, text="",
                           values=(row[3], row[0], row[1], row[2]))
            iteration = iteration + 1
    my_tree.grid(row=1, column=0)
    showrec.mainloop()
    return iteration

#Inserting data into the table
def registration():
    class register:
        def __init__(self,master,e1,e2,e3):
            record = (e2,)
            my_cursor.execute("SELECT email FROM Management.users WHERE email=(%s);", record)
            result = my_cursor.fetchone()
            if (e1 != "" and e2 != "" and e3 != ""):
                if ('@' in e2):
                    if (result == None):
                        insert = "INSERT INTO users(name,email,password) VALUES (%s,%s,%s);"
                        record = (e1, e2, e3)
                        my_cursor.execute(insert, record)
                        mydb.commit()
                        Entry_username.focus_set()
                        messagebox.showinfo("Successful!", "     Registration Completed!    ")
                    elif (Entry_email.get() in result[0]):
                        messagebox.showinfo("Failed!", "Entry already exists!")
                    else:
                        messagebox.showinfo("Failed!", "Something Went Wrong!")
                else:
                    messagebox.showinfo("Failed!", "Invalid Email!")
            else:
                messagebox.showinfo("Failed!", "Empty Fields!!")
    register(manage,Entry_username.get(),Entry_email.get(),Entry_password.get())

#Declaring Empty Label to store data in global scope
bal0=Label()
bal0.destroy()

#Logging in the user
def login():
    global flag
    counter=0
    my_cursor.execute("SELECT name, email, password FROM Management.users;")
    result = my_cursor.fetchall()

    if (Entry_username.get() != "" or Entry_email.get() != "" or Entry_password.get() != ""):
        for row in result:
            flag=False
            if (Entry_username.get() == row[counter] and Entry_email.get() == row[
                counter + 1] and Entry_password.get() == row[counter + 2] and '@' in Entry_email.get()):
                flag=True
                break
        if(flag):

            # Tuple for permanent storage of entries
            entries = (Entry_email.get(), Entry_password.get())

            logged = Tk()
            logged.title("Welcome User!")
            logged.configure(bg="salmon1")

            messagebox.showinfo("Logged in!", "You have logged in successfully!")
            temp = (entries[0],)
            my_cursor.execute("SELECT name FROM Management.users WHERE email=(%s)", temp)
            resultone = my_cursor.fetchone()

            Title = Label(logged, text="Welcome " + resultone[0] + "!", font=("Times", 20, "bold"),bg="salmon1")
            Title.grid(row=0, column=1)

            my_cursor.execute("SELECT balance FROM Management.users WHERE email=(%s)", temp)
            resultone = my_cursor.fetchone()
            if(resultone[0]==None):
                bal0 = Label(logged, text="Balance: N/A", font=18,bg="salmon1")
                bal0.grid(row=1, column=0)
            else:
                bal0 = Label(logged, text="Balance: " + str(resultone[0]), font=18,bg="salmon1")
                bal0.grid(row=1, column=0)

            # Labels and Entries for logged-in users
            bala = Label(logged, text="Transaction:", font=18,bg="salmon1")
            bala.grid(row=2, column=0)
            balance = Entry(logged, width=25, borderwidth=5)
            balance.grid(row=2, column=1)
            rpassw = Label(logged, text="Reset Password:", font=18,bg="salmon1")
            rpassw.grid(row=3, column=0)
            rpas = Entry(logged, width=25, borderwidth=5)
            rpas.grid(row=3, column=1)

            # Function to deposit
            def deposit():
                global bal0
                bal0.destroy()
                if (balance.get() != ""):
                    if (int(balance.get()) > 0):
                        bal = balance.get()
                        erms = (entries[0], entries[1])
                        my_cursor.execute("SELECT balance FROM Management.users WHERE email=(%s) AND password=(%s);",
                                          erms)
                        resul = my_cursor.fetchone()
                        if (resul[0] == None):
                            sel = (bal, entries[0], entries[1])
                            my_cursor.execute(
                                "UPDATE Management.users SET balance=(%s) WHERE email=(%s) AND password=(%s);", sel)
                            mydb.commit()
                            my_cursor.execute("SELECT balance FROM Management.users WHERE email=(%s)", temp)
                            resultone = my_cursor.fetchone()
                            bal0 = Label(logged, text="Balance: " + str(resultone[0]),font=18,bg="salmon1")
                            bal0.grid(row=1, column=0)
                            messagebox.showinfo("Successful!", "Added Balance to Account!")
                        elif (int(balance.get()) > 0):
                            bal = int(bal)
                            resul = resul[0]
                            resul = int(resul)
                            sum = resul + bal
                            update = (sum, entries[0], entries[1])
                            my_cursor.execute(
                                "UPDATE Management.users SET balance=(%s) WHERE email=(%s) AND password=(%s);", update)
                            mydb.commit()
                            my_cursor.execute("SELECT balance FROM Management.users WHERE email=(%s)", temp)
                            resultone = my_cursor.fetchone()
                            bal0 = Label(logged, text="Balance: " + str(resultone[0]),font=18,bg="salmon1")
                            bal0.grid(row=1, column=0)
                            messagebox.showinfo("Successful!", "Updated Balance to Account!")
                        else:
                            messagebox.showinfo("Warning", "Something went wrong!")
                    else:
                        messagebox.showinfo("Warning", "Enter a number!")
                else:
                    messagebox.showinfo("Warning!","Empty Balance field!")

            # Function to withdraw
            def withdraw():
                global bal0
                bal0.destroy()
                if (balance.get()!=""):
                    if (int(balance.get()) > 0):
                        bal = balance.get()
                        erms = (entries[0], entries[1])
                        my_cursor.execute("SELECT balance FROM Management.users WHERE email=(%s) AND password=(%s);",
                                          erms)
                        resul = my_cursor.fetchone()
                        if (resul[0] == None):
                            bal = bal * -1
                            sel = (bal, entries[0], entries[1])
                            my_cursor.execute(
                                "UPDATE Management.users SET balance=(%s) WHERE email=(%s) AND password=(%s);", sel)
                            mydb.commit()
                            bal0 = Label(logged, text="Balance: " + str(resul[0]),font=18,bg="salmon1")
                            bal0.grid(row=1, column=0)
                            messagebox.showinfo("Successful!", "Updated Balance from Account!")
                        elif (int(balance.get()) > 0 and int(balance.get()) <= resul[0]):
                            bal = int(bal)
                            resul = resul[0]
                            resul = int(resul)
                            sum = resul - bal
                            update = (sum, entries[0], entries[1])
                            my_cursor.execute(
                                "UPDATE Management.users SET balance=(%s) WHERE email=(%s) AND password=(%s);", update)
                            mydb.commit()
                            my_cursor.execute("SELECT balance FROM Management.users WHERE email=(%s)", temp)
                            resultone = my_cursor.fetchone()
                            bal0 = Label(logged, text="Balance: " + str(resultone[0]),font=18,bg="salmon1")
                            bal0.grid(row=1, column=0)
                            messagebox.showinfo("Successful!", "Updated Balance from Account!")
                        else:
                            messagebox.showinfo("Warning", "Not Enough Balance")
                    else:
                        messagebox.showinfo("Warning", "Enter a number!")
                else:
                    messagebox.showinfo("Warning!","Empty Balance field!")

            # Deleting records from database
            def delete():
                erms = (entries[0], entries[1])
                my_cursor.execute("DELETE FROM Management.users WHERE email=(%s) AND password=(%s);", erms)
                mydb.commit()
                messagebox.showinfo("Successful!", "Deleted account successfully!")
                logged.destroy()

            # Resetting the password
            def reset():
                if (rpas.get() != ""):
                    erms = (rpas.get(), entries[0], entries[1])
                    my_cursor.execute("UPDATE Management.users SET password=(%s) WHERE email=(%s) AND password=(%s);",
                                      erms)
                    mydb.commit()
                    messagebox.showinfo("Successful!", "The password has been reset!")
                else:
                    messagebox.showinfo("Warning!","Empty Reset Password field!")

            # Empty Labels to configure Buttons
            Label1 = Label(logged, text="",bg="salmon1")
            Label1.grid(row=4, column=1)
            Label2=Label(logged,text="",bg="salmon1")
            Label2.grid(row=6,column=1)

            #Buttons for logged in users
            dele = Button(logged, text="Delete", command=delete,padx=2,pady=2,bg="dark sea green")
            dele.grid(row=7, column=1)
            withd = Button(logged, text="Withdraw", command=withdraw,padx=2,pady=2,bg="dark sea green")
            withd.grid(row=5, column=0)
            depo = Button(logged, text="Deposit", command=deposit,padx=2,pady=2,bg="dark sea green")
            depo.grid(row=5, column=1)
            Reset = Button(logged, text="Reset", command=reset,padx=2,pady=2,bg="dark sea green")
            Reset.grid(row=7, column=0)
            logged.mainloop()
        else:
            messagebox.showinfo("Warning!", "Invalid Login!")

    else:
        messagebox.showinfo("Failed!", "          Empty Fields!         ")
    flag=False

#Empty Labels to configure Buttons
Label1=Label(manage,text="",bg="cornflower blue")
Label1.grid(row=4,column=1)

#Button(s) for GUI
regis=Button(manage,text="Register",command=registration,padx=2,pady=2,bg="blanched almond")
regis.grid(row=5,column=1)
log = Button(manage, text="Login", command=login,padx=2,pady=2,bg="blanched almond")
log.grid(row=5,column=2)
rec=Button(manage,text="Show Records",command=show_records,padx=2,pady=2,bg="blanched almond")
rec.grid(row=5,column=0)

#Putting main GUI in a loop
manage.mainloop()