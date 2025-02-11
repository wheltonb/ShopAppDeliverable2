import base64
import requests
from models.Product import Product
from models.User import User
from flask import Flask, render_template, request, redirect, url_for, session, flash
from services.ProductService import ProductService
from services.UserService import UserService


# imports are needed to drag elements of the project from custom DAO and Service modules as well as access pre-built flask libraries
app = Flask(__name__)

# secret key lets me create sessions to manage app-state
app.secret_key = 'ProjectSecretKey'


# home route to serve as site homepage and allow for product viewing or login
@app.route('/', methods=['GET', 'POST'])
def homepage():
    if 'session_user' not in session:  # used to check for and create a session user so app can track sign-in state and user type
        session['session_user'] = 'Guest'  # defaults user state to guest

    if request.method == 'POST':  # checks any POST methods for if its a logout and reloads the page with session_user as Guest
        if 'logout' in request.form:
            session.pop('cart')
            session['session_user'] = 'Guest'
            session.modified = True  # probably the single most instrumental line, is reused multiple times in code to save any changes made to sessions to ensure that data persists (was used in add_product func to ensure append was saved and carried over to checkout
            return redirect(url_for('homepage'))

        if 'show_cart' in request.form:
            if session['session_user'] == 'Guest':
                #return redirect(url_for('login'))
                pass
            else:
                return redirect(url_for('show_cart'))

    if session['session_user'] == 'Admin':  # checks for session_user type Admin and redirects to dashboard
        return redirect(url_for('admin_page'))

    # if page renders as GET creates an empty cart and renders all products for display
    productService = ProductService()
    products = productService.get_all_products()
    for product in products:
        # If the product has an image BLOB, convert it to base64
        if product.image_blob:
            product.image = base64.b64encode(product.image_blob).decode('utf-8')
        else:
            product.image = None  # Handle case with no image
    session.setdefault('cart', [])
    cart = session.get('cart', [])
    cart_len = len(cart)  # length check of cart object for basket icon count
    return render_template('index.html', products=products, cart_len=cart_len)

@app.route('/categories/<string:product_type>', methods=['GET', 'POST'])
def product_types(product_type):
    if 'session_user' not in session:  # used to check for and create a session user so app can track sign-in state and user type
        session['session_user'] = 'Guest'  # defaults user state to guest

    if request.method == 'POST':  # checks any POST methods for if its a logout and reloads the page with session_user as Guest
        if 'logout' in request.form:
            session.pop('cart')
            session['session_user'] = 'Guest'
            session.modified = True  # probably the single most instrumental line, is reused multiple times in code to save any changes made to sessions to ensure that data persists (was used in add_product func to ensure append was saved and carried over to checkout
            return redirect(url_for('homepage'))

        if 'show_cart' in request.form:
            if session['session_user'] == 'Guest':
                #return redirect(url_for('login'))
                pass
            else:
                return redirect(url_for('show_cart'))

    # if page renders as GET creates an empty cart and renders all products for display
    productService = ProductService()
    products = productService.get_product_by_type(product_type)
    for product in products:
        # If the product has an image BLOB, convert it to base64
        if product.image_blob:
            product.image = base64.b64encode(product.image_blob).decode('utf-8')
        else:
            product.image = None  # Handle case with no image
    session.setdefault('cart', [])
    cart = session.get('cart', [])
    cart_len = len(cart)  # length check of cart object for basket icon count
    return render_template('index_by_type.html', products=products, cart_len=cart_len)


@app.route('/product/<int:productID>', methods=['GET', 'POST'])
def show_details(productID):
    # reusing logout logic
    if request.method == 'POST':
        if 'logout' in request.form:
            session.pop('cart')
            session['session_user'] = 'Guest'
            session.modified = True
            return redirect(url_for('homepage'))

        if 'show_cart' in request.form:
            if session['session_user'] == 'Guest':
                return redirect(url_for('login'))
            else:
                return redirect(url_for('show_cart'))

        # conditional test to see if the POST request is adding to cart
        if 'add_to_cart' in request.form:
            if session['session_user'] == 'Guest':  # prevents guests from checking out
                return redirect(url_for('login'))
            else:
                # instantiates productService and retrieves by ID
                productService = ProductService()
                product = productService.get_product_by_id(productID)
                productID = request.form['productID']
                productName = request.form['productName']
                price = request.form['price']
                quantity = request.form['quantity']
                cart = session['cart']

                for item in cart:
                    if item['productID'] == productID:
                        item['quantity'] += quantity  # increments quantity if already in cart
                        session.modified = True
                        return redirect(url_for('homepage'))

                else:
                    cart.append({'productID': productID,
                                 'productName': productName,
                                 'price': price,
                                 'quantity': quantity,
                                 'description': product.description
                                 })
                    session.modified = True

                return redirect(url_for('homepage'))

    # retrieve product details on page render
    productService = ProductService()
    product = productService.get_product_by_id(productID)
    # Convert image BLOB to regular image
    if product.image_blob:
        product.image = base64.b64encode(product.image_blob).decode('utf-8')
    else:
        product.image = None

    # retrieve cart details from the session
    cart = session.get('cart', [])
    cart_len = len(cart)

    return render_template('product_details.html', product=product, cart_len=cart_len)  # Pass single product to template



