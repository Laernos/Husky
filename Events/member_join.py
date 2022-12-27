import discord
from discord import File
from discord.ext import commands
from easy_pil import Editor, load_image_async, Font


class Member_join(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self,member):
        
        try:
            a=await self.bot.server_config.find_field_value(member.guild.id,'commands', 'welcome_cmnd', 'status')
            if a is True:
                b=await self.bot.server_config.find_field_value(member.guild.id, 'commands', 'welcome_cmnd', 'channel')
                channel=self.bot.get_channel(int(b))
                background= Editor('pic3.png')
                profile_image = await load_image_async(str(member.avatar.url))
                profile = Editor(profile_image).resize((200,200)).circle_image()
                poppins = Font.poppins(size=50, variant='bold')
                poppins_small= Font.poppins(size=20, variant='light')
                background.paste(profile, (756,77))
                background.text((450,140), f'{member.name}#{member.discriminator}', color='white', font=poppins, align='center')
                file= File(fp=background.image_bytes, filename='pic1.jpg')
                message= await self.bot.server_config.find_field_value(member.guild.id, 'commands', 'welcome_cmnd', 'message') or (f'Welcome to {member.guild.name}')
                await channel.send(message)
                await channel.send(file=file)
        except KeyError:
            pass


       # try:
       #     if self.bot.muted_users[member.id]:
       #         role = discord.utils.get(member.guild.roles, name= 'Muted')
       #         if role:
       #             await member.add_roles(role)
       #             print(f'Remuted {member.display_name} upon guild entry')
       # except KeyError:
       #     pass


async def setup(bot):
    await bot.add_cog(Member_join(bot))