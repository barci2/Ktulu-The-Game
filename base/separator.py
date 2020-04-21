#####################################################################################
###     Class used by both networkers: client and server to inlcude separator     ###
#####################################################################################

class Separator:
    separator = b'\x03\x01'

    @staticmethod
    def add_separator(bytestring):
        output = b''
        for char in bytestring:
            if char == 1:
                output = output + b'\x02\x01'
            else:
                output = output + bytes([char])
        return output

    @staticmethod
    def remove_separator(bytestring):
        output = b''
        previous_char = 0
        for char in bytestring:
            if char == 2:
                if previous_char == 2:
                    output = output + bytes([2])
                previous_char = 2
            elif char == 1:
                if previous_char == 2:
                    output = output + bytes([1])
            else:
                output = output + bytes([char])
        return output