import random
import math
import numpy  as np
import pandas as pd
import copy
# Shorthand:
# "pd_" as a variable prefix means "partial derivative"
# "d_" as a variable prefix means "derivative"
# "_wrt_" is shorthand for "with respect to"
# "w_ho" and "w_ih" are the index of weights from hidden to output layer neurons and input to hidden layer neurons respectively


class NeuralNetwork:
    LEARNING_RATE = 0.05

    def __init__(self, num_inputs, num_hidden, num_outputs, hidden_layer_weights=None, hidden_layer_bias=None, output_layer_weights=None, output_layer_bias=None):
        #Your Code Here
        self.num_in = num_inputs
        self.num_hid = num_hidden
        self.num_out = num_outputs
        self.hidden_layer = NeuronLayer(num_hidden, hidden_layer_bias)
        self.output_layer = NeuronLayer(num_outputs, output_layer_bias)
        self.init_weights_from_inputs_to_hidden_layer_neurons(
            hidden_layer_weights)
        self.init_weights_from_hidden_layer_neurons_to_output_layer_neurons(
            output_layer_weights)

    #初始化隐藏层的权重
    def init_weights_from_inputs_to_hidden_layer_neurons(self, hidden_layer_weights):
        #依值初始化，或随机初始化
        if hidden_layer_weights:
            counter = 0
            for i in range(self.num_hid):
                self.hidden_layer.neurons[i].weights = hidden_layer_weights[counter:counter + self.num_in - 1]
                counter += self.num_in
        else:
            for i in range(self.num_hid):
                self.hidden_layer.neurons[i].weights = [
                    random.normalvariate(0, 1) for i in range(self.num_in)]
        #Your Code Here

    #初始化输出层的权重
    def init_weights_from_hidden_layer_neurons_to_output_layer_neurons(self, output_layer_weights):
        #Your Code Here
        #依值初始化，或随机初始化
        if output_layer_weights:
            counter = 0
            for i in range(self.num_out):
                self.output_layer.neurons[i].weights = output_layer_weights[counter:counter + self.num_hid - 1]
                counter += self.num_hid
        else:
            for i in range(self.num_out):
                self.output_layer.neurons[i].weights = [
                    random.normalvariate(0, 1) for i in range(self.num_hid)]

    def inspect(self):
        print('------')
        print('* Inputs: {}'.format(self.num_in))
        print('------')
        print('Hidden Layer')
        self.hidden_layer.inspect()
        print('------')
        print('* Output Layer')
        self.output_layer.inspect()
        print('------')

    def feed_forward(self, inputs):
        #Your Code Here
        #输入，计算各层输出
        mids = self.hidden_layer.feed_forward(inputs)
        self.output_layer.feed_forward(mids)

    def train(self, training_inputs, training_outputs):
        self.feed_forward(training_inputs)

        # 1. Output neuron deltas
        #Your Code Here
        # ∂E/∂zⱼ
        deltas_out = []
        for i in range(self.num_out):
            delta = self.output_layer.neurons[i].calculate_pd_error_wrt_total_net_input(
                int(training_outputs[i]))
            deltas_out.append(delta)

        # 2. Hidden neuron deltas
        # We need to calculate the derivative of the error with respect to the output of each hidden layer neuron
        # dE/dyⱼ = Σ ∂E/∂zⱼ * ∂z/∂yⱼ = Σ ∂E/∂zⱼ * wᵢⱼ
        # ∂E/∂zⱼ = dE/dyⱼ * ∂zⱼ/∂
        #Your Code Here
        deltas_hid = []
        for i in range(self.num_hid):
            dE_dyi = 0
            for j in range(self.num_out):
                dE_dyi += self.output_layer.neurons[j].weights[i] * \
                    deltas_out[j]
            delta = self.hidden_layer.neurons[i].calculate_pd_total_net_input_wrt_input(
            ) * dE_dyi
            deltas_hid.append(delta)

        # 3. Update output neuron weights
        # ∂Eⱼ/∂wᵢⱼ = ∂E/∂zⱼ * ∂zⱼ/∂wᵢⱼ
        # Δw = α * ∂Eⱼ/∂wᵢ
        #Your Code Here
        w_out = [[] for i in range(self.num_out)]
        for i in range(self.num_out):
            for j in range(self.num_hid):
                w = self.LEARNING_RATE * \
                    deltas_out[i] * \
                    self.hidden_layer.neurons[j].output
                w_out[i].append(w)
        for i in range(self.num_out):
            for j in range(self.num_hid):
                self.output_layer.neurons[i].weights[j] += w_out[i][j]

        # 4. Update hidden neuron weights
        # ∂Eⱼ/∂wᵢ = ∂E/∂zⱼ * ∂zⱼ/∂wᵢ
        # Δw = α * ∂Eⱼ/∂wᵢ
        #Your Code Here
        w_hid = [[] for i in range(self.num_hid)]
        for i in range(self.num_hid):
            for j in range(self.num_in):
                w = self.LEARNING_RATE * \
                    deltas_hid[i] * \
                    self.hidden_layer.neurons[i].calculate_pd_total_net_input_wrt_weight(
                        j)
                w_hid[i].append(w)
        for i in range(self.num_hid):
            for j in range(self.num_in):
                self.hidden_layer.neurons[i].weights[j] += w_hid[i][j]


