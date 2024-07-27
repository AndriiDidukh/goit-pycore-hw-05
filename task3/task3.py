import sys
import re
from typing import List, Dict


def parse_log_line(line: str) -> Dict[str, str]:
    match = re.match(r'(\S+ \S+) (\S+) (.+)', line)
    if match:
        return {
            'timestamp': match.group(1),
            'level': match.group(2),
            'message': match.group(3)
        }
    return {}


def load_logs(file_path: str) -> List[Dict[str, str]]:
    logs = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                parsed_line = parse_log_line(line)
                if parsed_line:
                    logs.append(parsed_line)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    return logs


def filter_logs_by_level(logs: List[Dict[str, str]], level: str) -> List[Dict[str, str]]:
    return [log for log in logs if log['level'] == level]


def count_logs_by_level(logs: List[Dict[str, str]]) -> Dict[str, int]:
    counts = {'INFO': 0, 'ERROR': 0, 'DEBUG': 0, 'WARNING': 0}
    for log in logs:
        if log['level'] in counts:
            counts[log['level']] += 1
    return counts


def display_log_counts(counts: Dict[str, int]):
    print("Log Level Counts:")
    for level, count in counts.items():
        print(f"{level}: {count}")


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Wrong arguments")
        sys.exit(1)

    file_path = sys.argv[1]
    logs = load_logs(file_path)

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if len(sys.argv) == 3:
        level = sys.argv[2].upper()
        filtered_logs = filter_logs_by_level(logs, level)
        print(f"Detailed logs for lever {level}")
        for log in filtered_logs:
            print(f"{log['timestamp']} {log['level']} {log['message']}")


if __name__ == "__main__":
    main()