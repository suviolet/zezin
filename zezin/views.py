from flask import Blueprint, make_response, request
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import DataError, IntegrityError

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
