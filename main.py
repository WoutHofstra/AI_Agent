import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
        print("Please provide a valid prompt")
        sys.exit(1)

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


def main():

	response = client.models.generate_content(
		model = 'gemini-2.0-flash-001',
		contents = f"{messages}, please only use 1 paragraph",
	)
	print(response.text)

	prompt_tokens = response.usage_metadata.prompt_token_count
	response_tokens = response.usage_metadata.candidates_token_count


	if is_verbose:
		print(f"User prompt: {prompt}")
		print(f"Prompt tokens: {prompt_tokens}")
		print(f"Response tokens: {response_tokens}")


if __name__ == "__main__":
    main()
