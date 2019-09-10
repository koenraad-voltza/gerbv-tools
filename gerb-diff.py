import os
import argparse

parser = argparse.ArgumentParser(description='Check differences between 2 sets of gerbers')
parser.add_argument('source1', action="store", help='location of the first set of gerbers')
parser.add_argument('source2', action="store", help='location of the second set of gerbers')
parser.add_argument('--diffs', '-d', action="store", default="", help='location of the difference images (removed if empty)')
args = parser.parse_args()

for filename1 in os.listdir(args.source1):
    if filename1.endswith(".gbr"):
        type = filename1.split('-')[-1]
        for filename2 in os.listdir(args.source2):
            if filename2.endswith(".gbr"):
                if(type == filename2.split('-')[-1]):
                    print "Analysing " + type
                    #print os.path.join(args.source1, filename1)
                    os.system("gerbv -x png -o " + filename1 + ".png '" + os.path.join(args.source1, filename1) + "'")
                    os.system("gerbv -x png -o " + filename2 + ".png '" + os.path.join(args.source2, filename2) + "'")
                    os.system("convert " + filename2 + ".png " + filename1 + ".png " + "-compose minus -composite "+ filename1+"-diff.png")
                    if (os.popen("identify -format '%k' " + filename1+"-diff.png").read()=="1"):
                        os.system("rm " + filename1 + ".png")
                        os.system("rm " + filename2 + ".png")
                        os.system("rm " + filename1 + "-diff.png")
                        print "\t No differences found"
                    else:
                        print "\t differences found!"
