import discord
from discord.ext import commands
from discord import app_commands, ui
from datetime import datetime
import platform
import psutil
from dateutil.relativedelta import relativedelta
import emotes as e
import asyncio
import os

GUILD_INVITE = os.getenv("GUILD_INVITE")
STATUS_PAGE = os.getenv("STATUS_PAGE")
BOT_INVITE_LINK = os.getenv("BOT_INVITE_LINK")
BUG_REPORT_CHANNEL_ID = int(os.getenv("BUG_REPORT_CHANNEL_ID"))
OWNER_ID = int(os.getenv("OWNER_ID"))



class Bug(discord.ui.Modal, title='Bug Report'):
    
    description = ui.TextInput(label='Description', style=discord.TextStyle.paragraph, placeholder='A brief description of the bug.')
    reproduce = ui.TextInput(label='Steps to Reproduce', style=discord.TextStyle.paragraph, placeholder='Please list each action necessary to make the bug happen.')
    result = ui.TextInput(label='Expected Result', style=discord.TextStyle.paragraph, placeholder='What should happen if the bug wasn\'t there?')
    ac_result = ui.TextInput(label='Actual Result', style=discord.TextStyle.paragraph, placeholder='What actually happens if you follow the steps.')
    add_info=ui.TextInput(label='Additional Info (optional) ', style=discord.TextStyle.paragraph, placeholder='More info or screenshot urls (https://imgur.com/6IS1jmH.png)', required=False)

    async def on_submit(self, interaction:discord.Interaction):
        channel= interaction.client.get_channel(BUG_REPORT_CHANNEL_ID)
        dm= await interaction.user.create_dm()
        embed1=discord.Embed(title='Bug Report Submission', description='')
        embed1.add_field(name='USER', value=f'{interaction.user.name}#{interaction.user.discriminator}\n`{interaction.user.id}`')
        embed1.add_field(name='GUILD', value=f'{interaction.guild.name}\n`{interaction.guild_id}`')
        embed1.add_field(name='MEMBER #', value= len(interaction.guild.members))
        embed2=discord.Embed(title='Description', description=self.description,)
        embed3=discord.Embed(title='Steps to Reproduce', description=self.reproduce)
        embed4=discord.Embed(title='Expected Result', description=self.result)
        embed5=discord.Embed(title='Actual Result', description=self.ac_result)
        embed6=discord.Embed(title='Additional Info', description=self.add_info,timestamp= datetime.now())
        embeds=[embed1,embed2,embed3,embed4,embed5,embed6]
        await channel.send(f'New Bug Reported! <@{OWNER_ID}>')
        try:
            await dm.send(f'Here is a copy of your submission')
            await interaction.response.send_message(f'Thank you for your submission! A copy of your subbmission has been sent to your dms', ephemeral=True)
        except:
            await interaction.response.send_message(f'Thank you for your submission! Copy couldn\'t send because your dm\'s are closed.', ephemeral=True)    
        #To DO: Bot doesnt send copy if user dms are closed
        for embed in embeds:
            try:
                await dm.send(embed=embed)
            except:
                pass
            await channel.send(embed=embed)

module=''
status=''

