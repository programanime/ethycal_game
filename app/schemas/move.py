from marshmallow import Schema, fields, validate


class MoveSchema(Schema):
    x = fields.Int(required=True, validate=validate.Range(min=0, max=2))
    y = fields.Int(required=True, validate=validate.Range(min=0, max=2))
