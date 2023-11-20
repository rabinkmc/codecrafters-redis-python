class RDBParser:
    def __init__(self, path):
        fp = open(path, "rb")
        assert fp.read(5) == b"REDIS"
        fp.read(4)
        self.auxiliary_filed = self.get_auxiliary_fields(fp)
        assert fp.read(3) == b"\xfe\x00\xfb"
        self.hash_table_size = self.get_length_encoded_int(fp)
        self.expiry_table_size = self.get_length_encoded_int(fp)
        self.key_values = self.get_key_value_dict(fp)

    def get_encoded_string(self, fp):
        encoding_byte = int(fp.read(1)[0])
        encoding_bits = encoding_byte >> 6
        if encoding_bits == 0:
            # next 6 bits are length
            len = encoding_byte & 0b00111111
            return fp.read(len).decode()
        elif encoding_bits == 1:
            # next 14 bits excluding the 2 encoding bits
            first_byte = encoding_bits & 0b00111111
            next_byte = int(fp.read(1)[0])
            len = (first_byte << 8) | next_byte
            return fp.read(len).decode()
        elif encoding_bits == 2:
            len = int.from_bytes(fp.read(4), byteorder="big")
            return fp.read(len).decode()
        elif encoding_bits == 3:
            special_type = encoding_byte & 0b00111111
            if special_type == 0:
                return int.from_bytes(fp.read(1), byteorder="big")
            if special_type == 1:
                return int.from_bytes(fp.read(2), byteorder="big")
            if special_type == 2:
                return int.from_bytes(fp.read(4), byteorder="big")
            else:
                # not handled
                return -1

    def get_length_encoded_int(self, fp):
        encoding_byte = int(fp.read(1)[0])
        encoding_bits = encoding_byte >> 6
        len = -1
        if encoding_bits == 0:
            len = encoding_byte & 0b00111111
        elif encoding_byte == 1:
            first_byte = encoding_byte & 0b00111111
            next_byte = int(fp.read(1)[0])
            len = (first_byte << 8) | next_byte
        elif encoding_byte == 2:
            len = int.from_bytes(fp.read(4), byteorder="big")
        return len

    def get_auxiliary_fields(self, fp):
        auf = {}
        while fp.peek(1)[:1] == b"\xfa":
            fp.read(1)  # skip \xfa
            key = self.get_encoded_string(fp)
            value = self.get_encoded_string(fp)
            auf[key] = value
        return auf

    def get_key_value_dict(self, fp):
        map = {}
        while fp.peek(1)[:1] != b"\xff":
            fp.read(1)
            key = self.get_encoded_string(fp)
            value = self.get_encoded_string(fp)
            map[key] = value
        return map
