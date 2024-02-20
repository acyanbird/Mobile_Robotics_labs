import subprocess

for _ in range(10):
    # run without noise
    subprocess.run(["ros2", "run", "lab32", "move", "--ros-args", "-p", "l_noise:=0.0", "-p", "a_noise:=0.0", "-p", "file_name:=p1.txt"])
    # run with low noise
    subprocess.run(["ros2", "run", "lab32", "move", "--ros-args", "-p", "l_noise:=0.002", "-p", "a_noise:=0.001", "-p", "file_name:=p2.txt"])
    # run with high noise
    subprocess.run(["ros2", "run", "lab32", "move", "--ros-args", "-p", "l_noise:=0.02", "-p", "a_noise:=0.01", "-p", "file_name:=p3.txt"])