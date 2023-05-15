# import MySQLdb
import time
import tkinter as tk
from tkinter import messagebox

from sql_connector import SQLiteConnector

# A global variable to store and retrieve logged in users.
USER_ID = None


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

        self.register_button = tk.Button(
            self.master,
            text="Register",
            command=self.register,
            highlightcolor="#38726c",
            highlightbackground="#38726c",
        )
        self.register_button.grid(row=3, column=1)

        self.login_page = tk.Button(
            self.master,
            text="Already have and account",
            command=self.get_login_page,
            highlightcolor="#38726c",
            highlightbackground="#38726c",
        )
        self.login_page.grid(row=4, column=1)

        # Instance of a database
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
        # Redirects to login page
        # self.master.destory
        # login_root = tk.Tk()     #new
        # login_root.configure(background="#38726c")
        for widgets in self.master.winfo_children():
            widgets.destroy()
        # nw = tk.Toplevel(self.master)
        # nw.configure(background="#38726c")
        LoginPage(
            self.master,
        )
        # self.master.mainloop()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        password_re_entry = self.password_re_entry.get()

        if password != password_re_entry:
            messagebox.showerror("Error", "Password doesn't match")
            return

        self._db_connector.execute_insert_query(
            "INSERT INTO USERS(username, password) VALUES(?, ?)", (username, password)  #into db
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
            CREATE TABLE IF NOT EXISTS "users" (
	            "id"	INTEGER UNIQUE,
	            "username"	VARCHAR(255) NOT NULL,
	            "password"	VARCHAR(255) NOT NULL,
	            PRIMARY KEY("id" AUTOINCREMENT)
            );
        """
        self._db_connector.execute_insert_query(create_table_query)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        result = self._db_connector.execute_fetch_query(
            "SELECT ID FROM users WHERE username=? AND password=?", (username, password)
        )

        if result:
            # Logged in user id is saved in global variable
            global USER_ID
            USER_ID = result[0][0]

            # nw = tk.Toplevel(self.master)
            # nw.configure(background="#38726c")
            for widgets in self.master.winfo_children():
                widgets.destroy()
            # self.master.withdraw()
            # root = tk.Tk()
            # root.configure(background="#38726c")
            YummyPizzaApp(
                self.master, database="database/shop.db"
            )  # Connecting to the next screen.
            # self.master.mainloop()
        else:
            messagebox.showerror("Error", "Invalid login credentials")


class YummyPizzaApp:
    def __init__(self, master, database):
        self.master = master
        self.master.title("Yammy Pizza Information")

        self._pizza_size = tk.Label(self.master, text="Pizza Size:", bg="#38726c")
        self._pizza_size.grid(row=1, column=0)
        self._size_selected = tk.StringVar()
        self._pizza_size_option_menu = tk.OptionMenu(
            master, self._size_selected, *[
                "Small (8 x 8)",
                "Medium (10 x 10)",
                "Large (12 x 12)"
            ]
        )
        self._pizza_size_option_menu.grid(row=1, column=1)

        self._drink_type = tk.Label(self.master, text="Drink Type:", bg="#38726c")
        self._drink_type.grid(row=3, column=0)
        self._drink_type_selected = tk.StringVar()
        self._drink_option_menu = tk.OptionMenu(
            master, self._drink_type_selected, *[
                "Water",
                "Soft Drink",
                "Juice"
            ]
        )
        self._drink_option_menu.grid(row=3, column=1)

        self.allergies = tk.Label(self.master, text="Allergies:", bg="#38726c")
        self.allergies.grid(row=4, column=0)
        self.allergies_entry = tk.Entry(self.master)
        self.allergies_entry.grid(row=4, column=1)

        self.topping_label = tk.Label(self.master, text="Toppings:", bg="#38726c")
        self.topping_label.grid(row=2, column=0)
        self.topping_entry = tk.Entry(self.master)
        self.topping_entry.grid(row=2, column=1)
        self.topping_search = tk.Button(
            self.master,
            text="Search",
            command=self.search_topping,
            highlightcolor="#38726c",
            highlightbackground="#38726c",
        )
        self.topping_search.grid(row=2, column=2)

        self.order_button = tk.Button(
            self.master,
            text="Insert",
            command=self.insert_order,
            highlightcolor="#38726c",
            highlightbackground="#38726c",
        )
        self.order_button.grid(row=6, column=0)
        self.fetch_button = tk.Button(
            self.master,
            text="Display Order",
            command=self.fetch_and_display_order,
            highlightcolor="#38726c",
            highlightbackground="#38726c",
        )
        self.fetch_button.grid(row=6, column=2)

        self.update_button = tk.Button(
            self.master,
            text="Update",
            command=self.update_address,
            highlightcolor="#38726c",
            highlightbackground="#38726c",
        )
        self.update_button.grid(row=6, column=1)

        self._connector = SQLiteConnector(database=database)
        self._current_order_id = None
        self.create_toppings_table()
        self.create_orders_table()

    def create_toppings_table(self):
        try:
            query = """
                DROP TABLE topping_types
            """
            self._connector.execute_insert_query(query)
        except:
            pass

        query = """
            CREATE TABLE IF NOT EXISTS "topping_types" (
                "topping_name" Text,
                "id" INTEGER NOT NULL UNIQUE,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """
        self._connector.execute_insert_query(query)
        insert_query = """
            INSERT INTO topping_types(topping_name)
            VALUES (?)
        """
        for v in [
                "fresh garlic",
                "sweet chilli flakes",
                "peri peri",
                "sweet peri peri",
                "Extra cheese",
                "black olives",
                "green peppers",
                "supreme pepperoni",
                "garlic butter"

            ]:
            self._connector.execute_insert_query(
                insert_query, (v,)
            )

    def create_orders_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS "orders" (
                "pizza_size"	TEXT,
                "topping"	TEXT,
                "drinks"	TEXT,
                "allergies"	TEXT,
                "id"	INTEGER NOT NULL UNIQUE,
                "ordered_by"	INTEGER,
                PRIMARY KEY("id" AUTOINCREMENT)
            );
        """
        self._connector.execute_insert_query(query)

    def insert_order(self):
        pizza_size = self._size_selected.get()
        topping = self.topping_entry.get()
        drinks = self._drink_type_selected.get()
        allergies = self.allergies_entry.get()

        try:
            # Get currently logged in user stored in the variable
            global USER_ID
            result = self._connector.execute_insert_query(
                "INSERT INTO orders (pizza_size, topping, drinks, allergies, ordered_by) VALUES (?, ?, ?, ?, ?) RETURNING id;",
                (pizza_size, topping, drinks, allergies, USER_ID),
            )
            self._current_order_id = result[0]
            messagebox.showinfo("Success", "Address inserted successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_topping(self):
        street = self.topping_entry.get()
        try:
            result = self._connector.execute_fetch_query(
                """
                    SELECT topping_name FROM topping_types
                    WHERE topping_name like ?
                """,
                ("%" + street + "%",),   # Pattern match
            )

            if result:
                result = result[0]  # to disable change the state
                self.topping_entry.delete(0, tk.END)
                self.topping_entry.insert(tk.END, result[0])
            else:
                messagebox.showerror("Error", "No record found for toppings: " + street)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_address(self):
        pizza_size = self._size_selected.get()
        topping = self.topping_entry.get()
        drinks = self._drink_type_selected.get()
        allergies = self.allergies_entry.get()

        try:
            global USER_ID
            self._connector.execute_insert_query(
                "UPDATE orders SET pizza_size=?, topping=?, drinks=?, allergies=? WHERE id=?",
                (pizza_size, topping, drinks, allergies, self._current_order_id),
            )
            messagebox.showinfo("Success", "Order updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def fetch_and_display_order(self):
        try:
            result = self._connector.execute_fetch_query(
                """
                    SELECT pizza_size, topping, drinks, allergies, u.USERNAME FROM orders
                    INNER JOIN users AS u
                    ON u.id == ordered_by
                    WHERE orders.id=?
                """,
                (self._current_order_id,),
            )

            if result:
                result = result[0]
                display_window = tk.Toplevel(self.master)
                display_window.title("Order Address")

                address_label = tk.Label(
                    display_window,
                    text=f"Pizza Size: {result[0]}, Topping:{result[1]}, Drinks: {result[2]}, Allergies: {result[3]}, Ordered By: {result[4]}",
                )
                address_label.pack()

                close_button = tk.Button(
                    display_window, text="Close", command=display_window.destroy
                )
                close_button.pack()
            else:
                messagebox.showerror("Error", "No record found for order_id: " + self._current_order_id)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def close_app(self):
        self.master.quit()


if __name__ == "__main__":
    # register_root = tk.Tk()
    #
    # register_root.configure(background="#38726c")
    #
    # register_app = YummyPizzaApp(
    #     register_root, database="database/shop.db"
    # )
    # register_root.mainloop()

    register_root = tk.Tk()
    register_root.update()

    register_root.configure(background="#38726c")

    register_app = RegisterPage(
        register_root,
    )
    register_root.mainloop()