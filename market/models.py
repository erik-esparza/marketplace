from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin): #MixIn provides us with various pre-defined methods we can use later
    __tablename__ = 'users'  # ✅ avoid reserved keyword, as we're using PostgreSQL
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=8900)

    #Attention! We're effectively linking the Users with Item (single instance of the Items class). If we weren't using db.relationship we'd have to exchange IDs with something called "Foreign Key."
    #Instead, we use relationship to be able to assign a One-to-many relationship, this means a user can have many items. In turn, 'backref' extends this
    #Ability to be able to "backtrack" the user that owns an item -through the item itself. E.g item.user = User 1, instead of only being able to user.item = Item 1, Item 2, Item 3, etc...
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property #Executing functions (these are called "Decorators")
    def prettier_budget(self): #defining the function to add coma after 4 digits in the budget
        if len(str(self.budget)) >= 4: #len() for length, str() to stringify
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$' #Essentially, we're splicing all contents before the index -3 (:-3), add a coma, and then add all contents after index -3 (-3:)
        else:
            return "{self.budget}$" # Returning the budget as-is

    @property #password could be called something else here, it may be too self referencing. It works completely fine this way, so I'll leave it as is.
    def password(self):
        return self.password
    
    @password.setter #'self' simply states that we're working within the User class, it's a sort of "hook"
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8') #generating the hashed password

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password) #We are skipping the IF here - simply because this function will check the hash, if correct and the password matches the hash of the encrypted password, it will return TRUE, if not, FALSE. as such, IF isn't needed in a Boolean function as it will just be able to say "Yes" or "No". :)
    
    #Checking if the user has more or equal budget in order to buy something
    def can_purchase(self, item_obj) :
        return self.budget >= item_obj.price
    
    #Checking a user effectively owns an object before buying - note that we simply use a return true (boolean statement)
    # Basically if this ite (item_obj) exists within User.items (Self.items)
    def can_sell(self, item_obj):
        return item_obj in self.items

#Class is a template, a platonic idea with predetermined fields
class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    image = db.Column(db.String(length=512), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey('users.id')) #Note! we've updated 'user' to users. This is explained in line 10, but note how we were even writing 'user' although the original note is 'User' — a testament of PGSQL issues with capitalization.

#attention! __repr__ provides a quick, human-readable way to identify the instance when you print it, log it, or inspect it. Basically, it's giving a bit of
#syntax to the item when its called from the console, logged somewhere or use the repr() or print() method in the console.
    def __repr__(self): #__Repr__ = [The syntax is:] ........ (self) = [The instance (all of them) of item] .......
        return f'Item {self.name}' #return a complex string, self (the instance of item) . name (the name property.) e.g of the output: 'Item Keyboard'

    #Here, we can pass user. This means: current_user in routes (through Flask login_form magic) is passed as the "user".
    #Effectively self refers to this current object and user is the parameter we brought from routes.
    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()