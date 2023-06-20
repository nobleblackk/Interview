#!/usr/bin/python

import json

"""
contains the command handlers for the User Management CLI. It defines functions for various commands such as create_command, list_command, update_command, and delete_command. Each command handler function takes command-line arguments, performs the necessary operations, and provides appropriate feedback to the user.

The module also includes utility functions like load_users and save_users for reading and writing user information to a file. These functions ensure that the user data is stored persistently between different invocations of the CLI.
"""

USERS_FILE = 'users.json'

def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return "File not Found"

def save_users(users):
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file)

def create_user(username, designation):
    users = load_users()

    if username in users:
        print(f"Error: User '{username}' already exists.")
    else:
        users[username] = {'username': username, 'designation': designation}
        save_users(users)
        print(f"User '{username}' created successfully.")

def list_users():
    users = load_users()

    if users:
        print("List of users:")
        for username, details in users.items():
            print(f"Username: {username}, Designation: {details['designation']}")
    else:
        print("No users found.")

def update_user(username, new_designation):
    users = load_users()

    if username in users:
        users[username]['designation'] = new_designation
        save_users(users)
        print(f"User '{username}' updated successfully.")
    else:
        print(f"Error: User '{username}' not found.")

def delete_user(username):
    users = load_users()

    if username in users:
        del users[username]
        save_users(users)
        print(f"User '{username}' deleted successfully.")
    else:
        print(f"Error: User '{username}' not found.")

# Command functions
def create_command(args):
    if args.user_name is None:
        print("Error: User name is required.")
    elif args.designation is None:
        print("Error: Designation is required.")
    else:
        create_user(args.user_name, args.designation)

def list_command(args):
    list_users()

def delete_command(args):
    if args.user_name is None:
        print("Error: User name is required.")
    else:
        delete_user(args.user_name)

def update_command(args):
    if args.user_name is None:
        print("Error: User name is required.")
    elif args.designation is None:
        print("Error: Designation is required.")
    else:
        update_user(args.user_name, args.designation)
