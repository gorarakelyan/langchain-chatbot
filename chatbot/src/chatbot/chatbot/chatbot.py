import os
import time
import random

from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent

from chatbot.chatbot.callback import AimCallbackHandler


def get_version():
    here = os.path.abspath(os.path.dirname(__file__))
    version_file = os.path.join(here, '..', 'VERSION')
    with open(version_file) as vf:
        __version__ = vf.read().strip()
    return __version__


def chatbot(model_name: str = 'gpt-3.5-turbo'):
    # User simulation
    usernames = ['JamesThompson', 'LisaHamilton', 'RobertFitzgerald', 'MariaGonzalez', 'DavidMorrison']
    username = random.choice(usernames)

    # Chatbot implementation
    memory = ConversationBufferMemory(memory_key="chat_history")

    search = SerpAPIWrapper(serpapi_api_key='f34963a8a633770c677eab766be98d57a7a3eddd98437e606d0191310bf18c0c')
    tools = [
        Tool(
            name = "Search",
            func=search.run,
            description="useful for when you need to answer questions about current events or the current state of the world"
        ),
    ]

    llm=ChatOpenAI(temperature=0, openai_api_key="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", model_name=model_name)

    aim_cb = AimCallbackHandler(username)
    aim_cb.session[...] = {
        'chatbot_version': get_version(),
        'model': model_name,
        'username': username,
        'started': time.time(),
        'available_tools': [{ 'name': tool.name, 'description': tool.description } for tool in tools],
    }

    agent_chain = initialize_agent(tools, llm,
                                   agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                                   verbose=True,
                                   memory=memory)
    return agent_chain, aim_cb
