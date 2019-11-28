
from perceptron import Perceptron

# 定义激活函数f
f = lambda x: x

# 通过继承Perceptron，实现线性单元
class LinearUnit(Perceptron):
	def __init__(self, input_num):	# 初始化线性单元，设置输入参数的个数
		Perceptron.__init__(self, input_num, f):

# 模拟生成5个人的收入数据，用于训练输入
def get_training_data():
	input_vecs = [[5], [3], [8], [1.4], [10.1]]
	labels = [5500, 2300, 7600, 1800, 11400]
	return input_vecs, labels

# 使用数据开始训练线性单元，获取感知器
def train_linear_unit():
	lu = LinearUnit(1)		# 创建感知器，参数的特征数为 1，即一个考虑因素
	input_vecs, labels = get_training_data()
	# 开始训练，迭代10轮，学习速率为0.01
	lu.train(input_vecs, labels, 10, 0.01)
	return lu 			# 返回训练好的线性单元


if __name__ == '__main__':
	linear_unit = train_linear_unit()
	print(linear_unit)
	print('Work 3.4 years, monthly salary = %.2f'%linear_unit.predict([3.4]))
	print('Work 15 years, monthly salary = %.2f'%linear_unit.predict([15]))
	print('Work 1.5 years, monthly salary = %.2f'%linear_unit.predict([1.5]))
	print('Work 6.3 years, monthly salary = %.2f'%linear_unit.predict([6.3]))