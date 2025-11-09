"""Ein einfacher Discord-Bot mit hilfreichen Standardbefehlen zum Testen."""

from __future__ import annotations

import argparse
import logging
import os
import random
from collections.abc import Iterable
from typing import Optional

import discord
from discord.ext import commands


def configure_logging(level: str | None) -> None:
    """Richtet das Logging mit einem lesbaren Format ein."""

    numeric_level = getattr(logging, (level or "INFO").upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Unbekannter Log-Level: {level}")

    logging.basicConfig(
        level=numeric_level,
        format="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
    )


def _load_env_file(path: str = ".env") -> None:
    """Lädt Variablen aus einer .env-Datei, falls vorhanden."""

    if not os.path.exists(path):
        return

    try:
        with open(path, "r", encoding="utf-8") as env_file:
            for line in env_file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())
    except OSError as exc:  # pragma: no cover - IO-Fehler sind schwer zu testen
        raise RuntimeError(f"Konnte die .env-Datei nicht lesen: {exc}") from exc


def load_token(env_var: str = "DISCORD_TOKEN") -> str:
    """Lädt den Bot-Token aus der Umgebung oder einer .env-Datei."""
    _load_env_file()
    token: Optional[str] = os.getenv(env_var)
    if not token:
        raise RuntimeError(
            "Kein Discord-Token gefunden. Lege eine .env-Datei mit DISCORD_TOKEN an "
            "oder setze die Umgebungsvariable."
        )
    return token


def build_bot(command_prefix: str = "!") -> commands.Bot:
    """Erstellt und konfiguriert die Bot-Instanz."""

    intents = discord.Intents.default()
    intents.message_content = True

    description = "Ein Test-Bot für Discord mit ein paar Standardbefehlen."
    bot = commands.Bot(command_prefix=command_prefix, description=description, intents=intents)

    @bot.event
    async def on_ready() -> None:  # pragma: no cover - wird nur zur Laufzeit aufgerufen
        if bot.user is None:
            logging.warning("Bot ist bereit, aber bot.user ist None")
            return

        logging.info("Eingeloggt als %s (ID: %s)", bot.user, bot.user.id)
        await bot.change_presence(activity=discord.Game(name=f"{command_prefix}help"))

    @bot.event
    async def on_guild_join(guild: discord.Guild) -> None:  # pragma: no cover - Ereignis basiert
        logging.info("Dem Server '%s' mit %s Mitgliedern beigetreten", guild.name, guild.member_count)

    @bot.command(name="ping", help="Zeigt die aktuelle Latenz des Bots an.")
    async def ping(ctx: commands.Context[commands.Bot]) -> None:
        latency_ms = bot.latency * 1000
        await ctx.send(f"Pong! {latency_ms:.0f} ms")

    @bot.command(name="say", help="Wiederholt die angegebene Nachricht.")
    async def say(ctx: commands.Context[commands.Bot], *, text: str) -> None:
        await ctx.send(text)

    @bot.command(name="roll", help="Würfelt eine Zahl zwischen 1 und den angegebenen Seiten.")
    async def roll(ctx: commands.Context[commands.Bot], sides: commands.Range[int, 2, 10_000] = 6) -> None:
        result = random.randint(1, sides)
        await ctx.send(f"🎲 Du hast eine {result} gewürfelt (1-{sides}).")

    @bot.command(name="add", help="Addiert zwei ganze Zahlen.")
    async def add(ctx: commands.Context[commands.Bot], left: int, right: int) -> None:
        await ctx.send(f"{left} + {right} = {left + right}")

    @bot.command(name="choose", help="Wählt zufällig aus den angegebenen Optionen aus.")
    async def choose(ctx: commands.Context[commands.Bot], *options: str) -> None:
        if len(options) < 2:
            await ctx.send("Bitte gib mindestens zwei Optionen an.")
            return
        choice = random.choice(options)
        await ctx.send(f"Ich wähle: {choice}")

    @bot.command(name="yesno", help="Antwortet zufällig mit Ja oder Nein.")
    async def yesno(ctx: commands.Context[commands.Bot]) -> None:
        answer = random.choice(["Ja", "Nein"])
        await ctx.send(answer)

    @bot.command(name="serverinfo", help="Zeigt Informationen über den aktuellen Server an.")
    async def serverinfo(ctx: commands.Context[commands.Bot]) -> None:
        guild = ctx.guild
        if guild is None:
            await ctx.send("Dieser Befehl kann nur auf einem Server verwendet werden.")
            return

        embed = discord.Embed(title=guild.name, colour=discord.Colour.blurple())
        embed.add_field(name="Mitglieder", value=str(guild.member_count))
        if guild.owner:
            embed.add_field(name="Server-Inhaber", value=str(guild.owner), inline=False)
        embed.add_field(name="Erstellt am", value=discord.utils.format_dt(guild.created_at, style="F"), inline=False)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        await ctx.send(embed=embed)

    @bot.command(name="userinfo", help="Zeigt Informationen über den aufrufenden Nutzer an.")
    async def userinfo(
        ctx: commands.Context[commands.Bot],
        member: Optional[discord.Member] = None,
    ) -> None:
        member = member or ctx.author
        colour = member.colour if isinstance(member.colour, discord.Colour) else discord.Colour.blurple()

        embed = discord.Embed(title=str(member), colour=colour)
        embed.add_field(name="ID", value=member.id, inline=False)
        embed.add_field(name="Account erstellt", value=discord.utils.format_dt(member.created_at, style="F"))
        if getattr(member, "joined_at", None):
            embed.add_field(
                name="Server beigetreten",
                value=discord.utils.format_dt(member.joined_at, style="F"),
            )
        embed.set_thumbnail(url=member.display_avatar.url)
        await ctx.send(embed=embed)

    @bot.event
    async def on_command_error(ctx: commands.Context[commands.Bot], error: commands.CommandError) -> None:
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Fehlendes Argument: {error.param.name}")
            return
        if isinstance(error, commands.BadArgument):
            await ctx.send("Bitte überprüfe deine Eingaben.")
            return
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send("Dieser Befehl ist nur auf Servern verfügbar.")
            return

        logging.exception("Fehler beim Ausführen eines Befehls", exc_info=error)
        await ctx.send("Beim Ausführen des Befehls ist ein Fehler aufgetreten.")

    return bot


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    """Parst Befehlszeilenargumente für die Bot-Konfiguration."""

    parser = argparse.ArgumentParser(description="Starte den Beispiel-Discord-Bot.")
    parser.add_argument(
        "--log-level",
        default=os.getenv("LOG_LEVEL", "INFO"),
        help="Log-Level (z. B. INFO, DEBUG, WARNING). Überschreibt LOG_LEVEL.",
    )
    parser.add_argument(
        "--prefix",
        default=os.getenv("COMMAND_PREFIX", "!"),
        help="Präfix für Textbefehle (Standard: !). Überschreibt COMMAND_PREFIX.",
    )
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args()
    configure_logging(args.log_level)

    token = load_token()
    bot = build_bot(command_prefix=args.prefix)
    bot.run(token)


if __name__ == "__main__":
    main()
