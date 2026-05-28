
from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__)
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

        session['loggedin'] = True
        session['email'] = request.form['email']

        flash('Login Successful!')

        return redirect('/dashboard')

    return render_template('login.html')

# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        flash('Registration Successful! Please Login.')

        return redirect('/login')

    return render_template('register.html')

# Dashboard
@app.route('/dashboard')
def dashboard():

    if 'loggedin' in session:
        return render_template('dashboard.html')

    return redirect('/login')

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