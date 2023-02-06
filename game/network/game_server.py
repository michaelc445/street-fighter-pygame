import socket
from proto import game_pb2 as pb
from threading import Thread
from datetime import datetime


class Player(object):

    def __init__(self, name, ip, port, id):
        self.name = name
        self.ip = ip
        self.port = port
        self.character = None
        self.id = id


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

                self.connections.append(Player(join_req.name, address[0], address[1], len(self.connections)))

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
            resp = pb.JoinLobbyResponse(ok=1, playerId=person.id, start=1)
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
                                              enemyCharacter=0)
            p = self.connections[i]
            self.socket.sendto(resp.SerializeToString(), (p.ip, p.port))
        # start listening for game updates

        self.start_game()
    def player_timeout(self, times):
        check = datetime.now()
        for t in times:
            diff = check - t
            if diff.total_seconds() > 10:
                return True

        return False

    def start_game(self):
        t = [datetime.now(),datetime.now()]
        while True:
            try:
                if self.player_timeout(t):
                    break
                data, address = self.socket.recvfrom(self.BUFFER_SIZE)
                game_update = pb.Update()
                game_update.ParseFromString(data)
                t[int(game_update.id)] = datetime.now()
                enemy = (game_update.id + 1) % 2
                p = self.connections[enemy]
                self.socket.sendto(game_update.SerializeToString(), (p.ip, p.port))
                if game_update.quit:
                    break
            except:
                continue

        self.socket.close()


# server listens for game requests and then creates a server on an unused port for the game
class MatchServer(object):

    def __init__(self, local_port):
        self.BUFFER_SIZE = 1024
        self.port = local_port
        self.free_ports = [i for i in range(1235, 1245)]
        self.threads = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self._get_local_address(), self.port))
        self.lobby_codes = {}

    def _get_local_address(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        local_ip = sock.getsockname()[0]
        sock.close()
        return local_ip

    def start(self):


        while True:
            try:
                self.free_threads()

                data, address = self.socket.recvfrom(self.BUFFER_SIZE)
                lobby_req = pb.CreateLobbyRequest()
                lobby_req.ParseFromString(data)
                response = pb.CreateLobbyResponse(ok=True, port=0, start=True)
                if lobby_req.lobbyCode not in self.lobby_codes:
                    self.lobby_codes[lobby_req.lobbyCode] = address
                    response.start = False
                    self.socket.sendto(response.SerializeToString(), address)
                    continue
                game_port = self.free_ports.pop(0)
                response.port = game_port
                self.socket.sendto(response.SerializeToString(), address)
                self.socket.sendto(response.SerializeToString(), self.lobby_codes[lobby_req.lobbyCode])
                del self.lobby_codes[lobby_req.lobbyCode]

                game_thread = GameThread(game_port, self.free_ports)
                self.threads.append(game_thread)
                game_thread.start()

            except:
                continue

    def free_threads(self):
        for i in range(len(self.threads)-1,-1,-1):
            if not self.threads[i].is_alive():
                self.threads.pop(i)

class GameThread(Thread):
    def __init__(self, local_port, free_ports):
        super().__init__()
        self.local_port = local_port
        # shared list for threads to append to when finished
        self.ports = free_ports

    def run(self):
        GameServer(self.local_port).create_lobby()
        self.ports.append(self.local_port)


if __name__ == "__main__":
    MatchServer(1234).start()

