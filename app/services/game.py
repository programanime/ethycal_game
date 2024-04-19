from sqlalchemy import desc

from app.models.base import with_db_session
from app.models.game import Game
from app.models.move import Move


@with_db_session
def get_games(db_session):
    games = db_session.query(Game).order_by(desc(Game.created_at)).all()
    return [game.as_dict() for game in games]


@with_db_session
def create_new_game(db_session):
    game = Game()
    db_session.add(game)
    db_session.commit()
    game_data = game.as_dict()
    return game_data


@with_db_session
def get_game_by_id(game_id: int, db_session):
    if game := db_session.query(Game).filter(Game.id == game_id).first():
        return game.as_dict()


@with_db_session
def get_moves_by_game(game_id: int, db_session):
    game = db_session.query(Game).filter(Game.id == game_id).first()
    return [move.as_dict() for move in game.moves]


@with_db_session
def create_move_for_game(game_id: int, x: int, y: int, db_session):
    game = db_session.query(Game).filter(Game.id == game_id).one()
    if game.completed:
        raise Exception(f"Game completed, the winner was {game.winner}")

    if existing_move := game.get_move(x, y):
        agent = "machine" if existing_move.is_machine_move else "user"
        raise Exception(f"Move done already by {agent}")
    move = Move(x=x, y=y)
    game.moves.append(move)
    db_session.add(game)
    db_session.commit()
    move_data = move.as_dict()
    return move_data


@with_db_session
def generate_move_for_game(game_id: int, db_session):
    if game := db_session.query(Game).filter(Game.id == game_id).first():
        if game.completed:
            return
        positions = [(x, y) for x in range(3) for y in range(3)]
        for x, y in reversed(positions):
            if not game.get_move(x, y):
                game.moves.append(Move(x=x, y=y, is_machine_move=True))
                db_session.add(game)
                break
