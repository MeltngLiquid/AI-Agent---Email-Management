EXTRACTION_SYSTEM_PROMPT = "You are an expert at extracting tasks and deadlines. Respond with a JSON object containing 'task' and 'deadline' keys, or 'null'."

# This single system message is for the classification task.
CLASSIFICATION_SYSTEM_PROMPT = "You are an email classification expert. Your job is to classify the email's intent. Choose ONLY one of the following categories: deadline, question, other."

def format_prompt_for_training(sample: dict) -> str:
    """
    A smart formatting function that uses the correct system prompt
    based on the type of response in the dataset.
    """
    response = sample['response']
    system_prompt = EXTRACTION_SYSTEM_PROMPT if response.startswith('{') else CLASSIFICATION_SYSTEM_PROMPT

    return f"""<|system|>
{system_prompt}<|end|>
<|user|>
{sample['text']}<|end|>
<|assistant|>
{response}<|end|>"""

def create_classification_prompt(email_content: str) -> str:
    """Creates the prompt for the classification tool, now using a consistent system message."""
    return f"""<|system|>
{CLASSIFICATION_SYSTEM_PROMPT}<|end|>
<|user|>
{email_content}<|end|>
<|assistant|>
"""

def create_extraction_prompt(email_content: str) -> str:
    """Creates the prompt for the extraction tool, now using a consistent system message."""
    return f"""<|system|>
{EXTRACTION_SYSTEM_PROMPT}<|end|>
<|user|>
{email_content}<|end|>
<|assistant|>
"""
