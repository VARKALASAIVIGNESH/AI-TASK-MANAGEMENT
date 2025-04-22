from flask import Flask, request, render_template, redirect, url_for
from workflow import WorkflowState, plan_agent, tool_agent, reflection, done_node, get_next_node, groq_llm, get_workflow_graph
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = Flask(__name__)

# Get the workflow graph
workflow = get_workflow_graph()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_workflow():
    query = request.form.get("query")
    if query:
        state = WorkflowState(query=query, sub_tasks=[], results={}, status="planning")
        current_node = "plan"
        max_iterations = 10

        for _ in range(max_iterations):
            if current_node == "done":
                break
            elif current_node == "plan":
                state = plan_agent(state)
                current_node = "tool"
            elif current_node == "tool":
                state = tool_agent(state, groq_llm)
                current_node = "reflect"
            elif current_node == "reflect":
                state = reflection(state)
                current_node = get_next_node(state)
        return render_template("index.html", sub_tasks=state.sub_tasks, results=state.results)
    return redirect(url_for("index"))

@app.route("/update_task", methods=["POST"])
def update_task():
    task_index = int(request.form.get("task_index"))
    new_task = request.form.get("new_task")
    state = WorkflowState(query="", sub_tasks=[], results={})
    state.sub_tasks = request.form.getlist("sub_tasks[]")  # Get current tasks from form
    if 0 <= task_index < len(state.sub_tasks):
        state.sub_tasks[task_index] = new_task
    # Re-run workflow with updated tasks
    current_node = "tool"  # Start from tool to process updated tasks
    max_iterations = 5  # Limit iterations to avoid infinite loops
    for _ in range(max_iterations):
        if current_node == "done":
            break
        elif current_node == "tool":
            state = tool_agent(state, groq_llm)
            current_node = "reflect"
        elif current_node == "reflect":
            state = reflection(state)
            current_node = get_next_node(state)
    return render_template("index.html", sub_tasks=state.sub_tasks, results=state.results)

@app.route("/delete_task", methods=["POST"])
def delete_task():
    task_index = int(request.form.get("task_index"))
    state = WorkflowState(query="", sub_tasks=[], results={})
    state.sub_tasks = request.form.getlist("sub_tasks[]")  # Get current tasks from form
    if 0 <= task_index < len(state.sub_tasks):
        state.sub_tasks.pop(task_index)
    # Re-run workflow with updated tasks
    current_node = "tool"  # Start from tool to process updated tasks
    max_iterations = 5  # Limit iterations to avoid infinite loops
    for _ in range(max_iterations):
        if current_node == "done":
            break
        elif current_node == "tool":
            state = tool_agent(state, groq_llm)
            current_node = "reflect"
        elif current_node == "reflect":
            state = reflection(state)
            current_node = get_next_node(state)
    return render_template("index.html", sub_tasks=state.sub_tasks, results=state.results)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # Removed stray 'app.py'