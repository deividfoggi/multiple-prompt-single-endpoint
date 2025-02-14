from dotenv import load_dotenv  # Import the load_dotenv function from the dotenv module
load_dotenv()  # Load environment variables from a .env file

from sys import argv  # Import argv from the sys module
import os  # Import the os module
import pathlib  # Import the pathlib module
from promptflow.tools.common import init_azure_openai_client  # Import init_azure_openai_client from promptflow.tools.common
from promptflow.connections import AzureOpenAIConnection  # Import AzureOpenAIConnection from promptflow.connections
from promptflow.core import (AzureOpenAIModelConfiguration, Prompty, tool)  # Import AzureOpenAIModelConfiguration, Prompty, and tool from promptflow.core
from flask import Flask, request, jsonify  # Import Flask, request, and jsonify from the flask module
from essay_type_a.essay_type_a import EssayTypeA  # Import EssayGradeA
from essay_type_b.essay_type_b import EssayTypeB  # Import EssayGradeB

@tool  # Decorator to define a tool
def get_response(essay_request):  # Define the get_response function
    print("inputs:", essay_request)  # Print the inputs
    print("getting result...")  # Print a message indicating that the result is being obtained

    model_config = AzureOpenAIModelConfiguration(  # Create an instance of AzureOpenAIModelConfiguration
       azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", ""),  # Get the AZURE_OPENAI_CHAT_DEPLOYMENT environment variable
       api_version=os.getenv("AZURE_OPENAI_API_VERSION", ""),  # Get the AZURE_OPENAI_API_VERSION environment variable
       azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),  # Get the AZURE_OPENAI_ENDPOINT environment variable
       api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),  # Get the AZURE_OPENAI_API_KEY environment variable
    )
    # at any time you can override the model configuration and use it in your flow class
    # override_model = {
    #     "configuration": configuration,
    #     "parameters": {"max_tokens": 512}
    # }
    
    # in this example we select the case based on the essay_type property from essay_request
    essay_type = essay_request['essay_type']  # Get the essay type from the essay_request

    result = ""  # Initialize the result variable

    if essay_type == 'essay_type_a':  # Check if the essay type is 'Poema Falado (Poetry Slam)'
        #calling using class based flow
        essay_type_a = EssayTypeA(model_config)  # Create an instance of Essay Type A
        result = essay_type_a(essay_request)  # Get the result from the Essay Type A instance
    elif essay_type == 'essay_type_b':  # Check if the essay type is 'redacao simples'
        #calling using class based flow
        essay_type_b = EssayTypeB(model_config)  # Create an instance of Essay Type B
        result = essay_type_b(essay_request)  # Get the result from the Essay Type B instance

    return result  # Return the result

# create an api to receive a post using flask

app = Flask(__name__)  # Create an instance of the Flask class

@app.route('/score', methods=['POST'])  # Define a route for the /score endpoint that accepts POST requests
def essay_request_router():  # Define the essay_request_router function
    essay_request = request.get_json()  # Get the JSON data from the request
    response = get_response(essay_request)  # Get the response from the get_response function
    return response  # Return the response

if __name__ == "__main__":  # Check if the script is being run directly
   app.run(port=8080, debug=True)  # Run the Flask app on port 8080 with debug mode enabled