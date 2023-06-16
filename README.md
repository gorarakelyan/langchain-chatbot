# LangChain-based chatbot with observabilty layer

The repo contains two python packages:
- chatbot: chatbot implementation with LangChain
- chatbot_logger: Aim-based logging and observability package for chatbots 

## Installation

1. Clone the repo
2. Add `.env` file at `chatbot` with `serpapi_key` and `openai_key` keys
2. Install the logger `pip install -e ./chatbot_logger` (in editable mode)
3. Install the chatbot `pip install -e ./chatbot` (in editable mode)

## Run

1. Start Aim server `aim server --package chatbot_logger`
2. Execute `cd chatbot && chatbot run` to run the chatbot

## Using Aim
- Start Aim UI: `aim up --package chatbot_logger`
- Checkout Aim docs: `aim up --port 43001 --package docs`