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
        "script": {
            "type": "object",
            "properties": {
                "response": { "$ref": "#/definitions/response"},
                "status_code": { "$ref": "#/definitions/status_code"},
                "headers": { "$ref": "#/definitions/headers"},
                "repeat": { "$ref": "#/definitions/repeat"}
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
    def __init__(self, status_code, headers=None, response=None, repeat=0):
        self.status_code = status_code
        self.headers = headers if headers is not None else {}
        self.response = response if response is not None else {}
        self.repeat = repeat
        self.count = 0

    def next_response(self):
        if not self.is_done:
            self.count += 1
            return self.response, self.status_code, self.headers
        else:
            raise RuntimeError("Script repeated too many times")

    @property
    def is_done(self):
        if self.repeat == -1:
            return False
        else:
            return self.count > self.repeat

    @classmethod
    def from_string(cls, string):
        scripts = []

        scripts_info = json.loads(string)
        schema = json.loads(SCHEMA)
        jsonschema.validate(scripts_info, schema)

        for script_info in scripts_info:
            scripts.append(cls(**script_info))

        return scripts
