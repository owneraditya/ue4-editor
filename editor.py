import struct
import os

class Editor:
    def __init__(self, data, path):
        self.data = bytearray(data)
        self.path = path

    def write_float(self, offset, value):
        self.data[offset:offset+4] = struct.pack('<f', value)

    def save(self):
        backup = self.path + ".bak"
        if not os.path.exists(backup):
            with open(backup, "wb") as f:
                f.write(self.data)

        with open(self.path, "wb") as f:
            f.write(self.data)