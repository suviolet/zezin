import json

import pytest

from zezin.models import Partner


@pytest.mark.usefixtures('session')
def test_create_partner_with_succes(client, payload, headers):
    data = json.dumps(payload)
    response = client.post('partners/', data=data, headers=headers)
    partner_recorded = Partner.query.first()

    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert (
        response.json['document']
        == payload['document']
        == partner_recorded.document
    )


@pytest.mark.usefixtures('session')
def test_create_partner_failed_bad_request_invalid_payload(client, headers):
    data = json.dumps({})
    response = client.post('partners/', data=data, headers=headers)

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert 'Bad request error' in response.json['message']


@pytest.mark.parametrize(
    'field',
    ['document', 'trading_name', 'owner_name', 'coverage_area', 'address'],
)
@pytest.mark.usefixtures('session')
def test_create_partner_failed_bad_request_without_some_field(
    client, payload, headers, field
):
    del payload[field]
    message = f"'{field}': ['Missing data for required field.']"

    data = json.dumps(payload)
    response = client.post('partners/', data=data, headers=headers)

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert message in response.json['message']


@pytest.mark.usefixtures('session')
def test_create_partner_failed_bad_request_dataerror_value_too_long(
    client, payload, headers
):
    payload['document'] = '9' * 51
    data = json.dumps(payload)
    response = client.post('partners/', data=data, headers=headers)

    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert 'value too long for type' in response.json['message']


@pytest.mark.usefixtures('session', 'partner_saved')
def test_create_partner_failed_already_exists_document(
    client, payload, headers
):
    document = payload['document']
    message = f'Partner already exists, document: {document}'

    data = json.dumps(payload)
    response = client.post('partners/', data=data, headers=headers)

    assert response.status_code == 409
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json['message'] == message


@pytest.mark.usefixtures('session')
def test_retrieve_partner_with_success(
    client, headers, payload, partner_saved
):
    # pylint: disable=protected-access
    response = client.get(f'partners/{partner_saved._id}/', headers=headers)

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json == payload


@pytest.mark.usefixtures('session')
def test_retrieve_partner_failed_not_found_partner(client, headers):
    partner_id = 666
    message = f'Partner: {partner_id} could not be found.'
    response = client.get(f'partners/{partner_id}/', headers=headers)

    assert response.status_code == 404
    assert response.headers['Content-Type'] == 'application/json'
    assert response.json['message'] == message
