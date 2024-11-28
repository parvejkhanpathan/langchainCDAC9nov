# ---
# # Exercise: Configuring Language Models and Prompts

# ## Objective
# To practice configuring language models (Cohere, Groq) and creating prompt templates to generate a story.

# ## Instructions
# Follow the steps below:

# 1. **Create `actor_picker` Function**:
#    - Write a function named `actor_picker()` that randomly returns an actor's name. You can use Python's random generator to select an actor.

# 2. **Create `location_picker` Function**:
#    - Write a function named `location_picker()` that randomly returns the name of a location.

# 3. **Create `theme_picker` Function**:
#    - Write a function named `theme_picker()` that randomly returns a theme.

# 4. **Configure and Use Cohere Model**:
#    - Set up the Cohere model using `ChatCohere`.
#    - Create a prompt template that generates a story centered around the chosen **Actor**, **Location**, and **Theme** using the Cohere model.
#    - Print the detailed story output from the model.

# 5. **Configure and Use Groq Model**:
#    - Set up the Groq model using `ChatGroq`.
#    - Create a prompt template to generate a story using the Groq model.
#    - Print the detailed response from the model.
     
# 6. **Add InMemoryChatMessageHistory to store conversation**:
#    - Use 'InMemoryChatMessageHistory', to store history and allow user customize the story.
#    - You can pass the story created with prompt saying 'change the given story according to user input'.

# 6. **Execution**:
#    - When you run the code, it should randomly pick an actor, location, and theme, then generate a story around these elements. Then it should ask for user input to customize the story. You may include heroines in the story for added detail.

# ## Example Output

# ### Selected Elements
# - **Actor**: Chris Evans
# - **Location**: New York
# - **Theme**: Adventure

# ---

# ### Story from Cohere Model
# Chris Evans found himself in the bustling streets of New York, surrounded by towering skyscrapers and the endless hum of city life. One evening, while exploring an old library, he stumbled upon a mysterious map hidden in a dusty, leather-bound book. The map hinted at an ancient artifact buried deep beneath the city, a relic that could change the course of history. Determined to uncover the truth, Chris embarked on a thrilling adventure, navigating secret tunnels, facing unexpected dangers, and relying on his courage to guide him through the labyrinthine passages beneath the city. With each step, he realized this journey would not only test his strength but also reveal secrets of New York’s hidden past. Would he find the artifact? Only time would tell.

# ---

# ### Story from Groq Model
# In the heart of New York, where lights shimmer like stars, Chris Evans was drawn into an unexpected journey. The city had always held secrets, but tonight it felt alive, whispering to him through the cold night air. Following an old legend, he ventured into abandoned subway stations and hidden alleyways, guided only by a cryptic poem and his instinct. Each clue led him closer to a fabled artifact said to hold immense power. Alongside a mysterious heroine he met along the way, Chris faced twists and turns that tested their resolve. In the end, the adventure would unveil not just the artifact but a part of himself he never knew existed.

import os
import configparser

from langchain_groq import ChatGroq
from langchain_cohere import ChatCohere
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage

config = configparser.ConfigParser()
config.read('/workspaces/langchainCDAC9nov/config.ini')
groq = config['groq']
cohere = config['cohere']

os.environ['GROQ_API_KEY'] = groq.get('GROQ_API_KEY')
os.environ['COHERE_API_KEY'] = cohere.get('COHERE_API_KEY')

def actor_picker():
   # d1={1:'Rajkumar Rao',2:'Salman khan',3:'Sanjay Dutt',4:'Irfan khan',5:'Ajay Devgn'}
   messages = [
       SystemMessage(content='You are a random actor_picker service. You will provide a different bollywood male actor name every time user ask you.Return different actor name every time just name and last name' ),
       HumanMessage(content='give me different actor name everytime I ask you')
   ]
   parser=StrOutputParser()
   
   model= ChatGroq(model="llama3-8b-8192")
   chain=model|parser
   response=chain.invoke(messages)
   return response

def location_picker():
    messages = [
       SystemMessage(content='You are a random location_picker service. You will provide a random location name and country.Return only different location name and country in one to two word' ),
       HumanMessage(content='give me different location name everytime I ask you in one word')
   ]
    parser=StrOutputParser()
   
    model = ChatCohere(model="command-r-plus")
    chain=model|parser
    response=chain.invoke(messages)
    return response

def theme_picker():
    messages = [
       SystemMessage(content='You are a random theme_picker service. You will provide a random theme for a movie .Return different theme every time for a movie in one or two words.' ),
       HumanMessage(content='give me different theme name everytime I ask you in one word')
   ]
    parser=StrOutputParser()
   
    model = ChatCohere(model="command-r-plus")
    chain=model|parser
    response=chain.invoke(messages)
    return response
actor=actor_picker()
location=location_picker()
theme=theme_picker()


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()
system_template = "Return an output in string form as a story reading the variables {actor},{location} and {theme} from above code."
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system_template),
        ("user", 'Create a story for a movie in which the actor is {actor} from above code, the location is {location} and the theme for the movie is {theme}.Tell the genre, location and starring for the movie and then display story.')  # Use string representation of my_list here
    ]
)

def story_generator():
    model_groq = ChatGroq(model="llama3-8b-8192")
    chain = prompt_template | model_groq | parser

    final_story_output = chain.invoke({"actor":actor,"location":location,"theme":theme})

    print(final_story_output)
    return final_story_output

def story_generator2():
    model = ChatCohere(model="command-r-plus")
    chain = prompt_template | model | parser

    final_story_output = chain.invoke({"actor":actor,"location":location,"theme":theme})

    
story=story_generator()
# story_generator()
# print("******************************Cohere Story****************************")
# story_generator2()

model = ChatGroq(model="llama3-8b-8192")

from langchain_core.chat_history import(InMemoryChatMessageHistory)
import asyncio
store=InMemoryChatMessageHistory()

async def func1():
    store.add_message(HumanMessage(content=f'{story}'))
    messages = await store.aget_messages()
    response = model.invoke(messages)
    print(response.content)
    store.add_message(SystemMessage(content=response.content))
# async def func2():
#     await asyncio.sleep(2)  
#     system_message_content = "Please ensure the story aligns with the requested changes and return the output in paragraphs."
#     store.add_message(SystemMessage(content=system_message_content))

#     user_input = input("Tell if you want to make changes to your story: ")
#     store.add_message(HumanMessage(content=user_input))

#     messages = await store.aget_messages()
#     print("Messages so far:", messages)
    
#     response = model.invoke(messages)
#     print("Model Response:", response.content)

#     store.add_message(SystemMessage(content=response.content))
from langchain_core.output_parsers import StrOutputParser

async def func2():
    parser = StrOutputParser()  # Add the parser for handling the response
    await asyncio.sleep(2)  
    system_message_content = "Please ensure the story aligns with the requested changes and return the output in paragraphs."
    store.add_message(SystemMessage(content=system_message_content))

    # Ask for user input to modify the story
    user_input = input("Tell if you want to make changes to your story: ")
    store.add_message(HumanMessage(content=user_input))

    # Fetch the updated messages from the chat history
    messages = await store.aget_messages()
    # print("Messages so far:", messages)

    # Invoke the model with the chat history
    response = model.invoke(messages)

    # Parse the model's response
    parsed_response = parser.parse(response.content)
    print("Model Response:", parsed_response)

    # Add the parsed response back to the chat history
    store.add_message(SystemMessage(content=parsed_response))


async def main():
    await func1()
    await func2()

# story = story_generator()
asyncio.run(main())
                    