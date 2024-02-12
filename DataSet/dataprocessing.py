import json

# Function to append data to a JSON file
def append_to_json_file(file_path, data):
    # Read existing JSON data
    with open(file_path, 'r') as file:
        existing_data = json.load(file)

    # Append new data to existing data
    existing_data.append(data)

    # Write updated data back to the JSON file
    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=0)



with open("./formated_instructiondata.json") as f:
    custom_data = json.load(f)

blocks =  len(custom_data)
print(blocks)
for block in custom_data:
    print(block["disease"])
    for pair in block["questions"]:
        question = pair["question"]
        answer =pair["answer"]

        structure = f"<s>### Instruction:\n{question} \n\n### Response:\n{answer}</s>"
        #print(structure)
        data = { "inputs":  structure }
        #append_to_json_file("./data.json", data)

