import os
import json
from pathlib import Path
from typing import Dict


def translate(key: str, *args) -> str:
	return Locale.translate(key, * args)

class Locale:
	__base_path = Path(__file__).resolve().parent 
	_locales_path = __base_path.parent / 'locales'
	_locale_data: Dict[str, str] = {}

	@classmethod
	def init(cls, locale_code: str):
		locale_file = locale_code + '.json'

		if locale_file not in os.listdir(cls._locales_path):
			locale_file = "en_us.json"

		with open(cls._locales_path / locale_file, 'r', encoding='utf-8') as file:
			Locale._locale_data = json.load(file)

	@classmethod
	def translate(cls, key: str, *args) -> str:
		return cls._locale_data.get(key, key).format(*args)

class LocaleKeys:
    class Label:
        modal_title = 'label.modal_title'
        modal_input_title = 'label.modal_input_title'
        modal_input_placeholder = 'label.modal_input_placeholder'
        budget = 'label.budget'
        currency_symbol = 'label.currency_symbol'
        command_desc = 'label.command_desc'
        take_part = 'label.take_part'
        ask_take_part = 'label.ask_take_part'
        event_desc = 'label.event_desc'
        change_wishes = 'label.change_wishes'
        leave_event = 'label.leave_event'

    class Info:
        registration_closed = 'info.registration_closed'
        santa_defined = 'info.santa_defined'
        member_has_no_wishes = 'info.member_has_no_wishes'
        member_wishes = 'info.member_wishes'
        member_embed_desc = 'info.member_embed_desc'
        not_yet = 'info.not_yet'
        no_wishes = 'info.no_wishes'
        wishes = 'info.wishes'
        all_members = 'info.all_members'
        you_are_member = 'info.you_are_member'
        you_are_no_longer_member = 'info.you_are_no_longer_member'
        few_users = 'info.few_users'