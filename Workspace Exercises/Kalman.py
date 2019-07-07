import argparse
import ast
import logging
import os
from datetime import datetime
import pdb

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

    parser.add_argument('--measurements', nargs='?', default='1.0',
                        help='Input Measurements.')
    parser.add_argument('--measurement_sig', nargs='?', default='1.0',
                        help='Input Variance for Measurements.')
    parser.add_argument('--motion', nargs='?', default='1.0',
                        help='Input Motion.')
    parser.add_argument('--motion_sig', nargs='?', default='1.0',
                        help='Input Variance for Motion.')
    parser.add_argument('--mu', nargs='?', default='1.0',
                        help='Input Mu.')
    parser.add_argument('--sigma', nargs='?', default='1.0',
                        help='Input Sigma')
    parser.add_argument('--log_dir', nargs='?', default='logs',
                        help='Input Log Directory')
    parser.add_argument('--log_file', nargs='?', default='log_default',
                        help='Input Filename for Log File')
    return parser.parse_args()
    
def update(mean1, var1, mean2, var2):
    new_mean = (var2 * mean1 + var1 * mean2) / (var1 + var2)
    new_var = 1/(1/var1 + 1/var2)
    logging.info("Output of Update Function {} {}".format(new_mean, new_var))
    return [new_mean, new_var]

def predict(mean1, var1, mean2, var2):
    new_mean = mean1+mean2
    new_var = var1+var2
    logging.info("Output of Predict Function {} {}".format(new_mean, new_var))
    return [new_mean, new_var]

def update_predict(mu,sigma,measurements,measurement_sig,motion,motion_sig):
    measurements=ast.literal_eval(measurements)
    motion=ast.literal_eval(motion)
    measurement_sig=ast.literal_eval(measurement_sig)
    motion_sig=ast.literal_eval(motion_sig)
    mu=ast.literal_eval(mu)
    sigma=ast.literal_eval(sigma)
    for i,_ in enumerate(measurements):
        new_mean, new_var=update(mu, sigma, measurements[i], measurement_sig)
        new_mean, new_var=predict(new_mean, new_var, motion[i], motion_sig)
        mu=new_mean
        sigma=new_var
    return [mu, sigma]

if __name__ == '__main__':
    args = parse_args()
    log_dir = args.log_dir
    log_file = args.log_file
    init_logging(log_dir,log_file)
    # literal eval for converting string to float
    logging.info(update_predict(args.mu,args.sigma,args.measurements,args.measurement_sig,args.motion,args.motion_sig))
    logging.info("Finished")

#     python Kalman.py -h
# python Kalman.py --measurements [5.,6.,7.,9.,10.] --measurement_sig 4. --motion [1.,1.,2.,1.,1.] --motion_sig 2. --mu 0.--sigma 10000.

# Output of Update Function 4.998000799680128 3.9984006397441023
# Output of Predict Function 5.998000799680128 5.998400639744102
# Output of Update Function 5.999200191953932 2.399744061425258
# Output of Predict Function 6.999200191953932 4.399744061425258
# Output of Update Function 6.999619127420922 2.0951800575117594
# Output of Predict Function 8.999619127420921 4.09518005751176
# Output of Update Function 8.999811802788143 2.0235152416216957
# Output of Predict Function 9.999811802788143 4.023515241621696
# Output of Update Function 9.999906177177365 2.0058615808441944
# Output of Predict Function 10.999906177177365 4.005861580844194
# [10.999906177177365, 4.005861580844194]
# Finished