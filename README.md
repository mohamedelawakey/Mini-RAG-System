# This Project About Mini RAG App

This is a minimal implementation of the RAG model for question answering.

## Requirements
```bash
Python 3.10.11 or later
```

#### Install Python using MiniConda

1) Download and install MiniConda from [here]: 
```bash
(https://docs.anaconda.com/free/miniconda/#quick-command-line-install)
```
2) Create a new environment using the following command:
```bash
$ conda create -n mini-rag python = 3.10.11
```
3) Activate the environment:
```bash
$ conda activate mini-rag
```

## Installation

#### Install the requirements Packages
```bash
$ pip install -r requirements.txt
```

#### setup the environment variables 
```bash
$ cp .env.example env
```
Set your environment variables in the `.env` file. Like `OPENAI_API_KEY` value.

## Run The FastAPI Server
```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```