async def info_data():
    modules_info = {
        "welcome": {
            "title": "Welcoming",
            "description": "The welcome module is a feature that allows you to customize the greeting message that is sent to new members when they join your server.\n\n \
                the bot will send a banner card to the designated channel every time a new member joins the server. The banner card will include the new member's name and profile picture.\n\n \
                The welcome module is a great way to make new members feel welcomed and included in your server. Have fun greeting your new members!    ",
           "field":{
            }
        },
        "logging": {
            "title": "LOGGING",
            "description": "The Logging module is a comprehensive tracking system designed to keep a detailed record of all activities within your server. It helps maintain order and provides valuable insights into user interactions.\n\n \
             **All:** This captures every single event on the server, giving you a complete overview in one place. \n\n  **Server Logging:** Tracks key server-wide events, such as role changes, channel updates, and server settings alterations. \n\n \
             **Member** Logging: Monitors individual member actions like joins, leaves, nickname changes, and role assignments. \n\n **Moderation Logging:** Records all moderation actions, such as kicks, bans, mutes, and warnings, providing a clear audit trail for moderators' actions. \n\n \
             **Message Logging:** Keeps a record of message activities, including message edits and deletions, which can be crucial for resolving disputes and monitoring compliance with server rules. \n\n \
             **Voice Logging:** Logs all voice channel activities, such as users joining or leaving voice channels, which can be useful for managing voice chat and resolving any related issues. \n\n **Invite Logging:** Tracks who is inviting new members to the server with their invite links, allowing you to understand how new members are finding your server. \n\n \
             **Activity Logging:** Keeps track of user statuses, such as when members start or stop playing games. This allows moderators to see who is active and what games are popular within the community. \n\n This Logging module is an essential tool for administrators and moderators to ensure a safe and well-managed Discord community.",
           "field":{
            }
        },
        "report": {
            "title": "Report Member/Message",
            "description": "The report module is a context menu, it allows member to access additional options by right-clicking on a member or message in the server.\n\n \
                If members right-click on a member, they will see an option to report them. If they select this option, they will be asked to provide a reason for the report.\n \
                This report will be sent to the server moderators.\n\nIf members right-click on a message, they will see an option to report the message. If they select this option, they will be asked to provide a reason for the report.\n \
                This report will be sent to the server moderators.",
           "field":{
            }
        },        
        "guess": {
            "title": " 💯 Guessing Numbers",
            "description": "Welcome to the guessing the numbers! In this activity, the bot will create a random number between 0 and 100 and users will try to guess the number.\n\n \
                To participate, simply type your guess in the designated channel.\n\n\
                If you try to guess the number 5 times without success, the bot will give you a hint by saying the number is between two specific numbers (e.g. \"The number is between 50 and 75\").\n\n\
                The first person to guess the correct number wins the event. Have fun guessing!",
           "field":{
            }
        },
        "count": {
            "title": "🔢 Counting Numbers",
            "description": "Welcome to the counting numbers! In this activity, members can participate by counting up in order.\n\n\
                To join the event, simply type a number in the channel. The next person must then type the next number in the sequence, and so on.\n\n \
                Rules:\nOnly numbers are allowed (no decimals or negative numbers).\nYou must type the next number in the sequence (e.g. if the last number typed was 3, you must type 4).\n \
                Do not type a number that has already been used.\nDo not spam the channel with numbers.",
           "field":{
            }
        },       
    } 
    return modules_info   

async def data(interaction, update=None):
    moduller= await interaction.client.server_config.find_document(interaction.guild.id, 'modules')
    fields= moduller[module]
    global status
    try:
        channel= await interaction.client.server_config.find_field_value(interaction.guild.id,'modules', module,'channel')
    except KeyError:
        pass
    try:  
        hint= await interaction.client.server_config.find_field_value(interaction.guild.id,'modules', module,'hint')
        number= await interaction.client.server_config.find_field_value(interaction.guild.id,'modules', module,'number')
    except KeyError:
        hint='hint'
        number='number'
    try:
        message= await interaction.client.server_config.find_field_value(interaction.guild.id,'modules', module,'message')
    except KeyError:
        message='message'
    try:
        count= await interaction.client.server_config.find_field_value(interaction.guild.id,'modules', module,'count')
    except KeyError:
        count='count'                     

    stat=''
    if status is True:
        stat= f'{e.true_png_top}\n{e.true_png_buttom}'
    elif status is False:
        stat=f'{e.false_png_top}\n{e.false_png_buttom}'

    if update == 'enable':
        stat= f'{e.true_gif_top}\n{e.true_gif_buttom}'
    elif update == 'disable':
        stat= f'{e.false_gif_top}\n{e.false_gif_buttom}'

    modules_list = {
        "welcome": {
            "title": "WELCOME",
            "description": "Sends a welcome message to the welcome channel",
           "field":{
                "Status": stat,
                "Channel":f'<#{channel}>',
                "Message":message
            }
        },
        "logging": {
            "title": "LOGGING",
            "description": "Logs everything happening in the server.",
            "field":fields
        },
        "report": {
            "title": "Report",
            "description": "Allows members to report issues or user conduct directly to the server moderation team.",
           "field":{
                "Status": stat,
                "Channel":f'<#{channel}>',
            }
        },        
        "guess": {
            "title": "GUESS NUMBER",
            "description": "A fun mini-game where members can guess a number for a chance to win server rewards.",
            "field":{
                "Status": stat,
                "Channel": f'<#{channel}>',
                "Hint":hint,
                'Current Number':number,
            }
        },
        "count": {
            "title": "Count Number",
            "description": " A collaborative game where members count upwards and try not to break the number sequence for rewards.",
            "field":{
                "Status": stat,
                "Channel":f'<#{channel}>',
                "Count":count,
            }
        }           
    }
    return modules_list

