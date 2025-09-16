# Autonomous AI Email Agent for Task Management

This repository contains the source code and documentation for an autonomous AI agent designed to automate email inbox management. The agent intelligently processes incoming emails, classifies their intent, and executes relevant actions such as creating calendar events for deadlines or drafting replies to inquiries.

---
## 1. Overview

The primary objective of this project was to address the manual, time-consuming task of email processing by developing an AI agent capable of reasoning, planning, and executing actions. The final prototype successfully connects to Google Workspace APIs (Gmail & Calendar) and leverages a fine-tuned language model to create a closed-loop automation system.

---
## 2. Core Features

* **Selective Processing:** The agent focuses exclusively on unread emails within the "Primary" Gmail category.
* **Intelligent Intent Classification:** It uses an LLM to classify each email's purpose as a `deadline`, `question`, or `other`.
* **Automated Scheduling:** For deadline-related emails, it extracts key details (task, date, time) and automatically creates a corresponding Google Calendar event.
* **Human-in-the-Loop Replies:** For inquiries, it generates a relevant response and saves it as a draft in Gmail, allowing for human review and approval before sending.
* **Persistent Memory:** The agent applies a custom Gmail label (`Agent-Processed`) to every email it handles, ensuring that emails are never processed more than once, even across separate runs.

---
## 3. System Architecture and Design Rationale

The agent's architecture was designed to be robust, modular, and scalable, based on a "perceive-think-act" cycle.

### 3.1. The Agentic Framework: LangGraph

A simple script would be too rigid for this task. I chose **LangGraph** as the foundational framework for several key reasons:

* **State Management:** LangGraph provides a robust, centralized state object (`AgentState`) that allows the agent to maintain context throughout its workflow.
* **Modularity:** Each core capability (fetching emails, classifying, creating events) is encapsulated in a separate "node." This makes the system easy to debug, maintain, and extend with new tools in the future.
* **Control Flow:** It enables the implementation of complex logic, including the loops and conditional routing (decision-making) necessary for a true agent.

### 3.2. The Reasoning Core: A Multi-Task Fine-Tuned LLM

The "brain" of the agent is a version of `microsoft/Phi-3-mini-4k-instruct`, which was fine-tuned using LoRA. The decision to fine-tune, rather than relying solely on prompting, was a critical choice driven by the need for **reliability**.

* **Why Fine-Tuning was Essential:** The agent's most critical function is extracting structured data (a JSON object with a task and deadline) from unstructured text. While a base instruction-tuned model can be prompted to do this, its output is not guaranteed to be consistent. It might include conversational filler or use a slightly different format, which would break the automation pipeline. Fine-tuning the model on a specialized dataset forced it to become an expert at producing a clean, machine-readable JSON or `null` value, ensuring the reliability needed for this task.

* **Evolution to Multi-Task Fine-Tuning:** Initial evaluations revealed that the agent's routing accuracy was suboptimal. To address this, the fine-tuning strategy was expanded. The training dataset was augmented with examples for the classification task. By training the model on a combined dataset, it became a specialist at **both** high-level classification and low-level data extraction, significantly improving the agent's overall performance.

### 3.3. Tool Integration
The agent is equipped with tools that serve as its "actuators" to interact with external services:
* **Google Gmail API:** Allows the agent to perceive its environment (read emails) and act within it (create drafts, apply labels).
* **Google Calendar API:** Allows the agent to execute scheduling tasks.

---
## 4. Setup and Usage

1.  **Prerequisites:** A Google Cloud project with the Gmail and Google Calendar APIs enabled, and `credentials.json` downloaded.
2.  **Configuration:**
    * Clone this repository.
    * Place the `credentials.json` and the `dataset.jsonl` files in the root directory.
    * In Gmail, create a new label named exactly `Agent-Processed`.
3.  **Installation:** Run the first cell in the `email_agent_prototype.ipynb` to install all dependencies.
4.  **Model Training (First Run Only):** Uncomment and run the "Fine-Tuning" cell to train the model and create the LoRA adapters. This only needs to be done once.
5.  **Execution:** Run the remaining cells to initialize and start the agent. The first run will require an OAuth2 authentication flow in the browser.
