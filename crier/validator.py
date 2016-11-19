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


def _load_schema():
    return json.loads(SCHEMA)


def load_and_validate(scripts_string):
    scripts = json.loads(scripts_string)
    jsonschema.validate(scripts, _load_schema())
    return scripts
