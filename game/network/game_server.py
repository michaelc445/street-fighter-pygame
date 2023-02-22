import socket
from game.proto import game_pb2 as pb
from threading import Thread
from datetime import datetime
import random


class Player(object):

    def __init__(self, name, ip, port, id):
        self.name = name
        self.ip = ip
        self.port = port
        self.character = 0
        self.id = id


class GameServer(object):
    def __init__(self, local_port):
        self.local_ip = self._get_local_address()
        self.connections = []
        self.map_pick = None
        self.player_count = 0
        self.local_port = local_port
        self.BUFFER_SIZE = 1024
        self.p1_addr = None
        self.p2_addr = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self._get_local_address(), local_port))
        self.socket.settimeout(10)

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
                return True
            except Exception as e:
                return False

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

    def character_select_new(self):
        locked_in = {}
        t = [datetime.now(), datetime.now()]
        while len(locked_in) < 2:
            if self.player_timeout(t):
                self.exit_character_select()
                return False

            try:
                data, address = self.socket.recvfrom(self.BUFFER_SIZE)
            except:

                self.exit_character_select()
                return False

            char_select_req = pb.CharacterSelectRequest()
            char_select_req.ParseFromString(data)
            if char_select_req.id < 0 or char_select_req.id > 1:
                resp = pb.CharacterSelectResponse(ok=0, playerId=0, start=False, enemyCharacter=0)
                self.socket.sendto(resp.SerializeToString(), address)
                raise ValueError
            t[char_select_req.id] = datetime.now()
            if char_select_req.lockedIn:
                locked_in[str(char_select_req.id)] = address
            self.connections[char_select_req.id].character = char_select_req.character
            enemy = (char_select_req.id + 1) % 2
            resp = pb.CharacterSelectResponse(ok=1,
                                              playerId=char_select_req.id,
                                              start=0,
                                              enemyCharacter=char_select_req.character)
            e_address = self.connections[enemy]
            # print("sending to player: %d value: %d"%(enemy,char_select_req.character))
            self.socket.sendto(resp.SerializeToString(), (e_address.ip, e_address.port))
        return True

    # if the game times out, this function will update both players telling them the game is over
    def exit_character_select(self):
        resp = pb.CharacterSelectResponse(playerId=0, ok=0, start=0, enemyCharacter=0)
        for player in self.connections:
            self.socket.sendto(resp.SerializeToString(), (player.ip, player.port))

    def exit_map_select(self):
        resp = pb.MapSelectResponse(ok=0, mapId=0, start=False)
        for player in self.connections:
            self.socket.sendto(resp.SerializeToString(), (player.ip, player.port))

    def map_select(self):
        # player_id: map_id
        # both players locked in if length is 2
        locked_in = {}
        t = [datetime.now(), datetime.now()]
        while len(locked_in) < 2:
            if self.player_timeout(t):
                self.exit_map_select()
                return False

            try:
                data, address = self.socket.recvfrom(self.BUFFER_SIZE)
            except TimeoutError:
                self.exit_map_select()
                return False

            map_select_req = pb.MapSelectRequest()
            map_select_req.ParseFromString(data)
            if map_select_req.playerId < 0 or map_select_req.playerId > 1:
                self.exit_map_select()
                return False
            t[map_select_req.playerId] = datetime.now()
            if map_select_req.playerId in locked_in:
                continue

            if map_select_req.lockedIn:
                print("player: %d picked map: %d" % (map_select_req.playerId, map_select_req.mapId))
                locked_in[map_select_req.playerId] = map_select_req.mapId

        votes = [v for _, v in locked_in.items()]
        self.map_pick = random.choice(votes)
        print("map select over final pick: ", self.map_pick)
        return True

    def create_lobby(self):

        # get 2 connections

        for i in range(2):
            if not self.get_connection():
                self.socket.close()
                return

        # tell clients character select is ready
        for i, person in enumerate(self.connections):
            resp = pb.JoinLobbyResponse(ok=1, playerId=person.id, start=True)
            self.socket.sendto(resp.SerializeToString(), (person.ip, person.port))

        # get character selections
        start = self.character_select_new()
        if not start:
            self.socket.close()
            return
        # tell clients game is ready
        for i in range(len(self.connections)):
            enemy = (i + 1) % 2
            resp = pb.CharacterSelectResponse(playerId=i,
                                              ok=1,
                                              start=True,
                                              enemyCharacter=self.connections[enemy].character)
            p = self.connections[i]
            self.socket.sendto(resp.SerializeToString(), (p.ip, p.port))

        map_success = self.map_select()

        if not map_success:
            self.socket.close()
            return

        for player in self.connections:
            map_response = pb.MapSelectResponse(ok=1, mapId=self.map_pick, start=True)
            self.socket.sendto(map_response.SerializeToString(), (player.ip, player.port))
        # start listening for game updates
        self.socket.settimeout(5)
        self.start_game()

    def player_timeout(self, times):
        check = datetime.now()
        for t in times:
            diff = check - t
            if diff.total_seconds() > 10:
                return True

        return False

    def quit_game(self):
        message = pb.Update(health=0,
                            enemyMove=0,
                            moving=False,
                            enemyHealth=0,
                            enemyAttack=0,
                            x=0,
                            y=0,
                            keys={},
                            id=0,
                            quit=True,
                            restart=False
                            )
        for player in self.connections:
            self.socket.sendto(message.SerializeToString(), (player.ip, player.port))

    def restart_game(self):
        message = pb.Update(health=0,
                            enemyMove=0,
                            moving=False,
                            enemyHealth=0,
                            enemyAttack=0,
                            x=0,
                            y=0,
                            keys={},
                            id=0,
                            restart=True,
                            quit=False
                            )
        for player in self.connections:
            self.socket.sendto(message.SerializeToString(), (player.ip, player.port))

    def start_game(self):
        t = [datetime.now(), datetime.now()]
        scores = [0, 0]
        round_time = datetime.now()
        while True:

            if self.player_timeout(t):
                self.quit_game()
                break

            try:
                data, address = self.socket.recvfrom(self.BUFFER_SIZE)
            except Exception as e:
                continue

            game_update = pb.Update()
            game_update.ParseFromString(data)
            time_in_round = datetime.now() - round_time
            if game_update.enemyHealth <= 0 and time_in_round.total_seconds() > 5:
                scores[game_update.id] += 1
                if scores[game_update.id] == 3:
                    self.quit_game()
                    break
                round_time = datetime.now()
                self.restart_game()
                continue

            if game_update.y > 1000 and time_in_round.total_seconds() > 5:
                enemy = (game_update.id+1) % 2
                scores[enemy] += 1
                if scores[enemy] == 3:
                    self.quit_game()
                    break
                round_time = datetime.now()
                self.restart_game()
                continue

            if game_update.quit:
                self.quit_game()

            t[int(game_update.id)] = datetime.now()
            enemy = (game_update.id + 1) % 2
            p = self.connections[enemy]
            try:
                self.socket.sendto(game_update.SerializeToString(), (p.ip, p.port))
            except Exception as e:
                continue
            if game_update.quit:
                break

        self.socket.close()


