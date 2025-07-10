import os



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
	except Error:
		print("Error occurred")
