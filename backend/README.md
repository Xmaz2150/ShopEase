# ShopEase API

Welcome consumer!!

## Table of Contents

- [Installation & Setup](#installation-Setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)

## Installation & Setup

1. Install the dependencies:
    ```sh
    $ pip install -r requirements.txt
    ```

2. Install & Start PostgresSQL:
      ```
      $ sudo apt update && sudo apt install postgresql postgresql-contrib -y && sudo systemctl start postgresql.service
      ```
3. Initialize Database:

     i. Create DB (Only if Starting from scratch):
      ```sh
      $ psql -U postgres -f create_db.sql
      ```
      ii. **OR** Load from dump to have som data beforehand:
      ```
      $ pg_restore -U postgres -d shopease shopease.dump
      ```



## Usage

1. Run application
   ```sh
    flask run
    ```

2. The server will run on `http://localhost:5000`.



## API Endpoints

### User Registration

- **Endpoint:** `/register`
- **Method:** `POST`
- **Description:** Registers new user. Should contain special flag(su) to register admin(s)
- **Request:**
    ```sh
    http POST :5000/register \
	    username=username \
	    email=username \
	    password=password
    ```

### User Login

- **Endpoint:** `/login`
- **Method:** `POST`
- **Description:** Logs user in and responds with a JWT
- **Request:**
     ```sh
    http POST :5000/login \
	    username=username \
	    password=password
    ```

### User Logout

- **Endpoint:** `/logout`
- **Method:** `POST`
- **Description:** Logs user out.
- **Request:**
     ```sh
    # coming soon
    ```

### User Profile

- **Endpoint:** `/profile`
- **Method:** `GET`
- **Description:** Retrieves user's profile.
- **Request:**
    ```sh
     http POST :5000/profile \ 
	    Authorization:"Bearer $JWT"
    ```

### Products

#### New
- **Endpoint:** `/shop/product`
- **Method:** `POST`
- **Description:** Uploads new product.
- **Request:**
    ```sh
    http -f POST :5000/shop/product \
    	Authorization:"Bearer $JWT" \
    	Content-Type:multipart/form-data \
    	name=name \
    	description=description \
    	price=price \
    	brand=brand \
    	stock_quantity=qty \
    	category=category \
    	file@product_image.png
    ```

#### Some Or All
- **Endpoint:** `/shop/products`
- **Method:** `GET`
- **Description:** Retrieves products by category all if not provided(ALL must be specified).
- **Request:**
    ```sh
    http POST :5000/shop/product 
	    Authorization:"Bearer $JWT" \
	    Content-Type:application/json \
	    category=category
    ```


### Cart

#### Get
- **Endpoint:** `/shop/cart`
- **Method:** `GET`
- **Description:** Gets users cart.
- **Request:**
    ```sh

    http POST :5000/shop/cart \
    	Authorization:"Bearer $JWT"
    ```

#### Add
- **Endpoint:** `/shop/cart/add`
- **Method:** `POST`
- **Description:** Adds product to users cart based on it's quantity.
- **Request:**
    ```sh
      http POST :5000/shop/cart/add \
  	    Authorization:"Bearer $JWT" \
  	    Content-Type:application/json \
  	    product_id=product_id
      	quantity=qty
    ```

### Remove
- **Endpoint:** `/shop/cart/remove`
- **Method:** `POST`
- **Description:** Removes product from users cart based on it's quantity.
- **Request:**
    ```sh
      http POST :5000/shop/cart/remove \
  	    Authorization:"Bearer $JWT" \
  	    Content-Type:application/json \
  	    product_id=product_id
      	quantity=qty
    ```

### Purchase

#### Checkout
- **Endpoint:** `/shop/checkout`
- **Method:** `GET`
- **Description:** Completes purchase.
- **Request:**
    ```sh
    http GET :5000/shop/checkout \
    	Authorization:"Bearer $JWT"
    ```

#### History
- **Endpoint:** `/shop/orderhistory`
- **Method:** `GET`
- **Description:** Shows users purchase history.
- **Request:**
    ```sh
    http GET :5000/shop/orderhistory \
    	Authorization:"Bearer $JWT"
    ```

## Image Server

### Get
- **Endpoint:** `/SE/img/<filename>`
- **Method:** `GET`
- **Description:** Gets image.
- **Request:**
    ```sh
    http GET :5000/SE/img/<filename> 
    ```
