from config import Config
from locale_provider import Locale

Config.load_config()
Locale.init(Config.locale)

import discord
from secret_santa import SecretSantaCog


bot = discord.Bot(intents=discord.Intents.all())
bot.add_cog(SecretSantaCog(bot))

bot.run(Config.token)