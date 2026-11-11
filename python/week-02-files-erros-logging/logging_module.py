import logging


def logger():
    """
    Configures the logging settings for the application.
    Logs messages to a file named 'app.log' with a specific format.
    """
logging.basicConfig(
    filename='app.log',
    level=logging.DEBUG,
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
