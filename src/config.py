import json
from pathlib import Path
from typing import List
from datetime import datetime
from dateutil import parser


class Config:
    __base_path = Path(__file__).resolve().parent 
    _config_path = __base_path.parent / 'config.json'

    token: str = ''
    guild_ids: List[int] = [0]
    utc_offset_hours: int = 0
    event_end_datetime: datetime = datetime(datetime.now().year, 12, 25, 23, 59, 59)
    gift_budget: int = 1000
    locale: str = 'en_us'

    @classmethod
    def load_config(cls):
        with open(cls._config_path, 'r', encoding='utf-8') as config_file:
            data = json.load(config_file)
            cls.token = data['token']
            cls.guild_ids = [data['guild_id']]
            cls.utc_offset_hours = data['utc_offset_hours']
            cls.event_end_datetime = parser.parse(data['event_end_datetime'])
            cls.gift_budget = data['gift_budget']
            cls.locale = data['locale']