# server listens for game requests and then creates a server on an unused port for the game
class MatchServer(object):

    def __init__(self, local_port):
        self.BUFFER_SIZE = 1024
        self.port = local_port
        # self.port_mappings = {1235: 16559,
        #                       1236: 16670,
        #                       1237: 16405,
        #                       1238: 16958,
        #                       1239: 16961,
        #                       1240: 17071,
        #                       1241: 16857,
        #                       1242: 17241,
        #                       1243: 16962,
        #                       1244: 16417
        #                       }
        self.port_mappings = {1235: 1235,
                              1236: 1236,
                              1237: 1237,
                              1238: 1238,
                              1239: 1239,
                              1240: 1240,
                              1241: 1241,
                              1242: 1242,
                              1243: 1243,
                              1244: 1244
                              }
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

            self.free_threads()
            try:
                data, address = self.socket.recvfrom(self.BUFFER_SIZE)
            except TimeoutError:
                continue
            except Exception as e:
                print(e)
                continue


            lobby_req = pb.CreateLobbyRequest()
            lobby_req.ParseFromString(data)
            response = pb.CreateLobbyResponse(ok=True, port=0, start=True)
            if lobby_req.lobbyCode not in self.lobby_codes:
                self.lobby_codes[lobby_req.lobbyCode] = address
                response.start = False
                self.socket.sendto(response.SerializeToString(), address)
                continue

            if len(self.free_ports) == 0:
                continue
            game_port = self.free_ports.pop(0)
            print("starting game on port %d\nactive game threads: %d\nfree ports: %s\n%s" % (game_port,
                                                                                             len(self.threads),
                                                                                             str(self.free_ports),
                                                                                             str(self.lobby_codes)))
            opponent = self.lobby_codes[lobby_req.lobbyCode]
            response.port = self.port_mappings[game_port]
            self.socket.sendto(response.SerializeToString(), address)

            self.socket.sendto(response.SerializeToString(), (opponent[0], opponent[1]))
            print(response)
            print("sending to : ", address)
            print("sending to : ", opponent)
            del self.lobby_codes[lobby_req.lobbyCode]

            game_thread = GameThread(game_port)
            self.threads.append(game_thread)
            game_thread.start()

    def free_threads(self):
        for i in range(len(self.threads) - 1, -1, -1):
            if self.threads[i].is_alive():
                continue

            if self.threads[i].local_port not in self.free_ports:
                self.free_ports.append(self.threads[i].local_port)

            self.threads.pop(i)


class GameThread(Thread):
    def __init__(self, local_port):
        super().__init__()
        self.local_port = local_port
        # shared list for threads to append to when finished

    def run(self):
        GameServer(self.local_port).create_lobby()


if __name__ == "__main__":
    MatchServer(1234).start()
