import os
import pickle

def load_user_data(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)  # Security: deserialisation vulnerability

def calculate_average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)  # Bug: ZeroDivisionError on empty list

def get_api_key():
    return "sk-1234567890abcdef"  # Security: hardcoded secret

def process_input(user_input):
    result = eval(user_input)  # Security: code injection
    return result

class UserManager:
    def __init__(self):
        self.users = {}

    def add_user(self, name, email):
        self.users[name] = email  # Bug: overwrites if name exists

    def get_user(self, name):
        return self.users[name]  # Bug: KeyError if not found