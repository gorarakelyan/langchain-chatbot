# LangChain-based chatbot with observabilty layer

The repo contains two python packages:
- chatbot: chatbot implementation with LangChain
- chatbot_logger: Aim-based logging and observability package for chatbots 

## Installation

1. Install the logger `cd chatbot_logger && pip install -e .`
2. Install the chatbot `cd chatbot && pip install .`
   
## Run

1. Start Aim server `aim server --package chatbot_logger`
2. Execute `chatbot run` to run the chatbot.
3. Up Aim UI `aim up --package chatbot_logger`