async def create_info(interaction, update=None):
    modules= await data(interaction, update)
    modules=modules[module]
    embed=discord.Embed(
        title= modules['title'],
        description=modules['description'],
        color= 0x303434)
    for key, value in modules['field'].items():
        embed.add_field(name=key, value=value)
    embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon)
    return embed

async def modules_info(interaction):
    modules= await info_data()
    modules=modules[module]
    embed=discord.Embed(
        title= modules['title'],
        description=modules['description'],
        color= 0x303434)
    for key, value in modules['field'].items():
        embed.add_field(name=key, value=value)
    embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon)
    return embed

def SecondEmbed(self, interaction):
    embed=discord.Embed(title=f'Modules for {interaction.guild.name} ', description='You can enabled or disable modules for your server.')
    embed.add_field(name='GENERAL MODULES', value= f'⚒️ Welcome\n⚙️ Logging', inline=True)
    embed.add_field(name='SECURITY MODULES', value='⭕ Report', inline=True)
    embed.add_field(name='FUN MODULES', value='💯 Guess Number\n🔢 Count Number', inline=True)  
    return embed  

class Channel(discord.ui.Modal, title='Set Channel'):
    channel = ui.TextInput(label='Channel ID', style=discord.TextStyle.short, placeholder='Please provide a channel id')

    async def on_submit(self, interaction:discord.Interaction):
        channels=[]
        for c in interaction.guild.channels:
            channels.append(str(c.id))
            
        if str(self.channel.value) in channels:   
            await interaction.client.server_config.update_field_value(interaction.guild.id,'modules', module, 'channel', str(self.channel))
            embed= await create_info(interaction)
            await interaction.response.edit_message(embed=embed, view=ModuleView())

        elif str(self.channel.value) not in channels:
            await interaction.response.defer()
            await interaction.followup.send('> ⭕ **You need to enter a valid channel id!**', ephemeral=True)


class Message(discord.ui.Modal,):
    def __init__(self, view:discord.ui.View):
        self.view = view
        self.button=''
        super().__init__(title=f'Set message')
    message = ui.TextInput(label='Message', style=discord.TextStyle.short, placeholder='Please provide a message')

    async def on_submit(self, interaction:discord.Interaction):
        await interaction.client.server_config.update_field_value(interaction.guild.id,'modules', module, 'message', str(self.message))
        view=ModuleView()
        mdlview=ModuleView()
        self.button=ui.Button(label='Set Message', style=discord.ButtonStyle.green)
        view.add_item(self.button)   
        self.button.callback= mdlview.message2_callback        
        embed= await create_info(interaction)
        await interaction.response.edit_message(embed=embed, view=view)

class Hint(discord.ui.Modal):
    def __init__(self, view:discord.ui.View):
        self.view = view
        self.button=''
        super().__init__(title=f'Set Hint')
    hint = ui.TextInput(label='Hint', style=discord.TextStyle.short, placeholder='Please provide a hint count')

    async def on_submit(self, interaction:discord.Interaction):

        await interaction.client.server_config.update_field_value(interaction.guild.id,'modules', module, 'hint', str(self.hint))
        view=ModuleView()
        mdlview=ModuleView()
        self.button=ui.Button(label='Set Hint', style=discord.ButtonStyle.green)
        view.add_item(self.button)   
        self.button.callback= mdlview.hint_callback
        embed= await create_info(interaction)
        await interaction.response.edit_message(embed=embed, view=view)


