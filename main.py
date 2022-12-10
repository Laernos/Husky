import settings
import discord
from discord.ext import commands
from discord import app_commands

logger= settings.logging.getLogger('bot')

def run():
    intents= discord.Intents.all()
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        logger.info(f'User: {bot.user} (ID: {bot.user.id})')

        for cog_file in settings.COGS_DIR.glob("*.py"):
            if cog_file.name != "__init__.py":
                await bot.load_extension(f"cogs.{cog_file.name[:-3]}")        

        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        await bot.tree.sync(guild=settings.GUILDS_ID)



    @bot.command()
    async def reload(ctx, cog:str):
        await bot.reload_extension(f'cogs.{cog.lower()}')

    @bot.command()
    async def test(ctx):
        await ctx.send('Working!')


    @bot.hybrid_command()
    async def ping(ctx):
        await ctx.send("pong", ephemeral=True)
        
    @bot.tree.command()
    async def ciao(interaction: discord.Interaction):
        await interaction.response.send_message(f"Ciao! {interaction.user.mention}", ephemeral=True)



    @bot.tree.context_menu(name="Show join date")
    async def get_joined_date(interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(f"Member joined: {discord.utils.format_dt(member.joined_at)} ", ephemeral=True)
  
    @bot.tree.context_menu(name="Report Message")
    async def report_message(interaction: discord.Interaction, message: discord.Message):
        await interaction.response.send_message(f"Message reported ", ephemeral=True)

    @bot.tree.command(description='Shows member count')
    async def say(interaction: discord.Interaction):
        member_count = len(interaction.guild.members)
        embed=discord.Embed(title="Member Count", description=(f"There is {member_count} people in this server. "), color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)


    bot.run(settings.DISCORD_API_SECRET, root_logger=True)

if __name__ == '__main__':
    run()
