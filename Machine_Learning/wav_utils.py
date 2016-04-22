import wave
import os.path

import consts

DIGITS_IN_NAME = 5

def split_wav_file(filename, part_length, dest_dir=None, basename=None):
	"""
	@brief: splits a wav file into smaller 
	@param filename: the name of the file
	@param part_length: the length in seconds of each part
	@param dest_dir: the directory in which all parts should be. default is current directory
	@param basename: the name of the output files. they will be called <basename>_00000.wav
	@note: the maxium original file length is 833 hours
	"""

	if dest_dir is None:
		dest_dir = '.'
	if basename is None:
		basename = os.path.basename(filename)
	original_file = wave.open(filename, 'r')
	file_params = original_file.getparams()
	number_of_frames_per_part = int(original_file.getframerate() * part_length)
	total_number_of_frames = file_params[3]
	file_counter = 0
	data = 'init'

	while len(data) != 0:
		new_filename = basename + '_' + '0' * (DIGITS_IN_NAME-len(str(file_counter))) + str(file_counter) + '.wav'
		current_file = wave.open(os.path.join(dest_dir, new_filename), 'w')
		current_file.setparams(file_params)
		data = original_file.readframes(number_of_frames_per_part)
		total_number_of_frames -= number_of_frames_per_part
		current_file.writeframes(data)
		current_file.close()
		file_counter += 1

	original_file.close()


def  _add_line_to_metadata_file(filename, data):
	"""
	@brief: adds a line csv metadata file
	@param filename: the full path to the file
	@param data: the data to add in a list/tuple
	"""

	line_to_add = ''
	for param in data:
		line_to_add += str(param) + ','

	line_to_add = line_to_add[:-1] + '\n'

	f = open(filename, 'a')
	f.write(line_to_add)
	f.close()

def split_wav_file_with_metadata(filename, part_length, metadata, meta_file, dest_dir=None, basename=None):
	"""
	@brief: splits a wav file into smaller parts, but keeps their rank in the new meta.csv file
	@param filename: the name of the file
	@param part_length: the length in seconds of each part
	@param metadata: a list of all the metadata
	@param meta_file: the metadata file to add data to
	@param dest_dir: the directory in which all parts should be. default is current directory
	@param basename: the name of the output files. they will be called <basename>_00000.wav
	@note: the maxium original file length is 833 hours
	"""

	if dest_dir is None:
		dest_dir = '.'
	if basename is None:
		basename = os.path.basename(filename)
	original_file = wave.open(filename, 'r')
	file_params = original_file.getparams()
	number_of_frames_per_part = int(original_file.getframerate() * part_length)
	total_number_of_frames = file_params[3]
	file_counter = 0
	data = 'init'
	while len(data) != 0:
		new_filename = basename + '_' + '0' * (DIGITS_IN_NAME-len(str(file_counter))) + str(file_counter) + '.wav'
		current_file = wave.open(os.path.join(dest_dir, new_filename), 'w')
		current_file.setparams(file_params)
		data = original_file.readframes(number_of_frames_per_part)
		total_number_of_frames -= number_of_frames_per_part
		current_file.writeframes(data)
		current_file.close()
		file_counter += 1

		_add_line_to_metadata_file(meta_file, [new_filename]+metadata.values()[1:])

	original_file.close()

def wav_file_reader(filename, part_length):
	"""
	@brief: generates a wav file splitter
	@param filename: the name of the wav file
	@param part_length: the length of each part
	@note: this function will return twice the data for stereo files
	"""

	wav_file = wave.open(filename, 'r')
	number_of_frames_per_part = int(wav_file.getframerate() * part_length)
	while True:
		data = wav_file.readframes(number_of_frames_per_part)
		if len(data) == 0:
			wav_file.close()
			return

		yield data


def _split_into_channels(data, number_of_channels, sample_width):
	data_length = len(data)
	if data_length % (number_of_channels * sample_width) != 0:
		raise Exception("invalid length of data")

	channels = []
	for i in range(number_of_channels):
		channels.append('')

	next_channel = 0
	cur_pos = 0
	while cur_pos < data_length:
		channels[next_channel] += data[cur_pos:cur_pos+sample_width] 
		next_channel += 1
		if next_channel == number_of_channels:
			next_channel = 0
		cur_pos += sample_width

	return channels



def wav_file_channel_reader(filename, part_length):
	"""
	@brief: a generator that returns parts of a wave file
	@param filename: the name of the wav file
	@param part_length: the length of each part
	@note: this function will return each time data from 1 channel
	"""

	wav_file = wave.open(filename, 'r')
	number_of_frames_per_part = int(wav_file.getframerate() * part_length)
	channels = wav_file.getnchannels()
	sample_width = wav_file.getsampwidth()

	while True:
		all_data = wav_file.readframes(number_of_frames_per_part)
		parts = _split_into_channels(all_data, channels, sample_width)
		if len(all_data) == 0:
			wav_file.close()
			return

		yield parts






