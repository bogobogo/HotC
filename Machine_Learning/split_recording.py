import os.path
import consts
import wav_utils
import argparse
import sys
import metadata_utils

PROGRAM_DESCRIPTION = """Splits a file from the original directory to the split directory,
						 and copies the metadata"""

PART_LENGTH_DESCRIPTION = 'The lgnth of each splitted part. Uses default if not specified'

def parse_arguments(arguments):
	parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
	parser.add_argument('-f', type=str, required=True, metavar='filename', help='File from the recordings directory')
	parser.add_argument('-l', type=float, required=False, metavar='Part Length', help=PART_LENGTH_DESCRIPTION)
	return parser.parse_args(arguments)

def split_file(filename, part_length):
	if part_length is None:
		part_length = consts.DEFAULT_SPLITTED_PART_LENGTH

	filename_full_path = os.path.join(consts.HOTC_ORIGINAL_RECORDINGS_DIR, filename)
	if not os.path.exists(filename_full_path):
		print filename_full_path + ' does not exists!'
		return

	metadata = metadata_utils.get_recording_data(consts.HOTC_ORIGINAL_META_FILE, filename)
	wav_utils.split_wav_file_with_metadata(
		filename, 
		part_length, 
		metadata, 
		consts.HOTC_SPLIT_META_FILE, 
		dest_dir=consts.HOTC_SPLIT_RECORDINGS_DIR, 
		basename=None
	)


def main(arguments):
	args = parse_arguments(arguments)
	split_file(args.f, args.l)

if __name__ == '__main__':
	main(sys.argv[1:])
