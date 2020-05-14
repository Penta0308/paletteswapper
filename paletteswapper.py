import sys
import os.path
import glob

if len(sys.argv) != 4 : # thisfile convtable fromfolder tofolder
    print("Usage: python ./paletteswapper.py conv.csv ./from ./to")
    print("convert table: [From color R, G, B, To color R, G, B] Line Repeat(CSV Format)")

import csv

colordict = {}

csvf = open(sys.argv[1], 'r', encoding='utf-8')
rdr = csv.reader(csvf)
for line in rdr:
    colordict[int(line[0]) << 16 | int(line[1]) << 8 | int(line[2])] = int(line[3]) << 16 | int(line[4]) << 8 | int(line[5])
csvf.close()

if not os.path.isdir(sys.argv[3]) :
    os.mkdir(sys.argv[3])

from PIL import Image

for fromimgfilename in glob.glob(sys.argv[2] + "/*.png") :
    iimg = Image.open(fromimgfilename)
    irgba = iimg.convert("RGBA")
    width, height = irgba.size
    orgba = Image.new("RGBA", (width, height))
    opix = orgba.load()
    for y in range(0, height) :
        for x in range(0, width) :
            r, g, b, a = irgba.getpixel((x, y))
            cc = r << 16 | g << 8 | b
            for aa, bb in colordict.items() :
                if cc == aa:
                    cc = bb
                    break
            opix[x, y] = ((cc >> 16) & 0xFF, (cc >> 8) & 0xFF, cc & 0xFF, a)
    orgba.save(sys.argv[3] + fromimgfilename[len(sys.argv[2]):])
            
    