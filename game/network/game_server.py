import socket
from proto import game_pb2 as pb


class Player(object):

    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.character = None


class GameServer(object):
    def __init__(self, local_port):
        self.local_ip = self._get_local_address()
        self.connections = []
        self.player_count = 0
        self.local_port = local_port
        self.BUFFER_SIZE = 1024
        self.p1_addr = None
        self.p2_addr = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self._get_local_address(), local_port))

    def _get_local_address(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        local_ip = sock.getsockname()[0]
        sock.close()
        return local_ip

    def get_connection(self):
        data, address, join_req = None, None, None
        while data is None:
            try:
                data, address = self.socket.recvfrom(self.BUFFER_SIZE)
                join_req = pb.JoinLobbyRequest()
                join_req.ParseFromString(data)
                if join_req.name == "":
                    resp = pb.JoinLobbyResponse(ok=0, playerId=0)
                    self.socket.sendto(resp.SerializeToString(), address)
                    raise ValueError

                self.connections.append(Player(join_req.name, address[0], address[1]))

            except:
                continue

    def handle_character_request(self):
        data, address, char_select_req = None, None, None
        while data is None:
            try:
                data, address = self.socket.recvfrom(self.BUFFER_SIZE)
                char_select_req = pb.CharacterSelectRequest()
                char_select_req.ParseFromString(data)
                if char_select_req.id < 0 or char_select_req.id > 1:
                    resp = pb.CharacterSelectResponse(ok=0, playerId=0, start=0, enemyCharacter=0)
                    self.socket.sendto(resp.SerializeToString(), address)
                    raise ValueError
                enemy = (char_select_req.id + 1) % 2

                resp = pb.CharacterSelectResponse(ok=1,
                                                  playerId=char_select_req.id,
                                                  start=0,
                                                  enemyCharacter=self.connections[enemy].character)
                self.connections.append(Player(char_select_req.name, address[0], address[1]))
                self.socket.sendto(resp.SerializeToString(), address)
            except:
                continue

    def create_lobby(self):
        # get 2 connections
        for i in range(2):
            self.get_connection()
        # tell clients character select is ready
        for i, person in enumerate(self.connections):
            resp = pb.JoinLobbyResponse(ok=1, playerId=len(self.connections), start=1)
            self.socket.sendto(resp.SerializeToString(), (person.ip, person.port))

        locked = 0
        # get character selections
        for i in range(2):
            self.handle_character_request()
        # tell clients game is ready
        for i in range(len(self.connections)):
            enemy = (i + 1) % 2
            resp = pb.CharacterSelectResponse(playerId=i,
                                              ok=1,
                                              start=1,
                                              enemyCharacter=self.connections[enemy].character)
            p = self.connections[i]
            self.socket.sendto(resp.SerializeToString(), (p.ip, p.port))
        # start listening for game updates
        self.start_game()

    def start_game(self):

        while True:
            try:
                data, address = self.socket.recvfrom(self.BUFFER_SIZE)
                game_update = pb.Update()
                game_update.ParseFromString(data)
                enemy = (game_update.id + 1) % 2
                p = self.connections[enemy]
                self.socket.sendto(game_update.SerializeToString(), (p.ip, p.port))

            except:
                continue

        self.socket.close()


if __name__ == "__main__":
    game = GameServer(1234)
    game.create_lobby()
