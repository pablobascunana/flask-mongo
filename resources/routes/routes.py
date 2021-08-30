from resources.status import IsAlive, Version
from resources.user import Login, User

API_PATH = '/api/v1'


def create_resources(api):
    api.add_resource(IsAlive, "/isalive")
    api.add_resource(Version, "/version")
    api.add_resource(Login, API_PATH + "/login")
    api.add_resource(User, API_PATH + "/user")
