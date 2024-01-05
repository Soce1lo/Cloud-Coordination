from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Node(db.Model):
    __tablename__ = 'nodes'

    # 节点ID
    id = db.Column(db.Integer, primary_key=True)
    # 网络状态
    network_status = db.Column(db.String(80), nullable=False)
    # 任务类型
    task_type = db.Column(db.String(80), nullable=False)
    # 负载
    load = db.Column(db.Float, nullable=False)
    # 节点ID
    node_id = db.Column(db.String(80), unique=True, nullable=False)
    # 更新方式
    update_method = db.Column(db.String(80), nullable=False)


    def to_dict(self):
        return {
            'id': self.id,
            'network_status': self.network_status,
            'task_type': self.task_type,
            'load': self.load,
            'node_id': self.node_id,
            'update_method': self.update_method
        }

