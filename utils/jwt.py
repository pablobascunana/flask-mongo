import logging

from utils.responses import unauthorized


def create_token_callbacks(jwt):

    @jwt.expired_token_loader
    def expired_token_callback():
        logging.error("The token has expired")
        return unauthorized({
            'description': 'The token has expired.',
            'error': 'expired_token'
        })

    @jwt.invalid_token_loader
    def invalid_token_callback():
        logging.error("Signature verification failed")
        return unauthorized({
            'description': 'Signature verification failed.',
            'error': 'token_invalid'
        })

    @jwt.unauthorized_loader
    def unauthorized_callback():
        logging.error("Request does not contain an access token")
        return unauthorized({
            'description': 'Request does not contain an access token.',
            'error': 'authorization_required'
        })

    @jwt.needs_fresh_token_loader
    def needs_fresh_token_callback():
        logging.error("The token is not fresh")
        return unauthorized({
            'description': 'The token is not fresh.',
            'error': 'fresh_token_required'
        })
