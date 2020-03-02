import json

from zezin.app import create_app, db
from zezin.models import Partner
from zezin.schema import PartnerSchema

app = create_app()


class Populate:
    def __init__(self):
        self.schema = PartnerSchema()
        with open('pdvs.json', 'r') as pdvs:
            self.pdvs = json.load(pdvs)

    def ingestion_values(self):

        for partner in self.pdvs['pdvs']:
            payload = self.prepare_payload(partner)
            data = self.schema.load(payload)
            partner = Partner(**data)
            db.session.add(partner)
            db.session.commit()

    @staticmethod
    def prepare_payload(partner):
        return {
            'trading_name': partner['tradingName'],
            'owner_name': partner['ownerName'],
            'document': partner['document'],
            'coverage_area': partner['coverageArea'],
            'address': partner['address'],
        }


if __name__ == "__main__":
    with app.app_context():
        Populate().ingestion_values()
