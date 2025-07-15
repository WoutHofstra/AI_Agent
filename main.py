import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import sys
from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_file import *
from functions.run_python import *
from functions.call_function import *

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
        print("Please provide a valid prompt")
        sys.exit(1)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
prompt = sys.argv[1]
is_verbose = False

if len(sys.argv) == 3 and sys.argv[2] == "--verbose":
	is_verbose = True
elif len(sys.argv) > 3:
	print("Too many arguments provided. Usage: uv run main.py \"<prompt>\" [--verbose]")
	sys.exit(1)

messages = [
	types.Content(role = "user", parts = [types.Part(text=prompt)]),
]

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python,
    ]
)

def main():

	response = client.models.generate_content(
		model = 'gemini-2.0-flash-001',
		contents = messages,
		config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
	)

	if response.function_calls:
		for function_call_part in response.function_calls:
			function_call_result=call_function(function_call_part, verbose=is_verbose)

			if not function_call_result.parts[0].function_response.response:
				raise Exception("Function call failed to return proper response")
			if is_verbose:
				print(f'-> {function_call_result.parts[0].function_response.response}')

	else:
		print(response.text)

	prompt_tokens = response.usage_metadata.prompt_token_count
	response_tokens = response.usage_metadata.candidates_token_count


	if is_verbose:
		print(f"User prompt: {prompt}")
		print(f"Prompt tokens: {prompt_tokens}")
		print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
