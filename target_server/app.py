from flask import Flask, session, redirect, url_for, request, jsonify, render_template
from flask_session import Session

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'MR!kG,aHi2sC>zE2vi&1uq$Ky$uY*3'

# Server-side session configuration
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions on the server

Session(app)

# In-memory storage for user sessions (to track single session)
active_sessions = {}

# Sample user data
users = {
    "test": "Pass@123"
}

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('protected'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            # Check if user is already logged in from another session
            if username in active_sessions:
                # Invalidate previous session
                active_sessions.pop(username)
                session.clear()

            # Log in the user and create a new session
            session['username'] = username
            active_sessions[username] = session.sid  # Track session ID
            return redirect(url_for('protected'))
        else:
            return render_template('login.html', message="Invalid credentials")
    return render_template('login.html')

@app.route('/protected')
def protected():
    if 'username' in session:
        current_session_id = session.sid
        if active_sessions.get(session['username']) != current_session_id:
            session.clear()  # Invalidate current session
            return redirect(url_for('login'))
        return render_template('protected.html', username=session['username'], session_id=session.sid)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    if 'username' in session:
        active_sessions.pop(session['username'], None)
        session.clear()
    return redirect(url_for('login'))

@app.route('/validate_session')
def validate_session():
    if 'username' in session:
        current_session_id = session.sid
        if active_sessions.get(session['username']) != current_session_id:
            session.clear()  # Invalidate current session
            return jsonify({"message": "Session invalidated."}), 401
        return jsonify({"message": "Session valid."})
    return jsonify({"message": "No active session."}), 401

if __name__ == '__main__':
    app.run(debug=True)