# login route to handle HTML form data and alter the User session
@app.route('/login', methods=['GET', 'POST'])
def login():
    # conditional check to allow page to handle  login-form POST
    if request.method == 'POST':
        # assigns email and password from form entry to variable for authentication
        email = request.form.get('emailField')
        password = request.form.get('passwordField')
        userService = UserService()
        userToLogin = userService.verify_user(email, password)  # uses the form submissions as arguments in User
        # Service authentication function

        if userToLogin:
            if userToLogin.isManager:  # checks logged-in User against objects isManager status and sets session
                # accordingly to ensure redirect to admin dashboard
                session['session_user'] = "Admin"  # changes session state to reflect user type
                session.modified = True
                return redirect(url_for("admin_page"))

            else:  # states that if login successful and isAdmin = False session_user is set to userEmail and returns
                # to homepage as logged in ( used in base.html to generate conditional logout button)
                session['session_user'] = userToLogin.userEmail  # changes session state and sets user as
                cart = session.get('cart', [])
                cart_len = len(cart)
                session.modified = True
                return redirect(url_for("homepage"))  # passes product to index to allow product spread to render

        else:  # on login failure re-render the login page
            return render_template("login.html")

    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    userService = UserService()
    if request.method == 'POST':
        # same issue as in products, for some reason have to initialise directly a model object so I have to manually instansiate an ID
        count = len(userService.get_all_users())
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form['emailField']
        password = request.form['passwordField']
        confirm_password = request.form['confirmPasswordField']
        isManager = False
        #
        if password != confirm_password:
           flash("Passwords don't match", "danger")
           return render_template("register.html")
        # conditional to see if that email is already registered to an account
        if userService.get_user_by_email(email):
            flash("Email already registered", "danger")
            return render_template("register.html")

        args = {
            'userID': count,
            'firstName': firstName,
            'lastName': lastName,
            'userEmail': email,
            'userPassword': password,
            'isManager': isManager
        }
        user = User(**args)
        userService.create_user(user)
        return redirect(url_for('login'))

    return render_template('register.html')


# admin route to interact with manager tools / display infographics
@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    # reuse of the logout conditional check and redirect on POST
    if request.method == 'POST':
        if 'logout' in request.form:
            session.pop('cart')
            session['session_user'] = 'Guest'
            session.modified = True
            return redirect(url_for('homepage'))

        if 'product_manager' in request.form:
            return redirect(url_for('product_manager_page'))


        if 'user_manager' in request.form:
            return redirect(url_for('user_manager_page'))

    return render_template('admin.html')


# route to handle cart logic and routing
@app.route('/cart', methods=['GET', 'POST'])
def show_cart():
    if request.method == 'POST':
        if 'checkout' in request.form:  # on receiving POST from checkout button cart must be reset and users are brought to homepage
            session.pop('cart')
            session.modified = True
            return redirect(url_for('homepage'))

        # conditional blocks detecting if the increment cart item operations are triggered by button press both conditions
        # compare the targeted product on cart page to cart contents by ID and then on match they convert quantity
        # to int for calculations quantity is either incremented or decremented by 1 each press and page refreshed,
        # if quant = 0 the product is removed from session
        if 'step_down' in request.form:
            productID = request.form['productID']
            for product in session['cart']:
                if product['productID'] == productID:
                    product['quantity'] = int(product['quantity'])
                    product['quantity'] -= 1
                    if product['quantity'] == 0:
                        session['cart'].remove(product)
                    session.modified = True
                    return redirect(url_for('show_cart'))


        elif 'step_up' in request.form:
            productID = request.form['productID']
            for product in session['cart']:
                if product['productID'] == productID:
                    product['quantity'] = int(product['quantity'])
                    product['quantity'] += 1
                    session.modified = True
                    return redirect(url_for('show_cart'))

    productService = ProductService()
    # creates variable using content of session cart
    cart = session.get('cart', [])
    cart_len = len(cart)
    # init cart_quant variable for total items in basket
    cart_quant = 0
    # loop through cart and for all products += the quantity to quant for total basket size
    for item in cart:
        cart_quant += int(item['quantity'])
    # calculation to obtain total basket cost
    cart_cost = 0

    for item in cart:
        # need to retrieve the image blob from DB based on cart product ID's
        productID = item['productID']
        product = productService.get_product_by_id(productID)  # Retrieve the full product details
    # convert
        if product and product.image_blob:
            item['image'] = base64.b64encode(product.image_blob).decode('utf-8')  # Convert image_blob to base64 string
        else:
            item['image'] = None
        item_quant = int(item['quantity'])
        item_cost = float(item['price'])
        total_cost_per_item = item_cost * item_quant
        cart_cost += total_cost_per_item
    return render_template('cart.html', cart=cart, cart_len=cart_len, cart_cost=cart_cost, cart_quant=cart_quant)



