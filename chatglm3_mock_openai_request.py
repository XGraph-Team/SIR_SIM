import requests
import json

base_url = "http://127.0.0.1:8000"

# this dose not make any differences??
# model = "chatglm3-6b"
model = "chatglm3-6b-32k"

def create_chat_completion(model, messages, functions, use_stream=False):
    data = {
        "functions": functions,  
        "model": model,  
        "messages": messages, 
        "stream": use_stream, 
        "max_tokens": 32000,  
        "temperature": 0.8,  
        "top_p": 0.8, 
    }

    response = requests.post(f"{base_url}/v1/chat/completions", json=data, stream=use_stream)
    if response.status_code == 200:
        if use_stream:
          
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')[6:]
                    try:
                        response_json = json.loads(decoded_line)
                        content = response_json.get("choices", [{}])[0].get("delta", {}).get("content", "")
                        print("OK:", response.status_code)
                        print(content)
                    except:
                        print("OK:", response.status_code)
                        print("Special Token:", decoded_line)
        else:
           
            decoded_line = response.json()
            content = decoded_line.get("choices", [{}])[0].get("message", "").get("content", "")
            print("OK:", response.status_code)
            print(content)
    else:
        print("Error:", response.status_code)
        # print("Error:", response)
        return None

def get_str(file_path):

    # Open the file and read its contents into a string
    with open(file_path, 'r') as file:
        file_str = file.read()

    # Now `file_str` contains the entire contents of the file as a single string
    return file_str 

def single_chat(use_stream=True):
    functions = None

    user_str = "I am providing the edge list of the graph. The first column is the source, the second column is the target, the third column is the weight:\n"
    file_path = '/home/zz242/SIR_SIM/temp/weighted_edge_list_connSW_run0.txt'
    user_str = user_str + get_str(file_path)
    print(user_str)

    chat_messages = [
        {
            "role": "system",
            "content": "I would like you to take on the role of a network science researcher. You will receive a graph that I have created using a Python library known as networkx, along with the parameters that were used in its creation. Additionally, I have utilized this graph to conduct SIR (Susceptible-Infectious-Recovered) simulations over multiple iterations. From these simulations, I have compiled three types of datasets: one tracking the progression of infections (forward dataset), one tracking the regression (backward dataset), and a third combining both approaches (mixed forward/backward dataset). I will select specific iterations and their corresponding infected nodes from one of these datasets at random. Your task will be to analyze this data to predict potential future infections (downstream infected nodes) as well as to trace back the source of the infections (upstream infected nodes).",
        },
        #  for a single chat
        {
            "role": "user",
            "content": user_str
        }
    ]
    response = create_chat_completion(model, messages=chat_messages, functions=functions, use_stream=use_stream)

def multi_chat(use_stream=True):
    functions = None
    
    graph_str = "I am providing the edge list of the graph. The first column is the source, the second column is the target, the third column is the weight:\n"
    file_path = '/home/zz242/SIR_SIM/temp/weighted_edge_list_connSW_run0.txt'
    graph_str = graph_str + get_str(file_path) + "\nI will use this graph to run SIR simulations for several iterations"

    print(graph_str)

    infected_str = "I am providing the inffected nodes in the 4th iterations (Indexing from 0). \n"
    file_path = '/home/zz242/SIR_SIM/temp/iteration_4_infected_nodes.txt'
    infected_str = infected_str + get_str(file_path) + "\n Could you predict the inffected nodes in the 5th iteration and track back to the infected nodes in the 3rd iteration?"

    chat_messages = [
        {
            "role": "system",
            "content": "I would like you to take on the role of a network science researcher. You will receive a graph that I have created using a Python library known as networkx, along with the parameters that were used in its creation. Additionally, I have utilized this graph to conduct SIR (Susceptible-Infectious-Recovered) simulations over multiple iterations. From these simulations, I have compiled three types of datasets: one tracking the progression of infections (forward dataset), one tracking the regression (backward dataset), and a third combining both approaches (mixed forward/backward dataset). I will select specific iterations and their corresponding infected nodes from one of these datasets at random. Your task will be to analyze this data to predict potential future infections (downstream infected nodes) as well as to trace back the source of the infections (upstream infected nodes).",
        }
    ]
  

    # for multiple chats
    user_qs = [
        graph_str, 
        infected_str, 
        # "Tell me more about the graph I just provided."
        ]

    for q in user_qs:
        user_dict = {"role": "user", "content": q}
        chat_messages.append(user_dict)

        response = create_chat_completion(model, messages=chat_messages, functions=functions, use_stream=use_stream)

        # assistant_dict = dict(response["choices"][0]["message"])
        # chat_messages.append(assistant_dict)

    #### chat gpt sample for multi chats
    # messages = [{"role": "system",
    #          "content": "You are a data science tutor who provides short, simple explanations."}]

    # user_qs = ["Why is Python so popular?", "Summarize this in one sentence."]

    # for q in user_qs:
    #     user_dict = {"role": "user", "content": q}
    #     messages.append(user_dict)

    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=messages
    #     )

    #     assistant_dict = dict(response["choices"][0]["message"])
    #     messages.append(assistant_dict)

if __name__ == "__main__":
    # single_chat(use_stream=False)
    multi_chat(use_stream=False)
