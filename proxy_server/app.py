from flask import Flask, session, redirect, url_for, request, render_template, jsonify
from flask_session import Session
import requests

app = Flask(__name__)

# Secret key for session management
app.secret_key = 'J}Kqn?rv:LRB6>/F%[1OJG{ouy^6'

# Server-side session configuration
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

MAIN_SERVER_URL = 'http://127.0.0.1:5000'  # Change this to the main server URL and port

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('proxy_protected'))
    return redirect(url_for('proxy_login'))

@app.route('/proxy_login', methods=['GET', 'POST'])
def proxy_login():
    if request.method == 'POST':
        # Get credentials and session ID from form input
        username = request.form['username']
        password = request.form['password']
        session_id = request.form['session_id']

        # Send request to main server's protected route using the session ID
        try:
            # Set the session ID in cookies
            cookies = {'session': session_id}
            
            # First, try to access the protected route directly on the main server
            response = requests.get(f"{MAIN_SERVER_URL}/protected", cookies=cookies)

            # Debugging: Check the main server's response content
            print("Main server response:", response.text)  # Log the response to see what's returned

            # Check if the response is in JSON format or HTML, depending on the main server's behavior
            try:
                main_server_data = response.json()  # Try to parse as JSON
            except ValueError:
                main_server_data = response.text  # If it's not JSON, return the text (e.g., HTML content)

            # If successful, store the session in the proxy server
            if response.status_code == 200:
                session['username'] = username
                return render_template('protected.html', username=username, session_id=session_id, protected_content=main_server_data)
            else:
                return jsonify({"message": "Access to protected route failed", "status_code": response.status_code, "response_content": response.text})

        except Exception as e:
            return jsonify({"error": str(e)})

    # If GET request, render the login form
    return render_template('proxy_login.html')

@app.route('/proxy_protected')
def proxy_protected():
    if 'username' in session:
        return f"Protected route accessed via proxy. Username: {session['username']}, Session ID: {session.sid}"
    return redirect(url_for('proxy_login'))

@app.route('/logout')
def logout():
    session.clear()
    return "Logged out."

if __name__ == '__main__':
    app.run(debug=True, port=5001)
