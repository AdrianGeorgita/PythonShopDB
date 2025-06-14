import tkinter as tk
from tkinter import messagebox, ttk
import oracledb
import random
from datetime import datetime
import os
from dotenv import load_dotenv
import hashlib

load_dotenv()

DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_SERVICE = os.getenv('DB_SERVICE')

connection_string = f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}"

try:
    connection = oracledb.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        dsn=connection_string
    )
except oracledb.Error as e:
    print(f"Database connection error: {e}")
    raise

id_client = None
is_admin = False

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")
        self.root.attributes('-fullscreen', True)

        self.root.configure(bg="#333333")

        self.main_menu_frame = tk.Frame(root, bg="#333333", padx=40, pady=40)
        self.main_menu_frame.pack(side="top", fill='both', anchor='n')  # Align to the top

        # Initialize the frames
        self.products_frame = None
        self.details_frame = None
        self.cart_frame = None
        self.wishlists_frame = None
        self.wishlists_list_frame = None
        self.wishlists_products_frame = None
        self.add_to_wishlist_frame = None
        self.orders_frame = None
        self.cart_total_frame = None
        self.order_items_frame = None
        self.edit_products_frame = None

        self.create_main_menu_frame()

    def create_main_menu_frame(self):
        top_panels_frame = tk.Frame(self.main_menu_frame, bg="#333333")
        top_panels_frame.pack(side="top", fill='y', anchor='n')

        browse_button = tk.Button(top_panels_frame, text="Browse Products", command=self.show_products_frame, bg="#555555", fg="white", font=('Helvetica', 14))
        browse_button.grid(row=1, column=0, padx=10)

        wishlists_button = tk.Button(top_panels_frame, text="Wishlists", command=self.view_wishlists, bg="#555555", fg="white", font=('Helvetica', 14))
        wishlists_button.grid(row=1, column=1, padx=10)

        cart_button = tk.Button(top_panels_frame, text="Cart", command=self.view_cart, bg="#555555", fg="white", font=('Helvetica', 14))
        cart_button.grid(row=1, column=2, padx=10)

        orders_button = tk.Button(top_panels_frame, text="Orders", command=self.view_orders, bg="#555555", fg="white", font=('Helvetica', 14))
        orders_button.grid(row=1, column=3, padx=10)

        if is_admin:
            change_products_button = tk.Button(top_panels_frame, text="Edit Products", command=self.view_change_products, bg="#555555",
                                      fg="white", font=('Helvetica', 14))
            change_products_button.grid(row=1, column=4, padx=10)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.destroy, bg="#555555", fg="white", font=('Helvetica', 14))
        self.quit_button.place(relx=1.0, rely=0.0, anchor='ne')

        top_panels_frame.pack_configure(pady=20)

    def destroyAllFrames(self):
        if self.products_frame:
            self.products_frame.destroy()

        if self.details_frame:
            self.details_frame.destroy()

        if self.cart_frame:
            self.cart_frame.destroy()

        if self.wishlists_frame:
            self.wishlists_frame.destroy()

        if self.add_to_wishlist_frame:
            self.add_to_wishlist_frame.destroy()

        if self.wishlists_list_frame:
            self.wishlists_list_frame.destroy()

        if self.wishlists_products_frame:
            self.wishlists_products_frame.destroy()

        if self.orders_frame:
            self.orders_frame.destroy()

        if self.cart_total_frame:
            self.cart_total_frame.destroy()

        if self.order_items_frame:
            self.order_items_frame.destroy()

        if self.edit_products_frame:
            self.edit_products_frame.destroy()

    def view_change_products(self):
        # View Wishlists
        global id_client
        # Destroy existing frames
        self.destroyAllFrames()

        self.id_promotie_combobox = None
        self.categorie_combobox = None
        self.descriere_entry = None
        self.garantie_entry = None
        self.stoc_entry = None
        self.producator_entry = None
        self.denumire_entry = None
        self.pret_entry = None

        def confirmChanges(productId):
            results = []
            results.append(self.denumire_entry.get())
            results.append(self.pret_entry.get())
            results.append(self.producator_entry.get())
            results.append(self.stoc_entry.get())
            results.append(self.garantie_entry.get())
            results.append(self.descriere_entry.get())
            results.append(self.categorie_combobox.get())
            results.append(self.id_promotie_combobox.get())
            if results[0] and results[1] and results[2] and results[3] and results[6] and results[7]:
                if not results[4]:
                    results[4] = 1
                results[7] = results[7][0]
                cur = connection.cursor()
                if productId:
                    try:
                        query = 'UPDATE produse SET denumire = :denumire, pret = :pret, producator = :producator, stoc = :stoc, categorie = :categorie, garantie = :garantie, descriere = :descriere, id_promotie = :id_promotie WHERE id_produs = :product_id'
                        cur.execute(query, {
                            'denumire': results[0],
                            'pret': int(results[1]),
                            'producator': results[2],
                            'stoc': int(results[3]),
                            'garantie': int(results[4]),
                            'descriere': results[5],
                            'categorie': results[6],
                            'id_promotie': int(results[7]),
                            'product_id': int(productId)
                        })

                        cur.execute('commit')
                        self.view_change_products()
                    except oracledb.DatabaseError as e:
                        print("Database error:", str(e))
                        messagebox.showerror("Database Error",
                                             "An error occurred while interacting with the database. Please try again. [Error Code: " + str(e) + "]")
                        cur.execute('rollback')
                    finally:
                        cur.close()
                else:
                    try:
                        query = 'INSERT INTO produse VALUES (NULL, :denumire, :pret, :producator, :stoc, :categorie, :garantie, :descriere, :id_promotie)'
                        cur.execute(query, {
                            'denumire': results[0],
                            'pret': int(results[1]),
                            'producator': results[2],
                            'stoc': int(results[3]),
                            'garantie': int(results[4]),
                            'descriere': results[5],
                            'categorie': results[6],
                            'id_promotie': int(results[7]),
                        })

                        cur.execute('commit')
                        self.view_change_products()
                    except oracledb.DatabaseError as e:
                        print("Database error:", str(e))
                        messagebox.showerror("Database Error",
                                             "An error occurred while interacting with the database. Please try again. [Error Code: " + str(
                                                 e) + "]")
                        cur.execute('rollback')
                    finally:
                        cur.close()
            else:
                messagebox.showerror("Error", "You must fill in all fields!")

        def addProducts():
            self.destroyAllFrames()

            edit_products_frame = tk.Frame(self.main_menu_frame, bg="#333333")
            edit_products_frame.pack(side="top", fill='y', anchor='n')
            self.edit_products_frame = edit_products_frame

            promotions = []
            cur = connection.cursor()
            cur.execute('SELECT id_promotie, procent_reducere, data_inceput FROM promotii')
            for result in cur:
                promotions.append((result[0], result[1], result[2]))

            possible_promotion_values = []
            for promo in promotions:
                possible_promotion_values.append(str(promo[0]) + " Reducere: " + str(promo[1]) + "% - " + str(promo[2]))

            # Denumire
            denumire_label = tk.Label(edit_products_frame, text="Denumire", bg="#333333", fg="white")
            denumire_label.grid(row=1, column=0, padx=10, pady=10)
            self.denumire_entry = tk.Entry(edit_products_frame, bg="#333333", fg="white")
            self.denumire_entry.grid(row=1, column=1, padx=10, pady=10)

            # Pret
            pret_label = tk.Label(edit_products_frame, text="Pret", bg="#333333", fg="white")
            pret_label.grid(row=2, column=0, padx=10, pady=10)
            self.pret_entry = tk.Entry(edit_products_frame, bg="#333333", fg="white")
            self.pret_entry.grid(row=2, column=1, padx=10, pady=10)

            # Producator
            producator_label = tk.Label(edit_products_frame, text="Producator", bg="#333333", fg="white")
            producator_label.grid(row=3, column=0, padx=10, pady=10)
            self.producator_entry = tk.Entry(edit_products_frame, bg="#333333", fg="white")
            self.producator_entry.grid(row=3, column=1, padx=10, pady=10)

            # Stoc
            stoc_label = tk.Label(edit_products_frame, text="Stoc", bg="#333333", fg="white")
            stoc_label.grid(row=4, column=0, padx=10, pady=10)
            self.stoc_entry = tk.Entry(edit_products_frame, bg="#333333", fg="white")
            self.stoc_entry.grid(row=4, column=1, padx=10, pady=10)

            # Garantie
            garantie_label = tk.Label(edit_products_frame, text="Garantie", bg="#333333", fg="white")
            garantie_label.grid(row=5, column=0, padx=10, pady=10)
            self.garantie_entry = tk.Entry(edit_products_frame, bg="#333333", fg="white")
            self.garantie_entry.grid(row=5, column=1, padx=10, pady=10)

            # Descriere
            descriere_label = tk.Label(edit_products_frame, text="Descriere", bg="#333333", fg="white")
            descriere_label.grid(row=6, column=0, padx=10, pady=10)
            self.descriere_entry = tk.Entry(edit_products_frame, bg="#333333", fg="white")
            self.descriere_entry.grid(row=6, column=1, padx=10, pady=10)

            # Categorie
            categorie_label = tk.Label(edit_products_frame, text="Categorie", bg="#333333", fg="white")
            categorie_label.grid(row=7, column=0, padx=10, pady=10)
            self.categorie_combobox = ttk.Combobox(edit_products_frame,
                                                   values=["Audio-Video", "Auto", "Bacanie", "Birotica", "Bricolaj",
                                                           "Carti", "Casa", "Diverse", "Electrocasnice", "Fashion",
                                                           "Foto", "Gaming", "Gradina", "Laptop", "Moto", "PC",
                                                           "Periferice", "Software", "TV", "Tablete", "Telefoane"])
            self.categorie_combobox.grid(row=7, column=1, padx=10, pady=10)

            # ID_Promotie
            id_promotie_label = tk.Label(edit_products_frame, text="ID_Promotie", bg="#333333", fg="white")
            id_promotie_label.grid(row=8, column=0, padx=10, pady=10)
            self.id_promotie_combobox = ttk.Combobox(edit_products_frame, values=possible_promotion_values)
            self.id_promotie_combobox.grid(row=8, column=1, padx=10, pady=10)

            confirm_edit_button = tk.Button(edit_products_frame, text="Confirm Changes",
                                            command=lambda: confirmChanges(None),
                                            bg="#555555", fg="white", font=('Helvetica', 14))
            confirm_edit_button.grid(row=9, column=0, padx=10)

        def editProducts(product_data):
            self.destroyAllFrames()

            edit_products_frame = tk.Frame(self.main_menu_frame, bg="#333333")
            edit_products_frame.pack(side="top", fill='y', anchor='n')
            self.edit_products_frame = edit_products_frame

            promotions = []
            cur = connection.cursor()
            cur.execute('SELECT id_promotie, procent_reducere, data_inceput FROM promotii')
            for result in cur:
                promotions.append((result[0], result[1], result[2]))

            possible_promotion_values = []
            for promo in promotions:
                possible_promotion_values.append(str(promo[0])+" Reducere: "+str(promo[1])+"% - "+str(promo[2]))

            # Denumire
            denumire_label = tk.Label(edit_products_frame, text="Denumire", bg="#333333", fg="white")
            denumire_label.grid(row=1, column=0, padx=10, pady=10)
            self.denumire_entry = tk.Entry(edit_products_frame, bg="#333333", fg="white")
            self.denumire_entry.grid(row=1, column=1, padx=10, pady=10)

            # Pret
            pret_label = tk.Label(edit_products_frame, text="Pret", bg="#333333", fg="white")
            pret_label.grid(row=2, column=0, padx=10, pady=10)
            self.pret_entry = tk.Entry(edit_products_frame, bg="#333333", fg="white")
            self.pret_entry.grid(row=2, column=1, padx=10, pady=10)

            # Producator
            producator_label = tk.Label(edit_products_frame, text="Producator", bg="#333333", fg="white")
            producator_label.grid(row=3, column=0, padx=10, pady=10)
            self.producator_entry = tk.Entry(edit_products_frame, bg="#333333", fg="white")
            self.producator_entry.grid(row=3, column=1, padx=10, pady=10)

            # Stoc
            stoc_label = tk.Label(edit_products_frame, text="Stoc", bg="#333333", fg="white")
            stoc_label.grid(row=4, column=0, padx=10, pady=10)
            self.stoc_entry = tk.Entry(edit_products_frame, bg="#333333", fg="white")
            self.stoc_entry.grid(row=4, column=1, padx=10, pady=10)

            # Garantie
            garantie_label = tk.Label(edit_products_frame, text="Garantie", bg="#333333", fg="white")
            garantie_label.grid(row=5, column=0, padx=10, pady=10)
            self.garantie_entry = tk.Entry(edit_products_frame, bg="#333333", fg="white")
            self.garantie_entry.grid(row=5, column=1, padx=10, pady=10)

            # Descriere
            descriere_label = tk.Label(edit_products_frame, text="Descriere", bg="#333333", fg="white")
            descriere_label.grid(row=6, column=0, padx=10, pady=10)
            self.descriere_entry = tk.Entry(edit_products_frame, bg="#333333", fg="white")
            self.descriere_entry.grid(row=6, column=1, padx=10, pady=10)

            # Categorie
            categorie_label = tk.Label(edit_products_frame, text="Categorie", bg="#333333", fg="white")
            categorie_label.grid(row=7, column=0, padx=10, pady=10)
            self.categorie_combobox = ttk.Combobox(edit_products_frame, values=["Audio-Video", "Auto", "Bacanie", "Birotica", "Bricolaj","Carti", "Casa", "Diverse", "Electrocasnice", "Fashion","Foto", "Gaming", "Gradina", "Laptop", "Moto","PC", "Periferice", "Software", "TV", "Tablete","Telefoane"])
            self.categorie_combobox.grid(row=7, column=1, padx=10, pady=10)

            # ID_Promotie
            id_promotie_label = tk.Label(edit_products_frame, text="ID_Promotie", bg="#333333", fg="white")
            id_promotie_label.grid(row=8, column=0, padx=10, pady=10)
            self.id_promotie_combobox = ttk.Combobox(edit_products_frame, values=possible_promotion_values)
            self.id_promotie_combobox.grid(row=8, column=1, padx=10, pady=10)

            confirm_edit_button = tk.Button(edit_products_frame, text="Confirm Changes",
                                            command=lambda: confirmChanges(product_data[0]),
                                            bg="#555555", fg="white", font=('Helvetica', 14))
            confirm_edit_button.grid(row=9, column=0, padx=10)

        def selectProducts():
            edit_products_button.destroy()
            add_products_button.destroy()

            # Create a frame below the buttons for text labels
            labels_frame = tk.Frame(self.edit_products_frame, bg="#333333")
            labels_frame.pack(side="top", fill='both', anchor='n')

            cur = connection.cursor()
            cur.execute(
                'SELECT p.ID_produs, p.Denumire, p.Producator, p.Pret * CASE WHEN procent_reducere > 0 THEN (1-prom.procent_reducere/100) ELSE 1 END FROM produse p, promotii prom WHERE p.id_promotie = prom.id_promotie')
            products = []
            for result in cur:
                products.append((result[0], result[1], result[2], result[3]))
            cur.close()

            labels_data = [
                ("ID", "Denumire", "Producator", "Pret", ""),
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
                    edit_button = tk.Button(labels_frame, text="Edit",
                                            command=lambda r=row_data: editProducts(r), bg=bg_color,
                                            fg="white", font=('Helvetica', 12), padx=10, pady=5)
                    edit_button.grid(row=row_idx, column=len(row_data), sticky="nsew")

            # Configure row and column weights to make labels expand with resizing
            for i in range(len(labels_data)):
                labels_frame.grid_rowconfigure(i, weight=1)

            for i in range(len(labels_data) - 3):  # Additional column for 'View' button
                labels_frame.grid_columnconfigure(i, weight=1)

        edit_products_frame = tk.Frame(self.main_menu_frame, bg="#333333")
        edit_products_frame.pack(side="top", fill='y', anchor='n')
        self.edit_products_frame = edit_products_frame

        # Add two buttons at the top for "My Wishlists" and "Public Wishlists"
        edit_products_button = tk.Button(edit_products_frame, text="Edit Product", command=selectProducts,
                                        bg="#555555", fg="white", font=('Helvetica', 14))
        edit_products_button.grid(row=0, column=0, padx=10)

        add_products_button = tk.Button(edit_products_frame, text="Create Product",
                                            command=addProducts, bg="#555555", fg="white",
                                            font=('Helvetica', 14))
        add_products_button.grid(row=0, column=1, padx=10)

    def show_products_frame(self):
        self.destroyAllFrames()

        labels_frame = tk.Frame(self.main_menu_frame, bg="#333333")
        labels_frame.pack(side="top", fill='both', anchor='n')
        self.products_frame = labels_frame

        cur = connection.cursor()
        cur.execute('SELECT p.ID_produs, p.Denumire, p.Producator, p.Pret * CASE WHEN procent_reducere > 0 THEN (1-prom.procent_reducere/100) ELSE 1 END FROM produse p, promotii prom WHERE p.id_promotie = prom.id_promotie')
        products = []
        for result in cur:
            products.append((result[0], result[1], result[2], result[3]))
        cur.close()

        labels_data = [
            ("ID", "Denumire", "Producator", "Pret", ""),
            *products
        ]

        for row_idx, row_data in enumerate(labels_data):
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
                label = tk.Label(labels_frame, text=str(value), bg=bg_color, fg="white", font=('Helvetica', 12),
                                 padx=10, pady=5)
                label.grid(row=row_idx, column=col_idx, sticky="nsew")

            if show_button:
                view_button = tk.Button(labels_frame, text="View",
                                        command=lambda r=row_data: self.view_product(r, labels_frame), bg=bg_color,
                                        fg="white", font=('Helvetica', 12), padx=10, pady=5)
                view_button.grid(row=row_idx, column=len(row_data), sticky="nsew")

        for i in range(len(labels_data)):
            labels_frame.grid_rowconfigure(i, weight=1)

        for i in range(len(labels_data) - 3):
            labels_frame.grid_columnconfigure(i, weight=1)

    def view_wishlists(self):
        global id_client
        self.destroyAllFrames()

        wishlists_frame = tk.Frame(self.main_menu_frame, bg="#333333")
        wishlists_frame.pack(side="top", fill='y', anchor='n')
        self.wishlists_frame = wishlists_frame

        my_wishlists_button = tk.Button(wishlists_frame, text="My Wishlists", command=self.show_my_wishlists,
                                        bg="#555555", fg="white", font=('Helvetica', 14))
        my_wishlists_button.grid(row=0, column=0, padx=10)

        public_wishlists_button = tk.Button(wishlists_frame, text="Public Wishlists",
                                            command=self.show_public_wishlists, bg="#555555", fg="white",
                                            font=('Helvetica', 14))
        public_wishlists_button.grid(row=0, column=1, padx=10)

    def view_cart(self):
        global id_client
        total_price = 0
        self.destroyAllFrames()

        cart_frame = tk.Frame(self.main_menu_frame, bg="#333333")
        cart_frame.pack(side="top", fill='both', anchor='n')
        self.products_frame = cart_frame

        cart_total_frame = tk.Frame(self.cart_frame, bg="#333333")
        cart_total_frame.pack(side="top", fill='both', anchor='n')
        self.cart_total_frame = cart_total_frame

        cur = connection.cursor()
        cur.execute(
            'SELECT c.ID_cos, prod.Denumire, prod.Producator, c.Cantitate, prod.Pret * CASE WHEN prom.procent_reducere > 0 THEN (1-prom.procent_reducere/100) ELSE 1 END FROM cosuri c, produse prod, promotii prom \
             WHERE c.ID_client = :id_client AND c.ID_produs = prod.ID_produs AND prod.Id_Promotie = prom.Id_Promotie', {'id_client': id_client})
        cart_items = []
        for result in cur:
                cart_items.append((result[0], result[1], result[2], result[3], result[4]))

        cur.execute('SELECT SUM(c.cantitate * prod.Pret * CASE WHEN prom.procent_reducere > 0 THEN (1-prom.procent_reducere/100) ELSE 1 END) FROM cosuri c, produse prod, promotii prom \
             WHERE c.ID_client = :id_client AND c.ID_produs = prod.ID_produs AND prod.Id_Promotie = prom.Id_Promotie', {'id_client': id_client})
        total_price = cur.fetchone()[0]

        cur.close()

        filtered_cart_items = [item[1:] for item in cart_items]

        cart_data = [
            ("Denumire Produs", "Producator", "Cantitate", "Pret", ""),
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
                if col_idx == 2 and row_idx > 0:
                    entry = tk.Entry(cart_frame, bg=bg_color if row_idx % 2 == 0 else "#555555", fg="white",
                                     font=('Helvetica', 12), justify="center")
                    entry.insert(0, str(value))
                    entry.grid(row=row_idx, column=col_idx, sticky="nsew")

                    entry.bind("<FocusOut>", lambda event, r=cart_items[row_idx-1], e=entry: self.update_quantity(event, r, e))
                else:
                    label = tk.Label(cart_frame, text=str(value), bg=bg_color if row_idx % 2 == 0 else "#555555",
                                     fg="white", font=('Helvetica', 12), padx=10, pady=5)
                    label.grid(row=row_idx, column=col_idx, sticky="nsew")

            if show_button:
                remove_button = tk.Button(cart_frame, text="Remove",
                                          command=lambda r=cart_items[row_idx-1]: self.remove_from_cart(r),
                                          bg=bg_color, fg="white", font=('Helvetica', 12), padx=10, pady=5)
                remove_button.grid(row=row_idx, column=len(row_data), sticky="nsew")

        for i in range(len(cart_data)):
            cart_frame.grid_rowconfigure(i, weight=1)

        for i in range(len(cart_data) + 1):
            cart_frame.grid_columnconfigure(i, weight=1)

        total_price_label = tk.Label(cart_total_frame, text=f"Total Price: {total_price} RON", font=('Helvetica', 14), bg="#333333",
                                       fg="white")
        total_price_label.pack()

        place_order_button = tk.Button(cart_total_frame, text="Place Order",
                                  command=lambda r=cart_items: self.place_order(r),
                                  bg=bg_color, fg="white", font=('Helvetica', 12), padx=10, pady=5)
        place_order_button.pack(pady=10)

    def view_orders(self):
        global id_client
        self.destroyAllFrames()

        orders_frame = tk.Frame(self.main_menu_frame, bg="#333333")
        orders_frame.pack(side="top", fill='both', anchor='n')
        self.orders_frame = orders_frame

        cur = connection.cursor()

        cur.execute(
            'SELECT MIN(c.ID_comanda), c.data_inregistrare, c.status, c.data_preluare, SUM(prod.Pret * CASE WHEN prom.procent_reducere > 0 THEN (1-prom.procent_reducere/100) ELSE 1 END * CASE WHEN cp.procent_reducere > 0 THEN (1-cp.procent_reducere/100) ELSE 1 END) FROM comenzi c, produse prod, promotii prom, coduri_promotionale cp \
             WHERE c.ID_client = :id_client AND c.ID_produs = prod.ID_produs AND prod.Id_Promotie = prom.Id_Promotie AND cp.Comenzi_ID_comanda = c.ID_comanda \
             GROUP BY c.data_inregistrare, c.status, c.data_preluare',
            {'id_client': id_client})
        cart_items = []
        for result in cur:
            cart_items.append((result[0], result[1], result[2], result[3], result[4]))
        cur.close()

        cart_data = [
            ("ID Comanda", "Data Inregistrare", "Status", "Data Preluare", "Pret Total", ""),
            *cart_items
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
                    label = tk.Label(orders_frame, text=str(value), bg=bg_color if row_idx % 2 == 0 else "#555555",
                                     fg="white", font=('Helvetica', 12), padx=10, pady=5)
                    label.grid(row=row_idx, column=col_idx, sticky="nsew")

            if show_button:
                view_order_button = tk.Button(orders_frame, text="View",
                                          command=lambda r=cart_items[row_idx - 1]: self.view_order_items(r),
                                          bg=bg_color, fg="white", font=('Helvetica', 12), padx=10, pady=5)
                view_order_button.grid(row=row_idx, column=len(row_data), sticky="nsew")

            for i in range(len(cart_data)):
                orders_frame.grid_rowconfigure(i, weight=1)

            for i in range(len(cart_data) + 1):
                orders_frame.grid_columnconfigure(i, weight=1)

    def place_order(self, cart_data):
        global id_client
        cur = connection.cursor()
        try:
            query = 'SELECT id_produs, cantitate FROM cosuri WHERE id_client = :id_client'
            cur.execute(query, {'id_client': id_client})
            products = []
            for result in cur:
                products.append((result[0], result[1]))

            for product in products:
                query = 'INSERT INTO comenzi (id_comanda, data_inregistrare, data_preluare, status, id_client, id_produs, cantitate)' \
                        'VALUES (NULL, SYSDATE, NULL, DEFAULT, :id_client, :id_produs, :cantitate)'
                cur.execute(query, {
                    'id_client': id_client,
                    'id_produs': product[0],
                    'cantitate': product[1]
                })

            query = 'DELETE FROM cosuri WHERE id_client = :id_client'
            cur.execute(query, {'id_client': id_client})

            randomVoucherPercent = random.randint(0, 100)
            randomVoucher = 0
            if randomVoucherPercent > 0:
                randomVoucher = random.randint(1, 99999)

            query = 'INSERT INTO coduri_promotionale (Clienti_ID_client,Comenzi_ID_comanda,Cod_Voucher,Procent_Reducere,Data_inceput,Data_sfarsit,Descriere)' \
                    'VALUES (:id_client, (SELECT MIN(id_comanda) FROM comenzi WHERE id_client = :id_client AND data_inregistrare = SYSDATE), :randomVoucher, :procent_reducere, SYSDATE, ADD_MONTHS(SYSDATE,3),NULL)'
            cur.execute(query, {
                'id_client': id_client,
                'randomVoucher': randomVoucher,
                'procent_reducere': randomVoucherPercent
            })

            cur.execute('commit')
            self.view_orders()
        except oracledb.DatabaseError as e:
            error, = e.args
            if str(error.code) == "20001":
                print("Custom application error:", str(e))
                messagebox.showerror("Stock Error", "Unele produse nu mai sunt in stoc momentan sau nu au stoc suficient!")
            else:
                print("Database error:", str(e))
                messagebox.showerror("Database Error",
                                     "An error occurred while interacting with the database. Please try again. [Error Code: " + str(e) + "]")
            cur.execute('rollback')
            self.view_cart()
        finally:
            cur.close()

    def view_order_items(self,order_data):
        global id_client
        self.destroyAllFrames()

        order_items_frame = tk.Frame(self.main_menu_frame, bg="#333333")
        order_items_frame.pack(side="top", fill='both', anchor='n')
        self.order_items_frame = order_items_frame

        cur = connection.cursor()
        cur.execute(
            'SELECT prod.Denumire, prod.Producator, c.Cantitate, prod.Pret * CASE WHEN prom.procent_reducere > 0 THEN (1-prom.procent_reducere/100) ELSE 1 END, \
             cp.procent_reducere, prod.Pret * CASE WHEN prom.procent_reducere > 0 THEN (1-prom.procent_reducere/100) ELSE 1 END * CASE WHEN cp.procent_reducere > 0 THEN (1-cp.procent_reducere/100) ELSE 1 END \
             FROM comenzi c, produse prod, promotii prom, coduri_promotionale cp \
             WHERE c.ID_client = :id_client AND c.ID_produs = prod.ID_produs AND prod.Id_Promotie = prom.Id_Promotie AND c.data_inregistrare = :data_inregistrare AND cp.Comenzi_Id_Comanda = c.Id_Comanda',
            {'id_client': id_client, 'data_inregistrare': order_data[1]})
        order_items = []
        for result in cur:
            order_items.append((result[0], result[1], result[2], result[3],result[4],result[5]))

        cur.close()

        cart_data = [
            ("Denumire Produs", "Producator", "Cantitate", "Pret", "Reducere Voucher", "Pret Final"),
            *order_items
        ]

        for row_idx, row_data in enumerate(cart_data):

            if row_idx == 0:
                bg_color = "#222222"
            elif row_idx % 2 == 0:
                bg_color = "#444444"
            else:
                bg_color = "#555555"

            for col_idx, value in enumerate(row_data):
                # Add a label or entry based on the column
                label = tk.Label(order_items_frame, text=str(value), bg=bg_color if row_idx % 2 == 0 else "#555555",
                                 fg="white", font=('Helvetica', 12), padx=10, pady=5)
                label.grid(row=row_idx, column=col_idx, sticky="nsew")

        for i in range(len(cart_data)):
            order_items_frame.grid_rowconfigure(i, weight=1)

        for i in range(len(cart_data) + 1):
            order_items_frame.grid_columnconfigure(i, weight=1)

    def view_product(self, product_data, labels_frame):
        labels_frame.destroy()

        detail_frame = tk.Frame(self.main_menu_frame, bg="#333333")
        detail_frame.pack(side="top", fill='both', anchor='n')
        self.details_frame = detail_frame

        cur = connection.cursor()
        cur.execute('SELECT p.id_produs,p.denumire,p.pret * CASE WHEN prom.procent_reducere > 0 THEN (1-prom.procent_reducere/100) ELSE 1 END, p.producator, p.stoc, p.categorie, p.garantie, p.descriere, p.id_promotie FROM produse p, promotii prom WHERE p.Id_Produs = :product_id AND prom.id_promotie = p.id_promotie', {'product_id': product_data[0]})
        product = cur.fetchone()
        cur.close()

        cur = connection.cursor()
        cur.execute('SELECT * FROM promotii prom WHERE prom.id_promotie = :prom_id', {'prom_id': product[8]})
        promo = cur.fetchone()
        cur.close()

        if not product:
            print("No product found.")
        else:

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
            if row_idx % 2 == 0:
                bg_color = "#444444"
            else:
                bg_color = "#555555"

            label = tk.Label(detail_frame, text=f"{label}: {value}", bg=bg_color, fg="white", font=('Helvetica', 12), padx=10, pady=5)
            label.grid(row=row_idx, column=0, sticky="nsew")

        if promo and promo[1] > 0:
            bg_color = "#444444" if bg_color == "#555555" else "#444444"
            label = tk.Label(detail_frame, text=f"[{promo[0]}] {promo[4]} incepand cu data de {promo[2]} pana la data de {promo[3]}", bg=bg_color, fg="white", font=('Helvetica', 12), padx=10, pady=5)
            label.grid(row=row_idx+1, column=0, sticky="nsew")

        buttons_frame = tk.Frame(detail_frame, bg="#333333")
        buttons_frame.grid(row=len(detail_labels_data)+1, column=0, sticky="n", pady=10)

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

        for i in range(len(detail_labels_data) + 1):
            detail_frame.grid_rowconfigure(i, weight=1)

        detail_frame.grid_columnconfigure(0, weight=1)

    def add_to_wishlist(self, product):

        global id_client

        if self.details_frame:
            self.details_frame.destroy()

        if self.add_to_wishlist_frame:
            self.add_to_wishlist_frame.destroy()

        def add_to_existing_wishlist():
            select_wishlist_button.destroy()
            new_wishlist_button.destroy()

            def confirm_adding_to_wishlist():
                wishlist_name = self.selected_value.get()

                try:
                    cur = connection.cursor()

                    cur.execute('SELECT id_produs FROM wishlists WHERE id_client = :id_client AND nume = :nume', {'id_client': id_client, 'nume':wishlist_name})
                    products = []
                    for result in cur:
                        products.append(result[0])

                    if not product[0] in products:

                        query = 'INSERT INTO wishlists (id_wishlist, nume, data_creare, vizibilitate, id_client, id_produs)' \
                              'VALUES (NULL,:nume, (SELECT data_creare FROM wishlists WHERE id_client = :id_client AND nume = :nume), ' \
                                '(SELECT vizibilitate FROM wishlists WHERE id_client = :id_client AND nume = :nume), :id_client, :id_produs)'
                        cur.execute(query, {
                            'nume': wishlist_name,
                            'id_client': id_client,
                            'id_produs': product[0]
                        })
                        cur.execute('commit')
                    else:
                        messagebox.showerror("Error!", "You can't have the same product in the wishlist twice!")

                    cur.close()

                except oracledb.DatabaseError as e:
                    print("Database error:", str(e))
                    messagebox.showerror("Database Error",
                                     "An error occurred while interacting with the database. Please try again. [Error Code: " + str(e) + "]")

                self.show_products_frame()

            wishlists_label = tk.Label(self.add_to_wishlist_frame, text="Select Wishlist::",
                                        font=('Helvetica', 14), bg="#333333", fg="white")
            wishlists_label.pack()

            try:
                cur = connection.cursor()
                query = 'SELECT DISTINCT nume FROM wishlists WHERE id_client = :id_client'
                cur.execute(query, {'id_client': id_client})
                predefined_values = []
                for result in cur:
                    predefined_values.append(result[0])
                cur.close()

                self.selected_value = tk.StringVar()
                values_comboBox = ttk.Combobox(self.add_to_wishlist_frame, values=predefined_values,
                                               textvariable=self.selected_value, font=('Helvetica', 14))
                values_comboBox.set(predefined_values[0])  # Set the default value
                values_comboBox.pack(pady=10)

                confirm_button = tk.Button(self.add_to_wishlist_frame, text="Create",
                                           command=confirm_adding_to_wishlist,
                                           bg="#555555", fg="white", font=('Helvetica', 14))
                confirm_button.pack(pady=10)

            except oracledb.DatabaseError as e:
                print("Database error:", str(e))
                messagebox.showerror("Database Error",
                                     "An error occurred while interacting with the database. Please try again. [Error Code: " + str(e) + "]")
        def create_new_wishlist():
            select_wishlist_button.destroy()
            new_wishlist_button.destroy()

            def confirm_creation():
                new_name = self.wishlist_name_entry.get()
                new_visibility = self.selected_value.get()

                try:
                    cur = connection.cursor()
                    query = 'INSERT INTO wishlists (id_wishlist, nume, data_creare, vizibilitate, id_client, id_produs)' \
                          'VALUES (NULL,:nume, SYSDATE, :vizibilitate, :id_client, :id_produs)'
                    cur.execute(query, {
                        'nume': new_name,
                        'vizibilitate': new_visibility,
                        'id_client': id_client,
                        'id_produs': product[0]
                    })
                    cur.execute('commit')
                    cur.close()

                except oracledb.DatabaseError as e:
                    print("Database error:", str(e))
                    messagebox.showerror("Database Error",
                                     "An error occurred while interacting with the database. Please try again. [Error Code: " + str(e) + "]")

                self.show_products_frame()

            # Name Field
            wishlist_name = tk.Label(self.add_to_wishlist_frame, text="Wishlist Name:", font=('Helvetica', 14), bg="#333333",
                                      fg="white")
            wishlist_name.pack()

            self.wishlist_name_entry = tk.Entry(self.add_to_wishlist_frame, bg="#333333", fg="white",
                                               font=('Helvetica', 14), width=30)
            self.wishlist_name_entry.pack(pady=10)  # Add padding between the fields

            # Visibility ComboBox
            visibility_label = tk.Label(self.add_to_wishlist_frame, text="Select Visibility:",
                                               font=('Helvetica', 14), bg="#333333", fg="white")
            visibility_label.pack()

            predefined_values = ["Public", "Privat", "Nelistat"]  # Replace with your predefined values
            self.selected_value = tk.StringVar()
            values_comboBox = ttk.Combobox(self.add_to_wishlist_frame, values=predefined_values,
                                                           textvariable=self.selected_value, font=('Helvetica', 14))
            values_comboBox.set(predefined_values[0])  # Set the default value
            values_comboBox.pack(pady=10)

            # Confirmation Button
            confirm_button = tk.Button(self.add_to_wishlist_frame, text="Create",
                                            command=confirm_creation,
                                            bg="#555555", fg="white", font=('Helvetica', 14))
            confirm_button.pack(pady=10)


        add_to_wishlist_frame = tk.Frame(self.main_menu_frame, bg="#333333")
        add_to_wishlist_frame.pack(side="top", fill='y', anchor='n')
        self.add_to_wishlist_frame = add_to_wishlist_frame

        # Add two buttons at the top for "My Wishlists" and "Public Wishlists"
        new_wishlist_button = tk.Button(add_to_wishlist_frame, text="Create a new Wishlist", command=create_new_wishlist,
                                        bg="#555555", fg="white", font=('Helvetica', 14))
        new_wishlist_button.grid(row=0, column=0, padx=10)

        select_wishlist_button = tk.Button(add_to_wishlist_frame, text="Add to an existing Wishlist",
                                            command=add_to_existing_wishlist, bg="#555555", fg="white",
                                            font=('Helvetica', 14))
        select_wishlist_button.grid(row=0, column=1, padx=10)

    def moveToCart(self,wishlistData,productData):
        global id_client
        already_in_cart = False
        try:
            cur = connection.cursor()
            query = 'SELECT id_cos FROM cosuri WHERE id_client = :id_client AND id_produs = :id_produs'
            cur.execute(query, {'id_client': id_client, 'id_produs': productData[0]});
            id_cos = cur.fetchone()
            if id_cos:
                already_in_cart = True

            if not already_in_cart:
                query = 'INSERT INTO cosuri(id_cos, cantitate, id_client, id_produs) ' \
                        'VALUES (NULL,1,:id_client,:id_produs)'
                cur.execute(query, {
                    'id_client': id_client,
                    'id_produs': productData[0]
                })
            else:
                query = 'UPDATE cosuri SET cantitate = cantitate + 1 WHERE id_cos = :id_cos'
                cur.execute(query, {'id_cos': id_cos[0]})

            query = 'DELETE FROM wishlists WHERE nume = :nume AND id_produs = :id_produs AND id_client = :id_client'
            cur.execute(query, {
                'nume': wishlistData[0],
                'id_produs': productData[0],
                'id_client': id_client
            })

            cur.execute('commit')
            cur.close()
        except oracledb.DatabaseError as e:
            print("Database error:", str(e))
            messagebox.showerror("Database Error",
                                 "An error occurred while interacting with the database. Please try again. [Error Code: " + str(e) + "]")

        self.viewWishlistProducts(wishlistData,True)

    def viewWishlistProducts(self, wishlist_data, ownWishlist):
        global id_client
        self.destroyAllFrames()

        wishlists_products_frame = tk.Frame(self.main_menu_frame, bg="#333333")
        wishlists_products_frame.pack(side="top", fill='both', anchor='n')
        self.wishlists_products_frame = wishlists_products_frame

        cur = connection.cursor()
        if ownWishlist:
            cur.execute(
                'SELECT p.ID_produs, p.Denumire, p.Producator, p.Pret * CASE WHEN procent_reducere > 0 THEN (1-prom.procent_reducere/100) ELSE 1 END '
                'FROM produse p, promotii prom, wishlists wish '
                'WHERE p.id_promotie = prom.id_promotie AND wish.id_produs = p.id_produs AND wish.id_client = :id_client AND wish.nume = :nume', {'id_client': id_client, 'nume': wishlist_data[0]})
        else:
            cur.execute(
                'SELECT p.ID_produs, p.Denumire, p.Producator, p.Pret * CASE WHEN procent_reducere > 0 THEN (1-prom.procent_reducere/100) ELSE 1 END '
                'FROM produse p, promotii prom, wishlists wish '
                'WHERE p.id_promotie = prom.id_promotie AND wish.id_produs = p.id_produs '
                'AND wish.id_client = (SELECT id_client FROM conturi cnt WHERE username = :username) AND wish.nume = :nume',
                {'username': wishlist_data[3], 'nume': wishlist_data[0]})
        products = []
        for result in cur:
            products.append((result[0], result[1], result[2], result[3]))
        cur.close()

        labels_data = [
            ("ID", "Denumire", "Producator", "Pret", "", "", ""),
            *products
        ]

        for row_idx, row_data in enumerate(labels_data):
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
                label = tk.Label(wishlists_products_frame, text=str(value), bg=bg_color, fg="white", font=('Helvetica', 12),
                                 padx=10, pady=5)
                label.grid(row=row_idx, column=col_idx, sticky="nsew")

            if show_button:
                view_button = tk.Button(wishlists_products_frame, text="View",
                                        command=lambda r=row_data: self.view_product(r, wishlists_products_frame), bg=bg_color,
                                        fg="white", font=('Helvetica', 12), padx=10, pady=5)
                view_button.grid(row=row_idx, column=len(row_data), sticky="nsew")
                if ownWishlist:

                    move_to_cart_button = tk.Button(wishlists_products_frame, text="Move to Cart",
                                                    command=lambda r=row_data: self.moveToCart(wishlist_data, r),
                                                    bg=bg_color,
                                                    fg="white", font=('Helvetica', 12), padx=10, pady=5)
                    move_to_cart_button.grid(row=row_idx, column=len(row_data) + 1, sticky="nsew")

                    remove_from_wishlist_button = tk.Button(wishlists_products_frame, text="Delete",
                                            command=lambda r=row_data: self.remove_from_wishlist(wishlist_data[0], r),
                                            bg=bg_color,
                                            fg="white", font=('Helvetica', 12), padx=10, pady=5)
                    remove_from_wishlist_button.grid(row=row_idx, column=len(row_data)+2, sticky="nsew")

        for i in range(len(labels_data)):
            wishlists_products_frame.grid_rowconfigure(i, weight=1)

        if ownWishlist:
            for i in range(len(labels_data) + 3):
                wishlists_products_frame.grid_columnconfigure(i, weight=1)
        else:
            for i in range(len(labels_data) + 1):
                wishlists_products_frame.grid_columnconfigure(i, weight=1)

    def deleteWishlist(self,wishlistName):
        global id_client
        try:
            cur = connection.cursor()
            query = 'DELETE FROM wishlists WHERE id_client = :id_client AND nume = :nume'
            cur.execute(query, {'id_client': id_client, 'nume':wishlistName})
            cur.execute('commit')
            cur.close()
        except oracledb.DatabaseError as e:
            print("Database error:", str(e))
            messagebox.showerror("Database Error",
                                 "An error occurred while interacting with the database. Please try again. [Error Code: " + str(e) + "]")
        self.show_my_wishlists()

    def remove_from_wishlist(self, wishlistName, productData):
        global id_client
        try:
            cur = connection.cursor()
            query = 'DELETE FROM wishlists WHERE id_client = :id_client AND nume = :nume AND id_produs = :id_produs'
            cur.execute(query, {
                'id_client': id_client,
                'nume': wishlistName,
                'id_produs': productData[0]
            })
            cur.execute('commit')
            cur.close()

        except oracledb.DatabaseError as e:
            print("Database error:", str(e))
            messagebox.showerror("Database Error",
                                 "An error occurred while interacting with the database. Please try again. [Error Code: " + str(e) + "]")

    def show_my_wishlists(self):
        global id_client
        self.destroyAllFrames()

        labels_frame = tk.Frame(self.main_menu_frame, bg="#333333")
        labels_frame.pack(side="top", fill='both', anchor='n')
        self.wishlists_list_frame = labels_frame

        cur = connection.cursor()
        cur.execute(
            'SELECT DISTINCT Nume, Vizibilitate, Data_creare FROM wishlists WHERE id_client = :id_client', {'id_client': id_client})
        wishlists = []
        for result in cur:
            wishlists.append((result[0], result[1], result[2]))
        cur.close()

        labels_data = [
            ("Nume", "Vizibilitate", "Data la care a fost creat", "", ""),
            *wishlists
        ]

        for row_idx, row_data in enumerate(labels_data):
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
                label = tk.Label(labels_frame, text=str(value), bg=bg_color, fg="white", font=('Helvetica', 12),
                                 padx=10, pady=5)
                label.grid(row=row_idx, column=col_idx, sticky="nsew")

            if show_button:
                view_button = tk.Button(labels_frame, text="View",
                                        command=lambda r=row_data: self.viewWishlistProducts(r, True), bg=bg_color,
                                        fg="white", font=('Helvetica', 12), padx=10, pady=5)
                view_button.grid(row=row_idx, column=len(row_data), sticky="nsew")

                delete_button = tk.Button(labels_frame, text="Delete",
                                        command=lambda r=row_data: self.deleteWishlist(row_data[0]),
                                        bg=bg_color,
                                        fg="white", font=('Helvetica', 12), padx=10, pady=5)
                delete_button.grid(row=row_idx, column=len(row_data)+1, sticky="nsew")

        for i in range(len(labels_data)):
            labels_frame.grid_rowconfigure(i, weight=1)

        for i in range(len(labels_data) + 2):
            labels_frame.grid_columnconfigure(i, weight=1)

    def show_public_wishlists(self):
        global id_client

        self.destroyAllFrames()

        labels_frame = tk.Frame(self.main_menu_frame, bg="#333333")
        labels_frame.pack(side="top", fill='both', anchor='n')
        self.wishlists_list_frame = labels_frame

        cur = connection.cursor()
        cur.execute('SELECT DISTINCT w.Nume, w.Vizibilitate, w.Data_creare, cnt.username FROM wishlists w, conturi cnt, clienti c WHERE c.id_client = cnt.id_client AND c.id_client = w.id_client AND w.vizibilitate = :vizibilitate', {'vizibilitate': "Public"})
        wishlists = []
        for result in cur:
            wishlists.append((result[0], result[1], result[2], result[3]))
        cur.close()

        labels_data = [
            ("Nume", "Vizibilitate", "Data la care a fost creat", "Creator", ""),
            *wishlists
        ]

        for row_idx, row_data in enumerate(labels_data):
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
                label = tk.Label(labels_frame, text=str(value), bg=bg_color, fg="white", font=('Helvetica', 12),
                                 padx=10, pady=5)
                label.grid(row=row_idx, column=col_idx, sticky="nsew")

            if show_button:
                view_button = tk.Button(labels_frame, text="View",
                                        command=lambda r=row_data: self.viewWishlistProducts(r, False), bg=bg_color,
                                        fg="white", font=('Helvetica', 12), padx=10, pady=5)
                view_button.grid(row=row_idx, column=len(row_data), sticky="nsew")

        for i in range(len(labels_data)):
            labels_frame.grid_rowconfigure(i, weight=1)

        for i in range(len(labels_data) + 1):
            labels_frame.grid_columnconfigure(i, weight=1)

    def add_to_cart(self, product):
        global id_client
        already_in_cart = False

        try:
            cur = connection.cursor()
            query = 'SELECT id_cos FROM cosuri WHERE id_client = :id_client AND id_produs = :id_produs'
            cur.execute(query, {'id_client': id_client, 'id_produs': product[0]});
            id_cos = cur.fetchone()
            if id_cos:
                already_in_cart = True

            if not already_in_cart:
                query = 'INSERT INTO cosuri(id_cos, cantitate, id_client, id_produs) ' \
                        'VALUES (NULL,1,:id_client,:id_produs)'
                cur.execute(query, {
                    'id_client': id_client,
                    'id_produs': product[0]
                })
            else:
                query = 'UPDATE cosuri SET cantitate = cantitate + 1 WHERE id_cos = :id_cos'
                cur.execute(query, {'id_cos': id_cos[0]})
            cur.execute('commit')
            cur.close()
        except oracledb.DatabaseError as e:
            print("Database error:", str(e))
            messagebox.showerror("Database Error",
                                 "An error occurred while interacting with the database. Please try again. [Error Code: " + str(e) + "]")

    def remove_from_cart(self, cart_item_data):

        try:
            cur = connection.cursor()
            query = 'DELETE FROM cosuri WHERE id_cos = :deletedItemId'
            cur.execute(query, {
                'deletedItemId': cart_item_data[0]
            })
            cur.execute('commit')
            cur.close()
        except oracledb.DatabaseError as e:
            print("Database error:", str(e))
            messagebox.showerror("Database Error",
                 "An error occurred while interacting with the database. Please try again. [Error Code: "+str(e)+"]")

        self.view_cart()

    def update_quantity(self, event, row_data, entry):
        updated_quantity = entry.get()

        try:
            cur = connection.cursor()
            query = 'UPDATE cosuri SET cantitate = :quantity WHERE id_cos = :modifiedCartId'
            cur.execute(query, {
                'quantity': updated_quantity,
                'modifiedCartId':row_data[0]
            })
            cur.execute('commit')
            cur.close()
            self.view_cart()
        except oracledb.DatabaseError as e:
            print("Database error:", str(e))
            messagebox.showerror("Database Error",
                 "An error occurred while interacting with the database. Please try again. [Error Code: "+str(e)+"]")


class LoginMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Menu")
        self.root.attributes('-fullscreen', True)

        self.root.configure(bg="#333333")

        self.create_account_frame = None
        self.login_frame = None

        self.login_frame = tk.Frame(root, bg="#333333", padx=40, pady=40)
        self.login_frame.pack(expand=True)
        self.create_login_frame()

    def create_login_frame(self):
        self.title_label = tk.Label(self.login_frame, text="Log into your account", font=('Helvetica', 16), bg="#333333", fg="white")
        self.title_label.pack()

        self.username_label = tk.Label(self.login_frame, text="Username:", font=('Helvetica', 14), bg="#333333", fg="white")
        self.username_label.pack()

        self.username_entry = tk.Entry(self.login_frame, bg="#333333", fg="white", font=('Helvetica', 14))
        self.username_entry.pack(pady=10)

        self.password_label = tk.Label(self.login_frame, text="Password:", font=('Helvetica', 14), bg="#333333", fg="white")
        self.password_label.pack()

        self.password_entry = tk.Entry(self.login_frame, show="*", bg="#333333", fg="white", font=('Helvetica', 14))
        self.password_entry.pack(pady=10)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login, bg="#555555", fg="white", font=('Helvetica', 14))
        self.login_button.pack(pady=10)

        self.note_label = tk.Label(self.login_frame, text="Don't have an account?", font=('Helvetica', 12), bg="#333333", fg="white")
        self.note_label.pack(pady=5)

        self.create_account_button = tk.Button(self.login_frame, text="Create Account", command=self.switch_to_create_account, bg="#555555", fg="white", font=('Helvetica', 14))
        self.create_account_button.pack()

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.destroy, bg="#555555", fg="white", font=('Helvetica', 14))
        self.quit_button.place(relx=1.0, rely=0.0, anchor='ne')

    def switch_to_create_account(self):
        self.login_frame.destroy()
        self.create_account_frame = tk.Frame(self.root, bg="#333333", padx=40, pady=40)
        self.create_account_frame.pack(expand=True)

        self.create_account()

    def create_account(self):
        title_label = tk.Label(self.create_account_frame, text="Create Account", font=('Helvetica', 16), bg="#333333",
                               fg="white")
        title_label.pack()

        username_label = tk.Label(self.create_account_frame, text="Username:", font=('Helvetica', 14), bg="#333333",
                                  fg="white")
        username_label.pack()

        self.new_username_entry = tk.Entry(self.create_account_frame, bg="#333333", fg="white", font=('Helvetica', 14), width=30)
        self.new_username_entry.pack(pady=10)

        password_label = tk.Label(self.create_account_frame, text="Password:", font=('Helvetica', 14), bg="#333333",
                                  fg="white")
        password_label.pack()

        self.new_password_entry = tk.Entry(self.create_account_frame, show="*", bg="#333333", fg="white",
                                           font=('Helvetica', 14), width=30)
        self.new_password_entry.pack(pady=10)

        confirm_password_label = tk.Label(self.create_account_frame, text="Confirm Password:", font=('Helvetica', 14),
                                          bg="#333333", fg="white")
        confirm_password_label.pack()

        self.confirm_password_entry = tk.Entry(self.create_account_frame, show="*", bg="#333333", fg="white",
                                               font=('Helvetica', 14), width=30)
        self.confirm_password_entry.pack(pady=10)

        billing_address_label = tk.Label(self.create_account_frame, text="Billing Address:", font=('Helvetica', 14),
                                         bg="#333333", fg="white")
        billing_address_label.pack()

        self.billing_address_entry = tk.Entry(self.create_account_frame, bg="#333333", fg="white",
                                              font=('Helvetica', 14), width=30)
        self.billing_address_entry.pack(pady=10)

        phone_number_label = tk.Label(self.create_account_frame, text="Phone Number:",
                                      font=('Helvetica', 14), bg="#333333", fg="white")
        phone_number_label.pack()

        self.phone_number_entry = tk.Entry(self.create_account_frame, bg="#333333", fg="white", font=('Helvetica', 14), width=30)
        self.phone_number_entry.pack(pady=10)

        email_label = tk.Label(self.create_account_frame, text="Email (Optional):", font=('Helvetica', 14), bg="#333333",
                               fg="white")
        email_label.pack()

        self.email_entry = tk.Entry(self.create_account_frame, bg="#333333", fg="white", font=('Helvetica', 14), width=30)
        self.email_entry.pack(pady=10)

        delivery_address_label = tk.Label(self.create_account_frame, text="Delivery Address (Optional):",
                                          font=('Helvetica', 14), bg="#333333", fg="white")
        delivery_address_label.pack()

        self.delivery_address_entry = tk.Entry(self.create_account_frame, bg="#333333", fg="white",
                                               font=('Helvetica', 14), width=30)
        self.delivery_address_entry.pack(pady=10)

        create_account_button = tk.Button(self.create_account_frame, text="Create Account",
                                          command=self.perform_account_creation, bg="#555555", fg="white",
                                          font=('Helvetica', 14))
        create_account_button.pack(pady=10)

        back_to_login_button = tk.Button(self.create_account_frame, text="Back to Login", command=self.switch_to_login,
                                         bg="#555555", fg="white", font=('Helvetica', 14))
        back_to_login_button.pack(pady=10)

        quit_button = tk.Button(self.root, text="Quit", command=self.root.destroy, bg="#555555", fg="white",
                                font=('Helvetica', 14))
        quit_button.place(relx=1.0, rely=0.0, anchor='ne')

    def perform_account_creation(self):
        new_username = self.new_username_entry.get()
        new_password = hashlib.sha256(self.new_password_entry.get().encode()).hexdigest()
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

                self.switch_to_login()
            else:
                messagebox.showerror("Error", "Password and Confirm Password do not match.")

        except oracledb.DatabaseError as e:
            print("Database error:", str(e))
            messagebox.showerror("Database Error",
                                 "An error occurred while interacting with the database. Please try again. [Error Code: "+str(e)+"]")

    def switch_to_main_menu(self):
        if self.create_account_frame:
            self.create_account_frame.destroy()
        if self.login_frame:
            self.login_frame.destroy()
        MainMenu(self.root)

    def switch_to_login(self):
        self.create_account_frame.destroy()
        self.login_frame = tk.Frame(self.root, bg="#333333", padx=40, pady=40)
        self.login_frame.pack(expand=True)
        self.create_login_frame()

    def login(self):
        global is_admin
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
                    'password': hashlib.sha256(password.encode()).hexdigest()
                })
                id_client = cur.fetchone()
                cur.close()

                if id_client:
                    id_client = id_client[0]

                if username == "admin":
                    is_admin = True

                if id_client is not None:
                    self.switch_to_main_menu()
                else:
                    messagebox.showerror("Error", "The username or the password is wrong!")

        except oracledb.DatabaseError as e:
            print("Database error:", str(e))
            messagebox.showerror("Database Error",
                                 "An error occurred while interacting with the database. Please try again. [Error Code: "+str(e)+"]")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginMenu(root)
    root.mainloop()