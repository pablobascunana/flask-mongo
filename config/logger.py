import logging.config
import os

path = os.path.join(os.getcwd(), 'log')
if not os.path.exists(path):
    os.makedirs(path)

log_filename = os.path.join(path, 'logging.log')

if 'development' in os.getenv('FLASK_ENV'):
    log_mode = 'console'
else:
    log_mode = 'rotate_file'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(asctime)s - %(levelname)-1s: %(name)s - %(filename)s:%(lineno)d -> %(message)s',
            'datefmt': '%d-%m-%Y %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
        'rotate_file': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': log_filename,
            'encoding': 'utf8',
            'maxBytes': 50000000,
            'backupCount': 20,
        }
    },
    'root': {
        'handlers': [log_mode],
        'level': 'DEBUG',
    }
}
logging.config.dictConfig(LOGGING)
