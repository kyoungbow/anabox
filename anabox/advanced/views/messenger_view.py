# from flask import Blueprint, render_template,session, redirect, url_for
# from functools import wraps
# from flask_login import login_required
# from ..websocket.messenger_socket import socketio
# from flask_socketio import emit

# messenger_bp = Blueprint('messenger', __name__, url_prefix='/messenger')

# # @socketio.on('send_message')
# # def handle_send_message(data):
# #     user = session.get('loginUserName', '익명')
# #     print(f"서버가 받은 메시지: {data}, 유저: {user}")
# #     emit('messenger_message', {'user': user, 'message': data['message']}, broadcast=True)

