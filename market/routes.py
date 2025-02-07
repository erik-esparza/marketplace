from market import app
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
@login_required #we won't render this if the user isn't logged in. To verify this, the URL needs to append ?next=...(page url) with the ...(page url) being the page that the user tried to access before logging in. The redirection will happen automatically and its defined in __init__.py
def market_page():
    items = Item.query.all()
    purchase_item = PurchaseItemForm()
    sell_item = SellItemForm()
    return render_template('market.html', items=items, purchase_item=purchase_item, sell_item=sell_item)

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

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'));