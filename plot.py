import matplotlib.pyplot as plt
import numpy as np

X = []
for line in open('actions.txt', 'r'):
    X.append(int(line))

labels, counts = np.unique(X, return_counts=True)

labels = ['right', 'left', 'jump', 'none']

plt.figure()
plt.bar(labels, counts, align='center')
plt.xlabel('Actions')
plt.ylabel('Amount')
plt.yscale('log')
plt.xticks(np.arange(0, 4), labels)

X1 = []
X2 = []
X3 = []
X4 = []
for line in open('q_values.txt', 'r'):
    l = line.replace('[', '').replace(']', '').replace(',', '').split()
    l = [float(i) for i in l]
    
    right, left, jump, none = l

    X1.append(right)
    X2.append(left)
    X3.append(jump)
    X4.append(none)


x1it = np.arange(0, len(X1))
x2it = np.arange(0, len(X2))
x3it = np.arange(0, len(X3))
x4it = np.arange(0, len(X4))

plt.figure()
plt.plot(x1it, X1, label='right')

plt.plot(x2it, X2, label='left')

plt.plot(x3it, X3, label='jump')

plt.plot(x4it, X4, label='none')
plt.xlabel('Iterations')
plt.ylabel('Q-values')
plt.xscale('log')

ax = plt.gca()
ax.set_ylim([-5, 15])
ax.set_xlim([1000, len(X1)])

plt.legend()

plt.show()

#plt.show()
