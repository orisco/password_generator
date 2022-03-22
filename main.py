from tkinter import *
from tkinter import messagebox
import pyperclip
import random
import json

WHITE = "white"
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_input.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [char for char in random.choices(letters, k=random.randint(6, 8))]
    password_list += [char for char in random.choices(symbols, k=random.randint(2, 4))]
    password_list += [char for char in random.choices(numbers, k=random.randint(2, 4))]

    random.shuffle(password_list)
    new_password = "".join(password_list)
    password_input.insert(0, new_password)
    pyperclip.copy(new_password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def clear_fields():
    website_input.delete(0, END)
    email_input.delete(0, END)
    password_input.delete(0, END)


def on_add():
    website = website_input.get().lower()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0:
        messagebox.showerror(title="website",
                             message="Please enter the website's name")

    if "@" not in email or "." not in email:
        messagebox.showerror(title="email invalid",
                             message="The email you have entered is invalid. please enter a valid email")
        return
    if len(password) < 6:
        messagebox.showerror(title="password too short",
                             message="The password you've entered is too short")
        return

    response = messagebox.askokcancel(title=website, message=f"These are the details entered:"
                                                             f"\nEmail: {email}\nPassword: {password}\n"
                                                             f"Is it ok to save?")
    if response:
        try:
            with open("data.json", "r") as data_file:
                passwords_file = json.load(data_file)
                passwords_file.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(passwords_file, data_file, indent=4)

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)

        finally:
            clear_fields()
    else:
        return
# ---------------------------- SEARCH ------------------------------- #

def search_website():
    website = website_input.get().lower()
    try:
        with open("data.json", "r") as data_file:
            passwords_file = json.load(data_file)

    except FileNotFoundError:
        messagebox.showerror(message="No password file found")

    else:
        if website in passwords_file:
            email = passwords_file[website]['email']
            password = passwords_file[website]['password']
            messagebox.showinfo(title=website, message=f"email: {email}\npassword: {password}")
        else:
            messagebox.showerror(message="No website info found")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(pady=20, padx=20, bg=WHITE)
canvas = Canvas(width=200, height=200, bg=WHITE, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:", background="white", fg="black")
website_label.grid(column=0, row=1)

website_input = Entry(width=21, background="white", fg="black", highlightthickness=0, insertbackground="black")
website_input.grid(column=1, row=1)
website_input.focus()

search_button = Button(text="Search", width=11, background="white", fg="black", highlightbackground="white", command=search_website)
search_button.grid(column=2, row=1)

email_label = Label(text="Email:", background="white", fg="black")
email_label.grid(column=0, row=2)

email_input = Entry(width=36, background="white", fg="black", highlightthickness=0, insertbackground="black")
email_input.grid(column=1, row=2, columnspan=2)

password_label = Label(text="Password", background="white", fg="black")
password_label.grid(column=0, row=3)

password_input = Entry(width=21, background="white", fg="black", highlightthickness=0, insertbackground="black")
password_input.grid(column=1, row=3)

generate_pass_button = Button(text="Generate Password", width=11, background="white", fg="black", highlightbackground="white", command=generate_password)
generate_pass_button.grid(column=2, row=3)

add_button = Button(text="Add", width=33, background="white", fg="black", highlightthickness=0,  highlightbackground="white", command=on_add)
add_button.grid(column=1, row=4, columnspan=2)
window.mainloop()