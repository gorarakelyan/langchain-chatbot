import click

from chatbot.chatbot.chatbot import chatbot


@click.group()
def entrypoint():
    pass


@entrypoint.command(name='run')
def run():
    agent, cb = chatbot()

    while True:
        msg = input('Message:\n')
        try:
            response = agent.run(input=msg, callbacks=[cb])
        except ValueError as e:
            response = str(e)
            if not response.startswith("Could not parse LLM output: `"):
                raise e
        response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")
