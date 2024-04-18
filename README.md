# slackbot-openai

LLM bots for integration with Slack.

![](https://img.shields.io/badge/Amazon%20AWS-232F3E.svg?style=flat&logo=Amazon-AWS&logoColor=white)
![](https://img.shields.io/badge/OpenAI-412991.svg?style=flat&logo=OpenAI&logoColor=white)
![](https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white)
![](https://img.shields.io/badge/Slack-4A154B.svg?style=flat&logo=Slack&logoColor=white)

## Contents

- [Models](#models)
- [Files](#files)
- [Setup](#setup)
  - [Installation](#installation)
  - [Operation](#operation)
- [Slack OAuth Scopes](#slack-oauth-scopes)

## Models

Source: [together.ai](https://docs.together.ai/docs/inference-models)

| Organization | Model Name            | Model String for API               | Context length | Type  |
| ------------ | --------------------- | ---------------------------------- | -------------- | ----- |
| 01.AI        | 01-ai Yi Chat (34B)   | zero-one-ai/Yi-34B-Chat            | 4096           | Chat  |
| Meta         | LLaMA-2 Chat (13B)    | meta-llama/Llama-2-13b-chat-hf     | 4096           | Chat  |
| mistralai    | Mistral (7B) Instruct | mistralai/Mistral-7B-Instruct-v0.1 | 8192           | Chat  |
| Stanford     | Alpaca (7B)           | togethercomputer/alpaca-7b         | 2048           | Chat  |
| Stability AI | Stable Diffusion 2.1  | stabilityai/stable-diffusion-2-1   | N/A            | Image |

## Files

- This app is run from `src/app.py`.
- Global variables such as LLM model types and token limits are configured in `src/utils/config.py`.
- Model-related functions are contained in `src/utils/model_funcs.py`.
- Text-formatting functions are contained in `src/utils/regex_funcs.py`.
- Error logging is handled via `src/utils/logger.py`, with logs stored in `logs/`

## Setup

### Installation

```console
$ git clone git@github:jenx-ai/slackbot-openai
Cloning into 'slackbot-openai'...
remote: Enumerating objects: 94, done.
remote: Counting objects: 100% (31/31), done.
remote: Compressing objects: 100% (28/28), done.
remote: Total 94 (delta 4), reused 11 (delta 3), pack-reused 63
Receiving objects: 100% (94/94), 29.27 KiB | 4.88 MiB/s, done.
Resolving deltas: 100% (33/33), done.
$ ls
slackbot-openai
```

Create a virtual environment using `uv`, then install dependencies from `requirements.txt`.

```console
$ cd slackbot
$ uv venv
$ source .venv/bin/activate
$ uv pip install --upgrade pip
$ uv pip install -r requirements.txt
```

Create a `.env` file with required variables as per `.env.example`. 

The file should be created at the top level of the `slackbot` repo directory, alongside the `src` and `.venv` directories.

### Operation

Activate the virtual environment, then change to the `src` directory and run `app.py`.

```console
$ cd slackbot-repos
$ cd {model-dir}
$ cd slackbot
$ source .venv/bin/activate
$ cd src
$ python3 app.py
⚡Bolt app is running!
```

## Slack OAuth Scopes

The following bot scopes are required for this implementation:

| OAuth Scope       | Scope Type | Description                                                                   |
| ----------------- | :--------: | ----------------------------------------------------------------------------- |
| app_mentions:read | Bot        | View messages that directly mention @app in conversations that the app is in  |
| channels:history | Bot | View messages and other content in public channels that app has been added to |
| chat:write        | Bot        | Send messages as @app                                                         |
| chat:write:public | Bot        | Send messages to channels app isn't a member of                              |
| groups:history | Bot | View messages and other content in private channels that the app has been added to |
| im:history        | Bot        | View messages and other content in direct messages that app has been added to |
| connections:write | App        | Route your app’s interactions and event payloads over WebSockets              |
