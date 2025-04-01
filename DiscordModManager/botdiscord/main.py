import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import logging

# Import app from app.py for the web interface
try:
    from app import app
except ImportError:
    # This is fine if we're just running the bot without the web interface
    pass

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("bot")

# Set up intents
intents = discord.Intents.default()
intents.message_content = True  # Nécessaire pour lire le contenu des messages
intents.members = True  # Nécessaire pour les commandes de modération sur les membres
# Note: Pour utiliser ces fonctionnalités avancées, vous devez activer les intents privilégiés sur
# https://discord.com/developers/applications/ dans les paramètres de votre bot

# Bot configuration
PREFIX = "!"  # Préfixe pour les commandes classiques (slash commands utilisent /)
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None, application_id=1348435532253761536)

@bot.event
async def on_ready():
    """Event triggered when the bot is ready and connected to Discord."""
    logger.info(f"Bot connected as {bot.user.name}")
    logger.info(f"Bot ID: {bot.user.id}")
    
    # Load all cogs
    for extension in ['cogs.commands', 'cogs.moderation', 'cogs.owner']:
        try:
            await bot.load_extension(extension)
            logger.info(f"Loaded extension: {extension}")
        except Exception as e:
            logger.error(f"Failed to load extension {extension}: {e}")
    
    # Sync slash commands with Discord
    try:
        # Attendre pour éviter le rate limit
        await asyncio.sleep(2)
        
        # Sync with rate limit handling
        try:
            # Sync all commands globally
            synced = await bot.tree.sync()
            logger.info(f"Synced {len(synced)} slash command(s) globally")
            
            # Log all available commands
            logger.info("Available slash commands:")
            for cmd in bot.tree.get_commands():
                logger.info(f"- /{cmd.name}: {cmd.description}")
        except discord.HTTPException as e:
            if e.status == 429:  # Rate limit error
                retry_after = e.retry_after
                logger.warning(f"Rate limited when syncing commands. Retrying in {retry_after} seconds...")
                await asyncio.sleep(retry_after)
                
                # Try once more
                synced = await bot.tree.sync()
                logger.info(f"Synced {len(synced)} slash command(s) globally after rate limit")
            else:
                raise e
    except Exception as e:
        logger.error(f"Failed to sync slash commands: {e}")
    
    # Set initial presence
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{PREFIX}help | Modération"
        )
    )
    logger.info("Bot is ready!")

@bot.event
async def on_command_error(ctx, error):
    """Global error handler for command errors."""
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Argument manquant: `{error.param.name}`\nUtilisez `{PREFIX}help {ctx.command.name}` pour plus d'informations.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"❌ Argument invalide. Utilisez `{PREFIX}help {ctx.command.name}` pour plus d'informations.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Vous n'avez pas les permissions nécessaires pour exécuter cette commande.")
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send("❌ Je n'ai pas les permissions nécessaires pour exécuter cette commande.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Cette commande est en cooldown. Réessayez dans {error.retry_after:.2f} secondes.")
    else:
        logger.error(f"Unhandled command error: {error}")
        await ctx.send("❌ Une erreur s'est produite lors de l'exécution de cette commande.")

@bot.command(name="help")
async def help_command(ctx, command_name=None):
    """Affiche l'aide pour les commandes du bot."""
    embed = discord.Embed(
        title="Aide du Bot de Modération",
        description=f"Préfixe: `{PREFIX}`",
        color=discord.Color.blue()
    )
    
    if command_name:
        command = bot.get_command(command_name)
        if command:
            embed.add_field(
                name=f"{PREFIX}{command.name}",
                value=command.help or "Aucune description disponible.",
                inline=False
            )
            embed.set_footer(text=f"Syntaxe: {PREFIX}{command.name} {command.signature}")
        else:
            embed.description = f"❌ La commande `{command_name}` n'existe pas."
    else:
        # Group commands by cog
        cogs = {}
        for command in bot.commands:
            cog_name = command.cog_name or "Autre"
            if cog_name not in cogs:
                cogs[cog_name] = []
            cogs[cog_name].append(command)
        
        # Add fields for each cog
        for cog_name, commands_list in cogs.items():
            commands_text = ", ".join(f"`{PREFIX}{cmd.name}`" for cmd in commands_list)
            embed.add_field(name=cog_name, value=commands_text, inline=False)
        
        embed.set_footer(text=f"Utilisez '{PREFIX}help <commande>' pour plus de détails sur une commande spécifique.")
    
    await ctx.send(embed=embed)

if __name__ == "__main__":
    # Get token from environment variable
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        logger.error("No token found. Set the DISCORD_TOKEN environment variable.")
        exit(1)
    
    # Run the bot
    bot.run(token)