# Multiple prompt deployment in one endpoint using prompt-flow
This repository was inspired by the Microsoft's prompt flow official repo: https://github.com/microsoft/promptflow/tree/main/examples

[![PR Pipeline](https://github.com/deividfoggi/llmops/actions/workflows/pr_pipeline.yml/badge.svg)](https://github.com/deividfoggi/llmops/actions/workflows/pr_pipeline.yml)

## Overview

This project is designed to demonstrate how to deploy multiple prompts using prompt flow in a single endpoint. As an example, it evaluate essays using AI models using prompt flow and a code-first approach. It supports multiple essay types and provides a structured way to assess various skills such as grammar, cohesion, orthography, and relevance to the theme.

## How essay type is selected

You send essay_type as a property in the json payload. This demo is ready to handle essay_type_a and essay_type_b. The first will assess multiple skills and the later one specific skill + returning each possible error and a respective suggestion.

## How to play with the prompts?

As specified by prompt flow, you evolve play with each prompt directly in the .prompty files. This demo implements prompt as class, so if you want to play with the app logics, go for the py files that define the prompt class.

## Resources needed in Azure

To run this project, you will need the following resources in Azure:

- Azure OpenAI Service
- Azure Container Registry
- Azure Container Apps
- Azure Key Vault (optional, for storing secrets)

## How to prepare environment variables in GitHub

To set up the necessary environment variables in GitHub, follow these steps:

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

## How to use sample files in each essay_type directory

Each essay type directory contains sample files that you can use to demo the project. Follow these steps:

1. Navigate to the `src` directory.
2. Choose the essay type you want to demo (`essay_type_a` or `essay_type_b`).
3. Each essay type directory contains a `.prompty` file and a sample JSON file (e.g., `essay_type_a.sample.json`).
4. Send the content of this file as the body in a POST request against the ingress endpoint of your container app using thunder client, postman or something else.