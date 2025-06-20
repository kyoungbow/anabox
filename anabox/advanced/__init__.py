from flask import Flask, render_template
from flask_login import LoginManager
from .views import main_view, auth_view, container_view, chat_view, company_view, stats_view
from .websocket.messenger_socket import socketio
from .models import db, User  # db import!

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'humanda5-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://kyoungbow:1234@localhost:5432/containerSharing_test'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)  # DB 초기화
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    # socketio.init_app(app)
    socketio.init_app(app, cors_allowed_origins="*")  # 소켓 초기화

    app.register_blueprint(main_view.main_bp)
    app.register_blueprint(auth_view.auth_bp)
    app.register_blueprint(container_view.container_bp)
    app.register_blueprint(chat_view.chat_bp)
    app.register_blueprint(company_view.company_bp)
    app.register_blueprint(stats_view.stats_bp)

    try:
        from .views.chat_view import initialize_chat_module
        initialize_chat_module()
    except Exception as e:
        print(f"모듈 초기화 실패: {e}")

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errorPage.html'), 404

    return app
