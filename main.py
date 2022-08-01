import json
import random
import tkinter as tk
from tkinter import messagebox
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []
    password_list += [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_list += [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_list += [random.choice(numbers) for _ in range(random.randint(2, 4))]

    random.shuffle(password_list)

    password = "".join([word for word in password_list])
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if not (bool(website) and bool(email) and bool(password)):
        messagebox.showinfo(title="Opps", message="Pleas make sure you haven't left any fields empty.")
    else:
        try:
            with open("./data.json", mode="r") as data_file:
                data = json.load(data_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open("./data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("./data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            website_entry.focus()


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()

    def not_registered_message():
        messagebox.showwarning(title="Not Registered", message=f"Site {website} is not registered.")

    try:
        with open("./data.json", mode="r") as data_file:
            json_data = json.load(data_file)
    except FileNotFoundError:
        not_registered_message()
    else:
        if website in json_data:
            password = json_data[website]["password"]
            email = json_data[website]["email"]
            messagebox.showinfo(title="Site Information", message=f"Password: {password}\nEmail: {email}")
        else:
            not_registered_message()


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = tk.Canvas(height=200, width=200)
logo_image = tk.PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=logo_image)

# row = 0
canvas.grid(row=0, column=1)

# Labels
website_label = tk.Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = tk.Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = tk.Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = tk.Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2, sticky="EW")
website_entry.focus()

email_entry = tk.Entry(width=35)
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
email_entry.insert(tk.END, "test@email.com")

password_entry = tk.Entry(width=21)
password_entry.grid(row=3, column=1, sticky="EW")

# Buttons
search_button = tk.Button(text="Search", command=find_password)
search_button.grid(row=1, column=2, sticky="EW")

generate_button = tk.Button(text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=2, sticky="EW")

add_button = tk.Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

window.mainloop()
