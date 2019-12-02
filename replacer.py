#!/usr/bin/env python3
"""
replacer.py
Created:
@author: Will Rhodes

"""
import argparse
from pathlib import Path
import re

def start():
    parser = argparse.ArgumentParser(description='Cycle through files and replace a constant expression with another.')

    parser.add_argument('-r','--recursive', action='store_true', help='include subdirectories',dest='recursive')
    
    parser.add_argument('-e','--regex', action='store_true', help='text to find is done via regex',dest='regex')

    parser.add_argument('-p','--pattern', type=str, help='file pattern', dest='pattern', default="*")

    parser.add_argument('-d','--directory', required=True, type=str, help='the directory to use', dest='directory')

    parser.add_argument('-f','--find', required=True, type=str, help='text to find',dest='find')

    parser.add_argument('-b','--backup', action='store_true', help='if supplied, backups are saved with this suffix', dest='backup')

    parser.add_argument('-s','--safe','--dry-run', action='store_true', help='if supplied, doesn\'t perform replacement', dest='safe')

    args = parser.parse_args()

    #print(args)
    #exit()

    #get all paths
    if(args.recursive):
        paths = Path(args.directory).rglob(args.pattern)
    else:
        paths = Path(args.directory).glob(args.pattern)

    #itterate through paths
    for path in paths:
        #get the path parts
        filename = path.stem
        parent = path.parent
        ext = path.suffix

        #ask the user for input
        replacement = input("Replace {} in {} with?".format(args.find,filename))
        
        #open the path
        with open(path.resolve(), 'r+') as f:
            
            #get contents
            contents = f.read()

            if args.backup:
                newpath = parent.joinpath(filename+'.backup'+ext)
                with open(newpath, 'w') as newfile:
                    newfile.write(contents)


            #do the replacement
            if(args.regex):
                num = len(re.findall(args.find,contents))
                contents = re.sub(args.find, replacement, contents)
            else:
                num = int((len(contents) - len(contents.replace(args.find,'')))/len(args.find))
                contents = contents.replace(args.find,replacement)
            

            #save
            if not args.safe:
                f.seek(0)
                f.write(contents)
                f.truncate()
            
            #tell the user the stats
            print('{} replacements made to {}'.format(num,filename+ext))

    

if  __name__ =='__main__':start()