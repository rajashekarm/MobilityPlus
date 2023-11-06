var options = {
    zone: document.getElementById('joystick'),
    mode: 'static',
    position: { left: '50%', top: '50%' },
    size: 150,
    color: 'blue',
};
var manager = nipplejs.create(options);

manager.on('move', function (evt, data) {
    // Send joystick data to your Flask server here
    console.log(data);
});

var recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;

document.getElementById('start').addEventListener('click', function() {
    recognition.start();
});

document.getElementById('stop').addEventListener('click', function() {
    recognition.stop();
});

recognition.onresult = function(event) {
    var transcript = event.results[event.results.length - 1][0].transcript;
    // Send transcript to your Flask server here
    console.log(transcript);
};

document.getElementById('break').addEventListener('click', function() {
    // Send break command to your Flask server here
    console.log('Break');
});
