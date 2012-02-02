x=100
y=100

floortilefile = 'art/map/floors.png'
pos = "3:0"

bordertilefile = "art/map/dark brick.jpg"
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
		line = "\n"+str(i)+":"+str(j)+"+"
		if (i==0) or (j==0) or (i == x-1) or (j == y-1):
			line+=("1->"+posborder+"(1)")
		else:
			line+=("0->"+pos+"(0)")
		line += "[0]"

		file.write(line)