import json
import os

def write_json(data, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Analysis written to {output_path}")

import aiofiles

async def stream_json_output_async(results, output_path):
    """
    Asynchronously write results to a JSON file in a streaming manner.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    async with aiofiles.open(output_path, "w", encoding="utf-8") as f:
        await f.write("[\n")
        for i, result in enumerate(results):
            json_str = json.dumps(result, ensure_ascii=False, indent=2)
            await f.write(json_str)
            if i < len(results) - 1:
                await f.write(",\n")
        await f.write("\n]")

async def stream_jsonline_output_async(result: dict, output_path: str):
    async with aiofiles.open(output_path, "a") as f:  # append mode
        await f.write(json.dumps(result) + "\n")