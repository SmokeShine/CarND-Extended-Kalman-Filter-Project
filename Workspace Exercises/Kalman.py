import argparse
import ast
import logging
import os
from datetime import datetime

def init_logging(log_dir,log_file):
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)

    date_str = datetime.now().strftime('%Y-%m-%d_%H-%M')
    log_file = 'log_{}.txt'.format(date_str)
    logging.basicConfig(
        filename=os.path.join(log_dir, log_file),
        level=logging.INFO,
        format='[[%(asctime)s]] %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    logging.getLogger().addHandler(logging.StreamHandler())

def parse_args():
    parser = argparse.ArgumentParser(description="usage: python Kalman.py --mean1 10. --var1 4. --mean2 12. --var2 4. ")

    parser.add_argument('--mean1', nargs='?', default='1.0',
                        help='Input Mean for 1st Distribution.')
    parser.add_argument('--var1', nargs='?', default='1.0',
                        help='Input Variance for 2nd Distribution.')
    parser.add_argument('--mean2', nargs='?', default='1.0',
                        help='Input Mean for 1st Distribution.')
    parser.add_argument('--var2', nargs='?', default='1.0',
                        help='Input Variance for 2nd Distribution.')
    parser.add_argument('--log_dir', nargs='?', default='logs',
                        help='Input Log Directory')
    parser.add_argument('--log_file', nargs='?', default='log_default',
                        help='Input Filename for Log File')
    return parser.parse_args()
    
def update(mean1, var1, mean2, var2):
    new_mean = (var2 * mean1 + var1 * mean2) / (var1 + var2)
    new_var = 1/(1/var1 + 1/var2)
    return [new_mean, new_var]

def predict(mean1, var1, mean2, var2):
    new_mean = mean1+mean2
    new_var = var1+var2
    return [new_mean, new_var]

if __name__ == '__main__':
    args = parse_args()
    log_dir = args.log_dir
    log_file = args.log_file
    init_logging(log_dir,log_file)
    # literal eval for converting string to float
    mean1 = ast.literal_eval(args.mean1)
    var1 = ast.literal_eval(args.var1)
    mean2 = ast.literal_eval(args.mean2)
    var2 = ast.literal_eval(args.var2)
    logging.info("mean1:{}  var1:{} mean2:{}  var2:{}"
                 .format(args.mean1, args.var1, args.mean2, args.var2))
    logging.info("Output of Update Function {}".format(update(mean1, var1, mean2, var2)))
    logging.info("Output of Predict Function {}".format(predict(mean1, var1, mean2, var2)))

#     python Kalman.py -h
# $ python Kalman.py --mean1 10. --var1 4. --mean2 12. --var2 4. 
# mean1:10.  var1:4. mean2:12.  var2:4.
# Output of Update Function [11.0, 2.0]
# Output of Predict Function [22.0, 8.0]
