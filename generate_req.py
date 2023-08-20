def create_requirements_in():
    with open('requirements.txt', 'r') as file:
        lines = file.readlines()

    # Extract the package names without version info
    packages = [line.split('==')[0] for line in lines if '==' in line]

    with open('requirements.in', 'w') as file:
        file.write('\n'.join(packages))


if __name__ == "__main__":
    create_requirements_in()
