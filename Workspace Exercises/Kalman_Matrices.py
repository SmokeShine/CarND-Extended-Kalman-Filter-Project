# Write a function 'kalman_filter' that implements a multi-
# dimensional Kalman Filter for the example given

import argparse
import ast
import logging
import os
from datetime import datetime
import pdb
from math import *

#Initializing list of global variables
measurements=None 
u=None
F=None
H=None
R=None
I=None

class matrix:
    
    # implements basic operations of a matrix class
    
    def __init__(self, value):
        self.value = value
        self.dimx = len(value)
        self.dimy = len(value[0])
        if value == [[]]:
            self.dimx = 0
    
    def zero(self, dimx, dimy):
        # check if valid dimensions
        if dimx < 1 or dimy < 1:
            raise ValueError("Invalid size of matrix")
        else:
            self.dimx = dimx
            self.dimy = dimy
            self.value = [[0 for row in range(dimy)] for col in range(dimx)]
    
    def identity(self, dim):
        # check if valid dimension
        if dim < 1:
            raise ValueError("Invalid size of matrix")
        else:
            self.dimx = dim
            self.dimy = dim
            self.value = [[0 for row in range(dim)] for col in range(dim)]
            for i in range(dim):
                self.value[i][i] = 1
    
    def show(self):
        for i in range(self.dimx):
            print(self.value[i])
        print(' ')
    
    def __add__(self, other):
        # check if correct dimensions
        if self.dimx != other.dimx or self.dimy != other.dimy:
            raise ValueError("Matrices must be of equal dimensions to add")
        else:
            # add if correct dimensions
            res = matrix([[]])
            res.zero(self.dimx, self.dimy)
            for i in range(self.dimx):
                for j in range(self.dimy):
                    res.value[i][j] = self.value[i][j] + other.value[i][j]
            return res
    
    def __sub__(self, other):
        # check if correct dimensions
        if self.dimx != other.dimx or self.dimy != other.dimy:
            raise ValueError("Matrices must be of equal dimensions to subtract")
        else:
            # subtract if correct dimensions
            res = matrix([[]])
            res.zero(self.dimx, self.dimy)
            for i in range(self.dimx):
                for j in range(self.dimy):
                    res.value[i][j] = self.value[i][j] - other.value[i][j]
            return res
    
    def __mul__(self, other):
        # check if correct dimensions
        if self.dimy != other.dimx:
            raise ValueError("Matrices must be m*n and n*p to multiply")
        else:
            # multiply if correct dimensions
            res = matrix([[]])
            res.zero(self.dimx, other.dimy)
            for i in range(self.dimx):
                for j in range(other.dimy):
                    for k in range(self.dimy):
                        res.value[i][j] += self.value[i][k] * other.value[k][j]
            return res
    
    def transpose(self):
        # compute transpose
        res = matrix([[]])
        res.zero(self.dimy, self.dimx)
        for i in range(self.dimx):
            for j in range(self.dimy):
                res.value[j][i] = self.value[i][j]
        return res
    
    # Thanks to Ernesto P. Adorio for use of Cholesky and CholeskyInverse functions
    
    def Cholesky(self, ztol=1.0e-5):
        # Computes the upper triangular Cholesky factorization of
        # a positive definite matrix.
        res = matrix([[]])
        res.zero(self.dimx, self.dimx)
        
        for i in range(self.dimx):
            S = sum([(res.value[k][i])**2 for k in range(i)])
            d = self.value[i][i] - S
            if abs(d) < ztol:
                res.value[i][i] = 0.0
            else:
                if d < 0.0:
                    raise ValueError("Matrix not positive-definite")
                res.value[i][i] = sqrt(d)
            for j in range(i+1, self.dimx):
                S = sum([res.value[k][i] * res.value[k][j] for k in range(self.dimx)])
                if abs(S) < ztol:
                    S = 0.0
                try:
                   res.value[i][j] = (self.value[i][j] - S)/res.value[i][i]
                except:
                   raise ValueError("Zero diagonal")
        return res
    
    def CholeskyInverse(self):
        # Computes inverse of matrix given its Cholesky upper Triangular
        # decomposition of matrix.
        res = matrix([[]])
        res.zero(self.dimx, self.dimx)
        
