from sqlalchemy.sql import func

from .models import Asset, AssetClass
from .db import get_db_session


class AssetSerializer:
    def __init__(self, asset=None, assets=None):
        self.assets = assets
        self.asset = asset

    def serialize(self):
        if self.assets:
            return self.serialize_assets(self.assets)
        if self.asset:
            return self.split_asset(self.asset)
        return {}

    def serialize_assets(self, assets):
        data = []
        for asset in assets:
            asset_details = self.split_asset(asset)
            data.append(asset_details)
        return data

    def split_asset(self, asset):
        name = asset.name
        asset_class = asset.asset_class_details.class_name.value
        asset_type = asset.asset_class_details.class_type.value
        created_at = str(asset.created_at)
        return {
            "name": name,
            "asset_class": asset_class,
            "asset_type": asset_type,
            "created_at": created_at,
        }

    def deserialize(self, data):
        session = get_db_session()
        try:
            name = data["name"]
            asset_class_name = data["asset_class"]
            asset_type = data["asset_type"]
            asset_class = (
                session.query(AssetClass).filter_by(class_name=asset_class_name).one()
            )
            asset = Asset(name=name, asset_class=asset_class.id, created_at=func.now())
            asset.verify_type(asset_class, asset_type)
            return asset
        finally:
            session.close()
