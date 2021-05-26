from freezegun import freeze_time


@freeze_time("2021-05-26")
def test_asset_list(client):
    response = client.get("/api/v1/assets/")
    data = response.json

    expected = [
        {
            "asset_class": "dove",
            "asset_type": "satellite",
            "created_at": "2021-05-26 00:00:00",
            "name": "cool_sat_12",
        },
        {
            "asset_class": "rapideye",
            "asset_type": "satellite",
            "created_at": "2021-05-26 00:00:00",
            "name": "cool_sat_23",
        },
    ]

    assert data == expected
    assert response.status_code == 200


@freeze_time("2021-05-26")
def test_asset_detail(client):
    response = client.get("/api/v1/assets/cool_sat_12")
    data = response.json

    expected = {
        "asset_class": "dove",
        "asset_type": "satellite",
        "created_at": "2021-05-26 00:00:00",
        "name": "cool_sat_12",
    }

    assert data == expected
    assert response.status_code == 200


@freeze_time("2021-05-26")
def test_asset_detail_no_results(client):
    response = client.get("/api/v1/assets/not_cool_sat_12")
    data = response.json

    expected = {}

    assert data == expected
    assert response.status_code == 200


@freeze_time("2021-05-26")
def test_bad_endpoint(client):
    response = client.get("/api/v1/trees")

    assert response.status_code == 404


@freeze_time("2021-05-26")
def test_create_asset(client, test_assets):
    data = {"asset_class": "dove", "asset_type": "satellite", "name": "test-_Check123"}
    created_response = client.post("/api/v1/assets/", json=data)

    response = client.get("/api/v1/assets/test-_Check123")
    actual = response.json

    assert created_response.status_code == 201
    assert actual["asset_class"] == "dove"
    assert actual["asset_type"] == "satellite"
    assert actual["name"] == "test-_Check123"
    assert response.status_code == 200


@freeze_time("2021-05-26")
def test_create_invalid_asset_name_underscore(client, test_assets):
    data = {"asset_class": "dove", "asset_type": "satellite", "name": "_test-check"}
    created_response = client.post("/api/v1/assets/", json=data)
    request_response = client.get("/api/v1/assets/_test-check")

    assert created_response.status_code == 400
    assert request_response.json == {}


@freeze_time("2021-05-26")
def test_create_invalid_asset_name_nonascii(client):
    data = {"asset_class": "dove", "asset_type": "satellite", "name": "test#check"}
    created_response = client.post("/api/v1/assets/", json=data)

    assert created_response.status_code == 400


@freeze_time("2021-05-26")
def test_create_invalid_asset_type_antenna(client):
    data_dove = {"asset_class": "dove", "asset_type": "antenna", "name": "testcheck"}
    data_rapideye = {
        "asset_class": "rapideye",
        "asset_type": "antenna",
        "name": "testcheck",
    }
    data_skysat = {
        "asset_class": "skysat",
        "asset_type": "antenna",
        "name": "testcheck",
    }

    created_response_dove = client.post("/api/v1/assets/", json=data_dove)
    created_response_rapideye = client.post("/api/v1/assets/", json=data_rapideye)
    created_response_skysat = client.post("/api/v1/assets/", json=data_skysat)

    assert created_response_dove.status_code == 400
    assert created_response_rapideye.status_code == 400
    assert created_response_skysat.status_code == 400


@freeze_time("2021-05-26")
def test_create_invalid_asset_type_satellite(client):
    data_dish = {"asset_class": "dish", "asset_type": "satellite", "name": "testcheck"}
    data_yagi = {"asset_class": "yagi", "asset_type": "satellite", "name": "testcheck"}

    created_response_dish = client.post("/api/v1/assets/", json=data_dish)
    created_response_yagi = client.post("/api/v1/assets/", json=data_yagi)

    assert created_response_dish.status_code == 400
    assert created_response_yagi.status_code == 400


@freeze_time("2021-05-26")
def test_create_invalid_asset_missing_some_data(client):
    data = {"name": "test#check"}
    created_response = client.post("/api/v1/assets/", json=data)

    assert created_response.status_code == 400


@freeze_time("2021-05-26")
def test_create_invalid_asset_missing_data(client):
    created_response = client.post("/api/v1/assets/")

    assert created_response.status_code == 400


@freeze_time("2021-05-26")
def test_create_duplicate_asset(client):
    data = {"asset_class": "dove", "asset_type": "satellite", "name": "test-check"}
    client.post("/api/v1/assets/", json=data)
    created_response = client.post("/api/v1/assets/", json=data)

    assert created_response.status_code == 409
