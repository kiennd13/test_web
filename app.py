from flask import Flask, render_template,request,redirect,url_for,session,flash
from db2 import get_player_MU,add_player_MU,add_account,get_account,add_blog,get_blog,update_blog
from forms import RegistrationForm
from flask_pymongo import PyMongo
app = Flask(__name__)
app.secret_key = "31051995a@"


@app.route('/')
def index():
    if 'username' in session:
        return render_template('lala.html')
    else:
        return redirect(url_for("login"))

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/login', methods = ["POST"])
def post_login():
  # error = None
  user_name = request.form.get('username')
  password = request.form.get('password')
  # if user_name == 'admin' and password == 'admin':
  t = get_account(user_name,password)
  if len(t) > 0:
      session["username"] = user_name
      flash('Login Successful!','success')
      return redirect(url_for("index"))
  else :
      # error = 'Invalid username or password. Please try again!'
      flash('Login Unsuccessful','success')
      return render_template('login.html')

@app.route("/logout")
def logout():
  session.pop('username')
  return redirect(url_for("login"))

@app.route('/man_united')
def get():
  if "username" in session:
    print(session["username"])
    return render_template('united.html',list_player = get_player_MU())
  else:
    return redirect(url_for("login"))

import datetime

@app.route('/feeling', methods=["POST"])
def add_feeling():
  if "username" in session:
    content = request.form.get('blog')
    time  = datetime.datetime.now()
    author = session["username"]
    t=request.form.get('comment')
    add_blog(author,content,time,t)
    a = get_blog()
    print(a)
    if len(str(t))>0:
      m = {"comment": None}
      n = {"$set":{"comment": t}}
      update_blog(m,n)
    print(a)
    return render_template('feeling.html', posts = get_blog())
  else:
    return redirect(url_for("login"))

@app.route('/feeling')
def get_feeling():
  if "username" in session:
    return render_template('feeling.html', posts = get_blog())
  else:
    return redirect(url_for("login"))

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # flash(f'Account created for {form.username.data}!', 'success')
        m = form.username.data
        n = form.password.data
        e = form.email.data
        add_account(m,n,e)
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
  
@app.route("/about")
def about():
  return render_template('about.html')

@app.route("/memory")
def memory():
  ds_image = []
  a = mongo.db.upfile.find()
  for a in a :
    ds_image.append(a['profile_image_name'])
  print(ds_image)
  return render_template('memory2.html',list_image = ds_image)

app.config["MONGO_URI"] = "mongodb+srv://kiennd13:jxDB1SH3TY0rBbpf@cluster0-nfuqv.mongodb.net/test?retryWrites=true"
mongo = PyMongo(app)

@app.route('/upfile')
def upfile():
   
    return render_template('upfile.html')

@app.route('/create', methods=["POST"])
def create():
    if 'profile_image' in request.files:
        profile_image = request.files['profile_image']
        mongo.save_file(profile_image.filename,profile_image)
        mongo.db.upfile.insert({"username":request.form.get('username'),"profile_image_name": profile_image.filename})
    
    return "Done!"

@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8000, debug=True)
 


