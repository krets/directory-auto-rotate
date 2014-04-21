__author__ = 'Jesse Kretschmer'
__version__ = '0.1'
import os
import errno
import sys
from datetime import datetime, timedelta
import logging
import argparse
import time
import shutil

OUTPUT_DIR = ".old"
ROTATION_DAYS = 30
EXPIRATION_DAYS = 0
DATE_FORMAT = "%Y%m"

class Rotator(object):
    """ Rotator for handling the walking, moving and deleting of files in a 
        given directory.
    """
    def __init__(self, directory, age=ROTATION_DAYS, expiration=EXPIRATION_DAYS,
                 outputdir=OUTPUT_DIR, verbose=False, dateformat=DATE_FORMAT,
                 keepempty=False):
        """
        :param directory: Directory to act on.
        :param age: Age of files to rotate.
        :param expiration: Age of files to delete.
        :param outputdir: Destination directory for rotated files.
        :param verbose: Flag whether to show verbose output
        :type verbose: boolean
        """
        self.dir = os.path.abspath(directory)
        self.old_diff = timedelta(days=age)
        self.exp_diff = timedelta(days=expiration)
        self.out = outputdir
        self.keepempty = keepempty
        self.date_format = dateformat
        self.log = logging.getLogger('autorotatedir')
        self.now = datetime.now()

        # Prepare the logger
        log_handler = logging.StreamHandler()
        log_formatter = logging.Formatter("%(levelname)s: %(message)s")
        log_handler.setFormatter(log_formatter)
        self.log.addHandler(log_handler)

        self.setVerbose(verbose)

    def process(self):
        # self.dir must be an absolute path
        destination = os.path.join(self.dir, self.out)
        empty_dirs = []
        for path, dirs, files in os.walk(self.dir):
            # Try to skip over the output directories
            compare_dirs = [path + os.path.sep, 
                            destination + os.path.sep]
            if os.path.commonprefix(compare_dirs) == destination:
                self.log.info("Ignoring output dir: %s" % path)
                continue
            self.log.info("Processing: %s" % path)
            for f in files:
                src_file = os.path.join(path, f)
                modified = datetime.fromtimestamp(os.path.getmtime(src_file))
                if modified + self.old_diff < self.now:
                    date_dir = modified.strftime(self.date_format)
                    sub_dir = path.replace(self.dir, '').lstrip(os.path.sep)
                    dst_dir = os.path.join(destination, date_dir, sub_dir)
                    if not os.path.isdir(dst_dir):
                        self.log.info("Creating dir: %s" % dst_dir)
                        try:
                            os.makedirs(dst_dir)
                        except Exception, e:
                            msg = "Can't make destination, %s: %s" % (dst_dir,e)
                            self.log.error(msg)
                            continue
                    self.log.info("Rotating file: %s to %s"%(src_file,dst_dir))
                    shutil.move(src_file, dst_dir)

            if not os.listdir(path):
                empty_dirs.insert(0, path)

        if not self.keepempty:
            for d in empty_dirs:
                os.rmdir(d)

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
    parser.add_argument('-k', '--keepempty', action='store_true',
                        help='Keep empty directories. Empty directories will '\
                             'otherwise be removed.')
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

if __name__ == '__main__':
    main()