class NeuronLayer:
    def __init__(self, num_neurons, bias):

        # Every neuron in a layer shares the same bias
        self.bias = bias if bias else random.random()

        self.neurons = []
        for i in range(num_neurons):
            self.neurons.append(Neuron(self.bias))

    def inspect(self):
        print('Neurons:', len(self.neurons))
        for n in range(len(self.neurons)):
            print(' Neuron', n)
            for w in range(len(self.neurons[n].weights)):
                print('  Weight:', self.neurons[n].weights[w])
            print('  Bias:', self.bias)

    def feed_forward(self, inputs):
        outputs = []
        for neuron in self.neurons:
            outputs.append(neuron.calculate_output(inputs))
        return outputs

    def get_outputs(self):
        outputs = []
        for neuron in self.neurons:
            outputs.append(neuron.output)
        return outputs

#输入结点不算神经元


class Neuron:
    def __init__(self, bias):
        self.bias = bias if bias else random.random()
        self.weights = []
        self.weighted_input = 0
        self.output = 0
        self.inputs = []

    #计算输出
    def calculate_output(self, inputs):
        #Your Code Here
        self.weighted_input = self.calculate_total_net_input(inputs)
        output = self.squash(self.weighted_input)
        self.output = output
        return output

    #计算加权后的输入
    def calculate_total_net_input(self, inputs):
        #Your Code Here
        total_net_input = 0
        num = len(self.weights)
        self.inputs = [inputs[i] for i in range(num)]

        for i in range(num):
            total_net_input += self.weights[i] * inputs[i]
        total_net_input += self.bias
        return total_net_input

        # Apply the logistic function to squash the output of the neuron
        # The result is sometimes referred to as 'net' [2] or 'net' [1]
        # 输出有三种格式：100 010 001
        # 激活函数
    def squash(self, total_net_input):
        #Your Code Here
        down = 1 + math.exp(-total_net_input)
        output = 1 / down
        return output

        # Determine how much the neuron's total input has to change to move closer to the expected output
        #
        # Now that we have the partial derivative of the error with respect to the output (∂E/∂yⱼ) and
        # the derivative of the output with respect to the total net input (dyⱼ/dzⱼ) we can calculate
        # the partial derivative of the error with respect to the total net input.
        # This value is also known as the delta (δ) [1]
        # δ = ∂E/∂zⱼ = ∂E/∂yⱼ * dyⱼ/dzⱼ
        #
    def calculate_pd_error_wrt_total_net_input(self, target_output):
        delta = self.calculate_pd_error_wrt_output(
            target_output) * self.calculate_pd_total_net_input_wrt_input()
        return delta
        #Your Code Here

        # The partial derivate of the error with respect to actual output then is calculated by:
        # = 2 * 0.5 * (target output - actual output) ^ (2 - 1) * -1
        # = -(target output - actual output)
        #
        # The Wikipedia article on backpropagation [1] simplifies to the following, but most other learning material does not [2]
        # = actual output - target output
        #
        # Alternative, you can use (target - output), but then need to add it during backpropagation [3]
        #
        # Note that the actual output of the output neuron is often written as yⱼ and target output as tⱼ so:
        # = ∂E/∂yⱼ = -(tⱼ - yⱼ)
    def calculate_pd_error_wrt_output(self, target_output):
        pd_error = target_output - self.output
        return pd_error
        #Your Code Here

        # The total net input into the neuron is squashed using logistic function to calculate the neuron's output:
        # yⱼ = φ = 1 / (1 + e^(-zⱼ))
        # Note that where ⱼ represents the output of the neurons in whatever layer we're looking at and ᵢ represents the layer below it
        #
        # The derivative (not partial derivative since there is only one variable) of the output then is:
        # dyⱼ/dzⱼ = yⱼ * (1 - yⱼ)
    def calculate_pd_total_net_input_wrt_input(self):
        pd = self.output * (1 - self.output)
        return pd
        #Your Code Here

        # The total net input is the weighted sum of all the inputs to the neuron and their respective weights:
        # = zⱼ = netⱼ = x₁w₁ + x₂w₂ ...
        #
        # The partial derivative of the total net input with respective to a given weight (with everything else held constant) then is:
        # = ∂zⱼ/∂wᵢ = some constant + 1 * xᵢw₁^(1-0) + some constant ... = xᵢ
    def calculate_pd_total_net_input_wrt_weight(self, index):
        #Your Code Here
        x_index = self.inputs[index]
        return x_index
        # An example:



