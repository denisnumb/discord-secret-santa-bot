import discord
from discord.ui import Modal, InputText
from typing import Dict
from locale_provider import LocaleKeys, translate


class SecretSantaModel:
    def __init__(self, wishes: str, member: discord.Member) -> None:
        self.wishes: str = wishes
        self.member: discord.Member = member

    def get_dict(self) -> dict:
        _dict = self.__dict__.copy()
        if self.member:
            _dict['member'] = self.member.id
        return _dict

class SecretSantaModal(Modal):
    def __init__(
        self, 
        members: Dict[discord.Member, SecretSantaModel], 
        member: discord.Member
        ) -> None:
        title = translate(LocaleKeys.Label.modal_title)
        wishes = InputText(
            label=translate(LocaleKeys.Label.modal_input_title),
            placeholder=translate(LocaleKeys.Label.modal_input_placeholder),
            value=members.get(member) and members[member].wishes,
            style=discord.InputTextStyle.long,
            required=False,
            max_length=750
        )
        self.members = members
        super().__init__(wishes, title=title, timeout=None)