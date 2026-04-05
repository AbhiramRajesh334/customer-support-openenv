# Customer Support AI Environment (OpenEnv)

## Overview

This project implements a real-world customer support ticket resolution environment using the OpenEnv framework. The environment simulates how an AI agent handles customer support tickets by classifying and resolving them step-by-step.

---

## Objective

The goal is to evaluate an AI agent’s ability to:

- Understand customer issues
- Classify tickets correctly
- Resolve issues efficiently
- Take optimal actions in sequence

---

## Environment Design

### Observation Space

The agent receives:

- ticket_id (int)
- ticket_text (string)
- status (string: open / classified / resolved)

---

### Action Space

The agent can perform:

- classify → assign a category (billing, delivery, refund, technical)
- resolve → mark the issue as resolved

---

### Reward Function

- Correct classification → +0.3  
- Incorrect classification → -0.1  
- Resolve after classification → +0.7  
- Resolve before classification → -0.2  
- Step limit exceeded → -0.2  

---

## Tasks

The environment includes 3 difficulty levels:

- Easy → Single issue tickets  
- Medium → Slightly complex issues  
- Hard → Multi-issue tickets  

Each task has a deterministic correct outcome.

---

## Grading

Final score (0.0 – 1.0):

- Correct classification → 0.5  
- Successful resolution → 0.5  

---

## Setup Instructions

### Install dependencies

pip install -r requirements.txt

---

### Run the environment

uvicorn app.main:app --reload

---

### Test API

Open in browser:

http://127.0.0.1:8000/docs

---

### Run baseline agent

python inference.py

---

## Docker

Build and run:

docker build -t customer-env .
docker run -p 7860:7860 customer-env

---

## Environment Variables

Set before running inference:

- API_BASE_URL  
- MODEL_NAME  
- OPENAI_API_KEY  

---

## Features

- Fully OpenEnv compliant  
- Deterministic grading  
- Real-world task simulation  
- Lightweight and fast execution  

---

## Example Output

[START]  
[STEP] action=classify billing  
[STEP] action=resolve  
[END] score=1.0  

---

## Conclusion

This environment provides a structured and realistic benchmark for evaluating AI agents on customer support workflows.