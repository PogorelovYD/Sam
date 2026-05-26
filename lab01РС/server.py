from concurrent import futures
import grpc

import game_pb2
import game_pb2_grpc


class GameLobbyServicer(game_pb2_grpc.GameLobbyServicer):

    def Matchmaking(self, request_iterator, context):
        players = []

        for player in request_iterator:
            print(f"Игрок: {player.nickname}")

            players.append(player)

            if len(players) >= 2:
                p1 = players.pop(0)
                p2 = players.pop(0)

                yield game_pb2.MatchResult(
                    message=f"Match found: {p1.nickname} vs {p2.nickname}"
                )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    game_pb2_grpc.add_GameLobbyServicer_to_server(
        GameLobbyServicer(),
        server
    )

    server.add_insecure_port('[::]:50051')
    server.start()

    print("Server started")

    server.wait_for_termination()


serve()