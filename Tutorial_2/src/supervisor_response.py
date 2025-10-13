import sys

## import supervisor query function
from utilities.utility_funcs import supervisor_query

## Import Agent
from Agent_MolecSims.agent_1 import molec_prep_agent, conversational_agent


## Create Supervisor Agent
from langgraph_supervisor import create_supervisor
from langchain.chat_models import init_chat_model

supervisor = create_supervisor(
    model=init_chat_model('gpt-oss:20b', model_provider='ollama'),
    agents=[conversational_agent, molec_prep_agent],
    prompt=(
        "You are a supervisor managing two agents:\n"
        "- a conversational agent. Assign conversational tasks to this agent\n"
        "- a molecular simulation agent. Assign molecular simulation-related tasks to this agent\n"
        "Assign work to one agent at a time, do not call agents in parallel.\n"
        "Do not do any work yourself."
    ),
    add_handoff_back_messages=True,
    output_mode="full_history",
).compile()



# Function to generate a response to user input
def generate_response(supervisor, user_input):
    # Your logic for generating a response goes here
    #model_response = "test response"
    model_response = supervisor_query(supervisor, user_input)
    return model_response

if __name__ == "__main__":
    # Get user input from command line
    user_input = sys.argv[1]
    # Generate response
    response = generate_response(supervisor, user_input)
    
    # Print the response
    print(response)


