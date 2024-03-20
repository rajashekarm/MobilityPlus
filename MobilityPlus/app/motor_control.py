import RPi.GPIO as GPIO
from time import sleep
import socket

# Define GPIO pins for motor control
in1 = 24
in2 = 23
en = 25

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)

# Create PWM object for speed control
p = GPIO.PWM(en, 1000)
p.start(25)

# Set up socket connection
HOST = 'localhost'  # Replace with your server's IP address if needed
PORT = 65432        # Replace with the port used by your server for communication

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

print("Connected to server")

try:
  while True:
    # Receive data from server
    data = sock.recv(1024).decode('utf-8')

    if data:
      # Process and execute received commands
      if data == 'forward':
        print("Moving forward")
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
      elif data == 'backward':
        print("Moving backward")
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
      elif data == 'left':
        print("Turning left (modify based on your motor setup)")
        # Implement logic for left turn (modify as needed)
      elif data == 'right':
        print("Turning right (modify based on your motor setup)")
        # Implement logic for right turn (modify as needed)
      elif data == 'stop':
        print("Stopping")
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
      elif data == 'break':
        print("Emergency break")
        # Implement logic for emergency break (e.g., stop motors immediately)
      else:
        print("Unknown command:", data)
    else:
      print("Connection closed")
      break

finally:
  # Clean up GPIO pins and socket connection
  GPIO.cleanup()
  sock.close()
  print("Cleaned up resources")

