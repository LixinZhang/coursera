#!/usr/bin/python
#!encoding:utf-8
'''
一元函数的梯度下降算法
不断迭代直到收敛
'''
import matplotlib
import matplotlib.pyplot as plt

def showPic(x, y, theta0, theta1) :
    matplotlib.rcParams['axes.unicode_minus'] = False
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x,y,'o')
    ax.set_title('test from zhanglixin')
    ax.plot([0,theta0],[1,theta0+theta1])
    plt.show()

def training() :
    x = [float(item) for item in open('ex2x.dat')]
    y = [float(item) for item in open('ex2y.dat')]

    size = len(x)

    theta0 = 0
    theta1 = 0 
    alpha = 0.07

    xy = zip(x,y)

    for i in range(10000) :
        theta0_temp = theta0 - sum([theta0 + theta1 * xitem - yitem for xitem,yitem in xy]) / size * alpha
        theta1_temp = theta1 - sum([(theta0 + theta1 * xitem - yitem) * xitem for xitem,yitem in xy]) / size * alpha
        if abs(theta0_temp - theta0) <= 0.00000001 and abs(theta1_temp - theta1) <= 0.00000001 :
            break;
        theta0 = theta0_temp
        theta1 = theta1_temp
        if i % 30 == 0 :
            print theta0, theta1

    showPic(x,y,theta0,theta1)
    return (theta0, theta1)

theta0, theta1 = training()

def testing(x) :
    return theta0 + theta1 * x

if __name__ == '__main__' :
    
    while(1) :
        x = raw_input('Please input float x :')
        print testing(float(x))

