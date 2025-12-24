import os
import json
from pathlib import Path
from typing import Dict


class Storage:
	__base_path = Path(__file__).resolve().parent 
	_secret_santa_data_path = __base_path.parent / 'data/secret_santa_data.json'

	@classmethod
	def prepare_path(cls) -> None:
		if not os.path.exists(directory := os.path.split(cls._secret_santa_data_path)[0]):
			os.mkdir(directory)

		if not os.path.exists(cls._secret_santa_data_path):
			with open(cls._secret_santa_data_path, 'w', encoding='utf-8') as file:
				file.write(cls.__obfuscate('{}'))

	@classmethod
	async def save_file(cls, json_data: Dict[str, Dict[str, str]]) -> None:
		cls.prepare_path()
		with open(cls._secret_santa_data_path, 'w', encoding='utf-8') as file:
			file.write(cls.__obfuscate(json.dumps(json_data, indent=4, ensure_ascii=False)))

	@classmethod
	async def load_data(cls) -> Dict[str, Dict[str, str]]:
		cls.prepare_path()

		try:
			with open(cls._secret_santa_data_path, 'r', encoding='utf-8') as file:
				return json.loads(cls.__obfuscate(file.read()))
		except Exception as e:
			print(f'Error loading secret santa data from file {cls._secret_santa_data_path}: {e}')

	@staticmethod
	def __obfuscate(text: str) -> str:
		return ''.join(chr(ord(c) ^ 1024) for c in text)