import sys,os,re
from pathlib import Path
import argparse

'''
regex_search.py
purpose
    needed when converting files where the original file (with metadata) already exists and just needs to be mapped over. Blame iTunes.
use
    python regex_search.py -d "C:\Users\Will\Documents\Scripts\Star Trek TNG" -p "(\t{5}RIKER((?!\n\n).)*[^A-Za-z]vessel[^A_Za-z])"
'''


def main():
    '''
    the driver
    '''
    args = parse()
    file_data = get_files(args)
    print(f'Found {len(file_data.items())} files to search')
    matches = get_matches(file_data,args)
    print(matches)
  
def parse():
    '''
    sets the args needed to run and returns them
    '''
    parser = argparse.ArgumentParser(description='finds multiline matches for all files in dir')
    parser.add_argument('-d','--directory',dest='dir',type=str,required=True, help='the directory with the files')
    parser.add_argument('-p','--pattern',dest='match',type=str,required=True, help='regex pattern')
    args = parser.parse_args()

    return args


def get_files(args):
    '''
    gets {filename:text}
    '''
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(args.dir) for f in filenames]
    return {f:Path(f).read_text() for f in files}


def get_matches(file_data,args):
    '''
    returns dict {filename:match}
    '''
    result = {}
    for filename,text in file_data.items():
        matches = re.findall(args.match,text,re.M|re.S)
        if(matches):
            result[filename] = matches
    return result


if __name__== "__main__": main()
