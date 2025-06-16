# 🤖 AI Task Management Workflow

This is a Flask-based AI Task Management application that allows users to submit a query or task, which is then processed step-by-step using an intelligent agent workflow. It leverages Groq's LLaMA3 model to assist in task planning, execution, and reflection through a state-driven pipeline.

## 🎥 Demo Video

Watch the demo video of the AI Task Manager in action:
👉 [AI Task Management Demo](https://drive.google.com/file/d/1Ja3UMTKTmwWRCQRRafw_b9a9PUaAhbhU/view)

GitHub Repository:
👉 [AI-TASK-MANAGEMENT Repo](https://github.com/VARKALASAIVIGNESH/AI-TASK-MANAGEMENT)

---

## 🛠️ Tech Stack

* **Python**: Backend logic
* **Flask**: Web framework
* **Jinja2**: Templating engine
* **Groq + LLaMA3 API**: Language model integration
* **dotenv**: For managing API keys and config securely

---

## 🚀 Getting Started

### 🔧 Prerequisites

* Python 3.8+
* pip

### 📅 Installation

1. **Clone the Repository**

```bash
git clone https://github.com/YOUR_USERNAME/AI-TASK-MANAGEMENT.git
cd AI-TASK-MANAGEMENT
```

2. **Install Dependencies**

```bash
pip install flask python-dotenv groq
```

3. **Set Up Environment Variables**

Create a `.env` file and add your Groq API key:

```ini
GROQ_API_KEY=your_groq_api_key_here
```

4. **Run the App**

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

---

## 🔄 Workflow Overview

This app uses a state machine to manage tasks:

1. **Planning**: Breaks the query into actionable subtasks
2. **Tool**: Executes subtasks using the LLM
3. **Reflect**: Evaluates results and decides next actions
4. **Done**: Marks task as completed

Each component is managed through modular agents (`plan_agent`, `tool_agent`, `reflection`, etc.).

---

## ✅ Features

* Submit any high-level query or task
* Intelligent breakdown into subtasks
* Real-time execution with Groq LLaMA3
* Reflection and revision capability
* Edit or delete subtasks

---

## 🔐 Security Notes

* Store your API keys in the `.env` file and never hardcode them.
* Do not commit `.env` to version control.

---

## 👨‍💼 Author

**Varkala Sai Vignesh**
GitHub: [@VARKALASAIVIGNESH](https://github.com/VARKALASAIVIGNESH)

---

## 📃 License

Licensed under the [MIT License](https://opensource.org/licenses/MIT). Feel free to use and adapt this project.

---

**Simplify your workflows with AI-powered task management!**
