import requests
from flask import Blueprint
from models import db, Node


election_blueprint = Blueprint('election', __name__)


@election_blueprint.route('/')
# 开始进行任务
def start():
    # TODO 实现开始任务逻辑
    # 请求其他节点的状态信息
    # 向多个ip发送请求，获取响应
    # 选取网络状态最好的节点作为主节点
    print("接收到任务请求")
    # 向127.0.0.1:5000/election/vote发送选举请求
    # requests.get('http://127.0.0.1:5079/election/vote')
    requests.get('http://172.16.238.12:5078/election/vote')
    print("发送选举")
    node = Node.query.first()

    data = {
        'is_leader': node.is_leader,
        'network_status': node.network_status,
        'task_type': node.task_type,
        'load': node.load,
        'node_id': node.node_id,
        'update_method': node.update_method
    }

    return "Start response"



@election_blueprint.route('/vote', methods=['GET', 'POST'])
def vote():
    # 实现主节点选举逻辑
    print("接收到选举请求1")
    # node = Node.query.first()
    return "Election response"


@election_blueprint.route('/heartbeat', methods=['GET', 'POST'])
def heartbeat():
    # TODO 实现心跳检测逻辑
    return "Heartbeat response"
