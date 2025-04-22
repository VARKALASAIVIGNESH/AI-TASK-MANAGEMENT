def assign_tool(task, llm_func):
    prompt = f"Suggest a specific tool (e.g., Google Meet, Google Calendar, Google Docs) to complete the task: '{task}'. Return only the tool name."
    tool = llm_func(prompt).strip()
    return tool if tool else "Google Meet"

def execute_tool(tool, task):
    return f"Completed {task} with {tool}"

def tool_agent(state, llm_func):
    results = {task: execute_tool(assign_tool(task, llm_func), task) for task in state.sub_tasks}
    return state.update(results=results, status="executing")