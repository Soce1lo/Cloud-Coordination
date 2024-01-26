import json
import threading
import time

import requests
from flask import Flask, jsonify, request
from config import Config, setup_logging
from master_election.election import election_blueprint
from task_scheduling.scheduler import scheduler_blueprint
from task_distribution.distribution import distribution_blueprint
from sync_update.sync import sync_blueprint
from network_monitoring.network import network_blueprint

# from config import Config
from models import db, Node

app = Flask(__name__)
# 设置日志
logger = setup_logging()

app.config.from_object(Config)

db.init_app(app)

# 注册各个模块的蓝图
app.register_blueprint(election_blueprint, url_prefix='/election')
app.register_blueprint(scheduler_blueprint, url_prefix='/scheduler')
app.register_blueprint(distribution_blueprint, url_prefix='/distribution')
app.register_blueprint(sync_blueprint, url_prefix='/sync')
app.register_blueprint(network_blueprint, url_prefix='/network')


# 从config.py文件中读取配置信息
# app.config.from_object(Config)
def create_or_get_node():
    with app.app_context():
        db.create_all()  # 创建表
        node = Node.query.first()  # 获取第一个 Node 记录
        if node is None:  # 如果不存在，则创建一个
            with open('initial_node.json', 'r') as file:
                data = json.load(file)
                node = Node(
                    is_leader=data['is_leader'],
                    network_status=data['network_status'],
                    task_type=data['task_type'],
                    load=data['load'],
                    node_id=data['node_id'],
                    update_method=data['update_method']
                )
                db.session.add(node)
                db.session.commit()
        else:  # 如果存在，则更新json文件
            with open('initial_node.json', 'w') as file:
                json.dump(node.to_dict(), file)
    logger.info("数据库更新完成")


@app.route('/')
def hello_world():
    logger.info("logger test")
    # app.logger.info("app logger test")
    return 'Hello!'


def update_node_properties(update_data):
    node = Node.query.first()
    if node:
        for key, value in update_data.items():
            if hasattr(node, key):
                setattr(node, key, value)
        db.session.commit()
        return True
    return False


# 动态修改节点属性
@app.route('/update_node', methods=['POST'])
def update_node():
    data = request.json
    success = update_node_properties(data)
    if success:
        return jsonify({"message": "Node updated successfully"}), 200
    else:
        return jsonify({"error": "Node not found"}), 404


# 注册路由接口为get_node
@app.route('/get_node', methods=['GET'])
def get_node():
    logger.info("收到get_node请求")
    node = Node.query.first()
    if node:
        return jsonify(node.to_dict()), 200
    else:
        return jsonify({"error": "Node not found"}), 404


@app.route('/task_start', methods=['GET'])
def task_start():
    logger.info("开始主持训练任务")
    requests.get("http://172.16.238.11:5078/train")
    logger.info("向节点 %d 发送训练任务", 2)
    requests.get("http://172.16.238.12:5078/train")
    logger.info("向节点 %d 发送训练任务", 3)
    return jsonify({"message": "task started"}), 200

@app.route('/train', methods=['GET'])
def train():
    node = Node.query.first()
    logger.info("Node %d 开始训练", node.id)
    # 启动一个线程，模拟训练任务,并传递节点地址
    thread = threading.Thread(target=train_task, args=("http://172.16.238.10:5078/task_update", node.node_id, 3))
    thread.start()
    return jsonify({"message": "train started"}), 200

def train_task(address, id,epoche):
    for i in range(epoche):
        time.sleep(5)
        requests.get(address, json={"node_id": id})

@app.route('/task_update', methods=['GET'])
def task_update():
    logger.info("接收到来自节点 %d 的训练结果", request.json['node_id'])
    return jsonify({"message": "task updated"}), 200

if __name__ == "__main__":
    create_or_get_node()
    app.run(debug=True, host='0.0.0.0', port=5078)
