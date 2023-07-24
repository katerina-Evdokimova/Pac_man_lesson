def load_level(filename):
    filename = 'data_level/' + filename
    with open(filename, 'r') as mapfile:
        level_map = [line.strip() for line in mapfile]
    maxW = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(maxW, '.')), level_map))



