# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import json
from promptflow.core import tool
import os
from promptflow.core import Prompty
from promptflow.core import AzureOpenAIModelConfiguration
from azure.storage.blob import BlobServiceClient, BlobClient
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

    def __call__(self, essay: str) -> json:
        # parse essay as a json
        essay_json = json.loads(essay)
        print("Essay type: " + essay_json['essay_type'])
        prompt_file_name = essay_json["essay_type"] + ".prompty"
        blob_client = BlobClient(prompt_file_name)
        prompt_file = blob_client(blob_name=prompt_file_name)
        prompty = Prompty.load(source=prompt_file)

        # Create a dictionary of arguments
        prompty_args = {
            "language": essay_json["language"],
            "genre": essay_json["genre"],
            "statement": essay_json["statement"],
            "title": essay_json["title"],
            "essay": essay_json["essay"],
            "support_material": essay_json["support_text"],
            "skills": essay_json["skills"]
        }

        result = prompty(**prompty_args)

        return result

@tool
def essay_selector(essay: str) -> json:
    model_config = AzureOpenAIModelConfiguration(
            azure_deployment=os.getenv("AZURE_DEPLOYMENT")
        )
    print(essay)
    essay_instance = Essay(model_config)
    result = essay_instance(essay)
    return result