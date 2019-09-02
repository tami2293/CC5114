from read_data import *
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import time
import matplotlib.pyplot as plt


def sigmoid(z):
	return 1/(1 + np.exp(-z))


def step(z):
    return np.heaviside(z, 1)


def tan_hip(z):
    return np.tanh(z)


# Produce a neural network randomly initialized
def initialize_parameters(n_x, n_h, n_y):
	W1 = np.random.randn(n_h, n_x)
	b1 = np.zeros((n_h, 1))
	W2 = np.random.randn(n_y, n_h)
	b2 = np.zeros((n_y, 1))

	parameters = {
	"W1": W1,
	"b1" : b1,
	"W2": W2,
	"b2" : b2
	}
	return parameters

# Evaluate the neural network
def forward_prop(X, parameters):
  W1 = parameters["W1"]
  b1 = parameters["b1"]
  W2 = parameters["W2"]
  b2 = parameters["b2"]

  # Z value for Layer 1
  Z1 = np.dot(W1, X) + b1
  # Activation value for Layer 1
  A1 = np.tanh(Z1)
  # Z value for Layer 2
  Z2 = np.dot(W2, A1) + b2
  # Activation value for Layer 2
  A2 = sigmoid(Z2)

  cache = {
    "A1": A1,
    "A2": A2
  }
  return A2, cache

# Evaluate the error (i.e., cost) between the prediction made in A2 and the provided labels Y 
# We use the Mean Square Error cost function
def calculate_cost(A2, Y):
  # m is the number of examples
  cost = np.sum((0.5 * (A2 - Y) ** 2).mean(axis=1))/m
  return cost


#Evaluate accuracy between the prediction made in A2 and the provided labels Y
def calculate_accuracy(a2, Y):
  a2_final = np.zeros((a2.shape[0], a2.shape[1]))
  max_i = np.argmax(a2, axis=0)
  i_acc = 0
  for index in max_i:
    a2_final[index][i_acc] = 1
    i_acc += 1
  a2_final = a2_final.astype(int)
  return np.count_nonzero((a2_final == Y).all(0))/Y.shape[1]


# Apply the backpropagation
def backward_prop(X, Y, cache, parameters):
  A1 = cache["A1"]
  A2 = cache["A2"]

  W2 = parameters["W2"]

  # Compute the difference between the predicted value and the real values
  dZ2 = A2 - Y
  dW2 = np.dot(dZ2, A1.T)/m
  db2 = np.sum(dZ2, axis=1, keepdims=True)/m
  # Because d/dx tanh(x) = 1 - tanh^2(x)
  dZ1 = np.multiply(np.dot(W2.T, dZ2), 1-np.power(A1, 2))
  dW1 = np.dot(dZ1, X.T)/m
  db1 = np.sum(dZ1, axis=1, keepdims=True)/m

  grads = {
    "dW1": dW1,
    "db1": db1,
    "dW2": dW2,
    "db2": db2
  }

  return grads

# Third phase of the learning algorithm: update the weights and bias
def update_parameters(parameters, grads, learning_rate):
  W1 = parameters["W1"]
  b1 = parameters["b1"]
  W2 = parameters["W2"]
  b2 = parameters["b2"]

  dW1 = grads["dW1"]
  db1 = grads["db1"]
  dW2 = grads["dW2"]
  db2 = grads["db2"]

  W1 = W1 - learning_rate*dW1
  b1 = b1 - learning_rate*db1
  W2 = W2 - learning_rate*dW2
  b2 = b2 - learning_rate*db2
  
  new_parameters = {
    "W1": W1,
    "W2": W2,
    "b1" : b1,
    "b2" : b2
  }

  return new_parameters

# model is the main function to train a model
# X: is the set of training inputs
# Y: is the set of training outputs
# n_x: number of inputs (this value impacts how X is shaped)
# n_h: number of neurons in the hidden layer
# n_y: number of neurons in the output layer (this value impacts how Y is shaped)
def model(X, Y, n_x, n_h, n_y, num_of_iters, learning_rate):
  parameters = initialize_parameters(n_x, n_h, n_y)
  cost_list = []
  acc_list = []
  for i in range(0, num_of_iters+1):
    a2, cache = forward_prop(X, parameters)
    cost = calculate_cost(a2, Y)
    acc = calculate_accuracy(a2, Y)
    grads = backward_prop(X, Y, cache, parameters)
    parameters = update_parameters(parameters, grads, learning_rate)
    if(i%100 == 0):
      print('Cost after iteration# {:d}: {:f}'.format(i, cost))
      print('Accuracy after iteration# {:d}: {:f}'.format(i, acc))
      cost_list.append(cost)
      acc_list.append(acc)

  return parameters, cost_list, acc_list


# Make a prediction
# X: represents the inputs
# parameters: represents a model
# the result is the prediction
def predict(X, parameters):
  a2, cache = forward_prop(X, parameters)
  yhat = a2

  # The next (commented) block used a threshold, we dont want that since the output label was 1-hot encoded
  """
  #yhat = np.squeeze(yhat)
  y_predict = np.zeros((yhat.shape[0], yhat.shape[1]))
  for j in range(0, yhat.shape[1]):
      for i in range(0, yhat.shape[0]):
        if(yhat[i][j] >= 0.5):
            y_predict[i][j] = 1
            break
  return y_predict"""
  print(yhat)
  print(yhat.shape)
  return yhat


# DATA PREDICTION
# Set the seed to make result reproducible
np.random.seed(42)

# No. of training examples
m = X_train.shape[1]

# Set the hyperparameters
n_x = X_train.shape[0]     # No. of neurons in first layer
n_h = 4     # No. of neurons in hidden layer
n_y = 2     # No. of neurons in output layer
num_of_iters = 6000
learning_rate = 0.01
# define a model
start_time = time.time()
total_model = model(X_train, y_train, n_x, n_h, n_y, num_of_iters, learning_rate)
elapsed_time = time.time() - start_time
trained_parameters = total_model[0]
cost_l = total_model[1]
acc_l = total_model[2]

# Test to calculate the result of its elements. Measure elapsed time.
y_predict = predict(X_test, trained_parameters)
print("elapsed time: ", elapsed_time)

# Transform results to 1-hot encoded label
y_final_predict = np.zeros((y_predict.shape[0], y_predict.shape[1]))
max_ind = np.argmax(y_predict, axis=0)
i = 0
for index in max_ind:
    y_final_predict[index][i] = 1
    i += 1

# Confusion matrix
# y_final_predict = y_predict.transpose()
# print(np.count_nonzero(np.equal([0, 0], y_pred).all(1)))
conf_matrix = confusion_matrix(y_test.transpose().argmax(axis=1), y_predict.transpose().argmax(axis=1))
print(conf_matrix)

# Plot error per epoch
epoch = []
epoch_n = 0
for ind in range(0, len(cost_l)):
    epoch.append(epoch_n)
    epoch_n += 100

plt.figure()
plt.plot(epoch, cost_l)
plt.title('Error per epoch')
plt.xlabel('Epoch number')
plt.ylabel('Error rate')
plt.savefig('error.png')

plt.figure()
plt.plot(epoch, acc_l)
plt.title("Accuracy per epoch")
plt.xlabel('Epoch number')
plt.ylabel('Accuracy')
plt.savefig('acc.png')



# Print the result
print(y_predict)
print(y_test)
#print('Neural Network prediction for example ({:d}, {:d}) is {:d}'.format(
#    X_test[0][0], X_test[1][0], y_predict))
