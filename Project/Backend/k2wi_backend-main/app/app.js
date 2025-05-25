const Server = require('./Server');

const PORT = 8080;

const server = new Server(PORT);

server.start();