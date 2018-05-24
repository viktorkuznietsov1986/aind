import time

s1 = .0001
w = 4
n = 50

seq = [s1]
for i in range(1, n):
    seq.append(w*seq[i-1] - w*seq[i-1]**2)

#print(seq)
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

plt.plot([x for x in range(0, n)], seq)
plt.show()
plt.draw()
_ = input()

#plot_sequence(seq)