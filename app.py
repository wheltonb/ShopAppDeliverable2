from flask import Flask, render_template, request, redirect, url_for, session, flash
from dao.productDAO import productDAO
from services.UserService import UserService

# imports are needed to drag elements of the project from custom DAO and Service modules as well as access pre-built flask libraries
app = Flask(__name__)

# secret key lets me create sessions to manage app-state
app.secret_key = 'ProjectSecretKey'

productDAO = productDAO()
userService = UserService()


# initializing an instance of productDAO and UserService allows app to access the functions stored in those classes


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
                return redirect(url_for('login'))
            else:
                return redirect(url_for('show_cart'))

    if session['session_user'] == 'Admin':  # checks for session_user type Admin and redirects to dashboard
        return redirect(url_for('admin_page'))

    # if page renders as GET creates an empty cart and renders all products for display
    session.setdefault('cart', [])
    products = productDAO.getAllProducts()  # accesses ProductDAO to grab all instances of the Product class
    cart = session.get('cart', [])
    cart_len = len(cart)  # length check of cart object for basket icon count
    return render_template('index.html', products=products, cart_len=cart_len)


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
                # conditional test where if users are signed in, retrieve data from page
                products = productDAO.getProductById(productID)
                productID = request.form['productID']
                productName = request.form['productName']
                price = request.form['price']
                quantity = request.form['quantity']
                cart = session['cart']
                for item in cart:  # needed to iterate through cart to ensure entries don't overwrite pre-existing
                    # cart item
                    if item['productID'] == productID:
                        item['quantity'] += quantity  # increments quantity if already in cart
                        break
                else:  # if item not in cart appends the product details as dictionary entries before redirecting to
                    # cart page
                    cart.append({'productID': productID,
                                 'productName': productName,
                                 'price': price,
                                 'quantity': quantity,
                                 'image_url': products.image_url,
                                 'description': products.description
                                 })
                session.modified = True
                return redirect(url_for('homepage'))

    products = productDAO.getProductById(productID)
    cart = session.get('cart', [])
    cart_len = len(cart)
    return render_template('product_details.html', products=products, cart_len=cart_len)


# login route to handle HTML form data and alter the User session
@app.route('/login', methods=['GET', 'POST'])
def login():
    # conditional check to allow page to handle  login-form POST
    if request.method == 'POST':
        # assigns email and password from form entry to variable for authentication
        email = request.form.get('emailField')
        password = request.form.get('passwordField')

        userToLogin = userService.verifyUser(email, password)  # uses the form submissions as arguments in User
        # Service authentication function

        if userToLogin:
            products = productDAO.getAllProducts()  # returns product list to pass to index for rendering on
            # successful login

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

    return render_template('admin.html')


# route to handle cart logic and routing
@app.route('/cart', methods=['GET', 'POST'])
def show_cart():
    if request.method == 'POST':
        if 'checkout' in request.form:  # on receiving POST from checkout button cart must be reset and users are brought to homepage
            session.pop('cart')
            session.modified = True
            flash("Order Placed",
                  category="success")  # wanted to integrate so display message but could not get working in time
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
        item_quant = int(item['quantity'])
        item_cost = int(item['price'])
        total_cost_per_item = item_cost * item_quant
        cart_cost += total_cost_per_item
    return render_template('cart.html', cart=cart, cart_len=cart_len, cart_cost=cart_cost, cart_quant=cart_quant)


if __name__ == '__main__':
    app.run()
