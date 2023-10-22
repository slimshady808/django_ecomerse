# GadgetGallery: Your Online Gadget Store



GadgetGallery is an educational Django project that simulates an e-commerce website for electronic gadgets, including neckbands, earbuds, smartwatches, and more. It offers a range of essential functionalities, such as product listing, adding items to the cart, secure checkout, and online payments through PayPal. Users can also take advantage of search, sorting, and filtering options to find the gadgets they desire easily.

## Table of Contents
- [Demo](#demo)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [ScreenShots](#ScreenShots)


## Demo

Check out the live demo of GadgetGallery at [gadgetgallery](https://gadgetgallery.online/).

## Features

- **Product Listing:** Browse and explore a wide range of electronic gadgets with detailed product information and images.

- **Add to Cart:** Select products and add them to your shopping cart for later purchase.

- **Secure Checkout:** Go through a hassle-free checkout process, providing your delivery information and payment details.

- **Online Payments:** Make secure payments using PayPal for your orders.

- **Search, Sort, and Filter:** Find products efficiently with search functionality and sorting and filtering options.

## Installation

Before you begin, ensure you have the following prerequisites:

-  Make sure you have Python installed on your  system. You can download and install Python from the official website: https://www.python.org/

- Install Postgres on your system. You can    download and install Postgres from the official website: https://www.postgresql.org/



To run GadgetGallery on your local machine, follow these steps:

1. Clone this repository:

git clone 
```
https://github.com/slimshady808/django_ecomerse.git
```
2. Create a virtual environment:
```
python -m venv venv
```

3. Activate the virtual environment:
- On Linux/macOS:
  ```
  source venv/bin/activate
  ```
- On Windows:
  ```
  venv\Scripts\activate
  ```

4. Install dependencies:
```
pip install -r requirements.txt
```

5. Configure your environment variables


6. Apply database migrations:
```
python manage.py migrate
```

7. Run the development server:
```
python manage.py runserver

```
8. Access the project in your web browser at [http://localhost:8000/](http://localhost:8000/).

## Usage

1. Create an account or log in.
2. Browse the wide selection of electronic gadgets.
3. Add your desired products to your cart.
4. Proceed to checkout, providing your delivery information and selecting PayPal as your payment method.
5. Complete the payment process and receive an order confirmation.

That's it! You're all set to run the ecomerse website with Django and Postgres. Happy learning..  

## ScreenShots


![Homepage](screenshots/home.jpg)


![Homepage](screenshots/product.jpg)


![Homepage](screenshots/cart.jpg)