@app.route('/manage_products', methods=['GET', 'POST'])
def product_management():
    if request.method == 'POST':
        if 'create_redirect' in request.form:
            return url_for('product_creation')
    else:
        productService = ProductService()
        products = productService.get_all_products()
        for product in products:
            # If the product has an image BLOB, convert it to base64
            if product.image_blob:
                product.image = base64.b64encode(product.image_blob).decode('utf-8')
            else:
                product.image = None  # Handle case with no image
        return render_template('product_management.html', products=products)



# handles updates to individual products
@app.route('/manage_product/<int:productID>', methods=['GET', 'POST'])
def manage_product(productID):
    # instantiates productServices
    productService = ProductService()
    product = productService.get_product_by_id(productID)

    if request.method == 'POST': # reused logout logic from previous iteration
        if 'logout' in request.form:
            session.pop('cart', None)
            session['session_user'] = 'Guest'
            session.modified = True
            return redirect(url_for('homepage'))

        if 'delete' in request.form:
            productService = ProductService()
            productService.delete_product(productID)
            return redirect(url_for('product_management'))

        if 'save_changes' in request.form:
            if product.type == 'poster':
                product.productName = request.form.get('productName')
                product.price = request.form.get('price')
                product.description = request.form.get('description')
                product.image = product.image_blob
                product.character = request.form.get('character')
                product.hasColour = 'hasColour' in request.form
                product.dimensions = request.form.get('dimensions')
                product.materials = None
                product.scale = None
                product.isLimited = None
                product.gender = None
                product.moveable = None
                product.isMirror = None
            # sets values for hidden fields and visible fields if form = replica
            elif product.type == 'replica':
                product.productName = request.form.get('productName')
                product.price = request.form.get('price')
                product.description = request.form.get('description')
                product.image = product.image_blob
                product.character = None
                product.hasColour = False
                product.dimensions = None
                product.materials = request.form.get('materials')
                product.scale = request.form.get('scale')
                product.isLimited = request.form.get('isLimited')
                product.gender = None
                product.moveable = None
                product.isMirror = None


            # sets values for hidden fields and visible fields if form = figurine
            elif product.type == 'figurine':
                product.productName = request.form.get('productName')
                product.price = request.form.get('price')
                product.description = request.form.get('description')
                product.image = product.image_blob
                product.character = None
                product.hasColour = None
                product.dimensions = None
                product.materials = None
                product.scale = None
                product.isLimited = None
                product.gender = request.form.get('gender')
                product.moveable = 'moveable' in request.form
                product.isMirror = 'isMirror' in request.form

            productservice = ProductService()
            productservice.update_product(product)
        else:
            pass
        # Handle the product type change from the radio buttons since I don't know Javascript well enough to use for dynamic response
        product_type = request.form.get('productType')
        if product_type:
            product.type = product_type # on radio button form submit, modifies product type to allow for form updating
            # sets values for hidden fields and visible fields if form = poster
            if product_type == 'poster':
                product.character = request.form.get('character')
                product.hasColour = 'hasColour' in request.form
                product.dimensions = request.form.get('dimensions')

            # sets values for hidden fields and visible fields if form = replica
            elif product_type == 'replica':
                product.materials = request.form.get('materials')
                product.scale = request.form.get('scale')
                product.isLimited = request.form.get('isLimited')
                # sets values for hidden fields and visible fields if form = figurine
            elif product_type == 'figurine':
                product.gender = request.form.get('gender')
                product.moveable = 'moveable' in request.form
                product.isMirror = 'isMirror' in request.form

            # If there's an image, handle image conversion
            if product.image_blob:
                product.image = base64.b64encode(product.image_blob).decode('utf-8')
            else:
                product.image = None
            productService.update_product(product)
            return render_template('manage_product.html', product=product)

    if product.image_blob:
        product.image = base64.b64encode(product.image_blob).decode('utf-8')
    else:
        product.image = None
    return render_template('manage_product.html', product=product)

