from fastapi import FastAPI, HTTPException, WebSocket, Request, status, Depends
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi.security import OAuth2PasswordBearer
import os
import json
import jwt
from pydantic import ValidationError

# FastAPI app instance
app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, 'static')

# Use the absolute path for the 'static' directory
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Secrets should be stored securely, not hardcoded
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'

# Define the OAuth2PasswordBearer instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Serve the login page as the root page
@app.get("/", response_class=HTMLResponse)
async def get_login():
    try:
        login_html_path = os.path.join(BASE_DIR, 'templates', 'login.html')
        with open(login_html_path, 'r') as file:
            html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"detail": "Login page not found"})

# ... rest of your code ...

# Handle the Google Sign-In token verification and redirect
@app.post("/token")
async def token_post(token: str = Depends(oauth2_scheme)):
    try:
        # Verify the token using Google's verifier
        idinfo = jwt.decode(token, CLIENT_SECRET, algorithms=["RS256"])

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # Token is valid, redirect to the control page
        return JSONResponse(content={"message": "Token is valid"}, status_code=status.HTTP_200_OK)
    except jwt.JWTError:
        # Invalid token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Serve the control page
@app.get("/control", response_class=HTMLResponse)
async def get_control():
    try:
        control_html_path = os.path.join(BASE_DIR, 'templates', 'integrate.html')
        with open(control_html_path, 'r') as file:
            html_content = file.read()
        return HTMLResponse(content=html_content, status_code=200)
    except FileNotFoundError:
        return JSONResponse(status_code=404, content={"detail": "Control page not found"})

# WebSocket endpoint
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


# Exception handler for HTTP errors
@app.exception_handler(HTTPException)
async def auth_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Run the application (modify host and port as needed)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 8000)))
