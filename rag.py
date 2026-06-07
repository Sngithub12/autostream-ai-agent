import os
import json
import logging

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_knowledge():
    """Load knowledge base from JSON file"""
    try:
        path = os.path.join(BASE_DIR, "data", "knowledge.json")
        if not os.path.exists(path):
            logger.warning(f"Knowledge file not found at {path}, returning empty dict")
            return {"pricing": {}, "policies": {}}
        
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading knowledge: {e}")
        return {"pricing": {}, "policies": {}}

def get_pricing_info():
    """Get pricing information from knowledge base"""
    data = load_knowledge()
    return json.dumps(data.get("pricing", {}), indent=2)

def get_policy_info():
    """Get policy information from knowledge base"""
    data = load_knowledge()
    return json.dumps(data.get("policies", {}), indent=2)
