x=200
y=200

tilefile = 'art/floors.png'
pos = "1:0"

file = open("maps/mapgen_map.map", "w")
file.write("~Tile Source\n"+tilefile+"\n~Tile Size (x/y)\n32\n32\n~Map Size in Tiles (x/y)\n"+str(x)+"\n"+str(y)+"\n~Setup (Map col:row/Tile col:row)")
for i in range(x):
	for j in range(y):
		file.write("\n"+str(i)+":"+str(j)+"/"+pos+"(0)")