class Setup(discord.ui.Modal):
    def __init__(self, view:discord.ui.View, view2:discord.ui.View):
        self.view = view
        self.view2= view2
        super().__init__(title=f'Setup')

    channel = ui.TextInput(label='Channel ID', style=discord.TextStyle.short, placeholder='Please provide a channel id')
    
    async def on_submit(self, interaction:discord.Interaction):
        global status
        data ={'status':True,'channel':str(self.channel)}
        view=ModuleView()
        if module=='welcome':
            view=ModuleView()
            mdlview=ModuleView()
            self.button=ui.Button(label='Set Message', style=discord.ButtonStyle.green)
            view.add_item(self.button)   
            self.button.callback= mdlview.message2_callback             
            data.update({'message': str(self.view.hint)})          
        elif module=='guess':
            view=ModuleView()
            mdlview=ModuleView()
            self.button=ui.Button(label='Set Hint', style=discord.ButtonStyle.green)
            view.add_item(self.button)   
            self.button.callback= mdlview.hint_callback                        
            data.update({'hint': str(self.view.hint), 'number':1})
        elif module=='count':
            data.update({'count': 1})
            channel= interaction.client.get_channel(int(self.channel.value))
            await channel.send('1')
        user_file= {f'modules.{module}':data}

        channels=[]
        for c in interaction.guild.channels:
            channels.append(str(c.id))
            
        if str(self.channel.value) in channels:   
            await interaction.client.server_config.update_dc(interaction.guild.id, user_file)
            status= True
            embed= await create_info(interaction)
            await interaction.response.edit_message(embed=embed, view=view)
        else:
            await interaction.response.defer()
            await interaction.followup.send('> ⭕ **You need to enter a valid channel id!**', ephemeral=True)                
        

class NodbView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.hint= '' 

    @discord.ui.button(label='', style=discord.ButtonStyle.primary, emoji= e.home_emoji)
    async def back_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.edit_message(embed=SecondEmbed(self,interaction), view=NewModuleView())

    @discord.ui.button(label='Setup', style=discord.ButtonStyle.green)
    async def setup_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        view2=ModuleView()
        modal=Setup(self, view2)
        
        if module == 'welcome':
            self.hint= ui.TextInput(label='Message', style=discord.TextStyle.short, placeholder='Please provide a message')
            modal.add_item(self.hint)
        elif module == 'guess':
            self.hint= ui.TextInput(label='Hint', style=discord.TextStyle.short, placeholder='Please provide a hint count')
            modal.add_item(self.hint) 
        await interaction.response.send_modal(modal)


class ModuleView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.view=NewModuleView()
        self.button=self.view.button


    @discord.ui.button(label='', style=discord.ButtonStyle.primary, emoji= e.home_emoji)
    async def back_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.edit_message(embed=SecondEmbed(self,interaction), view=NewModuleView())


    @discord.ui.button(label='Disable', style=discord.ButtonStyle.red)
    async def on_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        embed=''
        if button.label=='Enable':
            button.label='Disable'
            button.style= discord.ButtonStyle.red
            self.channel_button.disabled=False
            await interaction.client.server_config.update_field_value(interaction.guild.id,'modules', module, 'status', True)    
            embed= await create_info(interaction, 'enable')
            await interaction.response.edit_message(embed=embed,view=self)
        elif button.label=='Disable':
            button.label='Enable'
            button.style= discord.ButtonStyle.green
            self.channel_button.disabled=True
            await interaction.client.server_config.update_field_value(interaction.guild.id,'modules', module, 'status', False)    
            embed= await create_info(interaction, 'disable')                  
            await interaction.response.edit_message(embed=embed,view=self)

    @discord.ui.button(label='Set Channel', style=discord.ButtonStyle.green,)
    async def channel_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        view=ModuleView()
        await interaction.response.send_modal(Channel())



    @discord.ui.button(label='', style=discord.ButtonStyle.primary, emoji= e.info_emoji, row=1)
    async def info_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
        await interaction.followup.send(embed= await modules_info(interaction), ephemeral=True)

    async def message2_callback(self,interaction:discord.Interaction):
        await interaction.response.send_modal(Message(self))        

    async def hint_callback(self, interaction:discord.Interaction):
        await interaction.response.send_modal(Hint(self))
      



