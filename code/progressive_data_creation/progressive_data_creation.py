import os
import openai
import time
import json
import requests
import numpy as np
import tqdm
import pandas as pd
openai.api_key = ''#your key


def create_chat_completions(messages):
    """
    Create a list of message objects for the OpenAI API.
    Each message object should have a 'role' ("system", "user", or "assistant")
    and 'content' (the actual text of the message).
    """
    chat = []
    for role, text in messages:
        chat.append({
            'role': role,
            'content': text
        })
    return chat

def chat_with_gpt(messages, T=0.95, max_tokens=3000):
    """
    Send a list of messages to the ChatGPT API and get the model's response.
    """
    model = 'gpt-4'  # Model name

    chat = create_chat_completions(messages)
    while True:
        try:
            completion = openai.ChatCompletion.create(
                model=model,
                messages=chat,
                temperature=T,
                  max_tokens=max_tokens,
                  top_p=1,
                  frequency_penalty=0,
                  presence_penalty=0
            )
            return completion.choices[0].message.content
        except:
            time.sleep(1)
            continue

    return completion.choices[0].message.content

def generator(column_name, instruction_text, iter_every=10, skip_first=0):
	#Data loader
    text = ''
    current_number = 0
    start = 0+skip_first*iter_every
    for index, iter2 in zip(df['ID'][start:],df[column_name][start:]):
        current_number +=1
        text += f"{index}\t{iter2}\n"

        if current_number ==iter_every:
            text += '\n'+instruction_text
            yield text
            text = ''
            current_number=0
    text += '\n'+instruction_text
    yield text

hf_api_token = '' #insert your api token for huggingface, used to compute semantic similarity
API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {hf_api_token}"}
def query(payload):
    while True:
        response = requests.post(API_URL, headers=headers, json=payload)
        if isinstance(response.json(), list):
            return response.json()


def gen_iter1(tags,number_per_batch=15):
	'''
	Generate iter1 problems from input (a list of tags)
	input: tags = ['dining room', 'in the winter', 'rooftop terrace'] #example tags
		   number_per_batch: we generate problems in batches of 15 to promote diversity
	'''
	problems = []
	for tag in tags:
	    print(f'{tag}=====')

	    instruction_iter1 = f'''Generate {number_per_batch} problems that require physical problem solving skills, where the most handily available tools are not available and thus require 1) using other tools in an unconventional and creative way; and 2) multi-step planning.

	    Here are some examples:
	    1. You are hiking in the rain and accidentally drop your eyeglasses into a river. The water is too deep for you to reach them with your hands. The available items are a fishing net, a rope, a plastic container, a pencil, and a small towel. How can you retrieve your eyeglasses using only these items?
	    2. You need to staple a stack of papers together, but your stapler is out of staples, and you don't have any paperclips or binder clips. You have a pen, scissors, and a roll of masking tape. How can you securely fasten the papers together?
	    The problems should be related to {tag}. Provide necessary details.'''
	    conversation = [
	            ("user", instruction_iter1),
	        ]
	    response = chat_with_gpt(conversation).replace('\n\n','\n')
	    print(response)
	    problems.append(response.replace("Problem:","").strip('\n.1234567890 '))
	return problems


def gen_iter2(df=df,column_name='iter1'):
	'''
	Add constraints to veto a possible solution.
	Input: df: dataframe that stores the iter1 problems (in a column_name='iter1')
	'''
	
	instruction_iter2 = '''For each problem, can you add a description (such as material) to make the problem constrained and more challenging? Let's start by coming up with the solution to each problem. Then based on the solution, add reasonable constraints to the problem setting to make the original solution no longer valid.

	Use the following format: 
	1. Solution: 
	We can add the following constraints or description:

	Make sure the constraints added are reasonable and likely to ever exist.
	'''

	problems = []
	instruction_add_constraint = '''Good. Now insert the modified constraint to the original problem. Add the constraint after you present all available tools, before the last sentence starting with "How".'''
	for text in generator(column_name, instruction_iter2, skip_first=0):
	    
	    #step1: generate solutions and constraints
	    conversation = [
	            ("user", text),
	        ]
	    response = chat_with_gpt(conversation).replace('\n\n','\n')
	    

	    #step 2: add constraints to the original problem statement
	    conversation.append(("assistant", response))
	    conversation.append(("user", instruction_add_constraint))
	    response = chat_with_gpt(conversation).replace('\n\n','\n')
	    #print(response)
	    problems.append(response)
	    
	return problems

def gen_iter3(df=df,column_name='iter2'):
	'''
	Add additional tools as potential distractors.
	Input: df: dataframe that stores the iter2 problems (in a column_name='iter2')
	'''

	instruction_iter3 = 'For each problem, add five additional tools that are related but not used to solve the problems. They should serve as distractors to make the problem more challenging. Show the problem in the same format.'
	instruction_shuffle = "For each updated problem with additional tools, shuffle the order of the available tools. Keep the rest of the problem setting unchanged. Repeat the problem in the same format."
	
	problems = []
	for text in generator(column_name, instruction_iter3, skip_first=0):
	    conversation = [
	            ("user", text),
	        ]
	    response = chat_with_gpt(conversation).replace('\n\n','\n')
	   
	    
	    conversation.append(("assistant", response))
	    conversation.append(("user", instruction_shuffle))
	    response = chat_with_gpt(conversation).replace('\n\n','\n')
	    #print(response)
	    problems.append(response)
	return problems



if __name__ == "__main__":
	tags = ['dining room', 'in the winter', 'rooftop terrace'] #example tags
	filename = 'progressive_data_creation_new.xlsx' #the file that will be used to store the newly generate problems 
	#call gen_iter1,2,3 respectively to create the problem, and save them to {filename}
	
	

	#After that, compute semantic similarity and remove similar problems
	xl = pd.ExcelFile(filename)
	df = xl.parse('Sheet1') 

	database_filename = "database.xlsx" #the file that contains previously generated problems
	db = pd.ExcelFile(database_filename) 
	database = db.parse('Sheet1')
	existing_problems = list(database['iter3'] )

	T = 0.7 #remove all problems if similarity >T
	indices_to_drop=[]
	for index, row in tqdm.tqdm(df.iterrows()):
	    
	    source_sentence = row['iter1']
	    
	    similarity_scores = query(
	    {
	        "inputs": {
	            "source_sentence": source_sentence,
	            "sentences":existing_problems
	        }
	    })
	    if np.max(similarity_scores) >T:
	        print(np.max(similarity_scores), source_sentence)
	        indices_to_drop.append(index)
	df = df.drop(indices_to_drop)
	with pd.ExcelWriter(filename,mode='a', engine='openpyxl') as writer:
    	df.to_excel(writer, sheet_name='filtered_similar', index=False)
