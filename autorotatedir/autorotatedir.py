import os
import errno
import sys
import datetime
import argparse

OUTPUT_DIR = ".old"
ROTATION_DAYS = 30
EXPIRATION_DAYS = 0

def mkdirs(newdir, mode=0777):
    try: os.makedirs(newdir, mode)
    except OSError, err:
        # Reraise the error unless it's about an already existing directory 
        if err.errno != errno.EEXIST or not os.path.isdir(newdir): 
            raise

def main():
    desc = 'Download Directory Rotator - This tool will help cleanup desktop '\
           'and download directories by moving old files out of the way.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('directory',
                        help='Directory to work on.')
    parser.add_argument('-o','--outputdir', 
                        help='Destination folder for rotated files. This is '\
                             'treated as relative to the inpected directory. '\
                             'Default: (%s)' % OUTPUT_DIR, 
                        default=OUTPUT_DIR)
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-a', 
                        '--age', 
                        help='Age of files to rotate. Any file or folders '\
                             'older than this age will be move to the ouput '\
                             'directory. '\
                             'Default: (%s)' % ROTATION_DAYS, 
                        type=int,
                        default=ROTATION_DAYS)
    parser.add_argument('-e', 
                        '--expiration', 
                        help='Age of files to EXPIRE. If set to a value other '\
                             'than 0 files of this age will be deleted from '\
                             'the ouput directory. '\
                             'Default: (%s)' % EXPIRATION_DAYS, 
                        type=int,
                        default=EXPIRATION_DAYS)

    args = vars(parser.parse_args(sys.argv[1:]))
    pass

if __name__ == '__main__':
    main()
