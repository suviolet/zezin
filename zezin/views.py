from flask import Blueprint, make_response, request
from marshmallow.exceptions import ValidationError
from sqlalchemy import func
from sqlalchemy.exc import DataError, IntegrityError
from werkzeug.exceptions import NotFound

from zezin.app import db
from zezin.models import Partner
from zezin.schema import PartnerSchema

schema = PartnerSchema()

partners_routes = Blueprint('partners_routes', __name__, url_prefix='/')

HEADERS = {'Content-Type': 'application/json'}


@partners_routes.route('partners/', methods=['POST'])
def create_partner():
    try:
        payload = request.get_json()
        data = schema.load(payload)
        partner = Partner(**data)
        db.session.add(partner)
        db.session.commit()
    except IntegrityError as e:
        message = {
            'message': f'Partner already exists, document: {partner.document}'
        }
        return make_response(message, 409, HEADERS)
    except (DataError, ValidationError) as e:
        message = {'message': f'Bad request error: {e.args[0]}'}
        return make_response(message, 400, HEADERS)

    return make_response(schema.dump(data), 201, HEADERS)


@partners_routes.route('partners/<int:partner_id>/', methods=['GET'])
def retrieve_partner(partner_id):
    try:
        partner = Partner.query.get_or_404(partner_id)
    except NotFound:
        message = {'message': f'Partner: {partner_id} could not be found.'}
        return make_response(message, 404, HEADERS)

    return make_response(schema.dump(partner.__dict__), 200, HEADERS)


@partners_routes.route('partners/', methods=['GET'])
def search_nearest_partner():
    try:
        longitude = float(request.args.get('lng'))
        latitude = float(request.args.get('lat'))
    except ValueError:
        message = {
            'message': f'Bad request: lng and lat are '
            'required and should be float type'
        }
        return make_response(message, 400, HEADERS)
    else:
        partner = (
            Partner.query.filter(
                func.ST_Intersects(
                    Partner.coverage_area, f'POINT({longitude} {latitude})'
                )
            )
            .order_by(
                func.ST_Distance(
                    Partner.address, f'POINT({longitude} {latitude})'
                )
            )
            .first()
        )

        if partner:
            return make_response(schema.dump(partner), 200, HEADERS)

        return make_response('', 204, HEADERS)
