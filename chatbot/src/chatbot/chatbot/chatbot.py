import time

from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent

from aim import Repo
from chatbot.chatbot.callback import AimCallbackHandler
from chatbot_logger import Experiment, Release
from chatbot.chatbot.utils import (
    get_version,
    get_user,
)


def chatbot(serpapi_key, openai_key, dev_mode):
    # Configs
    model_name = 'gpt-3.5-turbo'
    username = get_user()
    version = get_version()

    # Init experiment and release
    repo = Repo.default()
    try:
        release = repo.containers(f'c.version == "{version}"', Release).first()
    except:
        release = Release()
        release[...] = {
            'version': version,
            'time': time.time(),
        }

    experiment = None
    if dev_mode:
        experiment = Experiment()
        experiment['release'] = release.hash
        experiment['version'] = version
        experiment['started'] = time.time()

    # ChatBot implementation
    memory = ConversationBufferMemory(memory_key="chat_history")
    if experiment is not None:
        experiment['memory'] = memory.__dict__

    search = SerpAPIWrapper(serpapi_api_key=serpapi_key)
    tools = [
        Tool(
            name = "Search",
            func=search.run,
            description="useful for when you need to answer questions about current events or the current state of the world"
        ),
    ]
    if experiment is not None:
        experiment['tools'] = [tool.__dict__ for tool in tools]

    llm = ChatOpenAI(temperature=0, openai_api_key=openai_key, model_name=model_name)
    if experiment is not None:
        experiment['llm'] = llm.__dict__

    agent_chain = initialize_agent(
        tools, llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
        handle_parsing_errors="Check your output and make sure it conforms!"
    )
    if experiment is not None:
        experiment['agent'] = agent_chain.__dict__

    # Init the callback
    aim_cb = AimCallbackHandler(username, dev_mode, experiment)
    aim_cb.session[...] = {
        'chatbot_version': version,
        'model': model_name,
        'username': username,
        'started': time.time(),
        'available_tools': [{ 'name': tool.name, 'description': tool.description } for tool in tools],
        'experiment': experiment.hash if experiment else None,
        'release': release.hash,
    }

    # Run the bot
    while True:
        msg = input('Message:\n')
        response = agent_chain.run(input=msg, callbacks=[aim_cb])
        # try:
        #     response = agent_chain.run(input=msg, callbacks=[aim_cb])
        # except ValueError as e:
        #     response = str(e)
        #     if not response.startswith("Could not parse LLM output: `"):
        #         raise e
        # response = response.removeprefix("Could not parse LLM output: `").removesuffix("`")
