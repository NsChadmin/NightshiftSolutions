from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
import aiosmtpd
from aiosmtpd.smtp import SMTP as Server, syntax
import psycopg2
import asyncio


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Database connection details
dbname = 'email_db_ns'
user = 'chadlin'
password = '4e0e776a78'
host = 'localhost'
port = '5432'

# Establish a connection
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

# Create the user table if it doesn't exist
with conn.cursor() as cursor:
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS nsusers (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        backup_email VARCHAR(255) NOT NULL
    )
    '''
    cursor.execute(create_table_query)

# Commit the changes
conn.commit()

# Define the Mail model
class Mail:
    def __init__(self, subject, sender, recipient):
        self.subject = subject
        self.sender = sender
        self.recipient = recipient

# Create the signup table if it doesn't exist
with conn.cursor() as cursor:
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS signup (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL,
        backup_email VARCHAR(255) NOT NULL
    )
    '''
    cursor.execute(create_table_query)

# Commit the changes
conn.commit()

# Sample mail data (replace with actual database queries)
received_mails = [
    Mail('Hello', 'user1@example.com', 'user2@example.com'),
    Mail('Greetings', 'user3@example.com', 'user2@example.com')
]
sent_mails = [
    Mail('Meeting', 'user2@example.com', 'user1@example.com'),
    Mail('Report', 'user2@example.com', 'user3@example.com')
]
deleted_mails = []
spam_mails = []

# Create the SignUpForm
class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    backup_email = StringField('Backup Email', validators=[DataRequired()])

# Index route (new route)
@app.route('/map')
def map():
    return render_template('map.html')

# Index route (new route)
@app.route('/navbar')
def navbar():
    return render_template('navbar.html')

# Index route (new route)
@app.route('/critical')
def critical():
    return render_template('critical.html')

# Index route (new route)
@app.route('/devices')
def devices():
    return render_template('devices.html')

# Index route (new route)
@app.route('/header')
def header():
    return render_template('header.html')

# Index route (new route)
@app.route('/base')
def base():
    return render_template('base.html')

# Index route (new route)
@app.route('/footer')
def footer():
    return render_template('footer.html')

# Index route (new route)
@app.route('/features')
def features():
    return render_template('features.html')

# Index route (new route)
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Index route (new route)
@app.route('/pricing')
def pricing():
    return render_template('pricing.html')
    
# Index route (new route)
@app.route('/reporting')
def reporting():
    return render_template('reporting.html')

# Index route (new route)
@app.route('/pricinghourly')
def pricinghourly():
    return render_template('pricinghourly.html')

# Index route (new route)
@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

# Index route (new route)
@app.route('/about')
def about():
    return render_template('about.html')

# Index route (new route)
@app.route('/comingsoon')
def comingsoon():
    return render_template('comingsoon.html')

# Index route (new route)
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Index route (new route)
@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/chart')
def chart():
    # Data for the chart
    labels = ['January', 'February', 'March', 'April', 'May']
    data = [10, 20, 30, 40, 50]

    return render_template('chart.html', labels=labels, data=data)

# Index route (new route)
@app.route('/index')
def index():
    return render_template('index.html')

# Root URL route
@app.route('/')
def root():
    return redirect(url_for('index'))

@app.route('/protected_html')
def protected_html():
    # Check if the user is authenticated
    if 'username' in session:
        return render_template('devices.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/protected1_html')
def protected1_html():
    # Check if the user is authenticated
    if 'username' in session:
        return render_template('critical.html')
    else:
        return redirect(url_for('login'))

@app.route('/protecte2_html')
def protected2_html():
    # Check if the user is authenticated
    if 'username' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))
    
# Index route (new route)
@app.route('/protecte3_html')
def protected3_html():
        # Check if the user is authenticated
    if 'username' in session:
        return render_template('support.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password are valid
        if username == 'admin' and password == '4e0e776a78':
            # Store the authenticated user in the session
            session['username'] = username
            return redirect(url_for('protected2_html'))
        else:
            return render_template('login.html', message='Invalid credentials')

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for('login'))

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        backup_email = form.backup_email.data
        
        with conn.cursor() as cursor:
            # Insert the user information into the signup table
            insert_query = '''
            INSERT INTO signup (username, password, backup_email)
            VALUES (%s, %s, %s)
            '''
            cursor.execute(insert_query, (username, password, backup_email))

        # Commit the changes
        conn.commit()
        
        return render_template('signup.html', form=form, success=True)
    
    return render_template('signup.html', form=form, success=False)

# Signup route
#@app.route('/signup', methods=['GET', 'POST'])
#def signup():
#    form = SignUpForm()
#    if form.validate_on_submit():
#        username = form.username.data
#        password = form.password.data
#        backup_email = form.backup_email.data
#        
#        with conn.cursor() as cursor:
#            # Insert the user information into the signup table
#            insert_query = '''
#            INSERT INTO signup (username, password, backup_email)
#            VALUES (%s, %s, %s)
#            '''
#            cursor.execute(insert_query, (username, password, backup_email))#
#
#        # Commit the changes
#        conn.commit()
#        
#        return render_template('signup.html', form=form, success=True)
#    
#    return render_template('signup.html', form=form, success=False)

# Inbox route
@app.route('/inbox')
def inbox():
    return render_template('inbox.html', received_mails=received_mails, sent_mails=sent_mails,
                           deleted_mails=deleted_mails, spam_mails=spam_mails)

# Send mail route
@app.route('/send_mail', methods=['POST'])
def send_mail():
    recipient = request.form.get('recipient')
    subject = request.form.get('subject')
    content = request.form.get('content')
    
    with conn.cursor() as cursor:
        # Insert the mail into the database table (replace 'mails' with your table name)
        insert_query = '''
        INSERT INTO mails (subject, sender, recipient, content)
        VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(insert_query, (subject, 'your-email@example.com', recipient, content))

    # Commit the changes
    conn.commit()

    # Redirect to the inbox
    return redirect(url_for('inbox'))

# Create the SignInForm
class SignInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# Signin route
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    form = SignInForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Logic to verify the user's credentials (e.g., query the database)
        # Replace this with your actual implementation
        with conn.cursor() as cursor:
            select_query = '''
            SELECT username, password
            FROM signup
            WHERE username = %s AND password = %s
            '''
            cursor.execute(select_query, (username, password))
            user = cursor.fetchone()
        
        if user:
            # User credentials are valid, redirect to inbox
            return redirect(url_for('inbox'))
        else:
            # User credentials are invalid, show error message
            error = 'Invalid username or password'
            return render_template('signin.html', form=form, error=error)
    
    return render_template('signin.html', form=form)

# ...

# Logout route
#@app.route('/logout')
#def logout():
    # Logic to handle logout (e.g., clear session, redirect to login page)
#    return redirect(url_for('signin'))

# SMTP Server Configuration

class CustomHandler(aiosmtpd.smtp.SMTP):
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        recipient = address.lower()  # Convert the recipient address to lowercase for case-insensitive comparison
        
        # Perform recipient validation logic here
        if recipient.endswith('@example.com'):
            # Valid recipient domain
            return '250 OK'
        else:
            # Invalid recipient domain
            return '550 Invalid recipient'

async def start_smtp_server():
    handler = CustomHandler()
    server = aiosmtpd.SMTP(handler)
    await server.start()


if __name__ == '__main__':
    # Start the SMTP server
    asyncio.ensure_future(start_smtp_server())
    # Run the Flask application
    app.run(debug=True)
