# Shop Management Application

A Python-based shop management application that connects to an Oracle database using the oracledb driver (Thin mode). The application provides a full shopping experience including product browsing, wishlists, cart management, and order processing. Admin users can also manage the product catalog

![2025-06-1416-10-12-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/3c9853f6-bb0b-4a6a-a30c-5f430ee7f691)

## Features
### Authentification
- Secure login system
- Account creation
- Passwords hashed (secure storage)
- SQL queries fully parameterized (SQL injection safe)

![Screenshot 2025-06-14 161329](https://github.com/user-attachments/assets/aa87d5bd-68fa-4f0c-b3f3-cf80a212eb60) ![Screenshot 2025-06-14 161357](https://github.com/user-attachments/assets/e0d30d9f-307f-4adc-b6ba-173e7206b1dd)



### User Interface
#### Browse Products
- View a list of available products
- View product details (description, price, stock, etc.)
- Add products to cart directly from product details

![Screenshot 2025-06-14 161432](https://github.com/user-attachments/assets/348003f2-b58b-4fde-9669-19d644560e89) ![Screenshot 2025-06-14 161442](https://github.com/user-attachments/assets/3ad68459-a44c-4ca1-8126-f4a5c85e98dd)

#### Wishlists
- View personal wishlists
- View other users' public wishlists
- Add/remove products from wishlists

#### Cart
- View items currently in cart
- Update product quantities
- Remove items
- Place orders

#### Orders
- View order history
- See order status, date, total cost, and ordered items

#### Admin Panel
- Create new products
- Edit existing products
- Update stock, descriptions, prices, etc.

![Screenshot 2025-06-14 161501](https://github.com/user-attachments/assets/70c3a848-f508-4fb6-9de1-6203d2b5c1fe) ![Screenshot 2025-06-14 161513](https://github.com/user-attachments/assets/c8678367-a74f-4cf8-a8d1-cacefe0cff67)

## Technologies Used
- Python
- OracleDB

## Entity-Relationship Diagram (ERD)

![Relational_1](https://github.com/user-attachments/assets/b95bbce7-8899-41bc-8f0e-c1f71cd1d7c8)

## Setup Instructions
1) Clone the repository.
2) Install dependencies using: pip install -r requirements.txt
3) Create the .env file and use your connection details.
4) Create & Populate the Database using the provided .ddl and .sql files.
5) Run the application. 
