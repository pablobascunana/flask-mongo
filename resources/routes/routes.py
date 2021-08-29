from resources.status import IsAlive, Version


def create_resources(api):
    api.add_resource(IsAlive, "/isalive")
    api.add_resource(Version, "/version")
