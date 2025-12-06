from dataclasses import dataclass
from typing import List

@dataclass
class Message:
    ciphertext: bytes
    mac: bytes
    iv: bytes # if present we know this ciphertext is a concatenation of the key + ciphertext

class History:
    def __init__ (self):
        """
        As dictated by the project directions, the first
        message in the history is always the concatenation
        of the ciphertext for the AES key and the plaintext
        message. This first message will be the only one 
        with a non-empty iv field. This is done because
        the directions specified that the MAC must cover
        both the AES key and the message.
        """
        self.messages: List[Message] = []