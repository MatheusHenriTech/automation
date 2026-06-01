from db.models import User

def get_user(session, discord_user):
    usuario = session.query(User).filter_by(
        user_id = str(discord_user.id)
    ).first()

    if not usuario:
        usuario = User(
            user_id = str(discord_user.id),
            username = discord_user.name,
            coins = 0
        )

        session.add(usuario)

    return usuario