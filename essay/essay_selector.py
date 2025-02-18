# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import json
from promptflow.core import tool
import os
from promptflow.core import Prompty
from promptflow.core import AzureOpenAIModelConfiguration
# import blob storage
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need

load_dotenv()

class BlobClient:
    def __init__(self, prompty_file: str):
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.container = "prompts"
        self.prompt_file = prompty_file

    def __call__(self, blob_name: str):
        temp_file_path = os.path.join(os.getcwd(), blob_name)
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        container_client = blob_service_client.get_blob_client(container=self.container, blob=blob_name)
        with open(file=temp_file_path, mode="wb") as download_file:
            download_file.write(container_client.download_blob().readall())

        return temp_file_path

class Essay:
    def __init__(self, model_config: AzureOpenAIModelConfiguration):
        self.model_config = model_config

    def __call__(self, essay: str) -> str:
        # parse essay as a json
        essay = json.loads(essay)
        print("Essay type: " + essay['essay_type'])
        prompt_file_name = essay["essay_type"] + ".prompty"
        blob_client = BlobClient(prompt_file_name)
        prompt_file = blob_client(blob_name=prompt_file_name)
        prompty = Prompty.load(source=prompt_file)

        result = prompty(
            language=essay["language"],
            genre=essay["genre"],
            statement=essay["statement"],
            title=essay["title"],
            essay=essay["essay"],
            support_material=essay["support_text"],
            skills=essay["skills"]
        )
        return result

@tool
def essay_selector(essay: str) -> str:
    model_config = AzureOpenAIModelConfiguration(
            azure_deployment=os.getenv("AZURE_DEPLOYMENT")
        )
    essay_instance = Essay(model_config)
    result = essay_instance(essay)
    return result
    
