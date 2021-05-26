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
        return {
            'name': name,
            'asset_class': asset_class,
            'asset_type': asset_type,
        }
