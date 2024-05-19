# ShopIt
Welcome to the ShopIt repository! This project is a fully functional e-commerce website developed using Python, HTML, and CSS, integrated with the Safaricom API for payment processing. The website features a user registration and login system, product listing, and order management. The backend is supported by a robust database, and the application runs on a local server for development and testing.

# Features
- User Authentication: Secure user registration and login system with password encryption to ensure data privacy and security.
- Product Listing: Dynamic display of products with essential details such as name, price, and description, allowing users to browse available items.
Order Management: Users can place orders for products and view their order history.
- Payment Integration: Seamless integration with the Safaricom API for secure payment processing.
- Database: A robust database system to store user information, product details, and order records, ensuring data integrity and reliability.
- Local Hosting: The application can be easily hosted and tested on a local server, making development and debugging straightforward.
# Technologies Used
- Backend: Python for server-side logic and API integration.
- Frontend: HTML and CSS for designing responsive and user-friendly web pages.
- Database: A database system to manage and store user and product data efficiently.
- API Integration: Safaricom Daraja API for handling payment transactions.
- Local Host: Local server setup for development and testing purposes.
# Getting Started
To get a local copy up and running, follow these simple steps:

- Clone the repository:

* bash
Copy code
git clone https://github.com/Roy538/ShopIt.git
Navigate to the project directory:

* bash
Copy code
cd ShopIt
Install the required dependencies:

* bash
Copy code
pip install -r requirements.txt
Set up the database:

- Ensure your database server is running.
Run the database migration scripts (if applicable) to set up the required tables.
Configure the Safaricom Daraja API:

- Add your Safaricom Daraja API credentials to the project's configuration file.
Run the application:

* bash
Copy code
python manage.py runserver
Access the application:
Open your web browser and navigate to http://localhost:8000 to start using ShopIt.