class NewModuleView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.category=None
        self.button=None

    def MainEmbed(self, interaction):
        embed=discord.Embed(
            title="",
            description='Commands in this server start with `!`',
            color= 0x303434)
        embed.add_field(name="・Help Panel", value="Welcome to Husky Bot's help panel! We have made a small overview to help you! \
            Make a choice via the menu below.", inline=False)    
        embed.add_field(name="・Links", value=f"[Invite]({BOT_INVITE_LINK}) : [Support Server]({GUILD_INVITE}) : [Status]({STATUS_PAGE})", inline=False)   
        embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon)        
        return embed

    @discord.ui.select(placeholder="Select a module first",max_values=1,min_values=1, options=[
            discord.SelectOption(label="Welcome",value= "welcome",emoji="⚒️",description="Sends a welcome message to the welcome channel"),
            discord.SelectOption(label="Logging",value= "logging",emoji="⚙️",description="Logs everything happening in the server."),
            discord.SelectOption(label="Report",value= "report",emoji="⭕",description="Let members report a user to the server moderation team."),
            discord.SelectOption(label="Guess Number",value= "guess",emoji="💯",description="A fun mini-game, members guess the secret number."),
            discord.SelectOption(label="Count Number",value= "count",emoji="🔢",description="Take turns to count up in sequence."),                  
            ])     
    async def select_callback(self, interaction: discord.Interaction, select:discord.ui.Select):
        global module
        global status
        module=select.values[0]
        try:
            status= await interaction.client.server_config.find_field_value(interaction.guild.id,'modules', module,'status')
            view=ModuleView()
            if status is False:    
                view.on_button.label='Enable'
                view.on_button.style=discord.ButtonStyle.green
                view.channel_button.disabled=True

            if select.values[0] =='welcome':    
                mdlview=ModuleView()
                self.button=ui.Button(label='Set Message', style=discord.ButtonStyle.green)
                view.add_item(self.button)   
                self.button.callback= mdlview.message2_callback                           
            elif select.values[0] =='guess':
                mdlview=ModuleView()
                self.button=ui.Button(label='Set Hint', style=discord.ButtonStyle.green)
                view.add_item(self.button)   
                self.button.callback= mdlview.hint_callback
            embed= await create_info(interaction)  
        except KeyError:
            status= False
            view=NodbView()  
            embed= await modules_info(interaction) 
        await interaction.response.edit_message(embed=embed, view=view)


    @discord.ui.button(label='', style=discord.ButtonStyle.primary, emoji= e.home_emoji)
    async def back_button(self, interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.edit_message(embed=self.MainEmbed(interaction), view=MainView())

class MainView(discord.ui.View):
    def __init__(self):
        super().__init__()   
        self.add_item(discord.ui.Button(label="Support",style=discord.ButtonStyle.link,url= GUILD_INVITE, emoji= e.support_emoji))
    
    @discord.ui.select(placeholder="Select an option",max_values=1,min_values=1,options=[
            discord.SelectOption(label="Commands",emoji="⚒️",description="Show the bot commands",),
            discord.SelectOption(label="Server Config",emoji="⚙️",description="Show the server configs"),
            discord.SelectOption(label="Bot Stats",emoji="📊",description="Show the bot statistics"),
            discord.SelectOption(label="Changelog",emoji="📃",description="Show the bot changelogs"),
            discord.SelectOption(label="Report Bug",emoji="🪲",description="Reports bugs"),
            ])


    async def select_callback(self, interaction: discord.Interaction, select:discord.ui.Select):
        if select.values[0] == 'Report Bug':
            await interaction.response.send_modal(Bug())
        elif select.values[0] == 'Commands':
            embed=discord.Embed(title='・Help Panel', description='View all command categories in the bot here!')
            embed.add_field(name='General Commands', value='`avatar`\n`echo`\n`huskies`\n`stats`')
            embed.add_field(name='Moderation Commands', value='`ban`\n`unban`\n`kick`')
            embed.add_field(name='Fun Commands', value='`rockpaperscissors`\n`guess`\n`slot`\n`roll`\n`dropout_chance`')       
            embed.add_field(name='Server Config Commands', value='`prefix`\n`welcome`\n`logging`')
            embed.add_field(name='Owner Commands', value='`reload`\n`resetdb`')    
            await interaction.response.edit_message(embed=embed, view=None)


        elif select.values[0] == 'Bot Stats':
            delta_uptime = relativedelta(datetime.utcnow(), interaction.client.launch_time)
            days, hours, minutes, seconds = delta_uptime.days, delta_uptime.hours, delta_uptime.minutes, delta_uptime.seconds

            uptimes = {x[0]: x[1] for x in [('days', days), ('hours', hours),
                                            ('minutes', minutes), ('seconds', seconds)] if x[1]}

            last = "".join(value for index, value in enumerate(uptimes.keys()) if index == len(uptimes)-1)
            uptime_string = "".join(
                f"{v} {k}" if k != last else f" and {v} {k}" if len(uptimes) != 1 else f"{v} {k}"
                for k, v in uptimes.items()
            )            
            python_version= platform.python_version()
            dpy_version= discord.__version__
            server_count= len(interaction.client.guilds)
            member_count= len(interaction.guild.members)
            embed=discord.Embed(title= f'{interaction.client.user.name} Bot Statistics', description="", color=interaction.user.colour, timestamp=interaction.message.created_at)
            embed.add_field(name='Python V.', value= f'```{python_version}```')
            embed.add_field(name='Discord.py V.', value= f'```{dpy_version}```')
            embed.add_field(name='CPU Usage', value=f'```{psutil.cpu_percent()}%```')
            embed.add_field(name='Memory Usage', value=f'```{psutil.virtual_memory().percent}%```')
            embed.add_field(name='Up Time', value=f'{uptime_string}')
            embed.add_field(name='Total Guilds', value=server_count)
            embed.add_field(name='Unique Users', value= member_count)
            embed.set_footer(text=f"Husky | {interaction.client.user.name}")
            embed.set_author(name=interaction.client.user.name, icon_url=interaction.client.user.avatar.url)
            await interaction.response.edit_message(embed=embed, view=None)

        elif select.values[0] == 'Server Config':
            if interaction.user.guild_permissions.administrator or interaction.user.guild_permissions.manage_guild: 
                wstatus= f'ㅤ{e.false_png_top}\nㅤ{e.false_png_buttom}'
                lstatus= f'ㅤ{e.false_png_top}\nㅤ{e.false_png_buttom}'
                try:
                    a=await interaction.client.server_config.find_field_value(interaction.guild_id,'modules', 'welcome', 'status')  
                    if a is True:
                        wstatus= f'ㅤ{e.true_png_top}\nㅤ{e.true_png_buttom}'
                except:
                    pass 
                                                                   
                await interaction.response.edit_message(embed=SecondEmbed(self, interaction), view=NewModuleView())
            else:
                await interaction.response.defer()
                await interaction.followup.send('You dont have the permissions to do that!', ephemeral=True)

        else:      
            await interaction.response.send_message(content=f"Your choice is {select.values[0]}!",ephemeral=True)








class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.launch_time = datetime.utcnow()

    @app_commands.command(name= 'help', description='Shows the help embed')
    async def help(self, interaction: discord.Interaction):
        embed=discord.Embed(
            title="",
            description=f'## Welcome to Husky Bot\'s Help Panel\n\nCommands in this server start with `!`',
            color= 0x303434)
        embed.add_field(name="・Help Panel", value="We have made a small overview to help you! \
            Make a choice via the menu below.", inline=False)    
        embed.add_field(name="・Links", value=f"[Invite]({BOT_INVITE_LINK}) : [Support Server]({GUILD_INVITE}) : [Status]({STATUS_PAGE})", inline=False)   
        embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon)
        await interaction.response.send_message(embed=embed, view=MainView(), ephemeral=True)




async def setup(bot):
    await bot.add_cog(Help(bot))