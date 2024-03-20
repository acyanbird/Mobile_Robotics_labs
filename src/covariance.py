import numpy as np

data1 = np.loadtxt('p1.txt')
data2 = np.loadtxt('p2.txt')
data3 = np.loadtxt('p3.txt')

data1_cov = np.cov(data1, rowvar=False)
data2_cov = np.cov(data2, rowvar=False)
data3_cov = np.cov(data3, rowvar=False)

data1_std_devs = np.sqrt(np.diag(data1_cov))
data2_std_devs = np.sqrt(np.diag(data2_cov))
data3_std_devs = np.sqrt(np.diag(data3_cov))


print("p1 cov: \n", np.cov(data1, rowvar=False))
print("p2 cov: \n", np.cov(data2, rowvar=False))
print("p3 cov: \n", np.cov(data3, rowvar=False))

print("p1 std devs: ", data1_std_devs)
print("p2 std devs: ", data2_std_devs)
print("p3 std devs: ", data3_std_devs)

# Calculate the standard deviations for each column
std_dev1_x = np.std(data1[:, 0])
std_dev1_y = np.std(data1[:, 1])

std_dev2_x = np.std(data2[:, 0])
std_dev2_y = np.std(data2[:, 1])

std_dev3_x = np.std(data3[:, 0])
std_dev3_y = np.std(data3[:, 1])

# Print the standard deviations
print("p1 std dev x: ", std_dev1_x)
print("p1 std dev y: ", std_dev1_y)

print("p2 std dev x: ", std_dev2_x)
print("p2 std dev y: ", std_dev2_y)

print("p3 std dev x: ", std_dev3_x)
print("p3 std dev y: ", std_dev3_y)