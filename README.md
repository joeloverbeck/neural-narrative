# Neural Narrative

Create immersive story universes powered by AI

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
    - [AI Models Configuration](#ai-models-configuration)
    - [Application Settings](#application-settings)
- [API Keys Setup](#api-keys-setup)
    - [OpenRouter API Key](#openrouter-api-key)
    - [OpenAI API Key](#openai-api-key)
    - [RunPod API Key (Optional)](#runpod-api-key-optional)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

**Neural Narrative** is a Flask application written in Python that allows users to generate rich story
universes populated with dynamic characters powered by large language models (LLMs). Users can create intricate
hierarchies of places, engage with non-player characters, and experience unique playthroughs with customizable
player characters. The application also features an action system to simulate complex situations beyond simple
dialogues, enhancing the storytelling experience.

## Features

- **Universe Generation**: Create expansive story universes with hierarchical locations.
- **Character Creation**: Generate character bios and images using AI models.
- **Multiple LLM Support**: Choose from various large language models to drive NPC interactions.
- **Action System**: Perform actions like Investigate, Research, or Gather Supplies to navigate complex scenarios.
- **Playthrough Management**: Manage different playthroughs, each with its own player character.
- **Customizable Settings**: Configure AI models and application behavior through config files.

## Prerequisites

- **Python**: Ensure you have Python 3.11 or later installed.
- **Conda**: Anaconda or Miniconda installed for environment management.
- **Git**: For cloning the repository.

## Installation

Follow these steps to set up Neural Narrative on your local machine:

### Clone the Repository

```bash
git clone https://github.com/joeloverbeck/neural-narrative.git
cd neural-narrative-generator
```

### Update Conda

```bash
conda update conda
```

### Create a Conda Environment

- To create an environment with the latest Python:

```bash
conda create -n neural-narrative-env python
```

- (Optional) To specify a specific Python version:

```bash
conda create -n neural-narrative-env python=3.11
```

### Activate the Environment

```bash
conda activate neural-narrative-env
```

### Install Requirements

```bash
pip install -r requirements.txt
```

## Usage

### Run the Application

```bash
python web_chat.py
```

### Access the Web Interface

Open your web browser and navigate to http://localhost:8080 to start using the application.

## Configuration

The application can be customized through various configuration files located in the root directory and the **data**
folder.

## AI Models Configuration

You can change the AI models used for different functions in the app by editing the **llms.json** file:

```bash
data/llms/llms.json
```

## Application Settings

Modify the **config.json** file to adjust application settings such as enabling voice lines:

```json
{
  "produce_voice_lines": "true",
  ...
}
```

## API Keys Setup

To fully utilize the application's features, you'll need to set up API keys for OpenRouter, OpenAI, and RunPod.

### OpenRouter API Key

#### Create an OpenRouter Account

- Sign up at [OpenRouter](https://openrouter.com/).

#### Add Credits and Generate API Key

- Add credits to your account.
- Generate an API key.

#### Store the API Key

Save the API key to a file named **OPENROUTER_SECRET_KEY.txt** in the root of the repository.

```bash
echo 'your-openrouter-api-key' > OPENROUTER_SECRET_KEY.txt
``` 

### OpenAI API Key

The application uses OpenAI models to generate images for characters.

#### Create an OpenAI Account

- Sign up at [OpenAI](https://openai.com/).

#### Add Funds and Create a Project

- Add billing details and ensure you have sufficient funds.
- Create a new project via the OpenAI Dashboard.

#### Generate an API Key

- Generate an API key for your project.

#### Store the API Key

Save the API key to a file named **OPENAI_PROJECT_KEY.txt** in the root of the repository.

```bash
echo 'your-openai-api-key' > OPENAI_PROJECT_KEY.txt
```

### RunPod API Key (Optional)

If you enable the **produce_voice_lines** feature, you'll need a RunPod API key.

#### Create a RunPod Account

- Sign up at [RunPod](https://runpod.io/).

#### Create a Pod

- Create a pod using the **xtts-mantella-custom-voices-pack** template.

#### Generate an API Key

- Generate an API key for your pod.

#### Store the API Key

Save the API key to a file named **RUNPOD_SECRET_KEY.txt** in the root of the repository.

```bash
echo 'your-runpod-api-key' > RUNPOD_SECRET_KEY.txt
```

## Contributing

Contributions are welcome! If you encounter any bugs or have feature suggestions,
please [open an issue](https://github.com/joeloverbeck/neural-narrative/issues) or submit a [pull
request](https://github.com/joeloverbeck/neural-narrative/pulls).

## License

This project is licensed under
the [GPL-3.0 license](https://github.com/joeloverbeck/neural-narrative?tab=GPL-3.0-1-ov-file#readme).

## Contact

If often post about this app and my playthroughs on [my site](https://jonurenawriter.com/). You can contact me through
it if you want.

