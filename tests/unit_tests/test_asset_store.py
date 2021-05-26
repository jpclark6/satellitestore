from datetime import datetime

import pytest
from freezegun import freeze_time
from sqlalchemy.exc import IntegrityError

from asset_store.models import Asset, AssetClass


@freeze_time("2021-05-26")
def test_create_good_asset(test_assets):
    asset_class = test_assets.query(AssetClass).first()
    data = {
        "name": "test-A-test_42",
        "asset_class": asset_class.id,
        "created_at": datetime.now(),
    }
    asset = Asset(
        name=data["name"],
        asset_class=data["asset_class"],
        created_at=data["created_at"],
    )
    test_assets.add(asset)
    test_assets.commit()
    real_asset = test_assets.query(Asset).filter_by(name=data["name"]).one()

    assert real_asset.name == data["name"]
    assert real_asset.asset_class == data["asset_class"]
    assert real_asset.created_at == data["created_at"]


@freeze_time("2021-05-26")
def test_asset_duplicate_name(test_assets):
    asset_class = test_assets.query(AssetClass).first()
    data = {
        "name": "TestGoodName",
        "asset_class": asset_class.id,
        "created_at": datetime.now(),
    }
    asset = Asset(
        name=data["name"],
        asset_class=data["asset_class"],
        created_at=data["created_at"],
    )
    test_assets.add(asset)
    test_assets.commit()

    asset = Asset(
        name=data["name"],
        asset_class=data["asset_class"],
        created_at=data["created_at"],
    )
    test_assets.add(asset)
    with pytest.raises(IntegrityError):
        test_assets.commit()


@freeze_time("2021-05-26")
def test_bad_asset_name_too_short(test_assets):
    asset_class = test_assets.query(AssetClass).first()
    data = {
        "name": "a" * 3,
        "asset_class": asset_class.id,
        "created_at": datetime.now(),
    }

    with pytest.raises(AssertionError):
        Asset(
            name=data["name"],
            asset_class=data["asset_class"],
            created_at=data["created_at"],
        )


@freeze_time("2021-05-26")
def test_good_asset_name_at_min(test_assets):
    asset_class = test_assets.query(AssetClass).first()
    data = {
        "name": "a" * 4,
        "asset_class": asset_class.id,
        "created_at": datetime.now(),
    }

    asset = Asset(
        name=data["name"],
        asset_class=data["asset_class"],
        created_at=data["created_at"],
    )
    test_assets.add(asset)
    test_assets.commit()
    real_asset = test_assets.query(Asset).filter_by(name=data["name"]).one()

    assert real_asset.name == data["name"]


@freeze_time("2021-05-26")
def test_bad_asset_name_too_long(test_assets):
    asset_class = test_assets.query(AssetClass).first()
    data = {
        "name": "a" * 65,
        "asset_class": asset_class.id,
        "created_at": datetime.now(),
    }

    with pytest.raises(AssertionError):
        Asset(
            name=data["name"],
            asset_class=data["asset_class"],
            created_at=data["created_at"],
        )


@freeze_time("2021-05-26")
def test_good_asset_name_at_max(test_assets):
    asset_class = test_assets.query(AssetClass).first()
    data = {
        "name": "a" * 64,
        "asset_class": asset_class.id,
        "created_at": datetime.now(),
    }

    asset = Asset(
        name=data["name"],
        asset_class=data["asset_class"],
        created_at=data["created_at"],
    )
    test_assets.add(asset)
    test_assets.commit()
    real_asset = test_assets.query(Asset).filter_by(name=data["name"]).one()

    assert real_asset.name == data["name"]


@freeze_time("2021-05-26")
def test_bad_asset_name_bad_characters(test_assets):
    asset_class = test_assets.query(AssetClass).first()
    data = {
        "name": "test*&test",
        "asset_class": asset_class.id,
        "created_at": datetime.now(),
    }

    with pytest.raises(AssertionError):
        Asset(
            name=data["name"],
            asset_class=data["asset_class"],
            created_at=data["created_at"],
        )


@freeze_time("2021-05-26")
def test_bad_asset_name_starting_dash(test_assets):
    asset_class = test_assets.query(AssetClass).first()
    data = {
        "name": "-test",
        "asset_class": asset_class.id,
        "created_at": datetime.now(),
    }

    with pytest.raises(AssertionError):
        Asset(
            name=data["name"],
            asset_class=data["asset_class"],
            created_at=data["created_at"],
        )


@freeze_time("2021-05-26")
def test_bad_asset_name_starting_underscore(test_assets):
    asset_class = test_assets.query(AssetClass).first()
    data = {
        "name": "_test",
        "asset_class": asset_class.id,
        "created_at": datetime.now(),
    }

    with pytest.raises(AssertionError):
        Asset(
            name=data["name"],
            asset_class=data["asset_class"],
            created_at=data["created_at"],
        )


def test_asset_serializer_assets(app, monkeypatch, test_assets):
    # must import inside test for correct ENV var to get set for test
    from asset_store.serializers import AssetSerializer

    assets = test_assets.query(Asset).all()

    serializer = AssetSerializer(assets=assets)
    output = serializer.serialize()
    expected = [
        {
            "name": "cool_sat_12",
            "asset_class": "dove",
            "asset_type": "satellite",
            "created_at": "2021-05-26 00:00:00",
        },
        {
            "name": "cool_sat_23",
            "asset_class": "rapideye",
            "asset_type": "satellite",
            "created_at": "2021-05-26 00:00:00",
        },
    ]
    assert output == expected


def test_asset_serializer_asset(app, monkeypatch, test_assets):
    # must import inside test for correct ENV var to get set for test
    from asset_store.serializers import AssetSerializer

    asset = test_assets.query(Asset).first()

    serializer = AssetSerializer(asset=asset)
    output = serializer.serialize()
    expected = {
        "name": "cool_sat_12",
        "asset_class": "dove",
        "asset_type": "satellite",
        "created_at": "2021-05-26 00:00:00",
    }
    assert output == expected


def test_asset_serializer_no_assets(app, monkeypatch, test_assets):
    # must import inside test for correct ENV var to get set for test
    from asset_store.serializers import AssetSerializer

    asset = test_assets.query(Asset).first()

    serializer = AssetSerializer()
    output = serializer.serialize()

    assert output == {}


def test_asset_deserializer(app, monkeypatch, test_assets):
    # must import inside test for correct ENV var to get set for test
    from asset_store.serializers import AssetSerializer

    asset = {"name": "test123", "asset_class": "dove", "asset_type": "satellite"}

    serializer = AssetSerializer()
    output = serializer.deserialize(asset)
    expected_class = test_assets.query(AssetClass).filter_by(class_name="dove").one().id
    asset = Asset(name="test123", asset_class=expected_class, created_at=datetime.now())

    assert output.name == asset.name
    assert output.asset_class == asset.asset_class


def test_asset_property(app, test_assets):
    asset = test_assets.query(Asset).first()

    assert asset.asset_type == 'satellite'


def test_verify_type(app, test_assets):
    asset = test_assets.query(Asset).first()
    asset_class = asset.asset_class_details

    assert None == asset.verify_type(asset_class, 'satellite')
    with pytest.raises(AssertionError):
        asset.verify_type(asset_class, 'antenna')
