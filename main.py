
import asyncio
import discord
from discord.ext import commands
import config

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

EXTENSIONS = [
    "cogs.moderation",
    "cogs.staff",
    "cogs.sessions",
    "cogs.tickets",
    "cogs.verification",
    "cogs.antiraid"
]

@bot.event
async def on_ready():
    print(f"{bot.user} is online")

    await asyncio.sleep(5)

    for attempt in range(3):
        try:
            target_guild = None

            if config.GUILD_ID:
                target_guild = bot.get_guild(config.GUILD_ID)

            if not target_guild and bot.guilds:
                target_guild = bot.guilds[0]

            if target_guild:
                synced = await bot.tree.sync(guild=target_guild)
                print(f"Synced {len(synced)} commands to {target_guild.name}")
                break
            else:
                synced = await bot.tree.sync()
                print(f"Synced {len(synced)} commands globally")
                break
        except Exception as e:
            print(f"Command sync attempt {attempt + 1} failed: {e}")
            if attempt < 2:
                await asyncio.sleep(5)

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name=config.WELCOME_CHANNEL)
    if channel:
        await channel.send(f"👋 Welcome {member.mention} to CSR!")

async def setup_hook():
    print("Loading extensions...")
    for ext in EXTENSIONS:
        try:
            await bot.load_extension(ext)
            print(f"Loaded extension: {ext}")
        except Exception as e:
            print(f"Failed to load extension {ext}: {e}")

bot.setup_hook = setup_hook

bot.run(config.TOKEN)
