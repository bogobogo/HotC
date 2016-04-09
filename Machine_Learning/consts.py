import os
import os.path
import metadata_utils

HOTC_ROOT_DIR = 'C:\Users\Michael\Dropbox\hotc'
HOTC_ORIGINAL_RECORDINGS_DIR = os.path.join(HOTC_ROOT_DIR,'original_recordings')
HOTC_SPLIT_RECORDINGS_DIR = 'C:\Users\Michael\Desktop\Projects\HotC\Machine_Learning\split_recordings'
HOTC_ORIGINAL_META_FILE = os.path.join(HOTC_ORIGINAL_RECORDINGS_DIR, 'original_meta.csv')
HOTC_SPLIT_META_FILE = os.path.join(HOTC_SPLIT_RECORDINGS_DIR, 'split_meta.csv')

DEFAULT_SPLITTED_PART_LENGTH = 3

def _init_meta_file(filename):
	param_line = ''
	for param in metadata_utils.METADATA_PARAMETERS:
		param_line += param + ', '

	param_line = param_line[:-1]

	f = open(filename, 'w')
	f.write(param_line)
	f.close()

def init_data():
	"""
	@brief: checks if all the required folders and files exists, and creates them if they dont
	"""

	if not os.path.exists(HOTC_ROOT_DIR):
		os.makedirs(HOTC_ROOT_DIR)

	if not os.path.exists(HOTC_ORIGINAL_RECORDINGS_DIR):
		os.makedirs(HOTC_ORIGINAL_RECORDINGS_DIR)

	if not os.path.exists(HOTC_SPLIT_RECORDINGS_DIR):
		os.makedirs(HOTC_SPLIT_RECORDINGS_DIR)

	if not os.path.exists(HOTC_ORIGINAL_META_FILE):
		_init_meta_file(HOTC_ORIGINAL_META_FILE)

	if not os.path.exists(HOTC_SPLIT_META_FILE):
		_init_meta_file(HOTC_SPLIT_META_FILE)

if __name__ == '__main__':
	init_data()