# route to handle product creation
@app.route('/create_product', methods=['GET', 'POST'])
def product_creation():
    #instansiate product service module
    productService = ProductService()
    # for some reason I cant create without manually assigning an ID so I just calculate what auto-increment should be??
    count = len(productService.get_all_products())
    if request.method == 'POST':
        if "create_product" in request.form:
            # turns opened image into binary and stores to blob variable
            image = request.files.get('image')
            image_blob = image.read()
            productID = count + 1
            # Retrieve product attributes from the form and set to none based on type
            if request.form.get('productType') == 'poster':
                product_data = {
                "productID": productID,
                "productName": request.form.get('productName'),
                "price": request.form.get('price'),
                "type": request.form.get('productType'),
                "gender": None,
                "movable": None,
                "isMirror": None,
                "character": request.form.get('character'),
                "hasColour": 'hasColour' in request.form,
                "dimensions": request.form.get('dimensions'),
                "material": None,
                "scale": None,
                "isLimited": None,
                "description": request.form.get('description'),
                "image_blob": image_blob}
                product = Product(**product_data)
                productService.create_product(product)

            if request.form.get('productType') == 'figurine':
                product_data = {
                "productID": productID,
                "productName": request.form.get('productName'),
                "price": request.form.get('price'),
                "type": request.form.get('productType'),
                "gender": request.form.get('gender'),
                "movable": 'movable' in request.form,
                "isMirror": 'isMirror' in request.form,
                "character": None,
                "hasColour": None,
                "dimensions": None,
                "material": None,
                "scale": None,
                "isLimited": None,
                "description": request.form.get('description'),
                "image_blob": image_blob}
                product = Product(**product_data)
                productService.create_product(product)

            if request.form.get('productType') == 'replica':
                product_data = {
                    "productID": productID,
                    "productName": request.form.get('productName'),
                    "price": request.form.get('price'),
                    "type": request.form.get('productType'),
                    "gender": request.form.get('gender'),
                    "movable": None,
                    "isMirror": None,
                    "character": None,
                    "hasColour": None,
                    "dimensions": None,
                    "material": request.form.get('material'),
                    "scale": request.form.get('scale'),
                    "isLimited": 'isLimited' in request.form,
                    "description": request.form.get('description'),
                    "image_blob": image_blob}
                product = Product(**product_data)
                productService.create_product(product)
            return redirect(url_for('product_management'))
        else:
            flash("Error creating product", "danger")
    return render_template("create_product.html")


@app.route('/manage_users', methods=['GET', 'POST'])
def user_management():
    userService = UserService()
    users = userService.get_all_users()
    return render_template('user_management.html', users=users)


@app.route('/manage_user/<int:userID>', methods=['GET', 'POST'])
def manage_user(userID):
    userService = UserService()
    user = userService.get_user_by_id(userID)
    if request.method == 'POST': # reused logout logic from previous iteration
        if 'logout' in request.form:
            session.pop('cart', None)
            session['session_user'] = 'Guest'
            session.modified = True
            return redirect(url_for('homepage'))

        if 'save_changes' in request.form:
            user.firstName = request.form.get('firstName')
            user.lastName = request.form.get('lastName')
            user.userEmail = request.form.get('userEmail')
            user.userPassword= request.form.get('userPassword')
            user.isManager = request.form.get('isManager')
            userService = UserService()
            userService.update_user(user)
            return redirect(url_for('user_management'))

        if 'delete' in request.form:
            userService.delete_user(userID)
            return redirect(url_for('user_management'))

    else:
        return render_template('manage_user.html', user=user)






@app.route('/get_api', methods=['GET'])
def get_api():
    response = requests.get('https://catfact.ninja/fact')
    if response.status_code == 200:
        data = response.json()
        return render_template('api_page.html', fact=data['fact'])
    else:
        flash("Error retrieving a daily cat fact", "danger")
        return render_template('api_page.html', fact=None)
if __name__ == '__main__':
    app.run()

