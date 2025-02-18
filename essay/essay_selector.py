# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from promptflow.core import tool
import os
from promptflow.core import Prompty
from promptflow.core import AzureOpenAIModelConfiguration
# import blob storage
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.identity import DefaultAzureCredential

# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need

class BlobClient:
    def __init__(self, prompty_file: str):
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.container_name = "prompts"

    def __call__(self, container_name: str, blob_name: str):
        blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        blob_client = blob_service_client.get_blob_client(container=self.container_name, blob=blob_name)
        return blob_client     

class Essay:
    def __init__(self, model_config: AzureOpenAIModelConfiguration, params: dict):
        self.model_config = model_config

    def __call__(self, params) -> str:
        print("Essay type: " + params['essay_type'])
        if params['essay_type'] == 'essay_type_a':
            prompty_file = BlobClient(prompty_file=params)
        elif params['essay_type'] == 'essay_type_b':
            prompty_file = BlobClient(prompty_file=params)

        prompty = Prompty.load(source=prompty_file)
        result = prompty(
            language=params["language"],
            genre=params["genre"],
            statement=params["statement"],
            title=params["title"],
            essay=params["essay"],
            support_material=params["support_text"],
            skills=params["skills"]
        )
        return result

@tool
def essay_selector(essay: str) -> str:
    essay = Essay(
        model_config=AzureOpenAIModelConfiguration(
            azure_deployment=os.getenv("AZURE_DEPLOYMENT"),
            api_key=os.getenv("OPENAI_API_KEY"),
            azure_endpoint=os.getenv("OPENAI_API_ENDPOINT")
        ),
        params=essay
    )
