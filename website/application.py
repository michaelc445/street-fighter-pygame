
from flask import Flask, render_template , request , make_response , session , redirect, url_for ,g
from database import get_db, close_db
from forms import  RegistrationForm ,LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session

application = app = Flask(__name__)
application.config["SECRET_KEY"] =  "this-is-my-secret-key"
application.config["SESSION_PERMANENT"] = False
application.config["SESSION_TYPE"] = "filesystem"
Session(app)



#####################################################################################################
#####################################################################################################
#####################################################################################################


@app.teardown_appcontext
def close_db_at_end_of_request(e=None):
    close_db(e)

#####################################################################################################
#####################################################################################################
#####################################################################################################

        # these change the login link in the nav bar dependent on wether or not the user
        # is logged in

@app.route("/login_status")
def login_status():
    if "user_id" in session:
        return redirect( url_for("log_out") )
    else: 
        return redirect( url_for("login") )

def log_status():

    if "user_id" in session:
        status ="Logout"
        return status
    else: 
        status="Login"
        return status


#####################################################################################################
#####################################################################################################
#####################################################################################################

@app.route("/")
def index():
    status = log_status()
    return render_template("index.html",status=status)



#####################################################################################################
#####################################################################################################
#####################################################################################################
@app.route("/game", methods=["GET","POST"])
def game():
    status = log_status()
    return render_template("game.html",status=status)

#####################################################################################################
#####################################################################################################
#####################################################################################################



#####################################################################################################
#####################################################################################################
#####################################################################################################

@app.route("/Download", methods=["GET","POST"])
def Download():
    status = log_status()
    return render_template("Download.html",status=status)

@app.route("/about", methods=["GET","POST"])
def about():
    status = log_status()
    return render_template("about.html",status=status)


@app.route("/characters", methods=["GET","POST"])
def characters():
    status = log_status()
    return render_template("characters.html",status=status)

@app.route("/nomad", methods=["GET","POST"])
def nomad():
    status = log_status()
    return render_template("nomad.html",status=status)

@app.route("/wizard", methods=["GET","POST"])
def wizard():
    status = log_status()
    return render_template("wizard.html",status=status)

@app.route("/warrior", methods=["GET","POST"])
def warrior():
    status = log_status()
    return render_template("warrior.html",status=status)

#####################################################################################################
#####################################################################################################
#####################################################################################################


# for registeration and login

@app.before_request
def load_logged_in_user():
    g.user = session.get("userNum_id",None)
    if "team" in session:
        session

@app.route("/register", methods=["GET","POST"])
def register():
    status = log_status()
    form = RegistrationForm()
    db = get_db()
    if form.validate_on_submit() :
        user_id =  form.user_id.data
        password = form.password.data
        password2= form.password2.data
        
        if db.execute("SELECT * FROM users WHERE user_id = ?",(user_id,)).fetchone() is not None:
            form.user_id.errors.append("Username already exists")
            return render_template("registration_form.html",form=form,status=status)
        else:
        	db.execute("""INSERT INTO users (user_id,password) values(?,?); """,(user_id,generate_password_hash(password)))
        
        db.commit()
        return redirect(url_for("login"))
    
    return render_template("registration_form.html",form=form,status=status)

    

@app.route("/login",methods=["GET","POST"])
def login():
    status = log_status()
    form = LoginForm()
    if form.validate_on_submit() :
        user_id =  form.user_id.data
        password = form.password.data
        db= get_db()
        user  = db.execute("SELECT * FROM users WHERE user_id = ?",(user_id,)).fetchone()
        if user == None:
            form.user_id.errors.append("User does not exist")
            return render_template("nomad.html",form=form,status=status)
        elif not check_password_hash(user["password"],password) :
            form.password.errors.append("Password incorect")
            return render_template("nomad.html",form=form,status=status)
        else:
            session.clear()
            session["user_id"]= user_id 
        return redirect(url_for("index"))
    return render_template("nomad.html",form=form,status=status)

@app.route("/log_out",methods=["GET","POST"])
def log_out():
    session.clear()
    return redirect(url_for("index"))


#####################################################################################################
#####################################################################################################
#####################################################################################################
#####################################################################################################
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    #application.debug = True
    application.run()


