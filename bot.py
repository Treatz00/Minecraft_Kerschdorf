"""Ein einfacher Discord-Bot mit ein paar Standardbefehlen zum Testen."""

from __future__ import annotations

import logging
import os
import random
from typing import Optional

import discord
from discord.ext import commands
from dotenv import load_dotenv


def load_token(env_var: str = "DISCORD_TOKEN") -> str:
    """Lädt den Bot-Token aus der Umgebung oder einer .env-Datei."""
    load_dotenv()
    token: Optional[str] = os.getenv(env_var)
    if not token:
        raise RuntimeError(
            "Kein Discord-Token gefunden. Lege eine .env-Datei mit DISCORD_TOKEN an "
            "oder setze die Umgebungsvariable."
        )
    return token


def build_bot() -> commands.Bot:
    """Erstellt und konfiguriert die Bot-Instanz."""
    intents = discord.Intents.default()
    intents.message_content = True

    description = "Ein Test-Bot für Discord mit ein paar Standardbefehlen."
    bot = commands.Bot(command_prefix="!", description=description, intents=intents)

    @bot.event
    async def on_ready() -> None:
        logging.info("Eingeloggt als %s (ID: %s)", bot.user, bot.user.id if bot.user else "?")
        await bot.change_presence(activity=discord.Game(name="!help"))

    @bot.command(name="ping", help="Zeigt die aktuelle Latenz des Bots an.")
    async def ping(ctx: commands.Context) -> None:
        latency_ms = bot.latency * 1000
        await ctx.send(f"Pong! {latency_ms:.0f} ms")

    @bot.command(name="say", help="Wiederholt die angegebene Nachricht.")
    async def say(ctx: commands.Context, *, text: str) -> None:
        await ctx.send(text)

    @bot.command(name="roll", help="Würfelt eine Zahl zwischen 1 und den angegebenen Seiten.")
    async def roll(ctx: commands.Context, sides: int = 6) -> None:
        if sides < 2:
            await ctx.send("Bitte gib eine Zahl größer als 1 an.")
            return
        result = random.randint(1, sides)
        await ctx.send(f"🎲 Du hast eine {result} gewürfelt (1-{sides}).")

    @bot.command(name="add", help="Addiert zwei ganze Zahlen.")
    async def add(ctx: commands.Context, left: int, right: int) -> None:
        await ctx.send(f"{left} + {right} = {left + right}")

    @bot.command(name="userinfo", help="Zeigt Informationen über den aufrufenden Nutzer an.")
    async def userinfo(ctx: commands.Context, member: Optional[discord.Member] = None) -> None:
        member = member or ctx.author
        embed = discord.Embed(title=str(member), colour=member.colour)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Account erstellt", value=discord.utils.format_dt(member.created_at, style="F"))
        if member.joined_at:
            embed.add_field(name="Server beigetreten", value=discord.utils.format_dt(member.joined_at, style="F"))
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    @bot.event
    async def on_command_error(ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Fehlendes Argument: {error.param.name}")
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send("Bitte überprüfe deine Eingaben.")
            return
        logging.exception("Fehler beim Ausführen eines Befehls", exc_info=error)
        await ctx.send("Beim Ausführen des Befehls ist ein Fehler aufgetreten.")

    return bot


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    token = load_token()
    bot = build_bot()
    bot.run(token)


if __name__ == "__main__":
    main()
