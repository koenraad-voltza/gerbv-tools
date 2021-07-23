import os
import argparse

parser = argparse.ArgumentParser(description='Check differences between 2 sets of gerbers')
parser.add_argument('source1', action="store", default="", help='location of the first (old) set of gerbers')
parser.add_argument('source2', action="store", default="", help='location of the second (new) set of gerbers')
parser.add_argument('--diffs', '-d', action="store", default="", help='location of the difference images (removed if empty)')
parser.add_argument('--crop1', action="store", default="", help='crop source1 to wxh+x+y (px)') #2117x4927+217+579
parser.add_argument('--crop2', action="store", default="", help='crop source1 to wxh+x+y (px)') #2117x4927+217+454
parser.add_argument('--clean', '-c', action="store_true", help='delete all png images in cwd before start')
parser.add_argument('--dpi', action="store", default=1000, type=int, help='dpi of the png export')

args = parser.parse_args()

if (args.clean):
    print "Cleaning PNG files"
    os.system("rm *.png")

for filename1 in os.listdir(args.source1):
    #print filename1.lower()
    if filename1.lower().endswith(".gbr"):
        type = filename1.split('-')[-1].lower()
        for filename2 in os.listdir(args.source2):
            if filename2.lower().endswith(".gbr"):
	    	#print '\t'+filename2.lower()
                if(type == filename2.split('-')[-1].lower()):
                    print "Analysing " + type
                    #print os.path.join(args.source1, filename1)
                    
                    ##Removals
                    #print "Creating PNG"	
                    os.system("gerbv -D " + str(args.dpi) + " -x png -f " + "'#FF0000'" + " -o " + filename1 + ".png '" + os.path.join(args.source1, filename1) + "'")
                    if (len(args.crop1)>0):
                        os.system("convert " + filename1 + ".png -crop " + args.crop1 + " " + filename1 + ".png")
                    #print os.path.join(args.source2, filename2)
                    os.system("gerbv -D " + str(args.dpi) + " -x png -f " + "'#FF0000'" + " -o " + filename2 + ".png '" + os.path.join(args.source2, filename2) + "'")
                    if (len(args.crop2)>0):
                        os.system("convert " + filename2 + ".png -crop " + args.crop2 + " " + filename2 + ".png")
                    #print "Creating difference"
                    os.system("convert " + filename2 + ".png " + filename1 + ".png " + "-compose minus -composite "+ filename1+"-diff.png")
                    
                    ##Additions
                    #print "Creating PNG"
                    os.system("gerbv -D " + str(args.dpi) + " -x png -f " + "'#00FF00'" + " -o " + filename1 + ".png '" + os.path.join(args.source1, filename1) + "'")
                    if (len(args.crop1)>0):
                        os.system("convert " + filename1 + ".png -crop " + args.crop1 + " " + filename1 + ".png")
                    #print os.path.join(args.source2, filename2)
                    os.system("gerbv -D " + str(args.dpi) + " -x png -f " + "'#00FF00'" + " -o " + filename2 + ".png '" + os.path.join(args.source2, filename2) + "'")
                    if (len(args.crop2)>0):
                        os.system("convert " + filename2 + ".png -crop " + args.crop2 + " " + filename2 + ".png")
                    #print "Creating difference"
                    os.system("convert " + filename1 + ".png " + filename2 + ".png " + "-compose minus -composite "+ filename2+"-diff.png")
                    
                    os.system("convert " + filename1 + "-diff.png " + filename2 + "-diff.png " + "-compose plus -composite "+ filename2+"-diff2.png")
                    
                    #print "Cleanup"
                    if (os.popen("identify -format '%k' " + filename1+"-diff.png").read()=="1"):
                        os.system("rm " + filename1 + ".png")
                        os.system("rm " + filename2 + ".png")
                        os.system("rm " + filename1 + "-diff.png")
                        print "\t No differences found"
                    else:
                    	os.system("rm *.gbr.png")
                        os.system("rm *.gbr-diff.png")
                        print "\t differences found!"
