import sys
#sys.path.append('C:\\Users\\rajas\\OneDrive\\Desktop\\MobilityPlus\\app\\libs')

import os
from fastapi import FastAPI, HTTPException, WebSocket, Response, requests, Request, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
#import jwt
import json
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from google.oauth2 import id_token
from google.auth.transport import requests
#from fastapi_socketio import SocketManager



# FastAPI app instance
app = FastAPI()
#socket_manager = SocketManager(app=app)

# @socket_manager.on('connect')
# async def on_connect(sid, environ):
#     print('Client connected', sid)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, 'static')

# Use the absolute path for the 'static' directory
app.mount("/static", StaticFiles(directory=static_dir), name="static")


# Secrets should be stored securely, not hardcoded
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


# Define the OAuth2PasswordBearer instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Serve the login page
@app.get("/login")
async def get_login():
    login_html_path = os.path.join('templates', 'login.html')
    with open(login_html_path, 'r') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)

# Handle the Google Sign-In token verification and redirect
@app.post("/token")
async def token_post(token: str = Depends(oauth2_scheme)):
    try:
        # Verify the token using Google's verifier
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.getenv('GOOGLE_CLIENT_ID'))

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # Token is valid, redirect to the integrate page
        return RedirectResponse(url='/integrate', status_code=status.HTTP_303_SEE_OTHER)
    except ValueError:
        # Invalid token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Serve the integrate page
@app.get("/control")
async def get_integrate():
    integrate_html_path = os.path.join('templates', 'integrate.html')
    with open(integrate_html_path, 'r') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    token = websocket.query_params.get("token")
    if not token:
        await websocket.send_text("Unauthorized access. Please login.")
        await websocket.close()
        return

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (jwt.JWTError, ValidationError):
        raise credentials_exception
    user = await load_user(token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": "Bearer"},
            )
    while True:
        data = await websocket.receive_text()
        print(f"Received message: {data}")

        # Parse the message as JSON
        message = json.loads(data)

        # Handle different types of messages
        if message['type'] == 'joystick':
            # Handle joystick data
            direction = message['direction']
            force = message['force']
            # ... your code here ...
        elif message['type'] == 'voice':
            # Handle voice command
            command = message['command']
            # ... your code here ...
        elif message['type'] == 'button':
            # Handle button command
            command = message['command']
            # ... your code here ...
        else:
            print(f"Unknown message type: {message['type']}")


@app.exception_handler(HTTPException)
async def auth_exception_handler(request, exc):
    if exc.status_code == 401:
        return {"detail": exc.detail}, exc.status_code


# Run the application (modify host and port as needed)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
    print("server up and running")
