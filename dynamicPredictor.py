class Perceptron:
    weights = []
    N = 0
    bias = 0
    threshold = 0

    def __init__(self, N):
        self.N = N
        self.bias = 0
        self.threshold = 2 * N + 14                 # optimal threshold depends on history length
        self.weights = [0] * N

    def predict(self, global_branch_history):
        running_sum = self.bias
        for i in range(0, self.N):                  # dot product of branch history with the weights
            running_sum += global_branch_history[i] * self.weights[i]
        prediction = -1 if running_sum < 0 else 1
        return (prediction, running_sum)

    def update(self, prediction, actual, global_branch_history, running_sum):
        if (prediction != actual) or (abs(running_sum) < self.threshold):
            self.bias = self.bias + (1 * actual)
            for i in range(0, self.N):
                self.weights[i] = self.weights[i] + (actual * global_branch_history[i])

    def statistics(self):
        print("bias is: " + str(self.bias) + " weights are: " + str(self.weights))


from collections import deque


def perceptron_pred(trace, l=1, tablesize=None):
    global_branch_history = deque([])
    global_branch_history.extend([0] * l)

    p_list = {}
    num_correct = 0

    for br in trace:  # iterating through each branch
        if tablesize:
            index = hash(br[0]) % tablesize
        else:
            index = hash(br[0])

        if index not in p_list:  # if no previous branch from this memory location
            p_list[index] = Perceptron(l)
        results = p_list[index].predict(global_branch_history)
        pr = results[0]
        running_sum = results[1]
        actual_value = 1 if br[1] else -1
        p_list[index].update(pr, actual_value, global_branch_history, running_sum)
        global_branch_history.appendleft(actual_value)
        global_branch_history.pop()
        if pr == actual_value:
            num_correct += 1

    return num_correct, len(p_list)

def getTableSize(ratio,k):
    return int(ratio * k)

with open('feedforward/gcc_branch', 'r') as branchfile:
    trace = []
    for line in branchfile.readlines():
        tok = line.split(' ')
        trace.append([tok[1], int(tok[2])])

import time

num_correct, num_p = perceptron_pred(trace, 5)  # , tablesize=tablesize)
print(num_p)

"""results = []
for i in range (1, 50):
    start_time = time.time()
    num_correct, num_p = perceptron_pred(trace, i)#, tablesize=tablesize)
    end_time = time.time()
    results.append((num_correct/float(len(trace)), end_time - start_time))
    print(results[-1])

print(num_correct / len(trace), num_p)"""


""""
ratios = [i*.033 for i in range(1,31)]
results = []
for ratio in ratios:
    uniqueAddr = 33
    tablesize = getTableSize(ratio, uniqueAddr)

    start_time = time.time()
    num_correct, num_p = perceptron_pred(trace, 5, tablesize=tablesize)
    end_time = time.time()
    results.append((num_correct/float(len(trace)), end_time - start_time, ratio, tablesize))
    print(results[-1])

for r in results:
    line = []
    for c in r:
        line.append(str(c))
    print(','.join(line))
    
    '"""


# history bits
# accuracy and time as number of history bits increases
# table size/collisions

