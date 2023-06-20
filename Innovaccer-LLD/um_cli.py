#!/usr/bin/python
import argparse
from commands import create_command, list_command, delete_command, update_command

"""
It is the entry point of the User Management CLI. It is responsible for parsing command-line arguments, identifying the user's intended command, and executing the corresponding command handler from the commands.py module.
"""

# TODO: 
# Scope of Improvement: 
# 1. Data Validation: Separate from Main layer
# 2. Logging: Incorporate Logging for events and actions
# 3. Pagination: Implement pagination for listing

# Command mappings
COMMANDS = {
    'create': create_command,
    'list': list_command,
    'delete': delete_command,
    'update': update_command
}

# Fuzzy matching threshold
FUZZ_THRESHOLD = 0.5


def parse_args():
    parser = argparse.ArgumentParser(prog='um-cli', description='User Management CLI')
    parser.add_argument('command', nargs='?', help='Available commands')
    parser.add_argument('-u', '--user-name', help='User name')
    parser.add_argument('-d', '--designation', help='Designation')

    args, _ = parser.parse_known_args()
    return args

def fuzzy_match_command(user_input, threshold=FUZZ_THRESHOLD):
    best_match = None
    min_distance = float('inf')

    for command in COMMANDS:
        distance = levenshtein_distance(user_input, command)
        similarity = 1 - (distance / max(len(user_input), len(command)))
        if similarity >= threshold and distance < min_distance:
            best_match = command
            min_distance = distance

    return best_match

def levenshtein_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j - 1], dp[i][j - 1], dp[i - 1][j]) + 1

    return dp[m][n]

# def fuzzy_match_command(command):
#     # Find the closest matching command
#     matches = []
#     for cmd in COMMANDS.keys():
#         similarity = calculate_similarity(command, cmd)
#         if similarity >= FUZZ_THRESHOLD:
#             matches.append((cmd, similarity))

#     if matches:
#         matches.sort(key=lambda x: x[1], reverse=True)
#         return matches[0][0]

#     return None

# def calculate_similarity(command, reference):
#     # Calculate similarity score between the command and reference
#     command = command.lower()
#     reference = reference.lower()


#     if command == reference:
#         return 1.0

#     len_command = len(command)
#     len_reference = len(reference)
#     max_len = max(len_command, len_reference)
#     min_len = min(len_command, len_reference)

#     match_count = 0
#     for i in range(min_len):
#         if command[i] == reference[i]:
#             match_count += 1

#     similarity = match_count / max_len
#     return similarity

def main():
    args = parse_args()

    if args.command is None:
        print("No command provided.")
        return

    # Check if the provided command matches any existing command
    if args.command not in COMMANDS:
        matched_command = fuzzy_match_command(args.command)
        if matched_command:
            command_function = COMMANDS[matched_command]
            command_function(args)
            return
        else:
            print(f"Command not found. Please use from following available commands: \n{list(COMMANDS.keys())}")
            return

    # Execute the command
    command_function = COMMANDS[args.command]
    command_function(args)

if __name__ == '__main__':
    main()
