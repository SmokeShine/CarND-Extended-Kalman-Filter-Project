#include <iostream>
#include <vector>
#include "Eigen/Dense"

using Eigen::MatrixXd;
using Eigen::VectorXd;
using std::cout;
using std::endl;

MatrixXd CalculateJacobian(const VectorXd& x_state);

int main() {
    /**
     * Compute the Jacobian Matrix
     */
    
    // predicted state example
    // px = 1, py = 2, vx = 0.2, vy = 0.4
    VectorXd x_predicted(4);
    x_predicted << 1, 2, 0.2, 0.4;
    
    MatrixXd Hj = CalculateJacobian(x_predicted);
    
    cout << "Hj:" << endl << Hj << endl;
    
    return 0;
}

MatrixXd CalculateJacobian(const VectorXd& x_state) {
    
    MatrixXd Hj(3,4);
    float px = x_state(0);
    float py = x_state(1);
    float vx = x_state(2);
    float vy = x_state(3);
    float px2=pow(px,2);
    float py2=pow(py,2);
    float px2y2=px2+py2;
    // TODO: YOUR CODE HERE
    
    // check division by zero
    if (px+py==0){
        Hj<<0,0,0,0,
        0,0,0,0,0,
        0,0,0,0,
        0,0,0,0;
    }
    // compute the Jacobian matrix
    
    
    
    
    Hj<<px/pow(px2y2,0.5),py/pow(px2y2,0.5),0,0,
    -py/px2y2,px/px2y2,0,0,
    py*(vx*py-vy*px)/pow(px2y2,1.5),
    px*(vx*py-vy*px)/pow(px2y2,1.5),
    px/pow(px2y2,0.5),
    py/pow(px2y2,0.5);
    return Hj;
}
