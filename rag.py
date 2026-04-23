import json
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_knowledge():
    path = os.path.join(BASE_DIR, "data", "knowledge.json")
    with open(path, "r") as f:
        return json.load(f)


def get_pricing_info():
    data = load_knowledge()
    return data["pricing"]

def get_policy_info():
    data = load_knowledge()
    return data["policies"]