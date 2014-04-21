import os
import errno
import sys
import datetime
import logging
import argparse

OUTPUT_DIR = ".old"
ROTATION_DAYS = 30
EXPIRATION_DAYS = 0
DATE_FORMAT = "%Y%m"

def mkdirs(newdir, mode=0777):
    try: os.makedirs(newdir, mode)
    except OSError, err:
        # Reraise the error unless it's about an already existing directory 
        if err.errno != errno.EEXIST or not os.path.isdir(newdir): 
            raise

class Rotator(object):
    """ Rotator for handling the walking, moving and deleting of files in a 
        given directory.
    """
    def __init__(self, directory, age=ROTATION_DAYS, expiration=EXPIRATION_DAYS,
                 outputdir=OUTPUT_DIR, verbose=False, dateformat=DATE_FORMAT):
        """
        :param directory: Directory to act on.
        :param age: Age of files to rotate.
        :param expiration: Age of files to delete.
        :param outputdir: Destination directory for rotated files.
        :param verbose: Flag whether to show verbose output
        :type verbose: boolean
        """
        self.dir = directory
        self.age = age
        self.exp = expiration
        self.out = outputdir
        self.date_format = dateformat
        self.log = logging.getLogger('autorotatedir')

        # Prepare the logger
        log_handler = logging.StreamHandler()
        log_formatter = logging.Formatter("%(levelname)s: %(message)s")
        log_handler.setFormatter(log_formatter)
        self.log.addHandler(log_handler)

        self.setVerbose(verbose)

    def process(self):
        self.log.info('Processing: %s' % self.dir)
        pass

    def setVerbose(self, verbose):
        level = logging.WARNING
        if verbose: level = logging.INFO
        self.log.setLevel(level)

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
    rot = Rotator(**args)
    rot.process()
    pass

if __name__ == '__main__':
    main()
