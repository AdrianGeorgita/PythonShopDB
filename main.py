import tkinter as tk
from tkinter import messagebox, ttk
import cx_Oracle
from datetime import datetime

connection = cx_Oracle.connect("bd124", "bd124", "bd-dc.cs.tuiasi.ro:1539/orcl")

id_client = None

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")
        self.root.attributes('-fullscreen', True)  # Set the app to fullscreen

        # Set the background color of the frame to dark gray
        self.root.configure(bg="#333333")

        # Create the main menu frame
        self.main_menu_frame = tk.Frame(root, bg="#333333", padx=40, pady=40)
        self.main_menu_frame.pack(side="top", fill='both', anchor='n')  # Align to the top

        # Initialize the product list frame
        self.products_frame = None
        self.details_frame = None
        self.cart_frame = None
        self.wishlists_frame = None

        self.create_main_menu_frame()

    def create_main_menu_frame(self):
        # Create a frame for the panels at the top
        top_panels_frame = tk.Frame(self.main_menu_frame, bg="#333333")
        top_panels_frame.pack(side="top", fill='y', anchor='n')

        # Button for "Browse Products"
        browse_button = tk.Button(top_panels_frame, text="Browse Products", command=self.show_products_frame, bg="#555555", fg="white", font=('Helvetica', 14))
        browse_button.grid(row=1, column=0, padx=10)

        # Button for "Wishlists"
        wishlists_button = tk.Button(top_panels_frame, text="Wishlists", command=self.view_wishlists, bg="#555555", fg="white", font=('Helvetica', 14))
        wishlists_button.grid(row=1, column=1, padx=10)

        # Button for "Cart"
        cart_button = tk.Button(top_panels_frame, text="Cart", command=self.view_cart, bg="#555555", fg="white", font=('Helvetica', 14))
        cart_button.grid(row=1, column=2, padx=10)

        # Button for "Orders"
        orders_button = tk.Button(top_panels_frame, text="Orders", command=self.view_orders, bg="#555555", fg="white", font=('Helvetica', 14))
        orders_button.grid(row=1, column=3, padx=10)

        # Quit button in the top right
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.destroy, bg="#555555", fg="white", font=('Helvetica', 14))
        self.quit_button.place(relx=1.0, rely=0.0, anchor='ne')

        # Add padding between the buttons and the frame with text labels
        top_panels_frame.pack_configure(pady=20)

    def show_products_frame(self):
        # Destroy the existing products frame if it exists
        if self.products_frame:
            self.products_frame.destroy()

        if self.details_frame:
            self.details_frame.destroy()

        # Create a frame below the buttons for text labels
        labels_frame = tk.Frame(self.main_menu_frame, bg="#333333")
        labels_frame.pack(side="top", fill='both', anchor='n')
        self.products_frame = labels_frame

        cur = connection.cursor()
        cur.execute('SELECT p.ID_produs, p.Denumire, p.Producator, p.Pret * CASE WHEN procent_reducere > 0 THEN (1+prom.procent_reducere/100) ELSE 1 END FROM produse p, promotii prom WHERE p.id_promotie = prom.id_promotie')
        products = []
        for result in cur:
            products.append((result[0], result[1], result[2], result[3]))
        cur.close()

        labels_data = [
            ("ID", "Denumire", "Producator", "Pret"),
            *products  # Use the unpacking operator to include all product tuples
        ]

        for row_idx, row_data in enumerate(labels_data):
            # Choose background color based on whether it's an even or odd row
            if row_idx == 0:
                bg_color = "#222222"
                show_button = False
            elif row_idx % 2 == 0:
                bg_color = "#444444"
                show_button = True
            else:
                bg_color = "#555555"
                show_button = True

            for col_idx, value in enumerate(row_data):
                # Add a label for text data
                label = tk.Label(labels_frame, text=str(value), bg=bg_color, fg="white", font=('Helvetica', 12),
                                 padx=10, pady=5)
                label.grid(row=row_idx, column=col_idx, sticky="nsew")

            # Add a 'View' button in the last column for rows where it should be shown
            if show_button:
                view_button = tk.Button(labels_frame, text="View",
                                        command=lambda r=row_data: self.view_product(r, labels_frame), bg=bg_color,
                                        fg="white", font=('Helvetica', 12), padx=10, pady=5)
                view_button.grid(row=row_idx, column=len(row_data), sticky="nsew")

        # Configure row and column weights to make labels expand with resizing
        for i in range(len(labels_data)):
            labels_frame.grid_rowconfigure(i, weight=1)

        for i in range(len(labels_data[0]) + 1):  # Additional column for 'View' button
            labels_frame.grid_columnconfigure(i, weight=1)

    def view_wishlists(self):
        # View Wishlists
        global id_client
        # Destroy existing frames
        if self.products_frame:
            self.products_frame.destroy()

        if self.details_frame:
            self.details_frame.destroy()

        if self.cart_frame:
            self.cart_frame.destroy()

        if self.wishlists_frame:
            self.wishlists_frame.destroy()

        # Create a frame below the buttons for cart items
        wishlists_frame = tk.Frame(self.main_menu_frame, bg="#333333")
        wishlists_frame.pack(side="top", fill='both', anchor='n')
        self.wishlists_frame = wishlists_frame

        # Replace the query with your actual query to fetch cart items from the database
        cur = connection.cursor()
        cur.execute(
            'SELECT w.ID_wishlist, prod.Denumire, prod.Producator FROM wishlists w, produse prod \
             WHERE w.ID_client = :id_client AND w.ID_produs = prod.ID_produs',
            {'id_client': id_client})
        wishlists_items = []
        for result in cur:
            #cart_items.append((result[0], result[1], result[2], result[3], result[4]))
            pass
        cur.close()

    def view_cart(self):
        global id_client
        # Destroy existing frames
        if self.products_frame:
            self.products_frame.destroy()

        if self.details_frame:
            self.details_frame.destroy()

        if self.cart_frame:
            self.cart_frame.destroy()

        # Create a frame below the buttons for cart items
        cart_frame = tk.Frame(self.main_menu_frame, bg="#333333")
        cart_frame.pack(side="top", fill='both', anchor='n')
        self.products_frame = cart_frame

        # Replace the query with your actual query to fetch cart items from the database
        cur = connection.cursor()
        cur.execute(
            'SELECT c.ID_cos, prod.Denumire, prod.Producator, c.Cantitate, prod.Pret * CASE WHEN prom.procent_reducere > 0 THEN (1+prom.procent_reducere/100) ELSE 1 END FROM cosuri c, produse prod, promotii prom \
             WHERE c.ID_client = :id_client AND c.ID_produs = prod.ID_produs AND prod.Id_Promotie = prom.Id_Promotie', {'id_client': id_client})
        cart_items = []
        for result in cur:
                cart_items.append((result[0], result[1], result[2], result[3], result[4]))
        cur.close()

        filtered_cart_items = [item[1:] for item in cart_items]

        cart_data = [
            ("Denumire Produs", "Producator", "Cantitate", "Pret"),
            *filtered_cart_items
        ]

        for row_idx, row_data in enumerate(cart_data):

            if row_idx == 0:
                bg_color = "#222222"
                show_button = False
            elif row_idx % 2 == 0:
                bg_color = "#444444"
                show_button = True
            else:
                bg_color = "#555555"
                show_button = True

            for col_idx, value in enumerate(row_data):
                # Add a label or entry based on the column
                if col_idx == 2 and row_idx > 0:  # Column for "Cantitate"
                    entry = tk.Entry(cart_frame, bg=bg_color if row_idx % 2 == 0 else "#555555", fg="white",
                                     font=('Helvetica', 12), justify="center")
                    entry.insert(0, str(value))  # Insert the default quantity
                    entry.grid(row=row_idx, column=col_idx, sticky="nsew")

                    # Bind the function to update the database on focus out
                    entry.bind("<FocusOut>", lambda event, r=cart_items[row_idx-1], e=entry: self.update_quantity(event, r, e))
                else:
                    label = tk.Label(cart_frame, text=str(value), bg=bg_color if row_idx % 2 == 0 else "#555555",
                                     fg="white", font=('Helvetica', 12), padx=10, pady=5)
                    label.grid(row=row_idx, column=col_idx, sticky="nsew")

                # Add a 'Remove' button in the last column for rows
            if show_button:
                remove_button = tk.Button(cart_frame, text="Remove",
                                          command=lambda r=cart_items[row_idx-1]: self.remove_from_cart(r),
                                          bg=bg_color, fg="white", font=('Helvetica', 12), padx=10, pady=5)
                remove_button.grid(row=row_idx, column=len(row_data), sticky="nsew")

            # Configure row and column weights to make labels/entries expand with resizing
            for i in range(len(cart_data)):
                cart_frame.grid_rowconfigure(i, weight=1)

            for i in range(len(cart_data[1]) + 1):  # Additional column for 'Remove' button
                cart_frame.grid_columnconfigure(i, weight=1)

    def view_orders(self):
        # Placeholder for the "Orders" functionality
        print("View Orders")

    def view_product(self, product_data, labels_frame):
        # Destroy the existing labels frame
        labels_frame.destroy()

        # Create a new frame for detailed product information
        detail_frame = tk.Frame(self.main_menu_frame, bg="#333333")
        detail_frame.pack(side="top", fill='both', anchor='n')
        self.details_frame = detail_frame

        cur = connection.cursor()
        cur.execute('SELECT p.id_produs,p.denumire,p.pret * CASE WHEN prom.procent_reducere > 0 THEN (1+prom.procent_reducere/100) ELSE 1 END, p.producator, p.stoc, p.categorie, p.garantie, p.descriere, p.id_promotie FROM produse p, promotii prom WHERE p.Id_Produs = :product_id AND prom.id_promotie = p.id_promotie', {'product_id': product_data[0]})
        product = cur.fetchone()
        cur.close()

        cur = connection.cursor()
        cur.execute('SELECT * FROM promotii prom WHERE prom.id_promotie = :prom_id', {'prom_id': product[8]})
        promo = cur.fetchone()
        cur.close()

        if not product:
            print("No product found.")
        else:
            # Detailed information about the selected product

            pret_value = f"{str(product[2])} RON"
            stoc_value = f"{str(product[4])} buc"
            if product[6] > 1:
                garantie_value = f"{str(product[6])} luni"
            else:
                garantie_value = f"{str(product[6])} luna"

            detail_labels_data = [
                ("ID", product[0]),
                ("Denumire", product[1]),
                ("Pret", pret_value),
                ("Producator", product[3]),
                ("Stoc", stoc_value),
                ("Categorie", product[5]),
                ("Garantie", garantie_value),
                ("Descriere", product[7])
            ]

        for row_idx, (label, value) in enumerate(detail_labels_data):
            # Choose background color based on whether it's an even or odd row
            if row_idx % 2 == 0:
                bg_color = "#444444"
            else:
                bg_color = "#555555"

            # Add a label for detailed information
            label = tk.Label(detail_frame, text=f"{label}: {value}", bg=bg_color, fg="white", font=('Helvetica', 12), padx=10, pady=5)
            label.grid(row=row_idx, column=0, sticky="nsew")

        if promo and promo[1] > 0:
            bg_color = "#444444" if bg_color == "#555555" else "#444444"
            label = tk.Label(detail_frame, text=f"[{promo[0]}] {promo[4]} incepand cu data de {promo[2]} pana la data de {promo[3]}", bg=bg_color, fg="white", font=('Helvetica', 12), padx=10, pady=5)
            label.grid(row=row_idx+1, column=0, sticky="nsew")

        # Create a new frame for buttons below the product description
        buttons_frame = tk.Frame(detail_frame, bg="#333333")
        buttons_frame.grid(row=len(detail_labels_data)+1, column=0, sticky="n", pady=10)

        # Add buttons for actions
        add_to_wishlist_button = tk.Button(buttons_frame, text="Add to Wishlist",
                                           command=lambda: self.add_to_wishlist(product), bg="#333333",
                                           fg="white", font=('Helvetica', 12), padx=10, pady=5)
        add_to_wishlist_button.grid(row=0, column=0, padx=10)

        add_to_cart_button = tk.Button(buttons_frame, text="Add to Cart",
                                       command=lambda: self.add_to_cart(product), bg="#5A5A5A", fg="white",
                                       font=('Helvetica', 12), padx=10, pady=5)
        add_to_cart_button.grid(row=0, column=1, padx=10)

        back_button = tk.Button(buttons_frame, text="Back to Products", command=lambda: self.show_products_frame(),
                                bg="#333333", fg="white", font=('Helvetica', 12), padx=10, pady=5)
        back_button.grid(row=0, column=2, padx=10)

        # Configure row and column weights to make detailed information and buttons expand with resizing
        for i in range(len(detail_labels_data) + 1):
            detail_frame.grid_rowconfigure(i, weight=1)

        detail_frame.grid_columnconfigure(0, weight=1)

    def add_to_wishlist(self, product):
        # Placeholder for adding to wishlist functionality
        print(f"Added {product[1]} to Wishlist")

    def add_to_cart(self, product):
        # Add a Product to the Shopping Cart
        global id_client

        #https://docs.oracle.com/cd/B13789_01/appdev.101/b10795/adfns_tr.htm
        #Check this for a trigger that either updates or inserts a new row

        try:
            cur = connection.cursor()
            query = 'INSERT INTO cosuri(id_cos, cantitate, id_client, id_produs) ' \
                    'VALUES (NULL,1,:id_client,:id_produs)'
            cur.execute(query, {
                'id_client': id_client,
                'id_produs': product[0]
            })
            cur.execute('commit')
            cur.close()
            #print(f"Added {product[0]} to Cart")
        except cx_Oracle.DatabaseError as e:
            print("Database error:", str(e))
            messagebox.showerror("Database Error",
                                 "An error occurred while interacting with the database. Please try again. [Error Code: " + str(e) + "]")

    def remove_from_cart(self, cart_item_data):
        # Remove the item from the cart

        try:
            cur = connection.cursor()
            query = 'DELETE FROM cosuri WHERE id_cos = :deletedItemId'
            cur.execute(query, {
                'deletedItemId': cart_item_data[0]
            })
            cur.execute('commit')
            cur.close()
        except cx_Oracle.DatabaseError as e:
            print("Database error:", str(e))
            messagebox.showerror("Database Error",
                 "An error occurred while interacting with the database. Please try again. [Error Code: "+str(e)+"]")

        # Refresh the cart view after removing the item
        self.view_cart()

    def update_quantity(self, event, row_data, entry):
        # Extract the updated quantity from the entry
        updated_quantity = entry.get()

        # Update the database with the new quantity
        try:
            cur = connection.cursor()
            query = 'UPDATE cosuri SET cantitate = :quantity WHERE id_cos = :modifiedCartId'
            cur.execute(query, {
                'quantity': updated_quantity,
                'modifiedCartId':row_data[0]
            })
            cur.execute('commit')
            cur.close()
            #print(f"Updated quantity for {row_data[0]} to {updated_quantity}")
        except cx_Oracle.DatabaseError as e:
            print("Database error:", str(e))
            messagebox.showerror("Database Error",
                 "An error occurred while interacting with the database. Please try again. [Error Code: "+str(e)+"]")


class LoginMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Menu")
        self.root.attributes('-fullscreen', True)  # Set the app to fullscreen

        # Set the background color of the frame to dark gray
        self.root.configure(bg="#333333")

        self.create_account_frame = None
        self.login_frame = None

        # Create the login frame
        self.login_frame = tk.Frame(root, bg="#333333", padx=40, pady=40)
        self.login_frame.pack(expand=True)
        self.create_login_frame()

    def create_login_frame(self):
        # Title above the fields
        self.title_label = tk.Label(self.login_frame, text="Log into your account", font=('Helvetica', 16), bg="#333333", fg="white")
        self.title_label.pack()

        self.username_label = tk.Label(self.login_frame, text="Username:", font=('Helvetica', 14), bg="#333333", fg="white")
        self.username_label.pack()

        self.username_entry = tk.Entry(self.login_frame, bg="#333333", fg="white", font=('Helvetica', 14))
        self.username_entry.pack(pady=10)  # Add padding between the fields

        self.password_label = tk.Label(self.login_frame, text="Password:", font=('Helvetica', 14), bg="#333333", fg="white")
        self.password_label.pack()

        self.password_entry = tk.Entry(self.login_frame, show="*", bg="#333333", fg="white", font=('Helvetica', 14))
        self.password_entry.pack(pady=10)  # Add padding between the fields

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login, bg="#555555", fg="white", font=('Helvetica', 14))
        self.login_button.pack(pady=10)  # Add padding between the button and the fields

        # Note between Login button and Create Account button
        self.note_label = tk.Label(self.login_frame, text="Don't have an account?", font=('Helvetica', 12), bg="#333333", fg="white")
        self.note_label.pack(pady=5)

        self.create_account_button = tk.Button(self.login_frame, text="Create Account", command=self.switch_to_create_account, bg="#555555", fg="white", font=('Helvetica', 14))
        self.create_account_button.pack()

        # Quit button in the top right
        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.destroy, bg="#555555", fg="white", font=('Helvetica', 14))
        self.quit_button.place(relx=1.0, rely=0.0, anchor='ne')

    def switch_to_create_account(self):
        print("Function: switch_to_create_account")
        # Destroy the login frame and create the create account frame
        self.login_frame.destroy()
        self.create_account_frame = tk.Frame(self.root, bg="#333333", padx=40, pady=40)
        self.create_account_frame.pack(expand=True)

        # Create the create account frame
        self.create_account()

    def create_account(self):
        # Title above the fields
        title_label = tk.Label(self.create_account_frame, text="Create Account", font=('Helvetica', 16), bg="#333333",
                               fg="white")
        title_label.pack()

        # Username field
        username_label = tk.Label(self.create_account_frame, text="Username:", font=('Helvetica', 14), bg="#333333",
                                  fg="white")
        username_label.pack()

        self.new_username_entry = tk.Entry(self.create_account_frame, bg="#333333", fg="white", font=('Helvetica', 14), width=30)
        self.new_username_entry.pack(pady=10)  # Add padding between the fields

        # Password field
        password_label = tk.Label(self.create_account_frame, text="Password:", font=('Helvetica', 14), bg="#333333",
                                  fg="white")
        password_label.pack()

        self.new_password_entry = tk.Entry(self.create_account_frame, show="*", bg="#333333", fg="white",
                                           font=('Helvetica', 14), width=30)
        self.new_password_entry.pack(pady=10)  # Add padding between the fields

        # Confirm Password field
        confirm_password_label = tk.Label(self.create_account_frame, text="Confirm Password:", font=('Helvetica', 14),
                                          bg="#333333", fg="white")
        confirm_password_label.pack()

        self.confirm_password_entry = tk.Entry(self.create_account_frame, show="*", bg="#333333", fg="white",
                                               font=('Helvetica', 14), width=30)
        self.confirm_password_entry.pack(pady=10)  # Add padding between the fields

        # Billing Address field
        billing_address_label = tk.Label(self.create_account_frame, text="Billing Address:", font=('Helvetica', 14),
                                         bg="#333333", fg="white")
        billing_address_label.pack()

        self.billing_address_entry = tk.Entry(self.create_account_frame, bg="#333333", fg="white",
                                              font=('Helvetica', 14), width=30)
        self.billing_address_entry.pack(pady=10)  # Add padding between the fields

        # Phone Number field (Optional)
        phone_number_label = tk.Label(self.create_account_frame, text="Phone Number:",
                                      font=('Helvetica', 14), bg="#333333", fg="white")
        phone_number_label.pack()

        self.phone_number_entry = tk.Entry(self.create_account_frame, bg="#333333", fg="white", font=('Helvetica', 14), width=30)
        self.phone_number_entry.pack(pady=10)  # Add padding between the fields

        # Email field
        email_label = tk.Label(self.create_account_frame, text="Email (Optional):", font=('Helvetica', 14), bg="#333333",
                               fg="white")
        email_label.pack()

        self.email_entry = tk.Entry(self.create_account_frame, bg="#333333", fg="white", font=('Helvetica', 14), width=30)
        self.email_entry.pack(pady=10)  # Add padding between the fields

        # Delivery Address field (Optional)
        delivery_address_label = tk.Label(self.create_account_frame, text="Delivery Address (Optional):",
                                          font=('Helvetica', 14), bg="#333333", fg="white")
        delivery_address_label.pack()

        self.delivery_address_entry = tk.Entry(self.create_account_frame, bg="#333333", fg="white",
                                               font=('Helvetica', 14), width=30)
        self.delivery_address_entry.pack(pady=10)  # Add padding between the fields

        # Create Account button
        create_account_button = tk.Button(self.create_account_frame, text="Create Account",
                                          command=self.perform_account_creation, bg="#555555", fg="white",
                                          font=('Helvetica', 14))
        create_account_button.pack(pady=10)  # Add padding between the button and the fields

        # Back to Login button
        back_to_login_button = tk.Button(self.create_account_frame, text="Back to Login", command=self.switch_to_login,
                                         bg="#555555", fg="white", font=('Helvetica', 14))
        back_to_login_button.pack(pady=10)  # Add padding between the button and the fields

        # Quit button in the top right
        quit_button = tk.Button(self.root, text="Quit", command=self.root.destroy, bg="#555555", fg="white",
                                font=('Helvetica', 14))
        quit_button.place(relx=1.0, rely=0.0, anchor='ne')

    def perform_account_creation(self):
        print("Function: perform_account_creation")
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        billing_address = self.billing_address_entry.get()
        email = self.email_entry.get()
        phone_number = self.phone_number_entry.get()
        delivery_address = self.delivery_address_entry.get()

        try:

            if not all([new_username, new_password, confirm_password, billing_address, phone_number]):
                messagebox.showerror("Error", "Please fill in all fields.")
            elif len(new_password) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters long.")
            elif new_password == confirm_password:

                cur = connection.cursor()
                query = 'INSERT INTO clienti (id_client,adresa_facturare,numar_telefon,email)' \
                        'VALUES (NULL, :billing_address, :phone_number, :email)'

                cur.execute(query, {
                    'billing_address': billing_address,
                    'phone_number': phone_number,
                    'email': email
                })

                query = 'INSERT INTO conturi (username, parola, data_creare, status_cont, adresa_livrare, id_client)' \
                        'VALUES (:username, :password, SYSDATE, DEFAULT, :delivery_address, clienti_id_client_seq.CURRVAL)'

                cur.execute(query, {
                    'username': new_username,
                    'password': new_password,
                    'delivery_address': delivery_address,
                })

                cur.execute('commit')
                cur.close()

                self.switch_to_main_menu()  # Switch to the main menu after successful account creation
            else:
                messagebox.showerror("Error", "Password and Confirm Password do not match.")

        except cx_Oracle.DatabaseError as e:
            # Handle the database error, you can log it or show an error message
            print("Database error:", str(e))
            messagebox.showerror("Database Error",
                                 "An error occurred while interacting with the database. Please try again. [Error Code: "+str(e)+"]")

    def switch_to_main_menu(self):
        print("Function: switch_to_main_menu")
        # Destroy the create account frame and create the main menu frame
        if self.create_account_frame:
            self.create_account_frame.destroy()
        if self.login_frame:
            self.login_frame.destroy()
        MainMenu(self.root)  # Create the main menu frame

    def switch_to_login(self):
        print("Function: switch_to_login")
        # Destroy the create account frame and recreate the login frame
        self.create_account_frame.destroy()
        self.login_frame = tk.Frame(self.root, bg="#333333", padx=40, pady=40)
        self.login_frame.pack(expand=True)
        self.create_login_frame()

    def login(self):
        print("Function: login")
        global id_client
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:

            if not all([username, password]):
                messagebox.showerror("Error", "Please fill in both fields.")
            else:

                cur = connection.cursor()
                query = 'SELECT id_client FROM conturi WHERE username = :username AND parola = :password'

                cur.execute(query, {
                    'username': username,
                    'password': password
                })
                id_client = cur.fetchone()
                cur.close()

                if id_client:
                    id_client = id_client[0]

                # Successfully logged in
                if id_client is not None:
                    self.switch_to_main_menu()  # Switch to the main menu after successful account creation
                else:
                    messagebox.showerror("Error", "The username or the password is wrong!")

        except cx_Oracle.DatabaseError as e:
            # Handle the database error, you can log it or show an error message
            print("Database error:", str(e))
            messagebox.showerror("Database Error",
                                 "An error occurred while interacting with the database. Please try again. [Error Code: "+str(e)+"]")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginMenu(root)
    root.mainloop()