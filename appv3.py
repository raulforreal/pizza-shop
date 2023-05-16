import tkinter as tk
from tkinter import messagebox

from sql_connector import SQLiteConnector

# A global variable to store and retrieve logged-in users.
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
        for widgets in self.master.winfo_children():
            widgets.destroy()  # Deletes existing components i.e. labels, text box, buttons etc. on current page

        LoginPage(
            self.master,
        )

    def register(self):
        # Code executes when register button is clicked
        username = self.username_entry.get()
        password = self.password_entry.get()
        password_re_entry = self.password_re_entry.get()

        if password != password_re_entry:
            messagebox.showerror("Error", "Password doesn't match")
            return

        self._db_connector.execute_insert_query(
            "INSERT INTO USERS(username, password) VALUES(?, ?)",
            (username, password),  # into db
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
        # This code is executed when login button is clicked
        username = self.username_entry.get()
        password = self.password_entry.get()

        result = self._db_connector.execute_fetch_query(
            "SELECT ID FROM users WHERE username=? AND password=?", (username, password)
        )

        if result:
            # Logged in user id is saved in global variable
            global USER_ID
            USER_ID = result[0][0]

            for widgets in self.master.winfo_children():
                widgets.destroy()  # Destroys components on current page i.e. text box, labels, buttons etc.

            ViewHomePage(
                self.master, database="database/shop.db"
            )  # Connecting to the next screen.
        else:
            messagebox.showerror("Error", "Invalid login credentials")


class ViewHomePage:
    def __init__(self, master, database):
        self._master = master
        self._master.title("Yammy Pizza Home")
        self._connector = SQLiteConnector(database=database)
        self.retrieve_order()

    def retrieve_order(self):
        for widgets in self._master.winfo_children():
            widgets.destroy()
        query = """
            SELECT id, pizza_size, topping, drinks, allergies
            FROM orders
            where ordered_by = ?
        """
        results = self._connector.execute_fetch_query(query, (USER_ID,))

        i = 0

        if not results:
            label = tk.Label(
                self._master,
                text="No orders have been placed",
                bg="#38726c",
                font="Arial 13 bold",
            )
            label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        else:
            for i, result in enumerate(results):
                label = tk.Label(
                    self._master,
                    text=f"Pizza Size: {result[1]}, Topping:{result[2]}, Drinks: {result[3]}, Allergies: {result[4]}",
                    bg="#38726c",
                )
                label.grid(row=i + 1, column=1)
                delete_button = tk.Button(
                    self._master,
                    text="Delete Order",
                    command=lambda: self.delete_entry(result[0]),
                    highlightcolor="#38726c",
                    highlightbackground="#38726c",
                )
                delete_button.grid(row=i + 1, column=2)

        new_order_button = tk.Button(
            self._master,
            text="Create new order",
            command=self._new_order,
            highlightcolor="#38726c",
            highlightbackground="#38726c",
        )
        new_order_button.grid(row=i + 2, column=1)

    def _new_order(self):
        for widgets in self._master.winfo_children():
            widgets.destroy()
        YummyPizzaApp(self._master, database="database/shop.db")

    def delete_entry(self, id):
        query = """
            delete from orders
            where id = ?
        """
        self._connector.execute_insert_query(query, (id,))
        messagebox.showinfo(message=f"Order with ID: {id} deleted")
        self.retrieve_order()


class YummyPizzaApp:
    def __init__(self, master, database):
        self.master = master
        self.master.title("Yammy Pizza Information")

        self._pizza_size = tk.Label(self.master, text="Pizza Size:", bg="#38726c")
        self._pizza_size.grid(row=1, column=0)
        self._size_selected = tk.StringVar()
        self._pizza_size_option_menu = tk.OptionMenu(
            master,
            self._size_selected,
            *["Small (8 x 8)", "Medium (10 x 10)", "Large (12 x 12)"],
        )
        self._pizza_size_option_menu.grid(row=1, column=1)

        self._drink_type = tk.Label(self.master, text="Drink Type:", bg="#38726c")
        self._drink_type.grid(row=3, column=0)
        self._drink_type_selected = tk.StringVar()
        self._drink_option_menu = tk.OptionMenu(
            master, self._drink_type_selected, *["Water", "Soft Drink", "Juice"]
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
            command=self.update_order,
            highlightcolor="#38726c",
            highlightbackground="#38726c",
        )
        self.update_button.grid(row=6, column=1)

        self.home_button = tk.Button(
            self.master,
            text="Orders page",
            command=self.return_home_page,
            highlightcolor="#38726c",
            highlightbackground="#38726c",
        )
        self.home_button.grid(row=6, column=3)

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
            "garlic butter",
        ]:
            self._connector.execute_insert_query(insert_query, (v,))

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
            # Get currently logged-in user stored in the variable
            global USER_ID
            result = self._connector.execute_insert_query(
                """INSERT INTO 
                    orders (pizza_size, topping, drinks, allergies, ordered_by)
                    VALUES (?, ?, ?, ?, ?) RETURNING id;
                """,
                (pizza_size, topping, drinks, allergies, USER_ID),
            )
            self._current_order_id = result[0]
            messagebox.showinfo("Success", "Address inserted successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def search_topping(self):
        topping = self.topping_entry.get()
        try:
            result = self._connector.execute_fetch_query(
                """
                    SELECT topping_name FROM topping_types
                    WHERE topping_name like ?
                """,
                ("%" + topping + "%",),  # Pattern match
            )

            if result:
                result = result[0]  # to disable change the state
                self.topping_entry.delete(0, tk.END)
                self.topping_entry.insert(tk.END, result[0])
            else:
                messagebox.showerror("Error", "No record found for toppings: " + topping)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_order(self):
        pizza_size = self._size_selected.get()
        topping = self.topping_entry.get()
        drinks = self._drink_type_selected.get()
        allergies = self.allergies_entry.get()

        try:
            global USER_ID
            self._connector.execute_insert_query(
                "UPDATE orders SET pizza_size=?, topping=?, drinks=?, allergies=? WHERE id=?",
                (pizza_size, topping, drinks, allergies, self._current_order_id),
                # Order id for previously inserted order is used to update that order
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
                messagebox.showerror(
                    "Error", "No record found for order_id: " + self._current_order_id
                )
        except Exception:
            messagebox.showerror("Error", "No order has been created")

    def return_home_page(self):
        for widgets in self.master.winfo_children():
            widgets.destroy()

        ViewHomePage(
            self.master, database="database/shop.db"
        )  # Connecting to the next screen.

    def close_app(self):
        self.master.quit()


if __name__ == "__main__":

    register_root = tk.Tk()
    register_root.update()

    register_root.configure(background="#38726c")

    register_app = RegisterPage(
        register_root,
    )
    register_root.mainloop()
