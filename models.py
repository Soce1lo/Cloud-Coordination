from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Node(db.Model):
    __tablename__ = 'nodes'

    # 节点ID
    id = db.Column(db.Integer, primary_key=True)

    # 是否是领导者 bool类型
    is_leader = db.Column(db.Boolean, nullable=True)

    # 网络状态 float类型 0-1
    network_status = db.Column(db.Float, nullable=False)

    # 任务类型
    task_type = db.Column(db.String(80), nullable=False)

    # 负载
    # 计算状态 存储状态 etc
    load = db.Column(db.Float, nullable=False)

    # 节点ID
    node_id = db.Column(db.Integer, unique=True, nullable=False)

    # 更新方式
    update_method = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'is_leader': self.is_leader,
            'network_status': self.network_status,
            'task_type': self.task_type,
            'load': self.load,
            'node_id': self.node_id,
            'update_method': self.update_method
        }


class Node_state(db.Model):
    __tablename__ = 'node_state'
    # 节点ID 主键
    id = db.Column(db.Integer, primary_key=True)

    # 网络状态 float类型 0-1
    network_status = db.Column(db.Float, nullable=False)

    # 任务类型
    task_type = db.Column(db.String(80), nullable=False)

    # 负载
    # 计算状态 存储状态 etc
    load = db.Column(db.Float, nullable=False)

    # 更新方式
    update_method = db.Column(db.String(80), nullable=False)
