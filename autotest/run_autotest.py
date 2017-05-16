__author__ = 'lmxiang'

import unittest
import os,sys, time, logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import coverage, configparser
from autotest.lib.test_utils import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
time_start = time.strftime("%Y%m%d-%H%M%S")

variables = {}
test_results = {}
vpc_names = []

args = args_parser()
#config_parser(args.config.name, variables)
config = configparser.ConfigParser()
config.read(args.config)
cloud_account_file = "testdata\\cloud_account"
cloud_account = configparser.ConfigParser()
cloud_account.read(cloud_account_file)


def generate_test_list(tests2run):
    if tests2run is '':
        logger.error("No tests to run. Abort.")
        return None
    else:
        input_list = tests2run.split(',')
        [__import__(x) for x in input_list]
        test_list = unittest.TestSuite()
        for scenario in [sys.modules[x] for x in input_list]:
            test_list.addTest(loader.loadTestsFromModule(scenario))
        return test_list

report_file_name = args.userID + "_" + time_start + ".txt"
zip_file_name = args.userID + "_" + time_start + ".zip"
json_file_name = args.userID + "_" + time_start + ".json"
result_file_name = args.userID + "_" + time_start + "_result" + ".txt"

report_file = "results\\temp\\" + report_file_name
zip_file = "results\\" + zip_file_name
json_file = "results\\temp\\" + json_file_name
result_file = "results\\temp\\" + result_file_name

_COVERAGE_DIR_NAME = '.cov_all'
if __name__ == '__main__':

    if not os.path.exists(os.path.dirname(report_file)):
        os.makedirs(os.path.dirname(report_file))

    report_file_abs = os.path.abspath(report_file)
    zip_file_abs = os.path.abspath(zip_file)

    # clear up the files left in temp directory
    directory_clearer(os.path.dirname(report_file_abs))

    # create logger with 'main'
    logger = logging.getLogger("autotest")
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler(report_file)
    fh.setLevel(logging.DEBUG)

    # create console handler which also logs debug messages
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    cov = coverage.Coverage(branch=True, config_file=False)
    current_dir = os.getcwd()
    cov_dir = os.path.sep.join((current_dir, _COVERAGE_DIR_NAME))
    if os.path.exists(cov_dir):
        shutil.rmtree(cov_dir)
    cov.erase()
    cov.start()

    loader = unittest.TestLoader()
    if args.cloud_type.lower() == 'azure':
        suite = generate_test_list(config['azure_tests']['suite'])
    elif args.cloud_type.lower() == 'gcloud':
        suite = generate_test_list(config['gcloud_tests']['suite'])
    else:
        suite = generate_test_list(config['aws_tests']['suite'])

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    cov.stop()
    cov.html_report(directory=cov_dir)

    time_stop = time.strftime("%Y%m%d-%H%M%S")

    report_writer(report_file, result, time_start, time_stop)

    result_printer(json_file, result_file)

    logger.debug("zip creator zip file is " + zip_file_abs)
    logger.debug("zip_creator dir is " + os.path.dirname(report_file_abs))

    zip_creator(zip_file_abs, os.path.dirname(report_file_abs))
    #upload_result(zip_file_abs)
    #notify_user(zip_file_abs, result, time_start, time_stop)
