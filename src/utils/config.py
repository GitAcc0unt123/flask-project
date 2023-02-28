import yaml
import os

from dotenv import load_dotenv


class Config():
    def __init__(self, path_yaml, path_env=None):

        with open(path_yaml, 'r') as file:
            config = yaml.safe_load(file)

        self.flask = config['flask']

        if path_env != None and os.path.exists(path_env):
            load_dotenv(path_env)

        self.flask['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
        self.flask['SQLALCHEMY_TEST_DATABASE_URI'] = os.environ['SQLALCHEMY_TEST_DATABASE_URI']
        self.flask['SECRET_KEY'] = os.environ['SECRET_KEY']
        self.flask['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']
        self.flask['DEBUG'] = True
