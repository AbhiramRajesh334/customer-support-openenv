import os
import requests
import json
from openai import OpenAI
from app.grader import grade_episode

# 🔑 Setup OpenAI client
client = OpenAI(
    base_url=os.getenv("API_BASE_URL"),
    api_key=os.getenv("OPENAI_API_KEY")
)

MODEL = os.getenv("MODEL_NAME", "unknown-model")

# Use env variable for base URL (important for deployment)
BASE_URL = os.getenv("ENV_BASE_URL", "http://127.0.0.1:8000")


def get_action_from_llm(state):
    prompt = f"""
You are a customer support agent.

Ticket: {state['ticket_text']}

Choose ONE action:
1. classify with category (billing, delivery, refund, technical)
2. resolve

Respond ONLY in JSON format:
{{
    "action_type": "...",
    "value": "..."
}}
"""

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

    except Exception:
        # fallback safe action
        return {"action_type": "resolve"}


def run_episode():
    actions = []
    rewards = []

    # 🔁 Reset
    try:
        state = requests.get(f"{BASE_URL}/reset").json()
        task = "ticket-resolution"
        env_name = "customer-support-env"
    except Exception:
        print("[START] task=customer-support env=openenv model={}".format(MODEL))
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
    run_episode()