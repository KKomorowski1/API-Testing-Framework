import json
import os
from datetime import datetime, timedelta

class DataProcessor:
    @staticmethod
    def get_dynamic_date(offset_days=0):
        return (datetime.now() + timedelta(days=offset_days)).strftime("%Y-%m-%d")

    @classmethod
    def process_payload(cls, payload):
        if isinstance(payload, dict):
            return {k: cls.process_payload(v) for k, v in payload.items()}
        elif isinstance(payload, list):
            return [cls.process_payload(item) for item in payload]
        elif isinstance(payload, str):
            if payload == "{{today}}": return cls.get_dynamic_date(0)
            if payload == "{{next_week}}": return cls.get_dynamic_date(7)
            if payload == "{{next_month}}": return cls.get_dynamic_date(30)
        return payload

    @classmethod
    def load_and_process_json(cls, file_name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, '..', 'data', file_name)
        with open(file_path, 'r') as f:
            raw_data = json.load(f)
        return cls.process_payload(raw_data)