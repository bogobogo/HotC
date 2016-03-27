import wave
import os.path


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

def wav_file_generator(filename, part_length):
	"""
	@brief: generates a wav file splitter
	@param filename: the name of the wav file
	@param part_length: the length of each part
	"""

	wav_file = wave.open(filename, 'r')
	number_of_frames_per_part = int(wav_file.getframerate() * part_length)
	while True:
		data = wav_file.readframes(number_of_frames_per_part)
		if len(data) == 0:
			wav_file.close()
			return

		yield data






