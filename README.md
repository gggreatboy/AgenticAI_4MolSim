# Agentic AI Tutorials 

## Installation and Usage 
We provide a conda enviroment that you can activate with the following command:
```bash
conda activate /groups/ycolon/group-envs/agentic-tutorials
```

Alternatively, run the `install_from_scratch.sh` file. Make desired changes to this installation. Users have the option to just installed Ollama running the `install_ollama.sh` script. The enviroment variable called `OLLAMA_MODELS` defines the path where the model's weights will be stored. Make relevant changes considering models are around ~15 GB. 

**MAKE SURE OLLAMA IS INSTALLED AND WORKING**
Note: Ollama is being used to integrate open-source LLMs, but if you have API keys for private models you can add them to the '.env' file. For Ollama, be sure to run `ollama serve` in an individual terminal so it can be used with LangChain workflows. Once this command is running, on a new terminal run the command `ollama pull model_name`, where model_name is one of the available open-source models. we currently recommend `gpt-oss:20b` or `qwen3:14b`. List of availale models is here: https://ollama.com/search


## Chatbot vs Agent Notebook
It is recommended to run this notebook to familiarize with essential concepts of this workflow and test installations. 

## Tutorial 1: AI Agents with custom tools
In this tutorial we will learn how to use LangChain to automate tasks using custom functions. As a test case we will Generate configurations of a molecular solvent, run a simulation and analyze trajectory results. For this, we will primarily use MoSDEF and LAMMPS. For detailed instructions see `Tutorial1_Doc.md`


## Tutorial 2: Agentic AI with LangGraph
THis tutorial builds on the basic concepts introduced in Tutorial one, and improve the capability of agents to plan and execute steps to achieve more complex tasks than what is capable with LangChain. The `Agent-2-dev.ipynb` notebook has the same functions developed in Tutorial 1, but changes the framework of the Agentic framework to build a Multi-Agent Supervisor grpah (https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/#research-agent). 

This framework is then converted into a package that enables using the agent directly on the terminal and the source files are stored at `Tutorial_2/src`. To use this form of the framework run the `chatbot.sh` script. 


