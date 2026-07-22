// frontend/src/lib/socket.js
// Socket.io client instance pointing to the Flask backend URL

import { io } from 'socket.io-client';

const SOCKET_URL = 'http://127.0.0.1:5000';

// Connect to the Flask SocketIO server
export const socket = io(SOCKET_URL, {
  autoConnect: true,
  transports: ['websocket', 'polling']
});
