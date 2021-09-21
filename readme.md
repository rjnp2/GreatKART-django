django-admin startproject project_name

python manage.py runserver

python manage.py migrate

python manage.py createsuperuser

python manage.py startapp app-name

python manage.py makemigrations

python manage.py collectstatic

Work on this project.

1. Django Custom User Model, Category & Media Files 
	- create Category Model
	- create Custom User Model
	- Making Custom User Mode
	- Making the Custom Password Field Read-only
	- Configuring Django Media Files
	- Pre-populate Category Slug
	
2. Working with Products
	- Store App & Product Model
	- Add Products
	- Display Product in Homepage
	- Make Store Page
	- Display Products in Store Page
	- Display Products by Category

3. Context Processors & Product Details 
	- Make Context Processors for Displaying Categories on Navbar
	- Display Categories in the Store Page
	- Implement Product Detail Url and Design
	- Single Product View
	- Get URL for Product
	- Changed Cover Photo
	- Product Out of Stock Tag

4. Setup Git and Start Carts Functionality
	- Setup Git for Project
	- Carts App & Cart Page Design
	- Cart & Cart Item Models

6. Add to Cart using Session Keys, Increment/decrement/remove Cart Items
	- Add to Cart Functionality without Logging-in and with Session Key 
	- Cart View for Getting Cart Items, Total & Quantity
	- Implement Data into Cart Page
	- Calculate Tax & Grand Total
	- Decrement & Remove Cart Items
	
7. Fixing Cart Bugs & Context Processor for Cart Item Counter
	- Check for Empty Cart
	- Fix Add to Cart Links
	- Check If the Product Added to the Cart
	- Counter Context Processor for Cart Icon in Navbar
	
8. Paginator & Search
	- View Details Button
	- Paginator Part 01
	- Paginator Part 02
	- Fixing Products Warning and Empty Cart Issue
	- Search Function

9. Product Variations & Variation Manager
	- Product Variation Preparation
	- Product Variation Model
	- Product Variation Fetch Dynamic Color
	- Variation Manager for Variation Model
	- Get the Instance of Variation 

10. Adding the Variation in Cart, Grouping Cart Item Variations
	- Add Variation in Cart Item
	- Grouping Cart Item Variations
	- Cart Increment/Decrement/Remove with Variations
		
11. Registration, log in with Token-Based Verification & Message Alerts
	- Registration Preparation : Setting Up Urls & Design
	- Registration : Implementing Model Forms and Editing __init__ Method
	- Registration : Making View & Editing Model Form Clean Method to Check Passwords
	- Django Message Alerts
	- User Login Functionality

12. User Account Activation & Activation Link Expiry
	- Account Activation – Encode User PK & Send Token Based Activation Link
	- Account Activation – Decode User PK & Activate the User | Expire Link
	- Dashboard

13. Forgot Password with Secure Validation Links
	- Forgot Password
	- Reset Password Validation
	- Push Code to GitHub

14. Cart Checkout, automatically assign the Cart Items to Logged-in User
	- Checkout Page Design
	- Assign the User to Cart Item
	- Modify Cart Counter & Cart View to Handle Logged-in Users
	- Variation Grouping for Logged-in Users Part1
	- Variation Grouping for Logged-in Users Part2
	- Fix Remove & Cart Decrement Functions
	- Dynamically Redirect the User to Next Page	
	
15. Orders & Order Number Generation
	- Order Flow Explained
	- Making Order Model, Order Product model and Payment Model
	- Place Order View and Generate Order Number Part 01
	- Place Order View and Generate Order Number Part 02
	- Review Order Page Setup
	- Review Order Payment Page

16. Payment Gateway Integration & Place Order
	- Create PayPal Business Account
	- PayPal Payment Gateway with Sandbox Account & Place Order
	- Send Transaction Details to Backend	
	
17. After Order Functionalities
	- Move Cart Items to Order Product Table
	- Set Variations to Ordered Products
	- Reduce Quantity of Sold Products and Clear the Cart
	- Send Order Received Email
	- Redirect the User to Order Completed Page
	- Generate Invoice on Order Completion
	- Push Code

18. Review and Rating System
	- Review & Rating Model
	- Making Rating Stars 01
	- Making Rating Stars Applying CSS 02
	- Store the Rating & Reviews
	
19. Two Factor Checks for Submitting Reviews (Login check & Product purchase check)
	- Check if the User has purchased the Product before submitting Review
	- Displaying Rating Stars
	
20. Rating Average & Review Count Calculation
	- Rating Average Calculation
	- Rating Average Stars & Review Counter
	- Anonymous User Error Fix
	- Push Code
	
21. My Account Functionalities
	- Dashboard Edits
	- My Orders
	- User Profile Model
	- Edit Profile Setup
	- Edit Profile Functionality
	- Automatically Create User Profile
	- Change Password
	- Order Detail Page
	- Fix Profile Picture in Dashboard
	
22. Product Gallery with Unlimited Images
	- Product Gallery Model with Image Preview
	- Product Gallery Implementation – Unlimited Product Images
	- Show Rating Stars on Homepage
	
23. Django Security Measures
	- Store Your Website’s Sensitive Information Securely
	- Secure your Admin panel & Record Hacking Attempts
	- Automatically logout after Inactivity
	
24. Deploying Application on AWS Elastic Beanstalk (EB)
	- AWS Elastic Beanstalk Deployment Introduction
	- Amazon AWS Account Creation
	- Deploy your Application on AWS Elastic Beanstalk (AWS EB)
	- AWS RDS Postgres Configuration
	- Postgres Installation and Load data from Sqlite3 to Postgres
	- AWS S3 Bucket for Static & Media Files Storage
	- Deploying the Application again for S3 Changes
	- Connect Custom Domain
	- Installing SSL Certificate on AWS Elastic Beanstalk
