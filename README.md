MailMind – AI Agent that manages your inbox intelligently.
===========================================================

Overview
--------

This project implements an autonomous AI agent to automate personal email management. The agent connects to Gmail, perceives incoming messages, reasons about their intent using a fine-tuned language model, and executes actions such as scheduling calendar events for deadlines or drafting replies for questions.

Built on a modular _perceive–think–act_ architecture, it leverages **LangGraph** for stateful workflows and a fine-tuned **Phi-3-mini-4k-instruct** model for reliable classification and data extraction.

### Key Features

*   **Email Classification**: Categorizes emails as _deadline_, _question_, or _other_.
    
*   **Deadline Extraction & Scheduling**: Parses tasks and deadlines, creates Google Calendar events on success.
    
*   **Reply Drafting**: Generates context-aware reply drafts for questions and saves them in Gmail for review.
    
*   **Workflow Automation**: Processes unread emails in a loop, applies labels to avoid re-processing, and marks emails as read post-success.
    
*   **Evaluation Suite**: Performance metrics – F1 Score (~0.7), Task Success Rate (~80%), Semantic Similarity (~80%).
    
*   **Efficient Fine-Tuning**: Uses LoRA (PEFT) on a quantized 3.8B parameter model.
    

The agent demonstrates high reliability in core tasks, reducing manual email workload.

For a detailed report, see **Agent Architecture.pdf**.

Prerequisites
-------------

### Hardware / Environment

*   GPU Recommended (e.g., T4 on Colab)
    
*   Python 3.10+ (tested on Python 3.12)
    
*   Google Colab or Jupyter Notebook
    

### Google API Setup

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
    
2.  Create a new project (or select an existing one).
    
3.  Enable Gmail API and Google Calendar API.
    
4.  Create OAuth 2.0 credentials:
    
    *   Select _Desktop Application_
        
    *   Download the JSON file and rename to credentials.json
        
    *   Place it in the project root
        
5.  Add scopes:
    
    *   https://www.googleapis.com/auth/gmail.modify
        
    *   https://www.googleapis.com/auth/calendar.events
        

> **Security Note**: Never commit credentials.json to version control.

Installation
------------

1.  Clone the repository and move into the project directory.
    
2.  Upgrade pip.
    
3.  Install dependencies: transformers, datasets, accelerate, peft, trl, bitsandbytes.
    
4.  Install Google API clients: google-api-python-client, google-auth, google-auth-httplib2, google-auth-oauthlib.
    
5.  Install other tools: langgraph, typing\_extensions, sentencepiece, html2text, huggingface\_hub.
    
6.  Install evaluation packages: scikit-learn, sentence-transformers.
    
7.  Upload credentials.json and restart runtime after installation.
    

Usage
-----

### 1\. Fine-Tune the Model

*   Run the _FINETUNING_ section in SOURCE_CODE.ipynb.
    
*   Trains LoRA adapters for ~6 epochs on Colab T4 GPU.
    
*   Outputs adapters in phi3-mini-deadline-extractor-adapters/.
    

### 2\. Initialize Services

*   Run the _AUTHENTICATION_ section.
    
*   Authenticate via OAuth (console flow). Token saved to token.json.
    
*   Loads the fine-tuned model with 4-bit quantization.
    

### 3\. Run the Agent

*   Execute the _THE AGENT_ section.
    
*   The agent monitors unread emails, classifies them, and applies actions.
    
*   Can be stopped anytime with Ctrl + C.
    

### 4\. Evaluate Performance

*   Run the _Evaluation_ section.
    
*   Reports F1 Score, Task Success Rate, and Semantic Similarity.
    

Future Work
-----------

*   **Two-Model Architecture**: Use a larger LLM (e.g., Gemini or GPT-4) as an _Orchestrator_, with Phi-3 as a _Specialist_.
    
*   **Enhanced Tools**: Email summarization, attachment handling, multilingual support.
    
*   **Deployment**: Containerize with Docker; deploy as cron job or serverless function.
    
*   **Robustness**: Add error recovery, user feedback, and A/B testing.
        


Author
------

**Sriharsha Rao C** – IIT Hyderabad
