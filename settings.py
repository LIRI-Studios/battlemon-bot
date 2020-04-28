from pathlib import Path  # python3 only
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path('.') / '.env')

def get_attribute(data, attribute, default_value):
    return data.get(attribute) or default_value