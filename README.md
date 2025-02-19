# Multiple prompt deployment in one endpoint using prompt-flow
This repository was inspired by the Microsoft's prompt flow official repo: https://github.com/microsoft/promptflow/tree/main/examples

[![PR Pipeline - Prompt flow endpoint](https://github.com/deividfoggi/multiple-prompt-single-endpoint/actions/workflows/pr_pipeline_prompt_flow.yml/badge.svg)](https://github.com/deividfoggi/multiple-prompt-single-endpoint/actions/workflows/pr_pipeline_prompt_flow.yml)

[![PR Pipeline - Scan Essay Demo](https://github.com/deividfoggi/multiple-prompt-single-endpoint/actions/workflows/pr_pipeline_scan_essay.yml/badge.svg)](https://github.com/deividfoggi/multiple-prompt-single-endpoint/actions/workflows/pr_pipeline_scan_essay.yml)

## Overview

### Prerequisites

 - Visual Studio Code
 - Promptflow extension
 - Python 3.11
 - Docker desktop

### Prompt flow
This project is designed to demonstrate how to deploy multiple prompts using prompt flow in a single endpoint. As an example, it evaluate essays using AI models to act as a professor by using prompt flow and a code-first approach. It supports multiple essay types and provides a structured way to assess various skills such as grammar, cohesion, orthography, and relevance to the theme, or whatever skills you would like to assess. You can use prompty files to define both user and system roles.

### Document intelligence
This project also implements a demonstration of how to scan handwritten essays with Document Intelligence before sending it to prompt flow for evaluation. This demonstration is under scan-essay directory as a node project. The pipeline builds a docker image of this web app.

## How essay type is selected
You send essay_type as a property in the json payload. This demo is ready to handle essay_type_a and essay_type_b. The first will assess multiple skills and the later one specific skill + returning each possible error and a respective suggestion.

To make the code simple, reusable and decoubled, it implements a class based flow that received the payload as a dictionary typed object, based on essay type property it will download the respective prompty file from a blob storage and will use it to parse all properties from the json to build up the prompt, then send a request to open AI object.

The entire demo allows you to upload a handwritten essay using the scan_essay nodejs web app that will send the OCR resulted string from Document Intelligence to the prompt flow endpoint, both deployed as docker images that can be easiley pulled from ACR into Azure Container Apps or any Kubernetes based platform.

## How to play with the prompts?
As specified by prompt flow, you play with each prompt directly in the .prompty files and using flow.dag.yaml. This demo implements prompts as a class, so if you want to play with the app logics, go for the py files that define the prompt class.

## Resources needed in Azure
To run this project, you will need the following resources in Azure:

- Azure OpenAI Service
- Azure Container Registry
- Azure Container Apps
- Azure Key Vault (optional, for storing secrets)
- Azure Storage Account and a blob container named _prompts_

## How to prepare environment variables in GitHub
1. Using azure cli, create a service principal to enable the pipeline to push the docker image to the azure container registry:

    ```shell
    az ad sp create-for-rbac --name <service-principal-name> --role Contributor --scopes /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.ContainerRegistry/registries/<registry-name> --sdk-auth
    ```
2. Copy the ouput.
2. Go to your GitHub repository.
3. Click on `Settings` > Environment > Add at least dev environment
4. Navigate to dev environment and create the following variables:
5. Click on `New repository secret` and add the following secrets:

   - `AZURE_SUBSCRIPTION_ID`: Your Azure subscription ID.
   - `AZURE_LOCATION`: The location of your Azure resources.
   - `AZURE_RESOURCE_GROUP`: The resource group name.
   - `AZURE_CONTAINER_REGISTRY_NAME`: The name of your Azure Container Registry.
   - `AZURE_CONTAINER_REPOSITORY_NAME`: The name of your container repository.

6. Add an environment secret named AZURE_CREDENTIALS and paste the content copied in step 2.

## How to test local
### prompt flow tool
1. Upload the prompty files under _demo_prompty_ folder to _prompts_ blob container in your storage account
2. Make sure your storage account has this setting enabled: Configuration > Allow storage account key access. For official environments such as QA or production, it is recommended to use Entra Authentication.
3. In VSCode, make sure you have the following environment variables in place either in a terminal or using a .env file (no worries, this project will not commit this file):
    ```
    AZURE_OPENAI_ENDPOINT=<your Azure OpenAI https endpoint>
    AZURE_OPENAI_API_KEY=<the Azure OpenAI api key>
    AZURE_DEPLOYMENT=<deployment name, ie: gpt-4>
    AZURE_STORAGE_CONNECTION_STRING=<storage account connection string>
    ```

4. Open prompt flow extension, under connections click on + button to create a new connection, name it _aoai_connection_.

5. Open a terminal and run the following commands:

    ```
    cd essay
    pf flow test --flow essay_flow:Essay --inputs input.json --init.json
    ```

### Build a docker image and run it local
1. Open essay/flow.dag.yaml
2. Either in yaml or visual editor, click on Build
3. An yaml file will open, click on _Build as docker_
4. Create a folder named _dist_ in the root and select it
5. Click on _Create Dockerfile_
6. Once the process is done the yaml file will be closed
7. Run the following commands in the dist directory:

    ```
    docker build -t essay_flow .
    docker run -p 8080:8080 -e AZURE_OPENAI_ENDPOINT=<your Azure OpenAI https endpoint> -e AZURE_OPENAI_API_KEY=<the Azure OpenAI api key> -e AZURE_DEPLOYMENT=<deployment name, ie: gpt-4> -e AZURE_STORAGE_CONNECTION_STRING=<storage account connection string> -e PROMPT_FLOW_SERVICE_ENGINE=fastapi -e PROMPTFLOW_WORKER_NUM=1 essay_flow
    ```

8. Use curl to confirm it is working:

    ```
    curl -X POST http://127.0.0.1:8080/score \
     -H "Content-Type: application/json" \
     -d @essay/input.json
    ```

9. the response should be something as follows:

    ```
    {"result":{"output":{"coes\u00e3o":{"comment":"A reda\u00e7\u00e3o apresenta uma coes\u00e3o razo\u00e1vel, com as ideias sendo apresentadas de forma l\u00f3gica e sequencial. No entanto, a transi\u00e7\u00e3o entre as partes do texto poderia ser mais fluida. A introdu\u00e7\u00e3o do contexto e das causas da guerra \u00e9 clara, mas faltam conectores que ajudem a ligar melhor as diferentes partes do texto, o que facilitaria a compreens\u00e3o do leitor.","score":7,"skill_id":"coes\u00e3o"},"gramatica":{"comment":"A reda\u00e7\u00e3o apresenta uma boa estrutura gramatical, com frases bem constru\u00eddas e uso adequado dos tempos verbais. No entanto, h\u00e1 um pequeno erro de concord\u00e2ncia na frase 'um dos conflitos mais significativos e transformadores hist\u00f3ria dos Estados Unidos', onde falta a preposi\u00e7\u00e3o 'da' antes de 'hist\u00f3ria'. Corrigindo esse detalhe, a gram\u00e1tica estaria quase perfeita.","score":8,"skill_id":"gramatica"},"ortografia":{"comment":"A ortografia est\u00e1 praticamente impec\u00e1vel, com apenas alguns pequenos deslizes. N\u00e3o h\u00e1 erros de grafia evidentes, o que demonstra um bom dom\u00ednio das regras ortogr\u00e1ficas. A \u00fanica observa\u00e7\u00e3o seria revisar sempre o texto para garantir que pequenos erros, como o mencionado na gram\u00e1tica, sejam corrigidos.","score":9,"skill_id":"ortografia"},"relev\u00e2ncia com o tema":{"comment":"A reda\u00e7\u00e3o est\u00e1 totalmente relevante ao tema proposto, abordando de maneira clara e direta a Guerra Civil Americana. O aluno conseguiu contextualizar bem o conflito, mencionando suas causas principais e os lados envolvidos. A escolha de focar na quest\u00e3o da escravid\u00e3o como causa principal \u00e9 pertinente e demonstra um bom entendimento do tema.","score":10,"skill_id":"relev\u00e2ncia com o tema"}}}}
    ```

### How to test on Azure
Push the image to Azure Container Registry, pull it using the choosen platform, like Azure Container Apps and enjoy it!