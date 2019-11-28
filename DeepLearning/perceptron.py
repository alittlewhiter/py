
from __future__ import print_function
from functools import reduce

class VectorOp(object):
    # 实现向量计算操作
    @staticmethod
    def dot(x, y):
        # 计算两个向量的内积
        return reduce(lambda a, b:a+b, VectorOp.element_multiply(x, y), 0.0)

    @staticmethod
    def element_multiply(x, y):
        # 将两个向量按元素配对打包，利用map函数计算内积
        return list(map(lambda x_y: x_y[0] * x_y[1], zip(x, y)))

    def element_add(x, y):
        return list(map(lambda x_y: x_y[0] + x_y[1], zip(x, y)))

    def scala_multiply(v, s):
        return map(lambda e: e * s, v)

class Perceptron(object):
    # 初始化感知器，设置输入参数个数，以及激活函数(类型为double->double)
    def __init__(self, input_num, activator):
        self.activator = activator
        self.weights = [0.0] * input_num;   # 权重向量初始化为0.0
        self.bias = 0.0         # 偏置项置为0.0

    # print the weights and bias that has learned
    def __str__(self):  
        return 'weights\t:%s\nbias\t:%f\n'%(self.weights, self.bias)

    # 输入向量，输出感知器的计算结果
    def predict(self, input_vec):
        return self.activator(
            VectorOp.dot(input_vec, self.weights)+self.bias)
    
    
    # 一次迭代过程，把所有训练数据过一遍
    def _one_iteration(self, input_vecs, labels, rate):
        # 输入输出打包在一起成为样本列表[(input_vecs, labels)...]
        samples = zip(input_vecs, labels)
        # 对每个样本按照感知器规则更新权重
        for (iv, lb) in samples:
            output = self.predict(iv)   # 计算感知器在当前权重下的输出
            self._update_weights(iv, output, lb, rate)  # 更新权重

    # 按感知器规则更新权重
    def _update_weights(self, input_vec, output, label, rate):
        delta = label - output      # 计算此时输出与标签的delta值
        self.weights = VectorOp.element_add(self.weights,
                                            VectorOp.scala_multiply(input_vec, rate*delta))
        self.bias += rate * delta;  # 更新bias

    # 训练函数，输入训练数据：一组向量、对应的label，训练轮数，学习率
    def train(self, input_vecs, labels, iteration, rate):
        for i in range(iteration):
            self._one_iteration(input_vecs, labels, rate)
    

# 定义激活函数f
def f(x):
    return 1 if x>0 else 0

# 基于&&真值表构建训练数据
def get_training_data():
    input_vecs = [[0,0], [0,1], [1,0], [1,1]]
    labels = [0, 0, 0, 1]       # 与输入一一对应的真值
    return input_vecs, labels

# 使用and真值表训练感知器
def train_and_perceptron():
    pct = Perceptron(2, f)
    input_vecs, labels = get_training_data()
    # 迭代10次，学习率为0.1
    pct.train(input_vecs, labels, 10, 0.1)  # 这里逻辑简单，5次即可收敛    
    # pct.train(input_vecs, labels, 20, 0.05)
    return pct      # 返回训练完成的感知器模型

if __name__ == '__main__':
    and_perceptron = train_and_perceptron() # 训练and感知器模型
    print(and_perceptron)

    print('0 and 0 = %d'%and_perceptron.predict([0,0]))
    print('0 and 1 = %d'%and_perceptron.predict([0,1]))
    print('1 and 0 = %d'%and_perceptron.predict([1,0]))
    print('1 and 1 = %d'%and_perceptron.predict([1,1]))



    

        
