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

from voice_recognition import recognize_speech
from motor_control import handle_motor_command, cleanup

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

# WebSocket endpoint for receiving commands from UI
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await handle_command(data)

# Handle different types of commands (joystick, voice, button)
async def handle_command(data: str):
    try:
        message = json.loads(data)
        message_type = message.get('type')
        if message_type == 'joystick':
            direction = message.get('direction')
            force = message.get('force')
            # Handle joystick data (implement your logic)
        elif message_type == 'voice':
            voice_command = message.get('command')
            if voice_command:
                await handle_motor_command(voice_command)
        elif message_type == 'button':
            button_command = message.get('command')
            # Handle button command (implement your logic)
        else:
            print(f"Unknown message type: {message_type}")
    except json.JSONDecodeError:
        print("Invalid JSON format")

# Clean up resources when stopping the server
@app.on_event("shutdown")
async def shutdown_event():
    cleanup()


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
