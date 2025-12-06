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

    def decode(self, json_dict) -> None:
        messages = []
        for msg_dict in json_dict["messages"]:
            message = Message(
                ciphertext=bytes.fromhex(msg_dict["ciphertext"]),
                mac=bytes.fromhex(msg_dict["mac"]),
                iv=bytes.fromhex(msg_dict["iv"]) if msg_dict["iv"] else b""
            )
            messages.append(message)
        self.messages = messages
    
    def encode(self) -> dict:
        json_dict = {"messages": []}
        for message in self.messages:
            msg_dict = {
                "ciphertext": message.ciphertext.hex(),
                "mac": message.mac.hex(),
                "iv": message.iv.hex() if message.iv else ""
            }
            json_dict["messages"].append(msg_dict)
        return json_dict