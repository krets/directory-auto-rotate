directory-auto-rotate
=====================

Auto-rotate files into a ".old" directory to keep download directories clear.

<pre>
usage: autorotatedir.py [-h] [-o OUTPUTDIR] [-v] [-k] [-a AGE] [-e EXPIRATION]
                        [--undo]
                        directory

Download Directory Rotator - This tool will help cleanup desktop and download
directories by moving old files out of the way.

positional arguments:
  directory             Directory to work on.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUTDIR, --outputdir OUTPUTDIR
                        Destination folder for rotated files. This is treated
                        as relative to the inpected directory. Default: (.old)
  -v, --verbose
  -k, --keepempty       Keep empty directories. Empty directories will
                        otherwise be removed.
  -a AGE, --age AGE     Age (in days) of files to rotate. Any file or folders
                        older than this age will be move to the ouput
                        directory. Default: (30)
  -e EXPIRATION, --expiration EXPIRATION
                        Age (in days) of files to EXPIRE. If set to a value
                        other than 0 files of this age will be deleted from
                        the ouput directory. Default: (0)
  --undo                Attempt to undo the process based on the given
                        parameters.
</pre>