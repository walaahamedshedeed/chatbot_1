#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from chatbot_1.crew import Chatbot1
import time

from mem0 import Memory
from dotenv import load_dotenv

load_dotenv()


# from RealtimeSTT import AudioToTextRecorder
# from elevenlabs import play
# from elevenlabs.client import ElevenLabs
import os

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")


config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "chatbot_memory",
            "path": "./chroma_db",
        },
    },
}

memory = Memory.from_config(config) 

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    print("Wait until it says 'speak now'")
    
    # client = ElevenLabs(
    #     api_key=ELEVENLABS_API_KEY, # Defaults to ELEVEN_API_KEY or ELEVENLABS_API_KEY
    # )
    # recorder = AudioToTextRecorder(language="en")
    while True:
        user_input = input("You: ")
        try:
            # text = recorder.text()
        
            # print(text)
            # recorder.stop()
            # user_input = text
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Chatbot: Goodbye! It was nice talking to you.")
                break
            
            start_time = time.time()
            print("adding  user message to memory")
            # Add user input to memory
            memory.add(f"User: {user_input}", user_id="Lennex")

            print("searching memory")
            # Retrieve relevant information from vector store
            relevant_info = memory.search(query=user_input,user_id="Lennex", limit=3)
            context = "\\n".join(message["memory"] for message in relevant_info)
            print(context)

            inputs = {
                "user_message": f"{user_input}",
                "context": f"{context} The current time is :  {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, today is {datetime.now().strftime("%A")}",
            }

            print("inputs",inputs)
        
            print("calling chatbot")
            response = Chatbot1().crew().kickoff(inputs=inputs)
            print(f"Time taken: {time.time() - start_time} seconds")

            # Add chatbot response to memory
            print(f"Assistant: {response} - {type(response)}")
            
            # audio = client.generate(
            #     text=str(response),
            #     voice="Mark - Natural Conversations",
            #     model="eleven_flash_v2_5",
            # )

            # play(audio)
            memory.add(f"Assistant: {response}", user_id="Assistant")
        except Exception as e:
            print(f"Error occurred: {e}")
            # print("Restarting recording...")
            # time.sleep(1)
            # continue



def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Chatbot1().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        Chatbot1().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        Chatbot1().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
