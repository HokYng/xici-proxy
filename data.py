import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn import datasets
from numpy import linalg as ln
from sklearn.linear_model import LinearRegression

# # 1、年龄与身高数据源
# age = np.loadtxt('ex2x.dat')
# high = np.loadtxt('ex2y.dat')
#
# figure = plt.figure('数据可视化', figsize=(5, 4))
# ax = figure.add_axes([0.1, 0.1, 0.8, 0.8], label='身高年龄')
#
# ax.set_xlim(left=1, right=10)
# ax.set_ylim(bottom=0, top=1.5)
# ax.set_xlabel('年龄')
# ax.set_ylabel('身高')
# ax.scatter(x=age, y=high, marker='.', color=(1, 0, 0, 1))
#
# figure.show()
# plt.show()
#
# # 2、鸢尾花数据源
# data, target = datasets.load_iris(return_X_y=True)
#
# figure = plt.figure('鸢尾花数据', figsize=(6, 4))
# ax = figure.add_axes([0.1, 0.1, 0.8, 0.8], label='鸢尾花')
#
# ax.set_xlabel('特征-1')
# ax.set_ylabel('特征-2')
# ax.scatter(x=data[0:50, 0], y=data[0:50, 1], marker='.', color=(1, 0, 0, 1), label='A类')
# ax.scatter(x=data[50:100, 0], y=data[50:100, 1], marker='x', color=(0, 1, 0, 1), label='B类')
# ax.scatter(x=data[100:150, 0], y=data[100:150, 1], marker='v', color=(1, 0, 1, 1), label='C类')
#
# ax.legend()
# figure.show()
# plt.show()

# # 1、身高年龄线性回归的numpy实现
#     # 准备数据
# X_DATA = np.loadtxt('ex2x.dat')
# Y_DATA = np.loadtxt('ex2y.dat')
#     # 改变形状(在上面的推导中，我们对x与X的定义是确定的，x是多元特征构成的行向量；X是多个样本构成的矩阵，其中每行是一个多元特征的样本)
# print(X_DATA.shape)
# X = np.zeros(shape=(X_DATA.shape[0], 2), dtype=np.float32)
# Y = Y_DATA.reshape(Y_DATA.shape[0], 1)
# X[:, 0] = X_DATA
# X[:, 1] = 1
#     # 训练
# w = np.matmul(X.T, X)
# w = ln.inv(w)
# w = np.matmul(w, X.T)
# W = np.matmul(w, Y)
# print(W.shape)
# print(W)
#     # 可视化
# figure = plt.figure('身高年龄可视化', figsize=(8, 4))
# ax = figure.add_axes([0.1, 0.1, 0.8, 0.8], label='年龄与身高')
# ax.set_xlim(left=1, right=10)
# ax.set_ylim(bottom=0, top=1.5)
# ax.set_xlabel('年龄')
# ax.set_ylabel('身高')
# ax.scatter(x=X_DATA, y=Y_DATA, marker='.', color=(1, 0, 0, 1), label='样本')
#
# y = np.matmul(X, W)
# ax.plot(X_DATA, y, color=(0, 1, 0, 1), label='线性回归')
#
# ax.legend()
# figure.show()
# plt.show()

# # 2、身高年龄线性回归的sklearn实现
# X_DATA = np.loadtxt('ex2x.dat')
# Y_DATA = np.loadtxt('ex2y.dat')
#
# regression = LinearRegression()# 线性回归对象
#
# # 训练(拟合fit)
# # 数据格式整理
# # 如果是一维特征，使用reshape处理单特征形状（-1, 1），如果只有一个样本，形状reshape(1,-1)
# X_RG = X_DATA.reshape(-1, 1)
# Y_RG = Y_DATA
#
# regression.fit(X_RG, Y_RG)
# print('评估', regression.score(X_RG, Y_RG))
# print('斜率', regression.coef_)
# print('截距', regression.intercept_)
#
# # 可视化
# figure = plt.figure('sklearn数据可视化', figsize=(8, 4))
# ax = figure.add_axes([0.1, 0.1, 0.8, 0.8], label='sklearn实现')
# ax.set_xlim(left=1, right=10)
# ax.set_ylim(bottom=0, top=1.5)
# ax.set_xlabel('年龄')
# ax.set_ylabel('身高')
# ax.scatter(x=X_DATA, y=Y_DATA, marker='.', color=(1, 0, 0, 1), label='样本数据')
#
# y = regression.predict(X_RG)
# ax.plot(X_DATA, y, color=(0, 1, 0, 1), label='线性回归')
# ax.legend()
# figure.show()
# plt.show()

# # 1、鸢尾花数据线性回归numpy实现
# X_DATA, Y_DATA = datasets.load_iris(return_X_y=True)
# X_DATA = X_DATA[0:100, :]
# Y_DATA = Y_DATA[0:100]
# X = np.zeros(shape=(X_DATA.shape[0], X_DATA.shape[1]+1), dtype=np.float32)
# Y = Y_DATA.reshape(Y_DATA.shape[0], 1)
# X[:, 0:X_DATA.shape[1]] = X_DATA
# X[:, X_DATA.shape[1]] = 1
# data = np.matmul(X.T, X)
# b = ln.inv(data)
# a = np.matmul(b, X.T)
# W = np.matmul(a, Y)

# # 2、鸢尾花数据分类
# X_DATA, Y_DATA = datasets.load_iris(return_X_y=True)
# X_DATA = X_DATA[0:100]
# Y_DATA = Y_DATA[0:100]
#
# regression = LinearRegression()
# regression.fit(X_DATA, Y_DATA)
# print('评估', regression.score(X_DATA, Y_DATA))
# print('斜率', regression.coef_)
# print('截距', regression.intercept_)
#
# pre = regression.predict(X_DATA)
#
# cls_a = pre[0:50]
# cls_a = cls_a < 0.1
# a_num = cls_a.sum()
# print('A类识别正确数: {}; A类正确率: {}'.format(a_num, 100.0*a_num/50))
#
# cls_b = pre[50:100]
# cls_b = cls_b > 0.9
# b_num = cls_b.sum()
# print('B类识别正确数: {}; B类正确率: {}'.format(b_num, 100.0*b_num/50))

# 1、波士顿房价的sklearn实现
X_DATA, Y_DATA = datasets.load_boston(return_X_y=True)
