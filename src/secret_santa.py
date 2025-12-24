import discord
import random
import asyncio
from typing import Dict, Tuple
from discord.ext import tasks
from discord.ui import View, Button
from datetime import datetime, timezone, timedelta
from model import SecretSantaModel, SecretSantaModal
from config import Config
from storage import Storage
from locale_provider import LocaleKeys, translate


class SecretSantaCog(discord.Cog, name='secret_santa'):
	__is_cog_loaded = False
	event_end_date = Config.event_end_datetime
	event_end_date_tz = event_end_date.replace(tzinfo=timezone(timedelta(hours=Config.utc_offset_hours)))
	event_end_date_time_tz = event_end_date.time().replace(tzinfo=timezone(timedelta(hours=Config.utc_offset_hours)))
	data: Dict[discord.Member, SecretSantaModel] = {}
	gift_budget = Config.gift_budget

	def __init__(self, bot: discord.Bot) -> None:
		self.bot: discord.Bot = bot

	@property
	def gift_budget_str(self) -> str:
		return f'💵 **{translate(LocaleKeys.Label.budget)}:** {self.gift_budget}{translate(LocaleKeys.Label.currency_symbol)}'

	@property
	def current_time(self) -> datetime:
		return datetime.utcnow() + timedelta(hours=Config.utc_offset_hours) 

	async def save_members(self) -> None:
		await Storage.save_file({str(member.id): model.get_dict() for member, model in self.data.items()})

	@discord.Cog.listener()
	async def on_ready(self) -> None:
		if self.__is_cog_loaded:
			return
		self.__is_cog_loaded = True

		raw_members = await Storage.load_data()
		guild = self.bot.get_guild(Config.guild_ids[0])
		get_member = lambda id: discord.utils.get(guild.members, id=int(id)) if id else None

		for id, model in raw_members.items():
			self.data[get_member(id)] = SecretSantaModel(
				model['wishes'], 
				get_member(model['member'])
			)

		if self.current_time < self.event_end_date:
			self.define_secret_santa.start()

	@discord.slash_command(
		name='secret_santa', 
		description=translate(LocaleKeys.Label.command_desc), 
		guild_ids=Config.guild_ids
	)
	async def secret_santa(self, ctx: discord.ApplicationContext) -> None:
		if ctx.author in self.data.keys():
			if self.current_time > self.event_end_date and len(self.data) <= 1:
				return await ctx.respond(translate(LocaleKeys.Info.few_users), ephemeral=True)

			embed, view = self.get_registered_santa_message_data(ctx.author)
			return await ctx.respond(embed=embed, view=view, ephemeral=True)

		if self.current_time > self.event_end_date:
			return await ctx.respond(translate(LocaleKeys.Info.registration_closed), ephemeral=True)

		view = View(timeout=None)
		start_button = Button(label=translate(LocaleKeys.Label.take_part),  emoji='🎅', style=discord.ButtonStyle.red)
		start_button.callback = self.open_secret_santa_modal
		view.add_item(start_button)

		await ctx.respond(
			embed=discord.Embed(
				title=translate(LocaleKeys.Label.ask_take_part),
				description=translate(LocaleKeys.Label.event_desc),
				color=discord.Colour.red()
			),
			view=view,
			ephemeral=True
		)
	
	@tasks.loop(time=event_end_date_time_tz)
	async def define_secret_santa(self) -> None:
		await asyncio.sleep(2)

		if self.current_time < self.event_end_date:
			return

		if len(self.data) <= 1:
			self.define_secret_santa.stop()
			return print('There are too few users participating in the event! At least 2 participants are required to determine the Secret Santa.')

		all_members = list(self.data.keys())
		santas_with_members = {}

		for santa in all_members:
			if (members_to_choice := [m for m in all_members if m != santa and m not in santas_with_members.values()]):
				member = random.choice(members_to_choice)
				santas_with_members[santa] = member
			else:
				random_old_santa = random.choice(list(santas_with_members.keys()))
				santas_with_members[santa] = santas_with_members.pop(random_old_santa)
				santas_with_members[random_old_santa] = santa


		for santa, member in santas_with_members.items():
			self.data[santa].member = member

		await self.save_members()

		for member, model in self.data.items():
			await member.send(embed=discord.Embed(
				title=translate(LocaleKeys.Info.santa_defined),
				description=self.get_santas_member_embed_description(model.member) + '\n\n' + self.gift_budget_str,
				color=discord.Colour.red()
			))

		self.define_secret_santa.stop()

	async def modal_callback(self, interaction: discord.Interaction) -> None:
		wishes: str = interaction.data['components'][0]['components'][0]['value']
		if not wishes or wishes.isspace():
			wishes = None

		member = self.data.get(interaction.user) and self.data[interaction.user].member

		self.data[interaction.user] = SecretSantaModel(wishes=wishes, member=member)
		await self.save_members()

		embed, view = self.get_registered_santa_message_data(interaction.user)
		await interaction.edit(embed=embed, view=view)

	async def open_secret_santa_modal(self, interaction: discord.Interaction) -> None:
		modal = SecretSantaModal(self.data, interaction.user)
		modal.callback = self.modal_callback
		await interaction.response.send_modal(modal)

	def get_santas_member_embed_description(self, member: discord.Member) -> str:
		member_wishes_text = (
			translate(LocaleKeys.Info.member_has_no_wishes, member.mention)
			if not (member_wishes := self.data[member].wishes)
			else translate(LocaleKeys.Info.member_wishes, member.mention, member_wishes)
		)
		return translate(LocaleKeys.Info.member_embed_desc, member.mention, member_wishes_text)

	def get_registered_santa_message_data(self, author: discord.Member) -> Tuple[discord.Embed, View]:
		if (member := self.data[author].member):
			description = self.get_santas_member_embed_description(member)
		else:
			description = translate(LocaleKeys.Info.not_yet, int(self.event_end_date_tz.timestamp()))

		author_wishes_text = (
			translate(LocaleKeys.Info.no_wishes)
			if not (author_wishes := self.data[author].wishes)
			else f'{translate(LocaleKeys.Info.wishes)} {author_wishes}'
		)

		description += f'\n\n🎁 {author_wishes_text}'
		description += f'\n\n' + self.gift_budget_str
		description += f'\n\n**{translate(LocaleKeys.Info.all_members)}:**\n' + '\n'.join(member.mention for member in self.data.keys())

		embed = discord.Embed(
			title=translate(LocaleKeys.Info.you_are_member),
			description=description,
			color=discord.Colour.red()
		)

		view = None
	
		if (self.event_end_date - self.current_time).total_seconds() > 3600:
			view = View(timeout=None)

			change_wishes_button = Button(label=translate(LocaleKeys.Label.change_wishes), emoji='🎁', style=discord.ButtonStyle.red)
			change_wishes_button.callback = self.open_secret_santa_modal
			view.add_item(change_wishes_button)

			dont_participate_button = Button(label=translate(LocaleKeys.Label.leave_event), emoji='❌', style=discord.ButtonStyle.red)
			dont_participate_button.callback = self.unregister_member
			view.add_item(dont_participate_button)

		return embed, view

	async def unregister_member(self, interaction: discord.Interaction) -> None:
		if interaction.user in self.data.keys():
			self.data.pop(interaction.user)

		await self.save_members()

		await interaction.edit(
			content=translate(LocaleKeys.Info.you_are_no_longer_member), 
			embed=None,
			view=None,
			delete_after=10
		)
