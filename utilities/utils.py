import inspect
import logging
import softest


class Utils(softest.TestCase):
    def custom_logger(loglevel=logging.DEBUG):
        #To set class/method name from where its called
        logger_name = inspect.stack()[1][3]

        # Create logger and set log level
        logger = logging.getLogger(logger_name)
        logger.setLevel(loglevel)

        # Creating Console Handler
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s  : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        ch.setFormatter(formatter)

        # Creating File Handler
        fh = logging.FileHandler('logs/test_logs.log')
        fh.setFormatter(formatter)

        # Add Handlers to logger
        logger.addHandler(ch)
        logger.addHandler(fh)
        return logger

    def compare_and_verify(self, expected_data, actual_data):
        if expected_data in str(actual_data):
            print('Verified the data is matching as expected')
        else:
            assert 0, 'Found there are mismatches between the expected and actual data'
