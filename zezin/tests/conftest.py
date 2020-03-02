import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError

from zezin.app import create_app, db
from zezin.models import Partner
from zezin.populate import Populate
from zezin.schema import PartnerSchema

address = 'postgresql://postgres:postgres@127.0.0.1'

# pylint: disable=redefined-outer-name
def create_database():
    conn = create_engine(address, isolation_level='AUTOCOMMIT')

    database_already_exists = conn.execute(
        "SELECT exists(SELECT datname FROM "
        "pg_catalog.pg_database where datname='test_ze')"
    )

    if not database_already_exists.first()[0]:
        conn.execute('CREATE DATABASE test_ze')

    db_conn = create_engine(f'{address}/test_ze', isolation_level='AUTOCOMMIT')
    try:
        db_conn.execute('SELECT PostGIS_full_version()')
    except ProgrammingError:
        db_conn.execute('CREATE EXTENSION postgis')


@pytest.fixture(scope='session')
def app(request):
    testing_settings = {
        'TESTING': True,
        'PROPAGATE_EXCEPTIONS': True,
        'SQLALCHEMY_DATABASE_URI': f'{address}/test_ze',
        'SQLALCHEMY_TRACK_MODIFICATIONS': True,
    }

    app = create_app(settings_override=testing_settings)

    context = app.app_context()
    context.push()

    create_database()
    db.create_all()

    def teardown():
        db.session.remove()
        db.drop_all()
        context.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='function')
def session(request):
    connection = db.engine.connect()
    transaction = connection.begin()

    session = db.create_scoped_session(
        options={'bind': connection, 'binds': {}}
    )

    db.session = session

    def teardown():
        if transaction.is_active:
            db.session.query(Partner).delete()
            transaction.commit()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)


@pytest.fixture()
def headers():
    return {'Content-type': 'application/json'}


@pytest.fixture()
def payload():
    return {
        'owner_name': 'aaaaa',
        'document': '92/233',
        'trading_name': 'bbbbbb',
        'coverage_area': {
            'type': 'MultiPolygon',
            'coordinates': [
                [
                    [
                        [-43.36556, -22.99669],
                        [-43.36539, -23.01928],
                        [-43.26583, -23.01802],
                        [-43.25724, -23.00649],
                        [-43.23355, -23.00127],
                        [-43.2381, -22.99716],
                        [-43.23866, -22.99649],
                        [-43.24063, -22.99756],
                        [-43.24634, -22.99736],
                        [-43.24677, -22.99606],
                        [-43.24067, -22.99381],
                        [-43.24886, -22.99121],
                        [-43.25617, -22.99456],
                        [-43.25625, -22.99203],
                        [-43.25346, -22.99065],
                        [-43.29599, -22.98283],
                        [-43.3262, -22.96481],
                        [-43.33427, -22.96402],
                        [-43.33616, -22.96829],
                        [-43.342, -22.98157],
                        [-43.34817, -22.97967],
                        [-43.35142, -22.98062],
                        [-43.3573, -22.98084],
                        [-43.36522, -22.98032],
                        [-43.36696, -22.98422],
                        [-43.36717, -22.98855],
                        [-43.36636, -22.99351],
                        [-43.36556, -22.99669],
                    ]
                ]
            ],
        },
        'address': {'type': 'Point', 'coordinates': [-43.297337, -23.013538]},
    }


@pytest.fixture()
def partner_saved(payload):
    data = PartnerSchema().load(payload)
    partner = Partner(**data)
    db.session.add(partner)
    db.session.commit()
    return partner


@pytest.fixture()
def populate_database():
    Populate().ingestion_values()
