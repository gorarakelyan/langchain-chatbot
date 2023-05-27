import time

from dotenv import dotenv_values

from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent

from chatbot.chatbot.callback import AimCallbackHandler
from chatbot.chatbot.utils import (
    get_version,
    get_user,
)


def chatbot(serpapi_key, openai_key):
    # Configs
    model_name = 'gpt-3.5-turbo'
    username = get_user()
    version = get_version()

    config = dotenv_values('.env')

    # ChatBot implementation
    memory = ConversationBufferMemory(memory_key="chat_history")

    search = SerpAPIWrapper(serpapi_api_key=serpapi_key)
    tools = [
        Tool(
            name = "Search",
            func=search.run,
            description="useful for when you need to answer questions about current events or the current state of the world"
        ),
    ]

    llm=ChatOpenAI(temperature=0, openai_api_key=openai_key, model_name=model_name)

    agent_chain = initialize_agent(tools, llm,
                                   agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                                   verbose=True,
                                   memory=memory)

    # Init the callback
    aim_cb = AimCallbackHandler(username)
    aim_cb.session[...] = {
        'chatbot_version': version,
        'model': model_name,
        'username': username,
        'started': time.time(),
        'available_tools': [{ 'name': tool.name, 'description': tool.description } for tool in tools],
    }

    # Run the bot
    while True:
        msg = input('Message:\n')
        try:
            response = agent_chain.run(input=msg, callbacks=[aim_cb])
        except ValueError as e:
            response = str(e)
            if not response.startswith("Could not parse LLM output: `"):
                raise e
        response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")
