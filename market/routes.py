from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/health')
def health():
    return "OK", 200

@app.route('/market', methods=['GET', 'POST'])
@login_required #we won't render this if the user isn't logged in. To verify this, the URL needs to append ?next=...(page url) with the ...(page url) being the page that the user tried to access before logging in. The redirection will happen automatically and its defined in __init__.py
def market_page():

    purchase_item = PurchaseItemForm()
    sell_item = SellItemForm()

    # Essentially, we can directly wrap the functions of a route by specifying which actions belong to which req method
    #, In this example POST is made for the "buy" process that'll POST the item has been "bought" (assigned in the models.py
    # To a User, literally "self.owner = user.id" in models (Item class), self is p_item_object here.
    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()

        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! Now you own {p_item_object.name}", category='success')
            else:
                flash("Not enough money. Sorry!")

        #Sell logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"You've sold {s_item_object.name}", category='success')
            else:
                flash("Sorry, there was a problem while selling your item.")

        return redirect(url_for('market_page'))
    

    if request.method == 'GET':
        items = Item.query.filter_by(owner=None) ##No Owner defaults to NULL or "None"
        owned_items = Item.query.filter_by(owner=current_user.id) #Invoke the items that belong to the current_user id.
        return render_template('market.html', items=items, purchase_item=purchase_item, owned_items=owned_items, sell_item=sell_item)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm() #specify the method we're invoking
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully. You're now logged in as {user_to_create.username} ", category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are no errors (!) from the valid
        for err_msg in form.errors.values():
            flash(f'There was an error while creating the User:  {err_msg}', category='danger')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first() # We need to query here because we need to pull both 1) The User and 2) the hashed password. Note we're only checking if the user exists here, so we will only query the User object on its entirety and then we access the data.

        if attempted_user and attempted_user.check_password_correction(
            attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! Youre now logged in as { attempted_user.username } ', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password do not match. Please try again', category='danger')
        
    return render_template('login.html', form=form)

@app.route('/logout', methods=['POST'])
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'));

@app.route('/seed')
def seed_db():
    sample_items = [
        {
            "name": "Dream Dust",
            "price": 19,
            "barcode": "111111111111",
            "description": "Sleep-enhancing tincture made from skullcap, valerian, and passionflower.",
            "image": "/static/images/dream_dust.png"
        },
        {
            "name": "Brain Boost",
            "price": 25,
            "barcode": "222222222222",
            "description": "Focus-enhancing blend with lion’s mane, bacopa, and ginkgo.",
            "image": "/static/images/brain_boost.png"
        },
        {
            "name": "Glow Elixir",
            "price": 15,
            "barcode": "333333333333",
            "description": "Antioxidant-rich infusion for skin, liver, and gut.",
            "image": "/static/images/glow_elixir.png"
        },
        {
            "name": "Health Potion",
            "price": 30,
            "barcode": "444444444444",
            "description": "Classic healing brew: echinacea, elderberry, and rose hips.",
            "image": "/static/images/health_potion.png"
        },
        {
            "name": "Mana Potion",
            "price": 30,
            "barcode": "555555555555",
            "description": "Nervine energy tonic: rhodiola, maca, and reishi extract.",
            "image": "/static/images/mana_potion.png"
        }
    ]

    seeded = []
    for item_data in sample_items:
        existing_item = Item.query.filter_by(name=item_data['name']).first()
        if not existing_item:
            item = Item(**item_data)
            db.session.add(item)
            seeded.append(item_data['name'])

    db.session.commit()
    return jsonify({"seeded": seeded if seeded else "Already seeded!"})