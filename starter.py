import os

# ── Mock LLM ─────────────────────
#Return simulated responses for the 3 prompt comparisons.
def mock_llm(prompt: str) -> str:

    #Task 1 - Code explanation
    if prompt.strip() == "What is st.session_state?":
        return """[SIMULATED BAD RESPONSE]

st.session_state stores session information in Streamlit."""

    if prompt.strip().startswith(
        "You are an experienced Python and Streamlit instructor"
    ):
        return """[SIMULATED GOOD RESPONSE]

What is st.session_state?
It stores values that persist between Streamlit script reruns.

Why is it useful?
Streamlit reruns your script when users interact with widgets.
Session state lets your app remember information.

Example:

if "counter" not in st.session_state:
    st.session_state.counter = 0

if st.button("Increase"):
    st.session_state.counter += 1

st.write(st.session_state.counter)

Explanation:
The counter starts at zero and increases whenever the
button is clicked. Its value persists across reruns."""

    #Task 2 - Data formatting 
    if prompt.strip().startswith("Convert these tasks to JSON:"):
        return """[SIMULATED BAD RESPONSE]

Here are your tasks in JSON format:

{
    "tasks": [
        "finish the module 7 exercises",
        "review chunking strategies notes",
        "watch the ChromaDB guided example video",
        "start the module project"
    ]
}

This is your converted task list."""

    if prompt.strip().startswith("You are a data formatting assistant"):
        return """[SIMULATED GOOD RESPONSE]
[
    {
        "title": "finish the module 7 exercises",
        "priority": "high",
        "status": "not started"
    },
    {
        "title": "review chunking strategies notes",
        "priority": "medium",
        "status": "not started"
    },
    {
        "title": "watch the ChromaDB guided example video",
        "priority": "medium",
        "status": "not started"
    },
    {
        "title": "start the module project",
        "priority": "high",
        "status": "not started"
    }
]"""
    # Task 3 - Course Study Assistant
    if prompt.strip().startswith("Help me with my course questions."):
        return """[SIMULATED BAD RESPONSE]

ChromaDB is a database for AI applications. 
It can store and search vector embeddings."""

    if (
        "COURSE NOTES:" in prompt
        and "STUDENT QUESTION:" in prompt
    ):
        return """[SIMULATED GOOD RESPONSE]

ChromaDB is a vector database that stores embeddings, documents, IDs and metadata.

PersistentClient saves ChromaDB collections to disk,
allowing the stored information to remain available
after the application restarts.

Source: chromadb.txt"""

    return "[SIMULATED RESPONSE] No matching task found."

# ── Real LLM (optional) ──────────────
def real_llm(prompt: str, system: str = "") -> str:
    """Call OpenAI with the given prompt. Requires OPENAI_API_KEY env var."""
    from openai import OpenAI
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    return response.choices[0].message.content


# Choose which function to use throughout this exercise
llm = mock_llm   # swap to real_llm if you have a key

# ── Helper ───────────────
def compare(task_name: str, bad_prompt: str, good_prompt: str):
    """Run both prompts and print their results for comparison."""
    print(f"\n{'='*60}")
    print(f"TASK: {task_name}")
    print(f"\n--- BAD PROMPT ---\n{bad_prompt}\n")
    print(f"BAD RESPONSE:\n{llm(bad_prompt)}")
    print(f"\n--- GOOD PROMPT ---\n{good_prompt}\n")
    print(f"GOOD RESPONSE:\n{llm(good_prompt)}")

# ── Task 1 — Code explanation ───────────
# Bad_prompt: vague, with no instructions about the audience or format 
bad_prompt_1 = "What is st.session_state?"

#Good prompt: uses role framing and specificity
good_prompt_1 = """
You are an experienced Python and Streamlit instructor teaching a beginner. 

Explain what st.session_state does in Streamlit.

Follow these instructions:
1. Explain its purpose in 2-3 simple sentences.
2. Describe why it is useful when Streamlit reruns a script.
3. Provide a short Python code example showing how to initialize
   and update a counter using st.session_state.
4. Explain the example in plain English.
5. Keep the entire explanation under 200 words.

Use clear headings and avoid unnecessary technical jargon.
"""

compare("Code Explanation — st.session_state", bad_prompt_1, good_prompt_1)


# ── Task 2 — Data formatting ───────────
TASK_LIST = """
finish the module 7 exercises
review chunking strategies notes
watch the ChromaDB guided example video
start the module project
"""

#Bad_prompt: vague, with no required JSON structure
bad_prompt_2 = f"Convert these tasks to JSON:\n{TASK_LIST}"

# A good_prompt that specifies the exact JSON structure
#       (array of objects with title, priority, status) and asks for
#       only valid JSON — no prose
good_prompt_2 = f"""
You are a data formatting assistant that converts task lists into JSON.

Convert the following natural language task list into a JSON array.

Requirements:
1. Return one JSON object for each task.
2. Every object must contain exactly these three fields:
   "title", "priority", and "status".
3. Keep each task's original wording in the "title" field.
4. Set "priority" to "high", "medium", or "low".
5. Use "high" for tasks involving completion of exercises or projects,
   "medium" for reviewing notes or watching instructional videos,
   and "low" for optional activities.
6. Set "status" to "not started" for every task.
7. Respond with only valid JSON. Do not include Markdown or explanations.

Example input:
submit the Python assignment

Example output:
[
  {{
    "title": "submit the Python assignment",
    "priority": "high",
    "status": "not started"
  }}
]

Tasks to convert:
{TASK_LIST}
"""

compare("Data Formatting — task list to JSON", bad_prompt_2, good_prompt_2)


# ── Task 3 — System prompt design ─────────
bad_prompt_3 = """
Help me with my course questions.

What is ChromaDB?
"""
#Good system prompt: role framing, specificity, and few-shot example
STUDY_ASSISTANT_SYSTEM_PROMPT = """
You are a Course Study Assistant helping students understand
Python, Streamlit, embeddings, and vector databases.

Follow these rules:

1. Answer questions using ONLY the provided course notes.
2. Do not use outside knowledge or invent missing information.
3. If the notes do not contain enough information, say:
   "I don't know based on the provided course notes."
4. Keep every answer under 150 words.
5. Use clear, beginner-friendly language.
6. Include the source document filename at the end of each answer.
7. Use this exact source format:
   Source: filename.txt

Example:

Context:
Source: streamlit.txt
Streamlit uses st.session_state to preserve values
between script reruns.

Question:
Why is st.session_state useful?

Answer:
st.session_state preserves values between Streamlit
script reruns, allowing applications to remember information.

Source: streamlit.txt
"""
#Sample course notes for testing
SAMPLE_CONTEXT = """
Source: chromadb.txt
ChromaDB is a vector database used to store embeddings, documents, IDs and metadata.

PersistentClient saves ChromaDB collections to disk.

Metadata filtering allows searches to be restricted
to specific documents or categories.
"""
#Good prompt: provide context and a specific question
good_prompt_3 = f"""
{STUDY_ASSISTANT_SYSTEM_PROMPT}

COURSE NOTES:
{SAMPLE_CONTEXT}

STUDENT QUESTION:
What is ChromaDB, and how does PersistentClient help?

Answer the student's question following all the rules above.
"""

compare("System Prompt Design — Study Assistant", bad_prompt_3, good_prompt_3)

# Print the final system prompt
print(f"\n{'='*60}")
print("STUDY ASSISTANT SYSTEM PROMPT:")
print(STUDY_ASSISTANT_SYSTEM_PROMPT)
