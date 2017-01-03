import discord
import re
from discord.ext import commands
from sys import argv

class Events:
    """
    Logs join and leave messages, bans and unbans, and member changes.
    """
    def __init__(self, bot):
        self.bot = bot
        print('Addon "{}" loaded'.format(self.__class__.__name__))

    async def scan_message(self, message):
        if message.author == self.bot.server.me or self.bot.staff_role in message.author.roles:  # don't process messages by the bot
            return
        msg = message.content.lower()
        contains_invite_link = "discordapp.com/invite" in msg or "discord.gg" in msg
        # special check for a certain thing
        contains_fs_repo_url = re.match('(.*)notabug\.org\/(.*)\/freeshop(.*)', msg, re.IGNORECASE)
        contains_piracy_site_mention = any(x in msg for x in ('3dsiso', '3dschaos', 'iso site', 'chaos site'))
        if contains_invite_link:
            await self.bot.send_message(self.bot.mods_channel, "✉️ **Invite posted**: {} posted an invite link in {}".format(message.author.mention, message.channel.mention))
        if contains_fs_repo_url != None:
            await self.bot.delete_message(message)
            await self.bot.send_message(self.bot.mods_channel, "**Bad URL**: {} posted a freeShop Repo URL in {} (message deleted)".format(message.author.mention, message.channel.mention))
        if contains_piracy_site_mention:
            await self.bot.delete_message(message)
            await self.bot.send_message(self.bot.mods_channel, "**Bad site**: {} mentioned a piracy site in {} (message deleted)".format(message.author.mention, message.channel.mention))

    async def on_message(self, message):
        await self.scan_message(message)

    async def on_message_edit(self, message_before, message_after):
        await self.scan_message(message_after)

def setup(bot):
    bot.add_cog(Events(bot))
