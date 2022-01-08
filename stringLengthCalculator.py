charDict = {}

def loadKey():
    keyFileName = 'strlength.txt'
    
    with open(keyFileName, encoding="utf8") as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    
    for line in lines:
        i = 0
        total = ""
        key = ""
        for char in line:
            if line[0] + line[1] == "//":
                break
            elif i == 0:
                key = char
            elif i != 1:
                total += char
            try:
                charDict[key] = float(total)
            except:
                1 + 1
            i += 1

def calculate(inputString):
    total = 0.0
    for char in inputString:
        if char == "'":
            char = "’"
        try:
            total += charDict[char]
        except:
            total += charDict["space"]
    return total


def main():
    loadKey()
    while (True):
        inputString = input("\ninput a string: ")
        total = 0.0
        for char in inputString:
            if char == "'":
                char = "’"
            try:
                total += charDict[char]
            except:
                total += charDict["space"] 
        print(total)


if (__name__ == "__main__"):
    main()