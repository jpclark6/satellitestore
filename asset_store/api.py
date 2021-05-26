from flask import Blueprint, jsonify

from .models import Asset, AssetClass
from .db import get_db_session
from .serializers import AssetSerializer


bp = Blueprint('api', __name__, url_prefix='/api/v1')


@bp.route('/assets/')
def list_assets():
    session = get_db_session()
    assets = session.query(Asset).all()
    if assets:
        serializer = AssetSerializer(assets=assets)
        data = serializer.serialize()
        return jsonify(data)
    else:
        return jsonify({})
