import json
import jsonschema

SCHEMA = """
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "List of Scripts",
    "description": "Script a crier webserver.",
    "definitions": {
        "response": {
            "type": "object",
            "description": "JSON serializable data to respond with"
        },
        "status_code": {
            "type": "integer",
            "description": "HTTP status code to respond with"
        },
        "headers": {
            "type": "object",
            "description": "Headers to respond with"
        },
        "repeat": {
            "type": "integer",
            "minimum": -1,
            "default": 0,
            "description": "Number of times to repeat this script, -1 means repeat forever"
        },
        "xpath": {
            "type": "string",
            "pattern": "[a-zA-Z0-9]+([a-zA-Z0-9_-]*[.][a-zA-Z0-9_-]+)*"
        },
        "script": {
            "type": "object",
            "properties": {
                "response": { "$ref": "#/definitions/response"},
                "status_code": { "$ref": "#/definitions/status_code"},
                "headers": { "$ref": "#/definitions/headers"},
                "repeat": { "$ref": "#/definitions/repeat"},
                "after_response": { "$ref": "#/definitions/xpath" }
            },
            "requiredProperties": [
                "status_code"
            ],
            "additionalProperties": false
        }
    },
    "type": "array",
    "items": { "$ref": "#/definitions/script" },
    "minItems": 1
}
"""  # noqa


class Script:
    def __init__(self, status_code,
            headers=None,
            response=None,
            after_response=None,
            repeat=0):
        self.status_code = status_code
        self.headers = headers if headers is not None else {}
        self.response = response if response is not None else {}
        self.after_response = after_response
        self.repeat = repeat

    @classmethod
    def from_string(cls, string):
        scripts = []

        scripts_info = json.loads(string)
        schema = json.loads(SCHEMA)
        jsonschema.validate(scripts_info, schema)

        for script_info in scripts_info:
            scripts.append(cls(**script_info))

        return scripts

    @property
    def as_dict(self):
        result = {
            'status_code': self.status_code,
            'headers': self.headers,
            'response': self.response,
            'repeat': self.repeat,
        }

        if self.after_response is not None:
            result['after_response'] = self.after_response

        return result
