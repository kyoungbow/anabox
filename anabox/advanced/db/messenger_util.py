from advanced.models import Message, db

def save_message_to_db(messengernum, user_id, content):
    msg = Message(
        messengernum=messengernum,
        sendid=user_id,
        content=content
    )
    db.session.add(msg)
    db.session.commit()

def get_last_messages(messengernum, limit=20):
    return (
        Message.query
        .filter_by(messengernum=messengernum)
        .order_by(Message.regtime.desc())
        .limit(limit)
        .all()[::-1]
    )

