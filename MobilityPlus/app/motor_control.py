# motor_control.py

import RPi.GPIO as GPIO
import socket

# Define GPIO pins for motor control (modify as needed)
in1 = 24
in2 = 23
en = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)

# Create PWM object for speed control
p = GPIO.PWM(en, 1000)
p.start(25)

# Set up socket connection to Raspberry Pi
HOST = 'localhost'  # Replace with your server's IP address if needed
PORT = 65432        # Replace with the port used by your server for communication

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

def handle_motor_command(command):
    if command == 'move forward':
        # Implement logic to move the wheelchair forward
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
    elif command == 'move backward':
        # Implement logic to move the wheelchair backward
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
    elif command == 'turn left':
        # Implement logic to turn the wheelchair left
        # For example, adjust motor speeds or direction
        pass
    elif command == 'turn right':
        # Implement logic to turn the wheelchair right
        # For example, adjust motor speeds or direction
        pass
    elif command == 'emergency stop':
        # Implement logic for emergency stop (e.g., stop motors immediately)
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
    else:
        print(f"Unknown command: {command}")

# Clean up GPIO pins and socket connection
def cleanup():
    GPIO.cleanup()
    sock.close()
