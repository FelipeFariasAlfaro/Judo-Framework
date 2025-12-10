"""
Utility helpers - Common utility functions
"""

import json
import yaml
import base64
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from faker import Faker
from .file_loader import (
    read, read_json, read_yaml, read_text, read_csv, read_binary,
    write_json, write_yaml, write_text, file_exists, set_base_path
)


# Initialize Faker
fake = Faker()


def to_json(data: Any, pretty: bool = False) -> str:
    """Convert data to JSON string"""
    if pretty:
        return json.dumps(data, indent=2, ensure_ascii=False)
    return json.dumps(data, ensure_ascii=False)


def from_json(json_str: str) -> Any:
    """Parse JSON string to data"""
    return json.loads(json_str)


def to_yaml(data: Any) -> str:
    """Convert data to YAML string"""
    return yaml.dump(data, default_flow_style=False, allow_unicode=True)


def from_yaml(yaml_str: str) -> Any:
    """Parse YAML string to data"""
    return yaml.safe_load(yaml_str)


def encode_base64(data: Union[str, bytes]) -> str:
    """Encode data to base64"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return base64.b64encode(data).decode('ascii')


def decode_base64(encoded: str) -> str:
    """Decode base64 to string"""
    return base64.b64decode(encoded).decode('utf-8')


def hash_md5(data: str) -> str:
    """Generate MD5 hash"""
    return hashlib.md5(data.encode('utf-8')).hexdigest()


def hash_sha256(data: str) -> str:
    """Generate SHA256 hash"""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def generate_uuid() -> str:
    """Generate UUID4"""
    return str(uuid.uuid4())


def current_timestamp() -> int:
    """Get current timestamp"""
    return int(datetime.now().timestamp())


def format_datetime(dt: datetime = None, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format datetime"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime(format_str)


def parse_datetime(date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """Parse datetime string"""
    return datetime.strptime(date_str, format_str)


def add_days(days: int, base_date: datetime = None) -> datetime:
    """Add days to date"""
    if base_date is None:
        base_date = datetime.now()
    return base_date + timedelta(days=days)


def subtract_days(days: int, base_date: datetime = None) -> datetime:
    """Subtract days from date"""
    if base_date is None:
        base_date = datetime.now()
    return base_date - timedelta(days=days)


# Fake data generators using Faker

def fake_name() -> str:
    """Generate fake name"""
    return fake.name()


def fake_email() -> str:
    """Generate fake email"""
    return fake.email()


def fake_phone() -> str:
    """Generate fake phone number"""
    return fake.phone_number()


def fake_address() -> str:
    """Generate fake address"""
    return fake.address()


def fake_company() -> str:
    """Generate fake company name"""
    return fake.company()


def fake_text(max_chars: int = 200) -> str:
    """Generate fake text"""
    return fake.text(max_nb_chars=max_chars)


def fake_url() -> str:
    """Generate fake URL"""
    return fake.url()


def fake_ipv4() -> str:
    """Generate fake IPv4 address"""
    return fake.ipv4()


def fake_user_agent() -> str:
    """Generate fake user agent"""
    return fake.user_agent()


def fake_credit_card() -> str:
    """Generate fake credit card number"""
    return fake.credit_card_number()


def fake_date(start_date: str = "-30d", end_date: str = "today") -> str:
    """Generate fake date"""
    return fake.date_between(start_date=start_date, end_date=end_date).strftime("%Y-%m-%d")


def fake_datetime_str(start_date: str = "-30d", end_date: str = "now") -> str:
    """Generate fake datetime string"""
    return fake.date_time_between(start_date=start_date, end_date=end_date).isoformat()


def deep_merge(dict1: Dict, dict2: Dict) -> Dict:
    """Deep merge two dictionaries"""
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    
    return result


def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    """Flatten nested dictionary"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def unflatten_dict(d: Dict, sep: str = '.') -> Dict:
    """Unflatten dictionary"""
    result = {}
    for key, value in d.items():
        keys = key.split(sep)
        current = result
        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]
        current[keys[-1]] = value
    return result