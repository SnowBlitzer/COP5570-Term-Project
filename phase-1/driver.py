from path_tools import get_filenames_from_path
from file_parser import parse_files

import sys,os

if __name__ == '__main__':
	if len(sys.argv) is not 3:
		print "usage: python %s pathname year" % os.path.basename(__file__)
	else:
		path = sys.argv[1]
		year = sys.argv[2]
		#parse_files(path)
		files = get_filenames_from_path(path)
		data  = parse_files(files, year)
