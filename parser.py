import struct

class UE4Parser:
    def __init__(self, data):
        self.data = data
        self.names = []
        self.exports = []

    def read_int(self, o):
        return struct.unpack_from("<i", self.data, o)[0]

    def read_name(self, o):
        length = self.read_int(o)
        o += 4
        name = self.data[o:o+length].decode(errors="ignore")
        o += length + 4
        return name, o

    def parse_names(self):
        count = self.read_int(0x18)
        offset = self.read_int(0x1C)

        for _ in range(count):
            name, offset = self.read_name(offset)
            self.names.append(name)

    def parse_exports(self):
        count = self.read_int(0x88)
        offset = self.read_int(0x8C)

        for i in range(count):
            try:
                name_index = struct.unpack_from("<i", self.data, offset+0x0C)[0]
                name = self.names[name_index] if name_index < len(self.names) else "Unknown"

                self.exports.append({
                    "index": i,
                    "name": name,
                    "offset": offset
                })

                offset += 0x68
            except:
                break

    def parse(self):
        self.parse_names()
        self.parse_exports()
        return self.exports