def test(network, data, result):
    global result_dic
    num = len(data)
    correct = 0
    outputs = []   
    for i in range(num):
        inputs = data.iloc[i].tolist()
        network.feed_forward(inputs)
        max_output = 0
        position = -1
        for j in range(network.num_out):
            if max_output < network.output_layer.neurons[j].output:
                max_output = network.output_layer.neurons[j].output
                position = j
        outputs.append(result_dic[position])
    for i in range(num):
        if outputs[i] == result.iloc[i]:
            correct += 1
    return correct / num

result_dic = {0:'100', 1:'010', 2:'001'}
data = pd.read_csv('train.data', header=None)
result = data[22]
result = result.replace(
    {-1:'100', 1:'100', 2:'010', 3:'001'})
data = data / 10
#去除无用属性及结果
del data[2]
del data[22]
del data[25]
del data[26]
del data[27]

test_data = pd.read_csv('train.data', header=None)
test_result = test_data[22]
test_result = test_result.replace(
    {-1: '100', 1: '100', 2: '010', 3: '001'})
test_data = test_data / 10
del test_data[2]
del test_data[22]
del test_data[25]
del test_data[26]
del test_data[27]

nn = NeuralNetwork(22, 6, 3, hidden_layer_weights=None, 
                   hidden_layer_bias=random.random(),
                   output_layer_weights=None, 
                   output_layer_bias=random.random())
num = len(data)
for j in range(1, 121):
    accuracy = 0
    if j % 8 == 0:
        print('after training ' + str(j) + ' times, accuracy:')
        accuracy = test(nn, test_data, test_result)
        print(accuracy)
        if accuracy >= 0.6:
            nn.hidden_layer.inspect()
            nn.output_layer.inspect()
    for i in range(num):
        nn.train(data.iloc[i].tolist(), result.iloc[i])
    


