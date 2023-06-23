import re

STR_LIST = []

def main():
    pass

def getStrings(file):
    chars = r"A-Za-z0-9/\-:.,_$%'()[\]<> "
    shortestRun = 4
    regexp = '[%s]{%d,}' % (chars, shortestRun)
    pattern = re.compile(regexp)

    return pattern.findall(file)


if __name__ == "__name__":
    main()



