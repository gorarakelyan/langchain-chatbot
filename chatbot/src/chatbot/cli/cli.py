import click
import os
from dotenv import dotenv_values

from chatbot.chatbot import chatbot


@click.group()
def entrypoint():
    pass


@entrypoint.command
def run():
    # Load config
    here = os.path.abspath(os.path.dirname(__file__))
    config_file_path = os.path.abspath(os.path.join(here, '..', '..', '..', '.env'))
    config = dotenv_values(config_file_path)

    # Run the bot
    chatbot(config['serpapi_key'], config['openai_key'])
