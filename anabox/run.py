from advanced import create_app
from advanced.websocket.messenger_socket import socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=5000, debug=True)
