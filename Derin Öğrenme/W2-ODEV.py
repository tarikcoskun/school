w1 = -0.7
w2 = -0.3
b = 0.1

inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]
targets = [0, 0, 0, 1]

while True:
    error = 0

    for i in range(len(inputs)):
        x1, x2 = inputs[i]
        t = targets[i]

        n = w1*x1 + w2*x2 + b
        a = n >= 0
        e = t - a
        error += abs(e)

        w1 += e*x1
        w2 += e*x2
        b += e

    if error == 0:
        break

print(f"w1 = {w1:.1f}\nw2 = {w2:.1f}\nb = {b:.1f}")
