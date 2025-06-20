from flask import session
from flask_socketio import SocketIO, emit,join_room
from flask_login import current_user
from datetime import datetime
from advanced.db.messenger_util import save_message_to_db, get_last_messages

socketio = SocketIO(cors_allowed_origins="*")


@socketio.on('join_room')
def handle_join_room(data):
    room_id = data.get('room_id')
    print("여기11")
    if not current_user.is_authenticated or not room_id:
        return
    join_room(str(room_id))
    print("여기!!")
    for msg in get_last_messages(room_id):
        emit('messenger_message', {
            'id' : msg.sender.id,
            'user': msg.sender.username,
            'message': msg.content,
            'timestamp': msg.regtime.strftime('%Y-%m-%d %H:%M:%S')
        }, room=str(room_id))


@socketio.on('send_message')
def on_send_message(data):
    room_id = data.get('room_id')
    message = data.get('message')
    print(f"서버가 받은 메시지: {data}")
    if current_user.is_authenticated and room_id and message:
        save_message_to_db(room_id, current_user.id, message)
        emit('messenger_message', {
            'id' : current_user.id,
            'user': current_user.username,
            'message': message,
            'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }, room=str(room_id))