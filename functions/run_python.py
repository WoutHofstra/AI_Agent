import os
import subprocess
from google import genai
from google.genai import types

def run_python(working_directory, file_path):


    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    parent_dir = os.path.dirname(abs_file_path)

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: {file_path} is not a Python file'

    try:
        result = subprocess.run(
            ['python', file_path],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_directory

        )

        if len(result.stdout) == 0 and len(result.stderr) == 0:
            return f'No output produced'

        return f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}'



    except Exception as e:
        return f'Error: {str(e)}'


schema_run_python = types.FunctionDeclaration(
    name="run_python",
    description="Runs a specific python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The python file to run",
            ),
        },
        required=["file_path"],
    ),
)
