document.addEventListener('DOMContentLoaded', function () {
  // Initialize the socket connection
  var socket = io.connect('http://' + document.domain + ':' + location.port);

  // Joystick options
  var options = {
    zone: document.getElementById('joystick'),
    mode: 'static',
    position: { left: '50%', top: '50%' },
    size: 150,
    color: 'blue',
  };

  // Create the joystick manager
  var manager = nipplejs.create(options);

  // Movement button event listeners
  document.getElementById('forward').addEventListener('click', function () {
    socket.emit('message', 'Move forward');
  });

  document.getElementById('backward').addEventListener('click', function () {
    socket.emit('message', 'Move backward');
  });

  document.getElementById('left').addEventListener('click', function () {
    socket.emit('message', 'Turn left');
  });

  document.getElementById('right').addEventListener('click', function () {
    socket.emit('message', 'Turn right');
  });

  // Joystick move event
  manager.on('move', function (evt, data) {
    socket.emit('joystick', { direction: data.direction.angle, force: data.force });
  });

  // Speech recognition setup
  var recognition = new webkitSpeechRecognition();
  recognition.continuous = true;
  recognition.interimResults = true;

  // Voice control start/stop event listeners
  document.getElementById('start').addEventListener('click', function () {
    recognition.start();
    socket.emit('message', 'Voice control started');
  });

  document.getElementById('stop').addEventListener('click', function () {
    recognition.stop();
    socket.emit('message', 'Voice control stopped');
  });

  // Process speech recognition results
  recognition.onresult = function (event) {
    var transcript = event.results[event.results.length - 1][0].transcript.trim();
    socket.emit('voice', transcript);
  };

  // Emergency stop button event listener
  document.getElementById('break').addEventListener('click', function () {
    socket.emit('message', 'Emergency break');
  });
});
