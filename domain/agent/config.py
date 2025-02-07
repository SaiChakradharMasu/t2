# from .function_declarations.function_declarations import function_declarations_list

def read_system_instruction():
    # with open("./system_instruction.txt", 'r') as archivo:
    with open("./domain/agent/system_instruction.txt", 'r') as archivo:
        contenido = archivo.read()
    return contenido

# system_instruction = read_system_instruction()

agent_config = {
    "model_name": "gemini-1.5-flash",
    "generation_config":  {
        "top_p": 0.95,
        "temperature": 1,
        "top_k": 64,
        "max_output_tokens": 8192
    },
    # "system_instruction": system_instruction,
    # "tools": function_declarations_list.values()
}

# print(agent_config)