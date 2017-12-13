from flask import Flask, redirect, request, url_for, render_template
from flask_login import login_required, login_user, LoginManager, logout_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from firebase import firebase
from datetime import datetime

app = Flask(__name__)
app.config.from_object(__name__) # consume the configuration above

#Firebase

firebase = \
    firebase.FirebaseApplication('https://mynotawesomeproject-81927.firebaseio.com/', None)

#Flask_Login

app.secret_key = "something only you know"
login_manager = LoginManager()
login_manager.init_app(app)

#Python Classes

class User(UserMixin):

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def get_id(self):
        return self.username

# all_users = {
#     "admin": User("admin", generate_password_hash("secret")),
#     "bob": User("bob", generate_password_hash("less-secret")),
#     "caroline": User("caroline", generate_password_hash("completely-secret")),
#     }

all_users = { }

@login_manager.user_loader
def load_user(user_id):
    return all_users.get(user_id)

#Routes to webpages:

@app.route('/E-Scooter')
def EScooter():
    return render_template("MainR.html")

@app.route('/signup')
def signup():
    return render_template("login.html")

@app.route('/feedback')
def feedback():
    return render_template("feedback.html")

@app.route("/confirm")
def confirm():
    return render_template("confirm.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    fire()
    if request.method == "GET":
        return render_template("reallogin.html", error=False)

    username = request.form["username"]
    if username not in all_users:
        return render_template("reallogin.html", error=True)
    user = all_users[username]

    if not user.check_password(request.form["pwd"]):
        return render_template("reallogin.html", error=True)

    login_user(user)
    return redirect(url_for('profile'))

def fire():
    result = firebase.get('/userInformations', None)
    for i in result:
        user = result[i]
        name = user.get('name')
        password = user.get('password')
        all_users[name] = User(name, generate_password_hash(password))
        print("debug")
# decorator which tells flask what url triggers this fn
@app.route('/messages')
def messages():
  result = firebase.get('/messages', None)
  return render_template('list.html', messages=result, timestamp=datetime.now())

@app.route('/submit_message', methods=['POST'])
def submit_message():
  message = {
    'body': request.form['message'],
    'who': request.form['who']
  }
  firebase.post('/messages', message)
  return redirect(url_for('messages'))

#for user to get the login informations
@app.route("/profile")
def profile():
    gettingInfo()
    result = firebase.get('/userInformations', None)
    return render_template('profile.html', stats=result)

def gettingInfo():
    print("FROM GETTING INFO")
    for listofUsers in all_users:
        current_user_pw = all_users[listofUsers].password_hash
        print(listofUsers)
        print(current_user_pw)
        # check = listofUsers.username
        # print(check)

@app.route("/submit_informations", methods=["POST"])
def submit_informations():
    realInformations = {
        "password" : request.form["userPassword"],
        "name" : request.form["userName"],
        "email" : request.form["userEmail"],
        "cardNumber" : request.form["cardNumber"]
    }
    firebase.post("/userInformations", realInformations)
    return redirect(url_for("confirm"))

if __name__ == '__main__':
    app.run(debug=True)
