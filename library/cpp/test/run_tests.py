import os


def join(*folders):
    if len(folders) == 1:
        return folders[0]

    return join(os.path.join(*folders[:2]), *folders[2:])


def print_message(m):
    print()
    print("="*len(m))
    print(m)
    print("="*len(m))


path = os.path.dirname(os.path.realpath(__file__))

for folder in os.listdir(path):
    if os.path.isdir(join(path, folder)):
        assert os.path.isfile(join(path, folder, "main.cpp"))
        assert os.path.isfile(join(path, folder, "CMakeLists.txt"))

        with open(join(path, folder, "CMakeLists.txt")) as f:
            executable = f.read().split("project(")[1].split(" ")[0]

        print_message(f"Running {executable}")
        assert os.system(f"cd {path}/{folder} && cmake . && make && ./{executable}") == 0
