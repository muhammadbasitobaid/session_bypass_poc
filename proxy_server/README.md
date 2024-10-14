### cUrl commands for testing!
### 1. **Home Endpoint (`GET /`)**

This endpoint checks if the user is logged in and returns the welcome message with the session ID if they are.

```bash
curl -X GET http://127.0.0.1:5001/
```

### 2. **Login Endpoint (`POST /login`)**

This endpoint logs the user in. You need to provide a username and password via form data.

```bash
curl -X POST http://127.0.0.1:5001/login \
     -d "username=user_proxy" \
     -d "password=Pass@123_Proxy" \
     -c cookies.txt
```

- `-d` sends form data with the `POST` request.
- `-c cookies.txt` saves the session cookie into `cookies.txt`, which you will use for the other requests.

### 3. **Session Info Endpoint (`GET /session_info`)**

This endpoint provides information about the current session. You'll need to send the session cookie with the request.

```bash
curl -X GET http://127.0.0.1:5001/session_info \
     -b cookies.txt
```

- `-b cookies.txt` sends the previously stored session cookie.

### 4. **Logout Endpoint (`GET /logout`)**

This endpoint logs the user out and clears the session.

```bash
curl -X GET http://127.0.0.1:5001/logout \
     -b cookies.txt
```

### 5. **Test Invalid Login (`POST /login`)**

You can test an invalid login by providing wrong credentials.

```bash
curl -X POST http://127.0.0.1:5001/login \
     -d "username=user_proxy" \
     -d "password=wrong_password"
```

### How to Run the Test:

1. First, log in using the `/login` endpoint and save the session cookie (`cookies.txt`).
2. Check the session information using the `/session_info` endpoint with the saved cookie.
3. Finally, you can log out using the `/logout` endpoint and clear the session.

These commands allow you to interact with and test the Flask server endpoints manually.
