"""
Custom models for Aiotdlib.
"""
from dataclasses import dataclass


@dataclass
class MessageInfo:
    chat_id: int
    message_id: int

    def __str__(self):
        return f'{self.chat_id}:{self.message_id}'

    @staticmethod
    def from_str(msg_info_str: str) -> 'MessageInfo':
        chat_id, message_id = map(int, msg_info_str.split(':'))
        return MessageInfo(chat_id, message_id)
