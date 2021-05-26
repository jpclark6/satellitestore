from flask import Blueprint, jsonify, request
from sqlalchemy.exc import NoResultFound, IntegrityError

from .models import Asset, AssetClass
from .db import get_db_session
from .serializers import AssetSerializer


bp = Blueprint('api', __name__, url_prefix='/api/v1')


@bp.route('/assets/', methods=['GET'])
def list_assets():
    session = get_db_session()
    assets = session.query(Asset).all()
    if assets:
        serializer = AssetSerializer(assets=assets)
        data = serializer.serialize()
        return jsonify(data)
    else:
        return jsonify([])


@bp.route('/assets/<asset_name>')
def asset_detail(asset_name):
    session = get_db_session()
    try:
        asset = session.query(Asset).filter_by(name=asset_name).one()
        serializer = AssetSerializer(asset=asset)
        data = serializer.serialize()
        return jsonify(data)
    except NoResultFound:
        return jsonify({})


@bp.route('/assets/', methods=['POST'])
def create_asset():
    data = request.json
    serializer = AssetSerializer()
    try:
        asset = serializer.deserialize(data)
        session = get_db_session()
        session.add(asset)
        session.commit()
        return '', 201
    except (AssertionError, NoResultFound):
        return jsonify({'error': 'invalid data'}), 400
    except IntegrityError:
        return jsonify({'error': 'data already exists'}), 409
