import os
import subprocess
import json

# Load problem descriptions
problem_descriptions = {
    "factorial": "Write a recursive function to compute the factorial of a number. The function should return 1 for factorial(0), and recursively compute the product for positive integers.",
    "reverse_array": "Write a function that reverses a list of integers in place without using extra memory.",
    "bubble_sort": "Write a function that takes a list of integers and sorts them in ascending order using bubble sort.",
    "is_palindrome": "Write a function that returns True if the input string is a case-insensitive palindrome.",
    "find_max": "Write a function that returns the maximum number in a list. Raise a ValueError if the list is empty."
}

# Build prompt template
def build_prompt(problem_desc, student_code):
    return f"""You are an expert Python tutor.

A student submitted the following code for the problem:

---
Problem:
{problem_desc}

---
Code:
{student_code}

---
Your tasks:
1. Describe what the code is trying to do.
2. Identify any mistakes or edge cases it fails to handle.
3. Provide feedback in two parts:
   a) Conceptual Feedback (Explain the mistake)
   b) Fix Suggestion (Give a corrected version or suggestion)

Respond in this format:

---
Intended Logic:
...

Errors:
...

Conceptual Feedback:
...

Fix Suggestion:
...
"""

# Call Ollama
def query_ollama(prompt, model="codellama"):
    result = subprocess.run(
        ["ollama", "run", model],
        input=prompt.encode(),
        capture_output=True
    )
    return result.stdout.decode()

# Process all files
def process_all_submissions():
    input_dir = "submissions"
    output_dir = "feedbacks"
    os.makedirs(output_dir, exist_ok=True)

    for problem_id in os.listdir(input_dir):
        problem_path = os.path.join(input_dir, problem_id)
        if not os.path.isdir(problem_path):
            continue

        problem_desc = problem_descriptions.get(problem_id, "No description available.")
        feedback_subdir = os.path.join(output_dir, problem_id)
        os.makedirs(feedback_subdir, exist_ok=True)

        for filename in os.listdir(problem_path):
            if filename.endswith(".py"):
                student_path = os.path.join(problem_path, filename)
                with open(student_path, "r") as f:
                    student_code = f.read()

                prompt = build_prompt(problem_desc, student_code)
                feedback = query_ollama(prompt)

                # Save as plain text
                base = filename.replace(".py", "")
                feedback_file = os.path.join(feedback_subdir, f"{base}_feedback.txt")
                with open(feedback_file, "w") as f:
                    f.write(feedback)

                print(f"Feedback saved for {problem_id}/{filename}")

if __name__ == "__main__":
    process_all_submissions()

