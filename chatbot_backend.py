# Import the necessary modules
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_aws import ChatBedrock
import boto3
import json
import langchain.globals as lg

# Set verbose mode if needed
lg.set_verbose(True)

# Define the keywords and common context
def format_model_id(model_id):
    if '-' in model_id and '.' in model_id:
        formatted_model_id = model_id.replace('.', '_').replace(':', '_')
    else:
        formatted_model_id = model_id
    return formatted_model_id

def load_prompt_template_from_s3(bucket_name, model_id):
    formatted_model_id = format_model_id(model_id)
    file_name = f"{formatted_model_id}.json"
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)
    prompt_template = obj['Body'].read().decode('utf-8') 
    return prompt_template

keywords = ["plant", "alarms", "criticality"]  # Removed "akron" from keywords
json_data = load_prompt_template_from_s3('prompttemplatebucket', 'alarm_intent')
json_data = json.loads(json_data)

alarm_context = " ".join([
    f"{plant['Plant']} there are {len(plant['Alarms'])} critical alarms. Those are " + 
    ", ".join([
        f"\"{alarm['AlarmName']}\" Alarm detected for {alarm['Equipmennt']} : {alarm['Equipmennt']} in plant {plant['Plant']}. Criticality Level : \"{alarm['Criticality']}\"." 
        for alarm in plant['Alarms']
    ]) 
    for plant in json_data
])

model_kwargs_dict = {
    'anthropic.claude-3-haiku-20240307-v1:0': {
        "max_tokens": 300,
        "temperature": 0.1,
        "top_p": 0.9,
        "stop_sequences": ["\n\nHuman:"]
    },
    'meta.llama3-8b-instruct-v1:0': {
        "max_gen_len": 512,
        "temperature": 0.5,
        "top_p": 0.9
    }
}

# Initialize the chatbot and memory once
def initialize_chatbot(model_id):
    model_kwargs = model_kwargs_dict[model_id]
    demo_llm = ChatBedrock(
       credentials_profile_name='default',
       model_id=model_id,
       model_kwargs=model_kwargs)
    print(f"Chatbot initialized with model_id: {model_id}")
    return demo_llm
    
def initialize_memory(llm_var):
    if llm_var is None:
        raise ValueError("llm_var is not initialized")
    print(f"Initializing memory with llm_var: {llm_var}")
    memory = ConversationSummaryBufferMemory(llm=llm_var, max_token_limit=300)
    print("Memory Initialized: ", memory)
    return memory

# Function to extract plant names
def extract_plant_names():
    return [plant['Plant'] for plant in json_data]

# Function to attach the common context to the user input
def attach_context(user_input, context_appended, plant_names, session_state):
    if not context_appended:
        print("plant names:", plant_names)
        
        words = user_input.split()
        print("Words:", words)
        for word in words:
            if word in keywords:
                # Check for plant names in user_input
                for name in plant_names:
                    if name.lower() in [word.lower() for word in words]:  # Case-insensitive match
                        session_state['plant_name'] = name
                        print("true**********************", name)
                        # Update the alarm context for the specific plant
                        filtered_alarms = [
                            f"{plant['Plant']} there are {len(plant['Alarms'])} critical alarms. Those are " + 
                            ", ".join([
                                f"\"{alarm['AlarmName']}\" Alarm detected for {alarm['Equipmennt']} : {alarm['Equipmennt']} in plant {plant['Plant']}. Criticality Level : \"{alarm['Criticality']}\"." 
                                for alarm in plant['Alarms']
                            ]) 
                            for plant in json_data if plant['Plant'].lower() == name.lower()
                        ]
                        filtered_context = " ".join(filtered_alarms)
                        user_input += " " + filtered_context
                        context_appended = True
                        return user_input, context_appended, name
        
    return user_input, context_appended, session_state.get('plant_name', None)

# Function to initialize the conversation
def start_conversation(input_text, llm, memory, model_id, context_appended, plant_names, session_state):
    llm_conversation = ConversationChain(llm=llm, memory=memory, verbose=True)
    input_text, context_appended, plant_name = attach_context(input_text, context_appended, plant_names, session_state)
    print("plant name :", plant_name)
    if plant_name is None:
        return "Please provide the plant name in the input text.", context_appended

    prompt_template = load_prompt_template_from_s3('prompttemplatebucket', model_id)
    prompt_template = prompt_template.replace('{question}', input_text)
    prompt_template = prompt_template.replace('{context}', alarm_context)
    chat_reply = llm_conversation.invoke(prompt_template)
    
    # Ensure inputs have a single key
    memory.save_context({"text": input_text}, {"text": chat_reply['response']})
    print(memory)
    
    return chat_reply['response'], context_appended
