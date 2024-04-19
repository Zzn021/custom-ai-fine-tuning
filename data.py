import sys
import json

REPORT_PATH = './report.txt'

# Read a dataset 
def load_data(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]
    
# Validates the dataset
def validate(file_path: str) -> bool:
    # Load the file
    data = load_data(file_path)
    
        
    ERROR = False
    report = []
    
    if len(data) < 10:
        ERROR = True
        report.append("* at least provide 10 examples")

    for line in data:
        # Check data type
        if not isinstance(line, dict):
            ERROR = True
            report.append("* Each enty in the dataset should be a dictionary.\n")

        # Check messages list is present
        messages = line.get("messages", None)
        if not messages:
            ERROR = True
            report.append("* A message list should be present in each entry.\n")
    
        recongnized_keys = set(["role", "content", "name", "function_call", "weight"])
        for msg in messages:
            # Check keys
            if "role" not in msg or "content" not in msg:
                ERROR = True
                report.append("* Each message in the messages list should contain the keys 'role' and 'content'\n")
            
            if not recongnized_keys.issuperset([k for k in msg]):
                ERROR = True
                report.append("* Unrecognized key in the messages list.\n")
            
            # Check Role
            if msg.get("role", None) not in ("system", "user", "assistant", "function"):
                ERROR = True
                report.append("* Unrecognized role. The role shoule be one of 'system', 'user', 'assistant' or 'function'.\n")

            # Check content
            content = msg.get("content", None)
            func = msg.get("function_call", None)
            if (not content and not func) or not isinstance(content, str):
                ERROR = True
                report.append("* The content should has textual data and is a string.\n")

        # Check assistant message presence
        if not any(msg.get("role", None) == "assistant" for msg in messages):
            ERROR = True
            report.append("* Each conversation should have at least one message from the assistant.\n")
        
    create_report(report) if ERROR else print('Dataset Validated')
            
    return not ERROR

# Creates a report
def create_report(report: list[str]) -> None:
    print('Error in dataset, creating report...')
    with open(REPORT_PATH, 'w') as f:
        for line in report:
            f.write(line)

if __name__ == "__main__":
    path = sys.argv[1]
    validate(load_data(path))