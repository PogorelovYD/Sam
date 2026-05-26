import grpc
import time

import game_pb2
import game_pb2_grpc


def generate_players():
    players = [
        ("PlayerOne", 10),
        ("PlayerTwo", 20),
        ("PlayerThree", 30),
        ("PlayerFour", 40),
    ]

    for nickname, level in players:
        yield game_pb2.PlayerInfo(
            nickname=nickname,
            level=level
        )

        time.sleep(1)


channel = grpc.insecure_channel('localhost:50051')

stub = game_pb2_grpc.GameLobbyStub(channel)

responses = stub.Matchmaking(generate_players())

for response in responses:
    print(response.message)