from flask import Flask

from master_election.election import election_blueprint
from task_scheduling.scheduler import scheduler_blueprint
from task_distribution.distribution import distribution_blueprint
from sync_update.sync import sync_blueprint
from network_monitoring.network import network_blueprint

app = Flask(__name__)

# 注册各个模块的蓝图
app.register_blueprint(election_blueprint, url_prefix='/election')
app.register_blueprint(scheduler_blueprint, url_prefix='/scheduler')
app.register_blueprint(distribution_blueprint, url_prefix='/distribution')
app.register_blueprint(sync_blueprint, url_prefix='/sync')
app.register_blueprint(network_blueprint, url_prefix='/network')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5078)
