import os
from google import genai
from google.genai import types
from .write_file import *
from .run_python import *
from .get_files_info import *
from .get_file_content import *



def call_function(function_call_part, verbose=False):

    functions = {
        "write_file": write_file,
        "run_python": run_python,
        "get_file_content": get_file_content,
        "get_files_info": get_files_info
    }

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name

    if function_name in functions:

        function_to_call = functions[function_name]

        args = function_call_part.args.copy()
        args["working_directory"] = "./calculator"

        function_result = function_to_call(**args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

