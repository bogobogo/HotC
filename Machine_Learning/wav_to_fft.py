from scipy.fftpack import fft
from scipy.io import wavfile
import wave

def wav_to_fft(filename, part_length, channel=None):
	"""
	@brief: converts wav file to parts of fft
	@param filename: the name of the wav file
	@param part_length: the length of each part
	@param channel: which channel to look at. if nothing is entreted, use the first
	@note: the output is not normalized
	"""

	if part_length == 0:
		raise Exception('part length cant be 0')

	if channel is None:
		channel = 0

	fs, all_data = wavfile.read(filename)
	if len(all_data.T) <= channel:
		raise Exception('channel {0} doesnt exists'.format(channel))

	frames_per_part = int(fs * part_length)
	channel_data = all_data.T
	if len(all_data.T) == 2:
		channel_data = all_data.T[channel]

	all_ffts = []

	for cur_pos in range(0,len(channel_data), frames_per_part):
		all_ffts.append(fft(channel_data[cur_pos:cur_pos+frames_per_part]))

	return all_ffts

def wav_to_normalized_fft(filename, part_length, channel=None):
	"""
	@brief: converts wav file to parts of fft
	@param filename: the name of the wav file
	@param part_length: the length of each part
	@param channel: which channel to look at. if nothing is entreted, use the first
	@note: the output is normalized
	"""

	if part_length == 0:
		raise Exception('part length cant be 0')

	if channel is None:
		channel = 0

	wave_file = wave.open(filename, 'r')
	sample_width = wave_file.getsampwidth()
	wave_file.close()

	fs, all_data = wavfile.read(filename)
	if len(all_data.T) <= channel:
		raise Exception('channel {0} doesnt exists'.format(channel))

	frames_per_part = int(fs * part_length)
	channel_data = all_data.T
	if len(all_data.T) == 2:
		channel_data = all_data.T[channel]

	# normalized data
	channel_data = [(ele/2.0**(sample_width*8))*2-1 for ele in channel_data] 
	all_ffts = []

	for cur_pos in range(0,len(channel_data), frames_per_part):
		all_ffts.append(fft(channel_data[cur_pos:cur_pos+frames_per_part]))

	real_ffts = []
	for cur_fft in all_ffts:
		real_ffts.append(abs(cur_fft[:len(cur_fft)/2]))

	return real_ffts