#         # Backward step for inverse.
        for j in reversed(range(self.dimx)):
            tjj = self.value[j][j]
            S = sum([self.value[j][k]*res.value[j][k] for k in range(j+1, self.dimx)])
            res.value[j][j] = 1.0/tjj**2 - S/tjj
            for i in reversed(range(j)):
                res.value[j][i] = res.value[i][j] = -sum([self.value[i][k]*res.value[k][j] for k in range(i+1, self.dimx)])/self.value[i][i]
        return res
    
    def inverse(self):
        aux = self.Cholesky()
        res = aux.CholeskyInverse()
        return res
    
    def __repr__(self):
        return repr(self.value)


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
    parser.add_argument('--measurements', nargs='?', default='[1,2,3]',
                        help='Input Measurements')
    parser.add_argument('--x', nargs='?', default='[[0.], [0.]]',
                        help='initial state (location and velocity)')
    parser.add_argument('--P', nargs='?', default='[[1000., 0.], [0., 1000.]]',
                        help='initial uncertainty (location and velocity)')
    parser.add_argument('--u', nargs='?', default='[[0.], [0.]]',
                        help='external motion')
    parser.add_argument('--F', nargs='?', default='[[1., 1.], [0, 1.]]',
                        help='next state function - x+v.t -both location and velocity')
    parser.add_argument('--H', nargs='?', default='[[1., 0.]]',
                        help='measurement function - only location')
    parser.add_argument('--R', nargs='?', default='[[1.]]',
                        help='measurement uncertainty')
    parser.add_argument('--I', nargs='?', default='[[1., 0.], [0., 1.]]',
                        help='identity matrix')
    parser.add_argument('--log_dir', nargs='?', default='logs',
                        help='Input Log Directory')
    parser.add_argument('--log_file', nargs='?', default='log_default',
                        help='Input Filename for Log File')
    return parser.parse_args()
    
def predict(x,P):
    '''
    Prediction based on laws of motion
    '''
    logging.info("Predict Output {} {}".format(F*x+u, F*P*F.transpose()))
    return [F*x+u, F*P*F.transpose()]

def update(x,P,Z):
    '''
    Measurement Update
    '''
    global u
    global F
    global H
    global R
    global I
    y=Z-(H*x) # y is deviation from the measurement / error
    S=H*P*H.transpose()+R
    K=P*H.transpose()*S.inverse()
    logging.info("Measurement Update Output {} {}".format(x+K*y, (I-K*H)*P))
    return [x+K*y, (I-K*H)*P]

def update_predict(x,P):
    global measurements 
    global u
    global F
    global H
    global R
    global I
    for i,Z in enumerate(measurements):

        x, P=update(x,P,matrix([[Z]]))
        x, P=predict(x,P)        
    return [x, P]
    
    
########################################

# Implement the filter function below

if __name__ == '__main__':
    args = parse_args()
    log_dir = args.log_dir
    log_file = args.log_file
    init_logging(log_dir,log_file)
    logging.info("**"*10)
    logging.info(args.__dict__)
    logging.info("**"*10)
    # literal eval for converting string to float
    x=matrix(ast.literal_eval(args.x))
    P=matrix(ast.literal_eval(args.P))

    measurements=ast.literal_eval(args.measurements)
    u=matrix(ast.literal_eval(args.u))
    F=matrix(ast.literal_eval(args.F))
    H=matrix(ast.literal_eval(args.H))
    R=matrix(ast.literal_eval(args.R))
    I=matrix(ast.literal_eval(args.I))
    # Keeping x and P as local variables
    finalx,finalp=update_predict(x,P)
    logging.info("x:{}".format(finalx))
    logging.info("p:{}".format(finalp))    
    logging.info("Finished")

############################################
### use the code below to test your filter!
############################################

# measurements = [1, 2, 3]

# x = matrix([[0.], [0.]]) # initial state (location and velocity)
# P = matrix([[1000., 0.], [0., 1000.]]) # initial uncertainty
# u = matrix([[0.], [0.]]) # external motion
# F = matrix([[1., 1.], [0, 1.]]) # next state function
# H = matrix([[1., 0.]]) # measurement function
# R = matrix([[1.]]) # measurement uncertainty
# I = matrix([[1., 0.], [0., 1.]]) # identity matrix

# print(kalman_filter(x, P))
# # output should be:
# # x: [[3.9996664447958645], [0.9999998335552873]]
# # P: [[2.3318904241194827, 0.9991676099921091], [0.9991676099921067, 0.49950058263974184]]
