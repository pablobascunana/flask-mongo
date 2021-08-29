SWAGGER_CONFIG = {
    "swagger_version": "2.0",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
    "specs": [
        {
            "version": "0.0.1",
            "title": "Flask-MongoDB status API",
            "description": "Example of Restful API with MongoDB",
            "endpoint": "/",
            "route": "/",
            "termsOfService": ""
        }
    ]
}
