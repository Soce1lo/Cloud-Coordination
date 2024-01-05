from flask import Blueprint

election_blueprint = Blueprint('election', __name__)


@election_blueprint.route('/vote', methods=['GET', 'POST'])
def vote():
    # 实现主节点选举逻辑
    return "Election response"


