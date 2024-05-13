from marshmallow import Schema, fields


class SpaceObjectSchema(Schema):
    sat_id = fields.Str(required=True)
    sat_catalog_number = fields.Str(required=True)
    sat_name = fields.Str(required=True)
    file_id = fields.Str(required=True)
    launch_country = fields.Str(required=True)
    launch_site = fields.Str(required=True)
    launch_date = fields.Str(required=True)
    launch_year = fields.Str(required=True)
    launch_number = fields.Str(required=True)
    launch_piece = fields.Str(required=True)
    object_type = fields.Str(required=True)
    object_name = fields.Str(required=True)
    object_id = fields.Str(required=True)
    object_number = fields.Str(required=True)
