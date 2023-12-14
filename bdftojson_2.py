import numpy as np
import binascii, json
file = open("font.bdf", "r")
lines = file.readlines()
fontname = input("Font-Name:")
maxCharLength = int(input("Max. Charlength:"))
output = {}
mode = ""
cchar = ""
ccharlength = 0
ccharlength_bbx= 0
cchardata = []


# Initialize 2D array with zeros
cchardata2D = np.zeros((12, maxCharLength+1))

for i in lines:
    if i.startswith("STARTCHAR"):
        mode = "readChar"
        continue

    if i.startswith("BBX"):
        v = i.split(" ")
        ccharlength_bbx = int(v[1])
        continue

    if i.startswith("BITMAP"):
        mode = "writeChar"
        row = 0
        continue

    if mode == "readChar":
        if i.startswith("ENCODING"):
            cchar = i.replace("ENCODING ", "")
            cchar = cchar[:-1]

    if i.startswith("ENDCHAR"):
        output[cchar] = cchardata2D
        cchardata2D = np.zeros((ccharlength_bbx, maxCharLength))

    if mode == "writeChar":
        if i.startswith("ENDCHAR"):
            mode = ""
            continue
        
        # Convert hexadecimal to binary
        integer = int(i, 16)
        currentCharLine = f'{integer:0>{maxCharLength}b}'
        for col in range(len(currentCharLine)):
            cchardata2D[row][col] = int(currentCharLine[col])


ofile = open("output.json", "w")
ofile.write(json.dumps({fontname: output}))
ofile.close()
print("finished without problems")
