from flask import Flask, request
import json

app = Flask(__name__)

# This would be replaced with the actual code to control the wheelchair
def control_wheelchair(data):
    print(f'Controlling wheelchair with data: {data}')

@app.route('/joystick', methods=['POST'])
def joystick():
    data = request.json
    control_wheelchair(data)
    return 'OK'

@app.route('/voice', methods=['POST'])
def voice():
    data = request.json
    control_wheelchair(data)
    return 'OK'

if __name__ == '__main__':
    app.run()

