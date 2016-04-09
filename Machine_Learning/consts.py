import os
import os.path

HOTC_ROOT_DIR = 'C:\Users\Michael\Dropbox\hotc'
HOTC_ORIGINAL_RECORDINGS_DIR = 'original_recordings'
HOTC_SPLIT_RECORDINGS_DIR = 'split_recordings'
HOTC_ORIGINAL_META_FILE = 'original_meta.csv'
HOTC_SPLIT_META_FILE = 'split_meta.csv'

META_PARAMETERS = ('filename', 'rank')

def _init_meta_file(filename):
	param_line = ''
	for param in META_PARAMETERS:
		param_line += param + ', '

	param_line = param_line[:-1]

	f = open(filename, 'w')
	f.write(param_line)
	f.close()

def init_data():
	"""
	@brief: checks if all the required folders and files exists, and creates them if they dont
	"""

	original_recordings_full_path = os.path.join(HOTC_ROOT_DIR, HOTC_ORIGINAL_RECORDINGS_DIR)
	split_recordings_full_path = os.path.join(HOTC_ROOT_DIR, HOTC_SPLIT_RECORDINGS_DIR)
	original_meta_full_path = os.path.join(original_recordings_full_path, HOTC_ORIGINAL_META_FILE)
	split_meta_full_path = os.path.join(split_recordings_full_path, HOTC_SPLIT_META_FILE)

	if not os.path.exists(HOTC_ROOT_DIR):
		os.makedirs(HOTC_ROOT_DIR)

	if not os.path.exists(original_recordings_full_path):
		os.makedirs(original_recordings_full_path)

	if not os.path.exists(split_recordings_full_path):
		os.makedirs(split_recordings_full_path)

	if not os.path.exists(original_meta_full_path):
		_init_meta_file(original_meta_full_path)

	if not os.path.exists(split_meta_full_path):
		_init_meta_file(split_meta_full_path)

if __name__ == '__main__':
	init_data()


