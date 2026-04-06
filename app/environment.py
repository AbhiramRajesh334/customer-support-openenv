import random
from app.tasks import tasks
from app.models import Observation, Action


class CustomerSupportEnv:
    def __init__(self):
        self.current_task = None
        self.status = "open"
        self.steps = 0
        self.max_steps = 5
        self.classified = False

    # 🔁 Reset environment
    def reset(self, task_id=None):
        if task_id is not None:
            self.current_task = next((t for t in tasks if t["id"] == task_id), random.choice(tasks))
        else:
            self.current_task = random.choice(tasks)
        self.status = "open"
        self.steps = 0
        self.classified = False

        return self.state()

    # 📥 Current state
    def state(self):
        if self.current_task is None:
            return Observation(
                ticket_id=-1,
                ticket_text="",
                status="empty",
                category=None
            )

        return Observation(
            ticket_id=self.current_task["id"],
            ticket_text=self.current_task["text"],
            status=self.status,
            category=self.current_task["category"]
        )

    # 🎮 Step function
    def step(self, action: Action):
        reward = 0.0
        done = False
        info = {}

        self.steps += 1

        correct_category = self.current_task["category"]

        # 🟢 CLASSIFY ACTION
        if action.action_type == "classify":
            if action.value == correct_category:
                reward += 0.5
                self.classified = True
                self.status = "classified"
            else:
                reward -= 0.1  # wrong classification

        # 🔵 RESOLVE ACTION
        elif action.action_type == "resolve":
            if self.classified:
                reward += 0.5
            else:
                reward -= 0.2  # resolving without classification

            self.status = "resolved"
            done = True

        # ❌ INVALID ACTION
        else:
            reward -= 0.1

        # ⏱️ Step limit check
        if self.steps >= self.max_steps:
            done = True
            reward -= 0.2  # penalty for inefficiency

        return self.state(), reward, done, info