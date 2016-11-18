import json
import jsonschema

SCHEMA = """
{
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "List of Scripts",
    "description": "Script a crier webserver.",
    "definitions": {
        "response": {
            "type": "object"
        },
        "status_code": {
            "type": "integer"
        },
        "headers": {
            "type": "object"
        },
        "script": {
            "type": "object",
            "properties": {
                "response": { "$ref": "#/definitions/response"},
                "status_code": { "$ref": "#/definitions/status_code"},
                "headers": { "$ref": "#/definitions/headers"}
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
"""


def _load_schema():
    return json.loads(SCHEMA)


def load_and_validate(scripts_string):
    scripts = json.loads(scripts_string)
    jsonschema.validate(scripts, _load_schema())
    return scripts
