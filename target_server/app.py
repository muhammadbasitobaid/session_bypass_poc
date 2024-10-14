from flask import Flask, session, redirect, url_for, request, jsonify, render_template
from flask_session import Session
import hashlib

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

def get_user_fingerprint():
    """Create a simple fingerprint based on user's IP and User-Agent"""
    user_agent = request.headers.get('User-Agent')
    user_ip = request.remote_addr
    fingerprint = f"{user_ip}-{user_agent}"
    return hashlib.sha256(fingerprint.encode()).hexdigest()

def regenerate_session():
    """Manually regenerate session by clearing and resetting session ID"""
    session.modified = True  # Mark the session as modified
    session.pop('_id', None)  # This will force Flask to regenerate a session ID

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
            session['fingerprint'] = get_user_fingerprint()  # Store fingerprint

            # Regenerate session to prevent session fixation attacks
            regenerate_session()

            # Track active session by using Flask's internal session ID
            active_sessions[username] = session.sid  # Use Flask's internal session ID
            return redirect(url_for('protected'))
        else:
            return render_template('login.html', message="Invalid credentials")
    return render_template('login.html')

@app.route('/protected')
def protected():
    if 'username' in session:
        current_session_id = session.sid
        stored_fingerprint = session.get('fingerprint')
        current_fingerprint = get_user_fingerprint()

        # Debug output
        print(f"Active session: {active_sessions.get(session['username'])}")
        print(f"Current session ID: {current_session_id}")
        print(f"Stored fingerprint: {stored_fingerprint}")
        print(f"Current fingerprint: {current_fingerprint}")

        # Validate session ID and fingerprint (IP/User-Agent)
        if active_sessions.get(session['username']) != current_session_id or stored_fingerprint != current_fingerprint:
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
        stored_fingerprint = session.get('fingerprint')
        current_fingerprint = get_user_fingerprint()

        # Validate session ID and fingerprint (IP/User-Agent)
        if active_sessions.get(session['username']) != current_session_id or stored_fingerprint != current_fingerprint:
            session.clear()  # Invalidate current session
            return jsonify({"message": "Session invalidated."}), 401
        return jsonify({"message": "Session valid."})
    return jsonify({"message": "No active session."}), 401

if __name__ == '__main__':
    app.run(debug=True)
