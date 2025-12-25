# Discord Music Bot

🎅 A simple Discord bot for organizing Secret Santa event.

---

## 🚀 Quick start:

1. Clone the repository:
```cmd
git clone https://github.com/denisnumb/discord-secret-santa-bot.git
```
2. Set up the configuration file (`config.json`):
```json
{
    "token": ". . .",
    "guild_id": 784123392834714566231,
    "utc_offset_hours": 5,
    "event_end_datetime": "2025-12-25T04:41:30",
    "gift_budget": 100,
    "locale": "en_us"
}
```
Configuration parameters:
- `token` — Bot token
- `guild_id` — The Discord server ID where the event is being hosted
- `utc_offset_hours` — Your time zone. For `UTC+5`, this value would be `5`
- `event_end_datetime` — The exact time for determining secret Santas, regardless of time zone
- `gift_budget` — Gift purchase budget. The currency is defined in the localization file in the `locales` directory.
- `locale` — Bot locale

🐍 Run simple
```cmd
python src/main.py
```

🐋 Run using docker:
```cmd
docker compose up --build
```

## 🎅 Usage example:

- On the server where the event is being held, enter the command `/secret_santa`

![start](https://github.com/user-attachments/assets/4fa7a0f8-a9ca-4c9b-a6cf-af2ffcc94912)

- Click the button to participate and indicate your gift wishes, or leave the field blank—you can change your wishes later *(But no later than an hour before the end of the event)*.

![wishes](https://github.com/user-attachments/assets/c68a5294-06d1-47ec-a5a2-8c698702d09b)

ℹ️ You are now participating in the event! Use the buttons below to change your preferences or cancel your participation. This message is visible only to the user who initiated the command—other participants will not see your preferences.

ℹ️ You can type the command `/secret_santa` again to see this message.

![registred_member](https://github.com/user-attachments/assets/d3864689-cf60-41e0-be21-f0ddc609afb1)

---

- When the time comes, the bot will distribute the participants among themselves, and each participant will receive information in direct messages about who they are a Secret Santa for and the wishes of the other participant.

denisnumb's DM with bot:

![results](https://github.com/user-attachments/assets/7945808c-77d2-47d2-8a42-7ea06c792977)

xeon's DM with bot:

![results](https://github.com/user-attachments/assets/c8aa0f5f-ef46-4a27-b295-8a7e9a8002a5)

---

# QA

❓ How to restart the Secret Santa event?

💬 To restart the event, stop the bot and delete the `data/secret_santa_data.json` file.

ℹ️ If the bot is running in a Docker container, you don't need to recreate anything — this file is used directly from the host machine.

---

❓ Why is there a strange string of characters inside the file `secret_santa_data.json`? How can I get the JSON?

💬 Instead of a direct JSON representation, the file contains an obfuscated set of characters to preserve the intrigue and mystery of each Santa. If for some reason you need to obtain the actual file contents, apply the `__obfuscate` method from the file [`src/storage.py`](https://github.com/denisnumb/discord-secret-santa-bot/blob/main/src/storage.py) to its text.

---

❓ How do I change the end date and time of an event?

💬 There is currently no command for this, so you need to turn off the bot, specify a new value for the `event_end_datetime` parameter in `config.json` and turn the bot back on.

ℹ️ If the bot is running in a Docker container, you don't need to recreate anything — this file is used directly from the host machine.


