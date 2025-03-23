from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import datetime
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# MongoDB connection
client = MongoClient('mongodb://mongo:27017/')
db = client['live_db']
users_collection = db['users']
login_collection = db['Login']

# Insert sample user if not exists
if users_collection.count_documents({'username': 'admin'}) == 0:
    users_collection.insert_one({'username': 'admin', 'password': 'admin123'})

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username, 'password': password})
        
        # Log the login attempt
        login_collection.insert_one({
            'username': username,
            'timestamp': datetime.datetime.now().isoformat(),
            'status': 'success' if user else 'failed'
        })
        
        if user:
            session['username'] = username
            return redirect(url_for('login'))
        return render_template('login.html', error='Invalid credentials')
    
    if 'username' in session:
        return render_template('login.html', message=f'Welcome, {session["username"]}!')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)