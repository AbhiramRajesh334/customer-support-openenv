from fastapi import FastAPI
from app.environment import CustomerSupportEnv
from app.models import Action

app = FastAPI()

env = CustomerSupportEnv()


# 🔁 Reset endpoint
@app.get("/reset")
@app.post("/reset")
def reset():
    state = env.reset()
    return state.model_dump()


# 📥 Get current state
@app.get("/state")
def get_state():
    state = env.state()
    return state.model_dump()


# 🎮 Step endpoint
@app.post("/step")
def step(action: Action):
    state, reward, done, info = env.step(action)
    return {
        "observation": state.model_dump(),
        "reward": reward,
        "done": done,
        "info": info
    }