# import MySQLdb
import time
import tkinter as tk
from tkinter import messagebox

from sql_connector import SQLiteConnector


class RegisterPage:
    def __init__(self, master):
        self.master = master

        self.master.title("Yummy Pizza Register")

        self.username_label = tk.Label(self.master, text="Username:", bg="#38726c")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self.master)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.master, text="Password:", bg="#38726c")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.grid(row=1, column=1)

        self.password_re_enter_label = tk.Label(
            self.master, text="Re-enter Password:", bg="#38726c"
        )
        self.password_re_enter_label.grid(row=2, column=0)
        self.password_re_entry = tk.Entry(self.master, show="*")
        self.password_re_entry.grid(row=2, column=1)

        self.login_button = tk.Button(
            self.master,
            text="Register",
            command=self.register,
            highlightcolor="#38726c",
            highlightbackground="#38726c",
        )
        self.login_button.grid(row=3, column=1)

        self.login_page = tk.Button(
            self.master,
            text="Already have and account",
            command=self.get_login_page,
            highlightcolor="#38726c",
            highlightbackground="#38726c",
        )
        self.login_page.grid(row=4, column=1)

        self._db_connector = SQLiteConnector(database="database/shop.db")
        self.create_table()

    def create_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
            )
        """
        self._db_connector.execute_insert_query(create_table_query)

    def get_login_page(self):
        self.master.withdraw()
        login_root = tk.Tk()
        login_root.configure(background="#38726c")
        LoginPage(
            login_root,
        )
        login_root.mainloop()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        password_re_entry = self.password_re_entry.get()

        if password != password_re_entry:
            messagebox.showerror("Error", "Password doesn't match")
            return

        result = self._db_connector.execute_insert_query(
            "INSERT INTO USERS(username, password) VALUES(?, ?)", (username, password)
        )

        self.get_login_page()


class LoginPage:
    def __init__(self, master):
        self.master = master

        self.master.title("Yammy Pizza Login")

        self.username_label = tk.Label(self.master, text="Username:", bg="#38726c")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self.master)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.master, text="Password:", bg="#38726c")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(
            self.master,
            text="Login",
            command=self.login,
            highlightcolor="#38726c",
            highlightbackground="#38726c",
        )
        self.login_button.grid(row=2, column=1)

        self._db_connector = SQLiteConnector(database="database/shop.db")
        self.create_table()

    def create_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
            )
        """
        self._db_connector.execute_insert_query(create_table_query)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        result = self._db_connector.execute_fetch_query(
            "SELECT * FROM users WHERE username=? AND password=?", (username, password)
        )

        if result:
            self.master.withdraw()
            main_app = tk.Toplevel(self.master)
            main_app.configure(background="#38726c")
            app = YammyPizzaApp(
                main_app, database="database/shop.db"
            )  # Connecting to the next screen.
            main_app.protocol("Login Close", app.close_app)
            main_app.mainloop()
        else:
            messagebox.showerror("Error", "Invalid login credentials")


