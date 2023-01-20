import socket
from proto import game_pb2 as pb


class GameClient(object):
    def __init__(self, local_port):
        # find local ip, get host by name returns "127.0.0.1" not good for testing on one network
        self.enemy_address = None
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
        self.socket.sendto("let me in".encode(), (ip_address, port))
        self.socket.setblocking(False)
        data = None
        # wait for join message
        while data is None:
            try:
                data, address = self.socket.recvfrom(self.BUFFER_SIZE)
                self.enemy_address = address
            except:
                continue
        print(self.enemy_address)
        if self.enemy_address is None:
            raise ConnectionAbortedError

    def send_update(self, update_message: pb.Update):
        self.socket.sendto(update_message.SerializeToString(), self.enemy_address)

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
