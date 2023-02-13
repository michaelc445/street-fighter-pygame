import socket
import sys
import time
from proto import game_pb2 as pb


class GameClient(object):
    def __init__(self, local_port):
        # find local ip, get host by name returns "127.0.0.1" not good for testing on one network
        self.game_port = None
        self.mm_port = None
        self.server_ip = None
        self.player_id = None
        self.server_port = None
        self.local_port = local_port
        self.BUFFER_SIZE = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.local_char = 0
        self.enemy_char = 0
        self.messages= []
        self.enemy_resp = pb.CharacterSelectResponse(enemyCharacter=0)

    def host_game(self):
        self.socket.bind((self.local_ip, self.local_port))
        self.socket.setblocking(False)
        # check for requests to join
        # wait until there is a join message then return socket and address of player
        data = None
        while data is None:
            try:
                data, address = self.socket.recvfrom(self.BUFFER_SIZE)
                self.socket.sendto("ready".encode(), address)
                self.enemy_address = address
                print("connected")
            except:
                continue
        print(self.enemy_address)
        if self.enemy_address is None:
            raise ConnectionAbortedError
    def join_lobby(self,ip_address,port,lobby_code):
        self.server_ip = ip_address
        self.mm_port = port
        lobby_req = pb.CreateLobbyRequest(lobbyCode=lobby_code)
        self.socket.sendto(lobby_req.SerializeToString(), (ip_address, port))

        lobby_resp = pb.CreateLobbyResponse()
        while True:
            data, address = self.socket.recvfrom(self.BUFFER_SIZE)
            lobby_resp.ParseFromString(data)
            if not lobby_resp.ok:
                print("failed to join lobby")
                self.socket.close()
                sys.exit(1)

            self.game_port = lobby_resp.port
            if lobby_resp.start:
                break

    def join_game(self, ip_address, port, name):
        self.server_ip = ip_address
        self.game_port = port
        join_req = pb.JoinLobbyRequest(name=name)
        self.socket.sendto(join_req.SerializeToString(), (ip_address, port))

        join_resp = pb.JoinLobbyResponse()
        while True:
            data, address = self.socket.recvfrom(self.BUFFER_SIZE)
            join_resp.ParseFromString(data)
            if not join_resp.ok:
                print("failed to join lobby")
                self.socket.close()
                sys.exit(1)

            self.player_id = join_resp.playerId
            if join_resp.start:
                break

    def character_select(self):
        char_req = pb.CharacterSelectRequest(id=self.player_id, character=0, lockedIn=True)

        self.socket.sendto(char_req.SerializeToString(), (self.server_ip, self.game_port))
        char_resp = pb.CharacterSelectResponse()
        while True:
            data, address = self.socket.recvfrom(self.BUFFER_SIZE)
            char_resp.ParseFromString(data)

            if char_resp.start:
                break
    def quit_game(self):
        message = pb.Update(health=0,
                            enemyMove=0,
                            moving=False,
                            enemyHealth=0,
                            enemyAttack=0,
                            x=0,
                            y=0,
                            keys={},
                            id=self.player_id,
                            quit=True
                            )
        self.socket.sendto(message.SerializeToString(),(self.server_ip,self.game_port))
    def connect(self, ip, port, name):
        self.join_lobby(ip,port,"")
        time.sleep(2)
        self.join_game(ip, self.game_port, name)



    async def send_update(self, update_message: pb.Update):
        self.socket.sendto(update_message.SerializeToString(), (self.server_ip, self.game_port))

    async def get_updates(self, local_player, enemy_character, SCREEN_WIDTH, SCREEN_HEIGHT, screen, obstacles):
        for message in self.get_update():
            local_player.health = message.enemyHealth
            enemy_character.move_enemy(SCREEN_WIDTH, SCREEN_HEIGHT, screen, local_player, obstacles, message.keys,
                                       message.x, message.y)
    async def get_enemy_character(self):
        char_resp = pb.CharacterSelectResponse()
        try:
            data, address = self.socket.recvfrom(self.BUFFER_SIZE)
            char_resp.ParseFromString(data)
            return char_resp
        except:
            return None
    async def send_character_choice(self,choice, locked_in):
        char_req = pb.CharacterSelectRequest(id=self.player_id, character=choice, lockedIn=locked_in)
        self.socket.sendto(char_req.SerializeToString(), (self.server_ip, self.game_port))
    async def get_update(self) -> list[pb.Update]:
        result: list[pb.Update] = []
        data = 1

        while data is not None:
            try:
                data, addr = self.socket.recvfrom(self.BUFFER_SIZE)
                if data is None:
                    break
                message = pb.Update()
                message.ParseFromString(data)
                result.append(message)
            except:
                break
        self.messages = result
        return result


if __name__ == "__main__":
    t = GameClient(1234)
