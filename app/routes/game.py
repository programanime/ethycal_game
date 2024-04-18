import logging
from http import HTTPStatus

from flask import Blueprint, abort, jsonify, render_template, request

from app.schemas.move import MoveSchema
from app.services.game import (create_move_for_game, create_new_game,
                               generate_move_for_game, get_game_by_id,
                               get_games, get_moves_by_game)

LOG = logging.getLogger(__name__)
game_router = Blueprint("game", __name__)


@game_router.get("/")
def get_all_games():
    games = get_games()
    return jsonify(games), HTTPStatus.OK


@game_router.get("/<int:game_id>")
def get_game(game_id: int):
    if game := get_game_by_id(game_id):
        return jsonify(game), HTTPStatus.OK
    else:
        return jsonify({"error": "Game not found"}), HTTPStatus.NOT_FOUND


@game_router.get("/<int:game_id>/move")
def get_game_moves(game_id: int):
    moves = get_moves_by_game(game_id)
    if moves is not None:
        return jsonify(moves), HTTPStatus.OK
    else:
        return jsonify({"error": "Game not found"}), HTTPStatus.NOT_FOUND


@game_router.post("/")
def start_new_game():
    try:
        game = create_new_game()
        return jsonify(game), HTTPStatus.CREATED
    except Exception as e:
        LOG.error("Error creating new game: %s", e)
        return (
            jsonify({"error": "Game creation failed", "message": str(e)}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@game_router.post("/<int:game_id>/move")
def apply_move(game_id: int):
    try:
        move_data = request.json
        move = MoveSchema().load(move_data)
        move = create_move_for_game(game_id, move.get("x"), move.get("y"))
        generate_move_for_game(game_id)
        return jsonify(move), HTTPStatus.CREATED
    except Exception as e:
        LOG.error("Error creating new game: %s", e)
        return (
            jsonify({"error": "Wrong move", "message": str(e)}),
            HTTPStatus.BAD_REQUEST,
        )