class YammyPizzaApp:
    def __init__(self, master, database):
        self.master = master
        self.master.title("Yammy Pizza Information")

        self.insert_button = tk.Button(
            self.master,
            text="Insert",
            command=self.insert_address,
            highlightcolor="#38726c",
            highlightbackground="#38726c",
        )
        self.insert_button.grid(row=5, column=0)

        self.search_label = tk.Label(
            self.master, text="Enter street name (Search): ", bg="#38726c"
        )
        self.search_label.grid(row=0, column=1)
        self.search_entry = tk.Entry(self.master)
        self.search_entry.grid(row=0, column=2)
        self.search_button = tk.Button(
            self.master,
            text="Search",
            command=self.search_address,
            highlightcolor="#38726c",
            highlightbackground="#38726c",
        )
        self.search_button.grid(row=0, column=3)

        self.street_label = tk.Label(self.master, text="Street:", bg="#38726c")
        self.street_label.grid(row=1, column=0)
        self.street_entry = tk.Entry(self.master)
        self.street_entry.grid(row=1, column=1)

        self.city_label = tk.Label(self.master, text="City:", bg="#38726c")
        self.city_label.grid(row=2, column=0)
        self.city_entry = tk.Entry(self.master)
        self.city_entry.grid(row=2, column=1)

        self.state_label = tk.Label(self.master, text="State:", bg="#38726c")
        self.state_label.grid(row=3, column=0)
        self.state_entry = tk.Entry(self.master)
        self.state_entry.grid(row=3, column=1)

        self.zipcode_label = tk.Label(self.master, text="Zip Code:", bg="#38726c")
        self.zipcode_label.grid(row=4, column=0)
        self.zipcode_entry = tk.Entry(self.master)
        self.zipcode_entry.grid(row=4, column=1)

        self.update_button = tk.Button(
            self.master,
            text="Update",
            command=self.update_address,
            highlightcolor="#38726c",
            highlightbackground="#38726c",
        )
        self.update_button.grid(row=5, column=1)

        self.fetch_button = tk.Button(
            self.master,
            text="Fetch & Display",
            command=self.fetch_and_display_address,
            highlightcolor="#38726c",
            highlightbackground="#38726c",
        )
        self.fetch_button.grid(row=5, column=2)

        self._connector = SQLiteConnector(database=database)

    def insert_address(self):
        street = self.street_entry.get()
        city = self.city_entry.get()
        state = self.state_entry.get()
        zipcode = self.zipcode_entry.get()

        try:
            self._connector.execute_insert_query(
                "INSERT INTO address (STREET, CITY, STATE, ZIP) VALUES (?, ?, ?, ?)",
                (street, city, state, zipcode),
            )
            messagebox.showinfo("Success", "Address inserted successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_address(self):
        street = self.search_entry.get()
        try:
            result = self._connector.execute_fetch_query(
                "SELECT STREET, CITY, STATE, ZIP FROM address WHERE street like ?",
                ("%" + street + "%",),
            )

            if result:
                result = result[0]
                self.street_entry.delete(0, tk.END)
                self.street_entry.insert(tk.END, result[0])
                self.city_entry.delete(0, tk.END)
                self.city_entry.insert(tk.END, result[1])
                self.state_entry.delete(0, tk.END)
                self.state_entry.insert(tk.END, result[2])
                self.zipcode_entry.delete(0, tk.END)
                self.zipcode_entry.insert(tk.END, result[3])
            else:
                messagebox.showerror("Error", "No record found for street: " + street)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_address(self):
        street = self.street_entry.get()
        city = self.city_entry.get()
        state = self.state_entry.get()
        zipcode = self.zipcode_entry.get()

        try:
            self._connector.execute_insert_query(
                "UPDATE address SET STREET=?, CITY=?, STATE=?, ZIP=? WHERE street=?",
                (street, city, state, zipcode, street),
            )
            messagebox.showinfo("Success", "Address updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def fetch_and_display_address(self):
        street = self.street_entry.get()
        try:
            result = self._connector.execute_fetch_query(
                "SELECT STREET, CITY, STATE, ZIP FROM address WHERE street=?", (street,)
            )

            if result:
                result = result[0]
                display_window = tk.Toplevel(self.master)
                display_window.title("Updated Address")

                address_label = tk.Label(
                    display_window,
                    text=f"Address: {result[0]}, {result[1]}, {result[2]} {result[3]}",
                )
                address_label.pack()

                close_button = tk.Button(
                    display_window, text="Close", command=display_window.destroy
                )
                close_button.pack()
            else:
                messagebox.showerror("Error", "No record found for street: " + street)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def close_app(self):
        self.master.quit()


if __name__ == "__main__":
    register_root = tk.Tk()

    register_root.configure(background="#38726c")

    register_app = RegisterPage(
        register_root,
    )
    register_root.mainloop()
