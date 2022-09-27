
from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import re
from flask_mail import Mail,Message


app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'jerin@gksinfotech.in'
app.config['MAIL_PASSWORD'] = 'Jerin@gks123'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM stud")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', students=data)


@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
      
        cur.execute( "SELECT * FROM stud WHERE email LIKE %s", [email] )
        check=cur.fetchone()
        if check:
            #return render_template('index.html')
            #flash("email already exists!", "danger")
            #redirect(url_for('Index'))
            return "already exist"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            return"Invalid email address!"
        elif not re.match(r'[A-Za-z0-9]+', email):
            return "Username must contain only characters and numbers!"
            
        else:
                
         cur.execute("INSERT INTO stud (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
       
         msg = Message(
                'Hello',
                sender ='jerin@gksinfotech.in',
                recipients = [email]
               )
         msg.body = 'Hello Flask message sent from Flask-Mail'
         mail.send(msg)
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM stud WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))



@app.route('/update', methods= ['POST', 'GET'])
def update():
    if request.method == 'POST':
       
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        id_data = request.form['id']

        cur = mysql.connection.cursor()
        
        cur.execute( """
        UPDATE stud SET name=%s, email=%s, phone=%s
        WHERE id=%s
       """, (name, email, phone, id_data))
        
        mysql.connection.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('Index'))




if __name__ == "__main__":
    app.run(debug=True)