import tkinter as tk
import mysql.connector
import os
import csv
import smtplib
from email.mime.text import MIMEText

os.system("cls" if os.name == "nt" else "clear")

conexao = mysql.connector.connect(host='localhost', user='root', passwd='')

x = conexao.cursor()

x.execute("show databases like 'my_db'")

result = x.fetchone()

if not result:
    x.execute("create database my_db")
    print("The database has been created!")
    conexao = mysql.connector.connect(host = 'localhost', user = 'root', passwd = '', database = 'my_db')
    x = conexao.cursor()


if result:
    print("Database connected!")
    conexao = mysql.connector.connect(host = 'localhost', user = 'root', passwd = '', database = 'my_db')
    x = conexao.cursor()


x.execute("create table if not exists users (id int auto_increment primary key, name varchar(50) not null, lastName varchar(50) not null, age int(3) not null, email varchar(50) not null, telephone varchar(10) not null)")

# Create a window
r = tk.Tk()

r.title("Register")

r.geometry("450x500")

r.wm_iconbitmap("aditionals/favicon.ico")

r['bg'] = "#444654"

title = tk.Label(r, text = 'Register', bg = "#444654", fg = "#fff", font = ("Arial", 20, "bold")).grid(row = 0, column = 0, columnspan = 2, padx = 50)

labelName = tk.Label(r, text = 'Name:', bg = "#444654", fg = "#fff").grid(row = 1, column = 0)

labelLastName = tk.Label(r, text = 'Last Name:', bg = "#444654", fg = "#fff").grid(row = 2, column = 0)

labelAge = tk.Label(r, text = 'Age:', bg = "#444654", fg = "#fff").grid(row = 3, column = 0)

labelEmail = tk.Label(r, text = 'Email:', bg = "#444654", fg = "#fff").grid(row = 4, column = 0)

labelTelephone = tk.Label(r, text = 'Telephone:', bg = "#444654", fg = "#fff").grid(row = 5, column = 0)

inputName = tk.Entry(r, width = 30)
inputName.grid(row = 1, column = 1)

inputLastName = tk.Entry(r, width = 30)
inputLastName.grid(row = 2, column = 1)

inputAge = tk.Entry(r, width = 30)
inputAge.grid(row = 3, column = 1)

inputEmail = tk.Entry(r, width = 30)
inputEmail.grid(row = 4, column = 1)

inputTelephone = tk.Entry(r, width = 30)
inputTelephone.grid(row = 5, column = 1 )


def save_data():
    name = inputName.get()
    lastName = inputLastName.get()
    age = inputAge.get()
    email = inputEmail.get()
    telephone = inputTelephone.get()

    if name != "" or lastName != "" or age != "" or email != "" or telephone != "":
        x.execute('insert into users (name, lastName, age, email, telephone) values (%s, %s, %s, %s, %s)', (name, lastName, age, email, telephone))
        conexao.commit()

        dir_name1 = f"CLIENTS"
        dir_name2 = f"{name.upper()}_{lastName.upper()}"
        csv_filename = f"{name.upper()}_{lastName.upper()}.csv"

        if not os.path.exists(dir_name1):
            os.mkdir(dir_name1)

        if not os.path.exists(os.path.join(dir_name1, dir_name2)):
            os.mkdir(os.path.join(dir_name1, dir_name2))

        csv_filepath = os.path.join(dir_name1, dir_name2, csv_filename)

        with open(csv_filepath, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f"Name: {name}\nLast Name: {lastName}\nAge: {age}\nEmail: {email}\nTelephone: {telephone}"])

        message = f"Welcome {name.capitalize()}"
        txtArea.config(text = message, fg = "#10a37f", font = ("Arial", 15, "bold"))

        # sender = 'your_email@example.com'
        # recipient = 'recipient_email@example.com'
        # subject = 'Your subject line'
        # body = 'The content of your email'

        # msg = MIMEText(body)
        # msg['From'] = sender
        # msg['To'] = recipient
        # msg['Subject'] = subject

        # # Send the email
        # with smtplib.SMTP('your_mail_server_address', your_mail_server_port) as smtp:
        #     smtp.login('your_mail_server_username', 'your_mail_server_password')
        #     smtp.send_message(msg)

    else:
        message = "Error: Could not register!"
        txtArea.config(text = message, fg = "#c30b06", font = ("Arial", 15, "bold"))


btnRegister = tk.Button(r, text = 'Register', width = 20, bg = "#fff", fg = "#444654", command = save_data).grid(row = 6, column = 0, columnspan = 2, pady = 10)

txtArea = tk.Label(r, text = "", bg = "#444654")
txtArea.grid(row = 7, column = 0, columnspan = 2)

r.mainloop()