import time
import random

from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent
from callback import AimCallbackHandler


# User management
usernames = ['JamesThompson', 'LisaHamilton', 'RobertFitzgerald', 'MariaGonzalez', 'DavidMorrison']
username = random.choice(usernames)


# Chatbot implementation
memory = ConversationBufferMemory(memory_key="chat_history")

search = SerpAPIWrapper(serpapi_api_key='f34963a8a633770c677eab766be98d57a7a3eddd98437e606d0191310bf18c0c')
tools = [
    Tool(
        name = "Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world"
    ),
]

llm=ChatOpenAI(temperature=0, openai_api_key="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", model_name='gpt-3.5-turbo')
aim_cll = AimCallbackHandler(username=username)
agent_chain = initialize_agent(tools, llm,
                               agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
                               verbose=True,
                               memory=memory)

while True:
    msg = input('Message:\n')
    agent_chain.run(input=msg, callbacks=[aim_cll])