import socket
import cv2
import pickle
import struct


class Server:
    def __init__(self) -> None:
        self.HOST = ""
        self.PORT = 0
        self.isbinded = False

    def __del__(self):
        self.server.close()

    def schedule(self, event_input_name, event_input_value, QI, HOST, PORT):
        'Write your code here.'
        if event_input_name == 'INIT':
            "Write your handler for current event here."
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if not self.isbinded:
                self.server.bind((HOST, int(PORT)))
                self.server.listen(10)
                self.conn, self.addr = self.server.accept()
            self.isbinded = True
            self.data = b""
            self.payload_size = struct.calcsize(">L")
            STATUS = "self.payload_size: {}".format(self.payload_size)
            return event_input_value, 0, QI, STATUS

        if event_input_name == 'REQ':
            "Write your handler for current event here."
            while len(self.data) < self.payload_size:
                self.data += self.conn.recv(4096)
                if not self.data:
                    cv2.destroyAllWindows()
                    self.conn, self.addr = self.server.accept()
                    continue
            packed_msg_size = self.data[:self.payload_size]
            self.data = self.data[self.payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            while len(self.data) < msg_size:
                self.data += self.conn.recv(4096)
            frame_data = self.data[:msg_size]
            self.data = self.data[msg_size:]
            frame = pickle.loads(
                frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            cv2.imshow('server', frame)
            cv2.waitKey(1)
            return 0, event_input_value, QI, "Rec image"
