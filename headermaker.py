def genHeader():
    header = {}
    counetr = 0
    with open("header.txt", "r") as f:
        prev = ""
        for line in f:
            line = line.strip()
            if counetr % 2 == 1:
                header[prev] = line
            else: prev = line.removeprefix(":").removesuffix(":")
            counetr += 1
        # print(header)

    return header