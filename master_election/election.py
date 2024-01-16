import logging
import socket

import requests
from flask import Blueprint
from models import db, Node, Node_state

election_blueprint = Blueprint('election', __name__)

logger = logging.getLogger('my_logger')


@election_blueprint.route('/')
# 开始进行任务
def start():
    # TODO 实现开始任务逻辑
    # 请求其他节点的状态信息
    # 向多个ip发送请求，获取响应
    # 选取网络状态最好的节点作为主节点
    logger.info("接收到任务请求")
    # 向127.0.0.1:5000/election/vote发送选举请求
    # requests.get('http://127.0.0.1:5079/election/vote')
    # requests.get('http://172.16.238.12:5078/election/vote')
    election()

    return "Start"


def election():
    # 访问get_node 接口 获取json数据
    response = requests.get('http://172.16.238.11:5078/get_node')
    response = response.json()
    update_node_state(response)
    response = requests.get('http://172.16.238.12:5078/get_node')
    response = response.json()
    update_node_state(response)
    logger.info("更新节点状态")
    # 比较网络状态，选取网络状态最好的节点作为主节点
    # TODO 选取网络状态最好的节点作为主节点
    # 查询Node_state表的所有记录，并按照network_status字段进行升序排序
    node_states = Node_state.query.order_by(Node_state.network_status).all()
    # 选取网络状态最小的记录
    min_network_status_node = node_states[0]
    # 更新Node表中的is_leader字段
    node = Node.query.first()
    if node.network_status < min_network_status_node.network_status:
        node.is_leader = True
        db.session.commit()
        logger.info("指定Node %d 为主节点", node.id)
    else:
        # 指定网络状态最小的节点为主节点
        logger.info("指定Node %d 为主节点", min_network_status_node.id)


def train():
    # TODO 实现训练逻辑

    return "Train"

def update_node_state(response):
    # 将json数据保存到数据库 node_state表中
    # 查询 node_id = response.node_id 的记录并返回
    node_state = Node_state.query.filter_by(id=response['node_id']).first()
    logger.info("Update node %d state", response['node_id'])
    # 如果已经存在，则更新记录
    if node_state is not None:
        node_state.network_status = response['network_status']
        node_state.task_type = response['task_type']
        node_state.load = response['load']
        node_state.update_method = response['update_method']
    else:
        node_state = Node_state(
            id=response['node_id'],
            network_status=response['network_status'],
            task_type=response['task_type'],
            load=response['load'],
            update_method=response['update_method']
        )
        db.session.add(node_state)
        db.session.commit()


def get_container_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


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
