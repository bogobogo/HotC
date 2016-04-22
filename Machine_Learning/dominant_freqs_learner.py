from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

import numpy as np

import os.path

import wav_to_fft
import metadata_utils
import consts

class DominantFreqsLearner(object):

	def _find_minimum_freq(self, freqs):
		"""
		@brief: finds the smallest freq index 
		"""
		min_index = 0
		min_amplitude = freqs[0][1]

		for f in range(len(freqs)):
			if freqs[f][1] < min_amplitude:
				min_amplitude  = freqs[f][1]
				min_index = f

		return min_index

	def _order_max_freqs(self, freqs):
		to_return = []
		while len(freqs) > 0:
			max_index = 0
			max_value = freqs[0][1]
			for f in range(len(freqs)):
				if max_value < freqs[f][1]:
					max_index = f
					max_value = freqs[f][1]

			to_return.append(freqs[max_index][0])		
			freqs.pop(max_index)

		return to_return

	def _find_max_freqs(self, frame, number_of_freqs):
		"""
		@brief: finds the maximum number of freqs in a frame
		@param frame: an array of all the freqs
		@param number_of_freqs: how much maximum freqs to find
		@return: an array with the freqs, ordered by amplitude (first is the strongest)
		@note: this was tested
		"""

		max_freqs = number_of_freqs * [(0,0)]
		min_amplitude = 0
		min_index = 0

		for f in range(len(frame)):
			if frame[f] > min_amplitude:
				max_freqs[min_index] = (f, frame[f])
				min_index = self._find_minimum_freq(max_freqs)
				min_amplitude = max_freqs[min_index][1]

		return self._order_max_freqs(max_freqs)

	def _get_file_activation(self, filename, channel=None):
		data = wav_to_fft.wav_to_normalized_fft(filename, self._part_length, channel=channel)
		all_dominant_freqs = []
		for part in data:
			all_dominant_freqs += self._find_max_freqs(part, self._max_freqs)

		return all_dominant_freqs

	def __init__(self, file_length, parts_length, max_freqs=consts.DOMINANT_FREQS_LEANRNER_MAX_FREQS):
		"""
		@param file_length: the length of each file (in seconds)	
		@param part_length: the length is seconds of each part
		@param max_freq: the number of dominant freqs to save from each part
		@param channel: the channel to inspect
		@note: the part length should divide the file length without any carry
		"""

		self._part_length = parts_length
		self._max_freqs = max_freqs
		self._started_training = False

		number_of_parts = int(file_length/parts_length)
		number_of_inputs = number_of_parts * self._max_freqs
		self._net = buildNetwork(number_of_inputs, number_of_inputs, 1)
		self._dataset = SupervisedDataSet(number_of_inputs,1)


	def add_split_file(self, filename, channel=None, verbose=True):
		full_path = os.path.join(consts.HOTC_SPLIT_RECORDINGS_DIR, filename)
		metadata = metadata_utils.get_recording_data(consts.HOTC_SPLIT_META_FILE, filename)
		expected_output = metadata_utils.get_param(metadata, 'rank')
		return self.add_file(full_path, expected_output, channel)

	def add_file(self, filename, expected_output, channel=None, verbose=True):
		"""
		@brief: adds a file to the dataset.
				if the file length is longer then specified, only the beginning is inspected
				if the file length is smaller then specified, the file wont be inspected
		"""

		all_dominant_freqs = self._get_file_activation(filename, channel)
		self._dataset.addSample(all_dominant_freqs, [expected_output])
		print 'added ' + filename

	def train_single_epoch(self):
		if self._started_training:
			return self._trainer.train()

		else:
			self._started_training = True
			self._trainer = BackpropTrainer(self._net, self._dataset)
			return self._trainer.train()

	def train(self):
		self._trainer = BackpropTrainer(self._net, self._dataset)
		erros = self._trainer.trainUntilConvergence()
		return erros

	def calculate_split_file(self, filename, channel=None):
		full_path = os.path.join(consts.HOTC_SPLIT_RECORDINGS_DIR, filename)
		return self.calculate_file(full_path, channel)

	def calculate_file(self, filename, channel=None):
		file_activation = self._get_file_activation(filename, channel)
		return self._net.activate(file_activation)[0]


		



