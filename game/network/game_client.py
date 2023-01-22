import socket
import sys

from proto import game_pb2 as pb


class GameClient(object):
    def __init__(self, local_port):
        # find local ip, get host by name returns "127.0.0.1" not good for testing on one network
        self.server_ip = None
        self.player_id = None
        self.server_port= None
        self.local_port = local_port
        self.BUFFER_SIZE = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.connect(("8.8.8.8", 80))
        self.local_ip = self.socket.getsockname()[0]
        self.socket.close()

    def host_game(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
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

    def join_game(self, ip_address, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_ip = ip_address
        self.server_port = port
        name = input("enter your name")
        join_req = pb.JoinLobbyRequest(name=name)
        self.socket.sendto(join_req.SerializeToString(),(ip_address,port))

        join_resp = pb.JoinLobbyResponse()
        while True:
            data, address = self.socket.recvfrom(self.BUFFER_SIZE)
            join_resp.ParseFromString(data)
            if not join_resp.ok:
                print("failed to join lobby")
                self.socket.close()
                sys.exit(1)

            if join_resp.start:
                self.player_id = join_resp.playerId
                break

    def character_select(self):
        char_req = pb.CharacterSelectRequest(id=self.player_id, character=0, lockedIn=True)

        self.socket.sendto(char_req.SerializeToString(), (self.server_ip, self.server_port))
        char_resp = pb.CharacterSelectResponse()
        while True:
            data, address = self.socket.recvfrom(self.BUFFER_SIZE)
            char_resp.ParseFromString(data)

            if char_resp.start:
                break






    def send_update(self, update_message: pb.Update):
        self.socket.sendto(update_message.SerializeToString(), (self.server_ip, self.server_port))

    def get_updates(self) -> list[pb.Update]:
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
        return result


if __name__ == "__main__":
    t = GameClient(1234)
