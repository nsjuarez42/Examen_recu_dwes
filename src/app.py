from flask import Flask,render_template,request,flash,url_for,redirect
from forms.Register import RegisterForm
from forms.Login import LoginForm
from config import Development
from flaskext.mysql import MySQL
from db.ModelUser import ModelUser
from db.ModelProducts import ModelProducts
from entities.User import User


from flask_login import LoginManager,login_user,login_required,current_user,logout_user





app = Flask(__name__)

app.config.from_object(Development)

login_manager = LoginManager(app)


mysql = MySQL(app)

@login_manager.user_loader
def load(id):
    return ModelUser.get_by_id(mysql.get_db(),id)

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("user"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user_found = ModelUser.get_by_username(mysql.get_db(),username)
        if not user_found:
            return redirect(url_for("register"))
        if not User.check_password(user_found.password,password):
            flash("Invalid credentials")
            return render_template("login.html",form=LoginForm())
        
        login_user(user_found)
       # ModelUser.add_view(mysql.get_db(),user_found.username)
        ##add visit

        return redirect(url_for("user"))
    return render_template("login.html",form=LoginForm())

@app.route("/register",methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("user"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        fullname = request.form.get("fullname")
        print(username,password,fullname)

        if ModelUser.get_by_username(mysql.get_db(),username):
            return redirect(url_for("login"))
        try:
            db = mysql.get_db()
            cursor = db.cursor()
            hashed = User.hash_password(password)
            ModelUser.create_user(db,cursor,username,hashed,fullname)
            flash("User registered successfully")
        except Exception as e:
            flash("Error ocurred while registering")
            print(e)
    return render_template("register.html",form=RegisterForm())

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))



@app.route("/user",methods=["GET"])
@login_required
def user():
    return render_template("user.html",user=current_user)

@app.route("/store",methods=["GET","POST"])
@login_required
def store():
    products = ModelProducts.get_all(mysql.get_db())
    print(products)
    form = request.form.to_dict()
    if request.method == "POST":
        print(form.items())
        cart = [{"id":int(item[0]),"amount":int(item[1])} for item in form.items() if item[1] != "" and int(item[1]) > 0]
        to_buy = []
        for c in cart:
            product = [p for p in products if p.id == c["id"]][0]
            to_buy.append({"name":product.name,
                           "amount":c['amount'],
                           "price":c['amount']*product.price})
            
       
        return render_template("checkout.html",products=to_buy,total_amount=sum([p['amount'] for p in to_buy]),total_price=sum([p['price'] for p in to_buy]))
        
        
                

        
    elif request.method == "GET":
        return render_template("store.html",products=products)
    
    return render_template("store.html",products=products)
if __name__ == "__main__":
    app.run(debug=True)