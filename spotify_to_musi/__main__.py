from __future__ import annotations

import pathlib
import rich_click as click
from rich.style import Style
from spotify_to_musi.cache import store_spotify_secrets
from spotify_to_musi.main import get_spotify

from spotify_to_musi.paths import app_data, spotify_cache_path

import spotipy

click.rich_click.STYLE_OPTION = "bold magenta"
click.rich_click.STYLE_SWITCH = "bold blue"
click.rich_click.STYLE_METAVAR = "bold red"
click.rich_click.MAX_WIDTH = 75

console = click.rich_click._get_rich_console()


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "-u/-nu",
    "--user/--no-user",
    is_flag=True,
    help="Transfer liked songs and playlists of authorized user.",
    default=True,
    show_default=True,
)
@click.option("-pl", "--playlist", help="Transfer Spotify playlist(s) by URL.", multiple=True, type=str)
def transfer(user: bool, playlist: list[str]):
    """Transfer songs from Spotify to Musi."""
    spotify = get_spotify()
    print(f"{spotify=}")


@cli.command()
def setup():
    """Configure Spotify API and other options."""
    welcome_text = "Welcome to [bold green]spotify-to-musi[/bold green] first time setup! [i](Ctrl + C to exit)[/i]"

    if spotify_cache_path and spotify_cache_path.is_file():
        welcome_text += "\n* You're already setup! Only run this script again if you're having issues."

    console.print(welcome_text, highlight=True, markup=True)

    def prompt(for_: str) -> str:
        # default_text = f" [#808080]\\[[i]{default}[/i]][/#808080]" if default else ""
        text = f"[magenta]{for_}[/magenta]: "

        res = console.input(text)
        while not res:
            console.print("[red]Please enter a value.[/red]")
            res = console.input(text)
        return res

    spotify_client_id = prompt("Spotify Client ID")
    spotify_client_secret = prompt("Spotify Client Secret")
    store_spotify_secrets(spotify_client_id, spotify_client_secret)
    get_spotify()


if __name__ == "__main__":
    cli()