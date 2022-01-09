from flask import Flask, render_template, redirect, url_for, request, flash
from flask_mysqldb import MySQL
app = Flask(__name__)
app.secret_key = "super secret key"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'alamien@786'
app.config['MYSQL_DB'] = 'my_project'

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("home.html")
@app.route('/success')
def success(name):
   return render_template("main.html")
@app.route('/login',methods = ['POST','GET'])
def login():
   if request.method == 'POST':
      user = request.form['uname']
      pwd = request.form['psw']
      sql = "select * from user_detail where user_name = %s and password = %s; "
      cur = mysql.connection.cursor()
      args = [user,pwd ]
      cur.execute(sql,args)

      records = cur.fetchall()
      cur.close()
      value_1 = len(records)
      if value_1 > 0:
          return render_template("main.html")
      else:
          flash("Incorrect credential, please try again")
          return redirect(request.url)
   else:
       return render_template("home.html")

@app.route('/register',methods = ['GET','POST'])
def register():
   if request.method == 'GET':
      return render_template("register.html")
   else:
       req = request.form

       username = req.get("userid")
       emailid = req.get("email")
       password = req.get("psw")
       firstName=req.get("fname")
       lastName = req.get("lname")
       contactno = req.get("mobile")
       if not len(password) >= 10:
           flash("Password length must be at least 10 characters")
           return redirect(request.url)
       else:
           cur = mysql.connection.cursor()
           cur.execute("INSERT INTO user_detail(user_name, first_name, Last_name,email_id,contact_number,password) VALUES (%s, %s,%s, %s,%s, %s)", (username,firstName, lastName,emailid,contactno,password))
           mysql.connection.commit()
           cur.close()
           flash("Registered successfully, please use sign in link to login")
           return redirect(request.url)


if __name__ == '__main__':
    app.run()
