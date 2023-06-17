# A basic langChain chatbot app for terminal.
LanngChain Chatbot implementation with Aim-based observability package.

## Repo Structure
There are two python packages in this repo:
- **chatbot**: the chatbot implementation with LangChain
- **chatbot_logger**: full end-to-end observability built with Aim framework.

## About Aim
Aim is a developer framework for building end-to-end observability and logs automation for AI Systems.
Use Aim to build the UI layer of your AI Systems Infrastructure (ML Infra). 
Aim is generic and well-integrated with the AI / LLM stack.
Aim is easy to integrate with every aspect of your AI Systems
Aim enables low-code pythonic UI SDK to build full-blown observability tools over the tracked data.

# Getting Started with the Chatbot
## Installation

1. Clone the repo
2. Add `.env` file at `chatbot` with `serpapi_key` and `openai_key` keys
2. Install the logger `pip install -e ./chatbot_logger` (in editable mode)
3. Install the chatbot `pip install -e ./chatbot` (in editable mode)

## Run

1. Start Aim server `aim server --package chatbot_logger`
2. Execute `cd chatbot && chatbot run` to run the chatbot

# Observability with Aim
## How Aim works
Aim enables an API for users to define the objects to track and use them in their application for tracking.
Also Aim enables a low-code pythonic interface for building visualizations over the tracked objects
Aim packages enable a mechanism to place all of this code in one package and just reuse in the ai system.
Aim is a fundamental framework and allows to define, track such objects from across the ai infra.
Also build end-to-end observability layer for the whole infra layer.

## Using Aim
- Start Aim UI: `aim up --package chatbot_logger`
- Checkout Aim docs: `aim up --port 43001 --package docs`

## Dashboards implemented
Overview page: full overview of the development and releases of the chatbot
Production page: full overview of the production sessions by the users 
User Activity page: select user and see the users' activity
Session page: observe the User sessions on the chatbot in detail

## Using the built-in playground documentation
Aim comes with a built-in playground documentation.
Here is how to start it: `aim up --port 43001 --package docs`
This command will open an Aim instance that will have all the examples users need to extend their chatbot observability toolkit.

## Next steps: make it your own
There are many ways this package can be extended
- Add new metrics that track chatbot efficiencies
- Add aggregate metrics of the openai cost
- potentially restructure the whole package to better see the lineage of the experiment -> dev session -> release -> user session -> issue -> experiment ->...

## Roadmap - features to expect
The Aim features upcoming:
- **Aim Actions:** Execute Aim-initiated actions. Actions could range from primitive automations to starting external workflows.
    - Attach external workflows to aim sessions (e.g. run a model checkpoint).
    - Implement arbitrary manipulations over aim objects (e.g. invert an image).
    - Importantly: Aim only connects the logged metadata to the action and initiates it. Aim does not provide the runtime.
- **Aim Callbacks:** Custom callbacks on storage-update.
    - Aim action executed on specific type of storage updates.
- **Aim Beats:** Notifications triggered on storage update.
    - A specific Aim action that triggers notification to various mediums (slack, email etc) when storage is updates and specific criteria is met.
