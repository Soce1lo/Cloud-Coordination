from flask import Blueprint, jsonify, request
from models import db, Node

network_blueprint = Blueprint('network', __name__)


@network_blueprint.route('/test', methods=['GET'])
def test():
    # 选择第一个节点，或者根据特定条件选择节点
    node = Node.query.first()
    if node:
        # node.network_status = '3'  # 更新 network_status
        # db.session.commit()  # 提交更改到数据库
        return jsonify(node.to_dict())  # 返回更新后的节点信息
    else:
        return "No node found", 404


@network_blueprint.route('/update', methods=['POST'])
def update():
    node = Node.query.first()
    if node is None:
        return jsonify({"error": "No node found"}), 404

    # 从请求中获取数据
    data = request.get_json()
    if 'network_status' not in data:
        return jsonify({"error": "Missing network_status in request"}), 400

    node.network_status = data['network_status']
    db.session.commit()

    return jsonify({"message": "Update success"}), 200

    # 保存到数据库
    db.session.commit()
