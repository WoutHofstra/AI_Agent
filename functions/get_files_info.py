import os
from google import genai
from google.genai import types


def get_files_info(working_directory, directory=None):

	if directory:
		full_path = os.path.join(working_directory, directory)
	else:
		full_path = working_directory


	absolute_working_dir = os.path.abspath(working_directory)
	absolute_target_dir = os.path.abspath(full_path)

	if not absolute_target_dir.startswith(absolute_working_dir):
		return "Error: Cannot list {absolute_target_dir} as it is outside the permitted working directory"

	if not os.path.isdir(full_path):
		return "Error: {directory} is not a directory"

	try:
		result_lines = []

		for item in os.listdir(full_path):

			item_path = os.path.join(full_path, item)
			size = os.path.getsize(item_path)
			is_directory = os.path.isdir(item_path)

			line = f"- {item}: file_size:{size} bytes, is_dir={is_directory}"
			result_lines.append(line)

		return "\n".join(result_lines)
	except Exception:
		print("Error occurred")

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
