import os
import requests
import json
from openai import OpenAI
from app.grader import grade_episode

# 🔑 Setup OpenAI client
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")

client = None
if API_KEY:
    try:
        client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    except Exception as e:
        print(f"[WARN] OpenAI client init failed: {e}")
else:
    print("[WARN] API_KEY is not set. Using fallback agent behavior.")

MODEL = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

# Use env variable for base URL (important for deployment)
BASE_URL = os.getenv("ENV_BASE_URL", "http://127.0.0.1:8000")


def get_fallback_action(state):
    ticket = state.get("ticket_text", "").lower()
    status = state.get("status", "")

    if status == "classified" or status == "resolved":
        return {"action_type": "resolve", "value": ""}

    if "refund" in ticket and "support" in ticket:
        category = "refund+support"
    elif "refund" in ticket or "damaged" in ticket:
        category = "refund"
    elif "charged twice" in ticket and "not delivered" in ticket:
        category = "billing+delivery"
    elif "charged twice" in ticket:
        category = "billing"
    elif "not arrived" in ticket or "not delivered" in ticket:
        category = "delivery"
    elif "app crashes" in ticket or "crash" in ticket:
        category = "technical"
    elif "support" in ticket:
        category = "refund+support"
    else:
        category = "billing"

    return {"action_type": "classify", "value": category}


def get_action_from_llm(state):
    prompt = f"""
You are a customer support agent.

Ticket: {state['ticket_text']}

Choose ONE action:
1. classify with category (billing, delivery, refund, technical, or combinations like billing+delivery, refund+support)
2. resolve

Respond ONLY in JSON format:
{{
    "action_type": "...",
    "value": "..."
}}
"""

    if client is None:
        return get_fallback_action(state)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        # 🔒 Safe JSON extraction
        start = content.find("{")
        end = content.rfind("}") + 1
        action_json = content[start:end]

        return json.loads(action_json)

    except Exception as e:
        print(f"[WARN] LLM request failed: {e}")
        return get_fallback_action(state)


def run_episode(task_id, difficulty):
    actions = []
    rewards = []
    task = f"{difficulty}-ticket"
    env_name = "customer-support-env"

    # 🔁 Reset
    try:
        state = requests.post(f"{BASE_URL}/reset", json={"task_id": task_id}).json()
    except Exception as e:
        print(f"[START] task={task} env={env_name} model={MODEL}")
        print(f"[WARN] Failed to reset environment: {e}")
        print("[END] success=false steps=0 score=0.00 rewards=")
        return

    print(f"[START] task={task} env={env_name} model={MODEL}")

    done = False
    step_count = 0
    max_steps = 5

    while not done and step_count < max_steps:
        step_count += 1

        action = get_action_from_llm(state)
        action_type = action.get("action_type", "resolve")
        value = action.get("value", "")

        action_str = f"{action_type} {value}".strip()

        error = None

        try:
            response = requests.post(f"{BASE_URL}/step", json=action).json()
            state = response.get("observation", {})
            reward = float(response.get("reward", 0.0))
            done = response.get("done", True)
        except Exception as e:
            reward = 0.0
            done = True
            error = str(e)

        rewards.append(reward)
        actions.append(action)

        print(f"[STEP] step={step_count} action={action_str} reward={reward:.2f} done={str(done).lower()} error={error or 'null'}")

    # Final score
    score = grade_episode(actions, {
        "category": state.get("category", "")
    })

    success = score >= 0.5

    rewards_str = ",".join(f"{r:.2f}" for r in rewards)

    print(f"[END] success={str(success).lower()} steps={step_count} score={score:.3f} rewards={rewards_str}")


if __name__ == "__main__":
    # Run on 3 tasks: easy, medium, hard
    tasks_to_run = [
        (1, "easy"),
        (3, "medium"),
        (5, "hard")
    ]
    for task_id, difficulty in tasks_to_run:
        run_episode(task_id, difficulty)