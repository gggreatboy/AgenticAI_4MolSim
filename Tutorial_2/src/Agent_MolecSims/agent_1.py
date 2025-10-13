from langgraph.prebuilt import create_react_agent
from langchain_ollama.chat_models import ChatOllama

## import functions from utilities.utility_funcs
import sys
import os

# # Get absolute path to the 'src' directory
# current_dir = os.path.dirname(os.path.abspath(__file__))
# src_dir = os.path.abspath(os.path.join(current_dir, '..'))
# sys.path.append(src_dir)
# from utilities.utility_funcs import pretty_print_messages, supervisor_query

## Import tools
from .agent_1_tools import molnum, gen_lammps_data, create_lammps_input_file, ensemble_average

conversational_agent = create_react_agent(
    model=ChatOllama(model="gpt-oss:20b"),
    tools=[],
    prompt=(
        "You are a Conversational agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Assist ONLY with tasks that do not require any tools. Only respond with text, DO NOT do any math\n"
        "- After you're done with your tasks, respond to the supervisor directly\n"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."
    ),
    name="conversational_agent",
)


molec_prep_agent = create_react_agent(
    model=ChatOllama(model="gpt-oss:20b"),
    tools=[molnum,gen_lammps_data,create_lammps_input_file,ensemble_average],
    prompt=(
        "You are a Molecular simulation agent.\n\n"
        "INSTRUCTIONS:\n"
        "- Assist ONLY with tasks related to molecular Dynamics and use relevant tools, DO NOT do any math\n"
        "- After you're done with your tasks, respond to the supervisor directly\n"
        "- Respond ONLY with the results of your work, do NOT include ANY other text."
    ),
    name="molec_prep_agent",
)

# ## Function to call the agent
# def agent_2_response(input_text:str):
#     for chunk in molec_prep_agent.stream(
#         {"messages": [{"role": "user", "content": input_text}]}
#     ):
#         pretty_print_messages(chunk)