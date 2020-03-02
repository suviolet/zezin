from geoalchemy2.shape import from_shape, to_shape
from marshmallow import Schema, fields
from shapely import geometry


# pylint: disable=arguments-differ,unused-argument
class CoverageAreaSchema(Schema):
    _type = fields.String(attribute='type', required=True)
    coordinates = fields.List(
        fields.List(
            fields.List(
                fields.List(fields.Float(required=True), required=True),
                required=True,
            ),
            required=True,
        ),
        required=True,
    )

    def _serialize(self, value, **kwargs):
        return geometry.mapping(to_shape(value))

    def _deserialize(self, value, **kwargs):
        return from_shape(geometry.shape(value))


class AddressSchema(Schema):
    _type = fields.String(attribute='type', required=True)
    coordinates = fields.List(fields.Float(required=True), required=True)

    def _serialize(self, value, **kwargs):
        return geometry.mapping(to_shape(value))

    def _deserialize(self, value, **kwargs):
        return from_shape(geometry.shape(value))


class PartnerSchema(Schema):
    _id = fields.Integer(attribute='id')
    trading_name = fields.String(required=True)
    owner_name = fields.String(required=True)
    document = fields.String(required=True)
    coverage_area = fields.Nested(CoverageAreaSchema, required=True)
    address = fields.Nested(AddressSchema, required=True)
