from flask import Flask, render_template, request, redirect, flash, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'studentnotesproject'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'mekha'
app.config['MYSQL_PASSWORD'] = 'mekha123'
app.config['MYSQL_DB'] = 'student_notes_db'

mysql = MySQL(app)

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cur.fetchone()

        cur.close()

        if user and check_password_hash(user[3], password):

            session['loggedin'] = True
            session['email'] = user[2]

            flash('Login Successful!')

            return redirect('/dashboard')

        else:
             return "Invalid Email or Password"

    return render_template('login.html')

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()

        cur.execute(
            "INSERT INTO users(fullname, email, password) VALUES(%s, %s, %s)",
            (fullname, email, hashed_password)
        )

        mysql.connection.commit()

        cur.close()

        return render_template('success.html')

    return render_template('register.html')
#dashboard
@app.route('/dashboard')
def dashboard():

    if 'loggedin' in session:
        return render_template('dashboard.html')

    return redirect('/login')

 #add note   
@app.route('/add_note', methods=['GET', 'POST'])
def add_note():

    if 'loggedin' not in session:
        return redirect('/login')

    if request.method == 'POST':

        title = request.form['title']
        content = request.form['content']
        user_email = session['email']

        cur = mysql.connection.cursor()

        cur.execute(
            "INSERT INTO notes(title, content, user_email) VALUES(%s, %s, %s)",
            (title, content, user_email)
        )

        mysql.connection.commit()

        cur.close()

        flash('Note Saved Successfully!')

        return redirect('/add_note')

    return render_template('add_note.html')

#view note
@app.route('/view_notes')
def view_notes():

    if 'loggedin' not in session:
        return redirect('/login')

    user_email = session['email']

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT * FROM notes WHERE user_email=%s",
        (user_email,)
    )

    notes = cur.fetchall()

    cur.close()

    return render_template('view_notes.html', notes=notes)

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM notes")

    notes = cur.fetchall()

    cur.close()

    return render_template('view_notes.html', notes=notes)

#delete_note
@app.route('/delete_note/<int:id>')
def delete_note(id):

    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM notes WHERE id=%s", (id,))

    mysql.connection.commit()

    cur.close()

    flash('Note Deleted Successfully!')

    return redirect('/view_notes')

#edit_note
@app.route('/edit_note/<int:id>', methods=['GET', 'POST'])
def edit_note(id):

    cur = mysql.connection.cursor()

    if request.method == 'POST':

        title = request.form['title']
        content = request.form['content']

        cur.execute(
            "UPDATE notes SET title=%s, content=%s WHERE id=%s",
            (title, content, id)
        )

        mysql.connection.commit()

        flash('Note Updated Successfully!')

        return redirect('/view_notes')

    cur.execute("SELECT * FROM notes WHERE id=%s", (id,))

    note = cur.fetchone()

    cur.close()

    return render_template('edit_note.html', note=note)

#logout
@app.route('/logout')
def logout():

    session.pop('loggedin', None)
    session.pop('email', None)

    flash('Logged Out Successfully!')

    return redirect('/login')
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)