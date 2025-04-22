from langgraph.graph import Graph
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define the state
class WorkflowState:
    def __init__(self, query, sub_tasks=[], results={}, status="planning"):
        self.query = query
        self.sub_tasks = sub_tasks
        self.results = results
        self.status = status

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self

# Function to interact with Groq LLaMA
def groq_llm(prompt):
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content

# Define next node function
def get_next_node(state):
    if state.status == "done":
        return "done"
    elif state.status == "refining":
        return "plan"
    elif state.status == "executing":
        return "tool"
    return "plan"

# PlanAgent node
def plan_agent(state):
    if state.status == "planning":
        prompt = f"Split this into sub-tasks: {state.query}. Provide a numbered list of concise, actionable tasks only (e.g., 1. Task, 2. Task), without examples, conditionals, or extra text."
        sub_tasks = groq_llm(prompt).split("\n")
        sub_tasks = [task.strip().replace(".", "").split(" ", 1)[-1] for task in sub_tasks if task.strip().startswith(tuple(str(i) for i in range(1, 11))) and len(task.split(".", 1)) > 1]
        return state.update(sub_tasks=sub_tasks, status="refining")
    prompt = f"Review the following tasks: {state.sub_tasks}. Suggest improvements or new tasks if needed. Return a numbered list of concise, actionable tasks only (e.g., 1. Task, 2. Task), without examples, conditionals, or extra text."
    updated_tasks = groq_llm(prompt).split("\n")
    updated_tasks = [task.strip().replace(".", "").split(" ", 1)[-1] for task in updated_tasks if task.strip().startswith(tuple(str(i) for i in range(1, 11))) and len(task.split(".", 1)) > 1]
    return state.update(sub_tasks=updated_tasks)

# ToolAgent node (using tools.py with LLaMA)
def tool_agent(state, llm_func):
    from tools import tool_agent as ta
    return ta(state, llm_func)

# Reflection node
def reflection(state):
    prompt = f"Review the results: {state.results}. Based on the sub-tasks {state.sub_tasks}, decide the next step. If tasks are incomplete, need modification, deletion, or addition, return 'refine'. If all tasks are ready, return 'execute'. If all tasks are completed and results are satisfactory, return 'done'. Return exactly one word."
    decision = groq_llm(prompt).strip().lower()
    print(f"Reflection decision: {decision}")
    if decision in ["refine", "execute", "done"]:
        if decision == "refine":
            return state.update(status="refining")
        elif decision == "execute":
            return state.update(status="executing")
        elif decision == "done":
            return state.update(status="done")
    print(f"Warning: Invalid decision from LLaMA: {decision}. Defaulting to 'execute'.")
    return state.update(status="executing")

# Done node
def done_node(state):
    return state

# Set up the graph
def get_workflow_graph():
    workflow = Graph()
    workflow.add_node("plan", plan_agent)
    workflow.add_node("tool", tool_agent)
    workflow.add_node("reflect", reflection)
    workflow.add_node("done", done_node)
    workflow.set_entry_point("plan")
    workflow.add_edge("plan", "tool")
    workflow.add_edge("tool", "reflect")
    workflow.add_edge("reflect", "plan")
    workflow.add_conditional_edges(
        "reflect",
        get_next_node,
        {"done": "done", "plan": "plan", "tool": "tool"}
    )
    return workflow