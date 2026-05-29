
from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)

app.secret_key = 'secret123'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mekha@2005'
app.config['MYSQL_DB'] = 'student_notes_db'

mysql = MySQL(app)
app.secret_key = 'studentnotessecret'

# Temporary notes storage
notes_data = []

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

        # Hash Password
        hashed_password = generate_password_hash(password)

        cur = mysql.connection.cursor()

        cur.execute(
            "INSERT INTO users(fullname,email,password) VALUES(%s,%s,%s)",
            (fullname, email, hashed_password)
        )

        mysql.connection.commit()

        cur.close()

        flash('Registration Successful! Please Login.')

        return redirect('/login')

    return render_template('register.html')

# Dashboard
@app.route('/dashboard')
def dashboard():

    if 'loggedin' in session:
        return render_template('dashboard.html')

    return redirect('/login')
#admin
@app.route('/admin')
def admin():

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.close()

    total_notes = len(notes_data)

    return render_template(
        'admin.html',
        total_users=total_users,
        total_notes=total_notes
    )
# Add Note
@app.route('/add_note', methods=['GET', 'POST'])
def add_note():

    if request.method == 'POST':

        title = request.form['title']
        content = request.form['content']

        notes_data.append({
            'title': title,
            'content': content
        })

        flash('Note Added Successfully!')

        return redirect('/view_notes')

    return render_template('add_note.html')

# View Notes
@app.route('/view_notes')
def view_notes():

    return render_template(
        'view_notes.html',
        notes=notes_data
    )

# Edit Note
@app.route('/edit_note/<int:index>', methods=['GET', 'POST'])
def edit_note(index):

    if request.method == 'POST':

        notes_data[index]['title'] = request.form['title']
        notes_data[index]['content'] = request.form['content']

        flash('Note Updated Successfully!')

        return redirect('/view_notes')

    note = notes_data[index]

    return render_template('edit_note.html', note=note, index=index)

# Delete Note
@app.route('/delete_note/<int:index>')
def delete_note(index):

    notes_data.pop(index)

    flash('Note Deleted Successfully!')

    return redirect('/view_notes')

# Logout
@app.route('/logout')
def logout():

    session.pop('loggedin', None)
    session.pop('email', None)

    flash('Logged Out Successfully!')

    return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

@app.after_request
def add_security_headers(response):

    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'

    return response