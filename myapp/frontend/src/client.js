const WebSocket = require("ws");

// Connect to the WebSocket server at ws://localhost:8001
const ws = new WebSocket("ws://localhost:8001");

// Event listener for when the connection is opened
ws.on("open", function open() {
  console.log("Connected to the WebSocket server");

  const samples = [
    "https://github.com/Supremolink81/TTSCeleb/raw/master/barack.wav",
  ];

  // Send a message to the server
  const message = {
    op: "query",
    params: {
      model_name: "llama-3-8b",
      prompt: "What is the capital of Texas?",
      samples,
    },
  };
  ws.send(JSON.stringify(message));
});

// Event listener for when a message is received from the server
ws.on("message", function incoming(bytes) {
  data = new Buffer.from(bytes).toString("ascii");

  console.log("Received message from server:", data);
});

// Event listener for when the connection is closed
ws.on("close", function close() {
  console.log("Disconnected from the WebSocket server");
});

// Event listener for errors
ws.on("error", function error(err) {
  console.error("WebSocket error:", err);
});
