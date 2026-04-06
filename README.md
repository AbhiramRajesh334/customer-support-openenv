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

The agent receives an `Observation` object:

```json
{
  "ticket_id": 1,
  "ticket_text": "I was charged twice for my order",
  "status": "open",
  "category": null
}
```

- `ticket_id` (int): Unique ticket identifier
- `ticket_text` (string): Customer complaint
- `status` (string): "open", "classified", or "resolved"
- `category` (string or null): Assigned category after classification

---

### Action Space

The agent sends an `Action` object:

```json
{
  "action_type": "classify",
  "value": "billing"
}
```

- `action_type` (string): "classify" or "resolve"
- `value` (string): For "classify", the category (e.g., "billing", "billing+delivery"); for "resolve", empty or ignored

---

### Reward Function

- Correct classification → +0.5  
- Resolve after correct classification → +0.5  
- Incorrect classification → -0.1  
- Resolve before classification → -0.2  
- Step limit exceeded → -0.2  

Final episode score (0.0 – 1.0) based on grader.  

---

## Tasks

The environment includes 3 difficulty levels with specific tasks:

- **Easy (ID 1)**: "I was charged twice for my order" (Category: billing)  
- **Medium (ID 3)**: "I want a refund for a damaged product" (Category: refund)  
- **Hard (ID 5)**: "I was charged twice and my order is still not delivered" (Category: billing+delivery)  

Each task has a deterministic correct outcome.

---

## Grading

Final score (0.0 – 1.0):

- Correct classification → 0.5  
- Successful resolution → 0.5  

---

## Baseline Scores

Run `python inference.py` with environment variables set. Example output:

```
[START] task=easy-ticket env=customer-support-env model=gpt-4
[STEP] step=1 action=classify billing reward=0.50 done=false error=null
[STEP] step=2 action=resolve  reward=0.50 done=true error=null
[END] success=true steps=2 score=1.000 rewards=0.50,0.50

[START] task=medium-ticket env=customer-support-env model=gpt-4
...
```

*Note: Actual scores depend on the model and API.*  

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