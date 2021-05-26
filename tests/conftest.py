from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from freezegun import freeze_time

from asset_store.models import Base, Asset, AssetClass


@pytest.fixture(scope="function", autouse=True)
def app(monkeypatch, test_assets):
    monkeypatch.setenv("SQLITE_URL", "sqlite://")
    from asset_store import db

    def mock_return():
        return test_assets

    monkeypatch.setattr(db, "get_db_session", mock_return)

    # must import after monkeypatch
    from asset_store import create_app

    app = create_app({"SQLITE_URL": "sqlite://"})

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def setup_database():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    return session


@pytest.fixture
def test_asset_classes():
    test_data = [
        {"id": 1, "class_name": "dove", "class_type": "satellite"},
        {"id": 2, "class_name": "rapideye", "class_type": "satellite"},
        {"id": 3, "class_name": "skysat", "class_type": "satellite"},
        {"id": 4, "class_name": "dish", "class_type": "antenna"},
        {"id": 5, "class_name": "yagi", "class_type": "antenna"},
    ]
    assets = [
        AssetClass(
            id=item["id"], class_name=item["class_name"], class_type=item["class_type"]
        )
        for item in test_data
    ]
    return assets


@pytest.fixture
def setup_test_data(setup_database, test_asset_classes):
    session = setup_database
    session.bulk_save_objects(test_asset_classes)
    session.commit()
    return session


@pytest.fixture
def test_assets(setup_test_data):
    session = setup_test_data
    asset_classes = session.query(AssetClass).all()
    with freeze_time("2021-05-26"):
        test_data = [
            {
                "name": "cool_sat_12",
                "asset_class": asset_classes[0].id,
                "created_at": datetime.now(),
            },
            {
                "name": "cool_sat_23",
                "asset_class": asset_classes[1].id,
                "created_at": datetime.now(),
            },
        ]
    assets = [
        Asset(
            name=item["name"],
            asset_class=item["asset_class"],
            created_at=item["created_at"],
        )
        for item in test_data
    ]
    session.bulk_save_objects(assets)
    session.commit()
    return session
