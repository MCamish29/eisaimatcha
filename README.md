# Eisai Matcha
## Elevate your senses with matcha.

At Eisai Matcha, our business model is all about bringing premium, ceremonial-grade matcha from Japan straight to your doorstep. We partner with trusted farms to deliver fresh, vibrant matcha with authentic flavor. By keeping things simple and direct, we’re able to focus on what matters most—quality you can taste and a shopping experience that feels effortless. Alongside our matcha, we also offer beautifully crafted kits and equipment to help you prepare it the way it’s meant to be enjoyed. Whether matcha is part of your daily ritual or a moment of calm in your week, we’re here to make it easy and enjoyable to get the good stuff, anytime you want it.

![Site Preview](static/images/eisaimatcha_site.gif)

[Link to site](https://eisai-matcha-05ff09384237.herokuapp.com/)<br>
[Link to repository](https://github.com/MCamish29/eisaimatcha.git)<br><br>
_To open links in a new tab, hold CTRL + Click_

# Table of Contents

- [Wireframe](#wireframe)
- [Design](#design)
- [Features](#features)
- [Installation](#installation)
- [Database](#database)
- [Testing](#testing)
- [Validation](#validation)
- [Deployment](#deployment)
- [Technologies Used](#technologies-used)
- [Acknowledgments](#acknowledgments)


# WireFrame

#### Home page
![Homepage](static/images/eisai_WF_index.png)

#### Products page
![Productspage](static/images/eisai_WF_products.png)

#### Add product page
![Addproductpage](static/images/eisai_WF_add.png)

#### Edit product page
![Editproductpage](static/images/eisai_WF_edit.png)

#### Bag page
![Bagpage](static/images/eisai_WF_bag.png)

#### Checkout page
![Checkoutpage](static/images/eisai_WF_checkout.png)

# Design

The design of Eisai Matcha reflects the clean, calm, and minimalist essence of Japanese tradition. A grayscale color palette was intentionally chosen to convey sophistication and tranquility, allowing the vibrant colors of the product to stand out on screen.

The name Eisai Matcha honors the Japanese Buddhist monk Eisai, who is credited with introducing matcha to Japan in 1191. After returning from a study trip to China with tea seeds, he advocated for their cultivation and consumption. His efforts laid the foundation for the development of matcha as we know it today.

## Features
### User Experience
The website provides a smooth and intuitive experience for customers. Users can easily navigate through various categories, select their desired products, add items to their shopping bag, and complete a straightforward checkout process. After placing an order, customers receive an order confirmation.

### Admin Functionality
Admins enjoy the same user-friendly navigation with added functionality. They can:

- Add new products directly from the front end
- Edit existing product details
- Delete products from the site

This allows for efficient, real-time content management without needing to access a backend dashboard.

### User Accounts
All users—whether customers or admins—can log in to their accounts for a personalized experience and access to relevant features.

- Homepage with navigation.
![Home](static/images/index.jpg)
_A home page to welcome customers with easy navigation:_<br>
[Home page](https://github.com/users/MCamish29/projects/6/views/1?pane=issue&itemId=105767890&issue=MCamish29%7Ceisaimatcha%7C4)


- Products page.
![Products](static/images/products.jpg)
_A products page to showcase what is available for purchase:_<br>
[Products page](https://github.com/users/MCamish29/projects/6/views/1?pane=issue&itemId=105767890&issue=MCamish29%7Ceisaimatcha%7C4)

- Bag page.
![Bag](static/images/bag.png)
_A bag page to showcase what the visitor is going to purchase or make amendments to:_<br>
[Bag page](https://github.com/users/MCamish29/projects/6/views/1?pane=issue&itemId=105767952&issue=MCamish29%7Ceisaimatcha%7C5)

- Checkout page.
![Checkout](static/images/checkout.png)
_A checkout page to allow the visitor to complete their transaction:_<br>
[Checkout page](https://github.com/users/MCamish29/projects/6/views/1?pane=issue&itemId=105767952&issue=MCamish29%7Ceisaimatcha%7C5)

- Admin front end products page.
![Admin](static/images/admin_edit.jpg)
![Admin](static/images/admin_edit_p2.jpg)
_A page to edit products for the admin of site:_<br>
[Admin edit page](https://github.com/users/MCamish29/projects/6/views/1?pane=issue&itemId=105768168&issue=MCamish29%7Ceisaimatcha%7C9)
![Admin](static/images/admin_edit.jpg)
_A delete button on products for the admin of site:_<br>
[Admin delete page](https://github.com/users/MCamish29/projects/6/views/1?pane=issue&itemId=105768217&issue=MCamish29%7Ceisaimatcha%7C10)

- Django admin page.
![Admin](static/images/admin.png)


- Facebook social page
![Facebook page](static/images/eisai_FB.png)

## Future enhancements
The site allows for future enhancements on the customer and admin side. 

Admin:
- Implementing partial forms throughout the site will enable controlled access to specific URLs for visitors.
- If the business expands beyond tea, kits, and equipment, refining the current models can help streamline and improve the back-end experience.
- As the number of products and pages grows, introducing a front-end admin dashboard would enhance efficiency and make content management more intuitive.

Customer:
- Like most e-commerce platforms, providing access to customer terms and conditions and FAQs offers a quick source of information, improving the overall user experience.
- A wishlist feature would be a valuable future enhancement, as it indicates customer interest and supports future purchasing decisions based on user engagement data.
- Adding a ratings and reviews section would help build trust with potential customers and support confident purchasing decisions.
- Personalized product recommendations tailored to individual users can significantly improve user experience and increase conversion rates.


<br>

# Installation

## Clone the Repository

### 1. Clone the repository
Clone the GitHub repository to your local machine : [Link to repository](https://github.com/MCamish29/eisaimatcha.git)

### 2. Install dependencies
pip install -r requirements.txt

### 3. Apply migrations
python manage.py migrate

### 4. Run server
python manage.py runserver

## Forking

To make changes or contribute, fork the repository to your GitHub account by clicking the "Fork" button on the repository page : [Link to repository](https://github.com/MCamish29/eisaimatcha.git)

### Prerequisites

Make sure you have the following installed:

- Django==3.2.25
- django-allauth==0.50.0
- django-countries==7.2.1
- django-crispy-forms==1.14.0
- django-storages==1.14.6
- gunicorn==23.0.0
- pillow==10.3.0
- psycopg2==2.9.10
- boto3==1.37.28


You can install them via `pip3`<br>
Packages must be added to requirements.txt `pip3 freeze --local > requirements.txt`

## Deployment


1. Log in to Heroku or create account
2. Click the **new** button on the top right to display drop down
3. Select **create new app**
4. Enter app name - *this must be a unique name*
5. Choose relevant region
6. Click **create app**
7. On the application dashboard select **settings**
8. Scroll down to *Config Vars*
9. Click on **Reveal_Config vars**
10. Enter **DATABASE_URL**
11. Click add
12. Enter **Cloudinary API**
13. Click add
14. Enter **Secret Key**
15. Click add
16. Select **deploy** at the top of the application dashboard
17. Select **GitHub** as deployment method
18. Search for repository name and click **connect**
19. Scroll down and select either **Enable Automatic Deploys** or **Deploy Branch** for manual deployment.
20. This will then run the process to deploy the application
21. Click on **View** once successfully deployed

# Database

## Entity-Relationship Diagram (ERD)

![ERD](static/images/Eisai_Matcha_ERD.jpeg)



<br>

# Testing 




# Validation

### W3C

All HTML pages were passed through [W3C HTML Validator](https://validator.w3.org/) to ensure it met required standards. The HTML pages were all successful when passing the code through from page source.

All CSS pages were passed through [W3C CSS Validation](https://jigsaw.w3.org/css-validator/) successfully.

### PEP8

All Python files were passed through [Code Institute PEP8 Linter](https://pep8ci.herokuapp.com/#) to ensure it met required standards. The only warnings given related to the settings.py file this was due to 4 lines in AUTH_PASSWORD_VALIDATORS being greater than the desired amount of characters, this code was installed by Django on setup.

### JSHint

The Javascript file was passed [JSHint](https://jshint.com/) successfully.

## Bugs

Bugs were found during development of the site and resolved which can be seen on the [Kanban workflow](https://github.com/users/MCamish29/projects/6).




# Technologies Used

* **VSCode** was the code editor used for the project
* **Django** was the framework used throughout the project
* **Python, HTML, CSS, Javascript** was the language used throughout the project
* **Heroku** was used to deploy the application
* **Git** was used to commit code
* **GitHub** was used to store the repo
* **Code Institute Python Linter** was used for python validation
* **W3C** was used for HTML and CSS validation
* **JSHint** was used for Javascript validation
* **AWS** was used to store media and static files
* **Google Fonts** was used for styling
* **Font Awesome** was used for icons across the site

# Acknowledgments

* Thank you to Code Institute for their comprehensive guides and support.
* A big thank you to my Code Institute mentor Graeme Taylor for all his guidance, support and endless counts of knowledge.
* All images were taken from free stock photo website [Pexels](https://www.pexels.com/)