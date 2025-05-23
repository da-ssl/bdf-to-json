import binascii, json
file = open("font.bdf", "r")
lines = file.readlines()
fontname = input("Font-Name:")
space = input("Zwischenraum:")
output = {}
mode = ""
cchar = ""
ccharlength = 0
cchardata = []

for i in lines:
    if i.startswith("STARTCHAR"):
        mode = "readChar"
        continue

    if i.startswith("BBX"):
        v = i.split(" ")
        ccharlength = v[1]
        continue

    if i.startswith("BITMAP"):
        mode = "writeChar"
        continue

    if mode == "readChar":
        if i.startswith("ENCODING"):
            cchar = i.replace("ENCODING ", "")
            cchar = cchar[:-1]

    if i.startswith("ENDCHAR"):
        output[cchar] = cchardata
        cchardata = []
        ccharlength = 0
        

    if mode == "writeChar":
        if i.startswith("ENDCHAR"):
            mode = ""
            continue

        
        integer = int(i, 16)
        if ccharlength == 0: raise Exception
        length = 13
        currentCharLine = f'{integer:0>16b}'
       
        currentCharLineList = []
        for i in range(len(currentCharLine)):
            currentCharLineList.append(int(currentCharLine[i]))

        cchardata.append(currentCharLineList)

    output["meta"]= {"space": space}

ofile = open("output.json", "w")
ofile.write(json.dumps({fontname: output})[1:-1]+ ",\n")
ofile.close()
print("finished without problems")
