import matplotlib.pyplot as plt

def read_file(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    x_values = []
    y_values = []

    for line in lines:
        x, y = line.split()
        x_values.append(float(x))
        y_values.append(float(y))

    return x_values, y_values

# Read the files
x_values1, y_values1 = read_file('close_final1.txt')
x_values2, y_values2 = read_file('close_final2.txt')
x_values3, y_values3 = read_file('close_final3.txt')

plt.xlim(-0.3, 0.3)
plt.ylim(-0.2, 0.2)
plt.axis('equal')

# Plot the scatter graphs
plt.scatter(x_values1, y_values1, color='red')
plt.scatter(x_values2, y_values2, color='green')
plt.scatter(x_values3, y_values3, color='blue')

plt.show()