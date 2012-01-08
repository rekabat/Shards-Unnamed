x=30
y=30

floortilefile = 'art/floors.png'
pos = "3:0"

bordertilefile = "art/dark brick.jpg"
posborder = "0:0"

file = open("maps/mapgen_map.map", "w")
file.write(">>> Tile Source [size x:y]\n" + \
	"0-> "+floortilefile +" [32:32]\n" + \
	"1-> "+bordertilefile+" [32:32]\n" + \
	">>> Map Size in Tiles (x/y)\n" + \
	str(x)+":"+str(y)+"\n" + \
	">>> Setup (Source-> Map col:row/Tile col:row)")
for i in range(x):
	for j in range(y):
		if (i==0) or (j==0) or (i == x-1) or (j == y-1):
			file.write("\n1-> "+str(i)+":"+str(j)+"/"+posborder+"(1)")
		else:
			file.write("\n0-> "+str(i)+":"+str(j)+"/"+pos+"(0)")