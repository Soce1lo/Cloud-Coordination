import json
from flask import Flask

from master_election.election import election_blueprint
from task_scheduling.scheduler import scheduler_blueprint
from task_distribution.distribution import distribution_blueprint
from sync_update.sync import sync_blueprint
from network_monitoring.network import network_blueprint

# from config import Config
from models import db, Node

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///node_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

if __name__ == "__main__":
    create_or_get_node()
    app.run(debug=True, host='0.0.0.0', port=5078)
