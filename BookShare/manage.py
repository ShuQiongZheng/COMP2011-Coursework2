from app import app, db
from flask_script import Manager

from flask_migrate import Migrate, MigrateCommand

from logging.handlers import TimedRotatingFileHandler
import logging

manager = Manager(app)
Migrate(app, db)
manager.add_command("db", MigrateCommand)

# the entrance of the whole project
if __name__ == '__main__':
    app.debug = True
    formatter = logging.Formatter("[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s][%(thread)d] - %(message)s")
    handler = TimedRotatingFileHandler("flask.log", when="D", interval=1, backupCount=15, encoding="UTF-8", delay=False, utc=True)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)

    app.run()
