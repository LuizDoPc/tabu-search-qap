def readFile(name):
    with open(name, 'r') as fh:
        valor = int(fh.readline())
        lines = fh.readlines()
        lines1 = lines[1: valor + 1]
        lines2 = lines[valor + 2:(valor + 2)+valor]

    # Remove newlines, tabs, and split each string separated by spaces.
    clean1 = [[float(value) for value in line.strip().replace(
        '\t', '').split()] for line in lines1]
    clean2 = [[float(value) for value in line.strip().replace(
        '\t', '').split()] for line in lines2]

    return {"distric": clean1, "flow": clean2, "len": valor}
