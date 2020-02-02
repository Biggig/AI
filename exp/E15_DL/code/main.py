from data_utils import *
from solver import *
from cnn import *

data = get_CIFAR10_data(num_training=49000, num_validation=1000, num_test=1000, subtract_mean=True)
model = ThreeLayerConvNet()
solver = Solver(model, data, update_rule='sgd', optim_config={'learning_rate':1e-3,}, lr_decay=0.95, num_epochs=10, batch_size=100, print_every=100)
solver.train()
