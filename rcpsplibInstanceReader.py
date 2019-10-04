def readjslibfile(filename="j301_1"):
    big_num = 10000
    file = open(filename + ".sm", "r")
    precedence_line = big_num
    resource_line = big_num
    capacity_line = big_num
    line_count = 0
    prec = dict()
    resource = dict()
    duration = dict()
    for line in file:
        line_count += 1
        if line.startswith("jobs"):
            jobs_count = int(line.split(":")[1])  # include source and sink
        if line.startswith("PRECEDENCE"):
            precedence_line = line_count + 2
        if line_count >= precedence_line and line_count <= precedence_line + jobs_count - 1:
            tmp = [int(i) for i in line.split()]
            prec[tmp[0]] = tmp[3:]
        if line.startswith("REQUESTS/DURATIONS"):
            resource_line = line_count + 3
        if line_count >= resource_line and line_count <= resource_line + jobs_count - 1:
            tmp = [int(i) for i in line.split()]
            resource[tmp[0]] = tmp[3:]
            duration[tmp[0]] = tmp[2]
        if line.startswith("RESOURCEAVAI"):
            capacity_line = line_count + 2
        if line_count == capacity_line:
            capacity = [int(i) for i in line.split()]
    file.close()

    return prec, resource, capacity, duration



