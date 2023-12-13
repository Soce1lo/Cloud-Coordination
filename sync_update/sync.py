from flask import Blueprint

sync_blueprint = Blueprint('sync', __name__)

@sync_blueprint.route('/update', methods=['POST'])
def update():
    # 实现同步与异步更新逻辑
    return "Sync response"
