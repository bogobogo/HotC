from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

import numpy as np

import os.path

import wav_to_fft
import metadata_utils
import consts

class WavLearner(object):

	def __init__(self, file_length, part_length, max_freq=consts.WAV_LEARNER_MAX_FREQS):
		"""
		@param file_length: the length of each file (in seconds)	
		@param part_length: the length is seconds of each part
		@param max_freq: the maximum frequency that should be analyzed
		@param channel: the channel to inspect
		@note: the part length should divide the file length without any carry
		@note: number_of_inputs at 17500 crashed my pc
		"""

		self._part_length = part_length
		self._max_freq = max_freq

		number_of_parts = int(file_length / part_length)
		number_of_inputs = number_of_parts * max_freq
		self._net = buildNetwork(number_of_inputs, number_of_inputs, 1)
		self._dataset = SupervisedDataSet(number_of_inputs,1)

	def add_split_file(self, filename, channel=None):
		full_path = os.path.join(consts.HOTC_SPLIT_RECORDINGS_DIR, filename)
		metadata = metadata_utils.get_recording_data(consts.HOTC_SPLIT_META_FILE, filename)
		expected_output = metadata_utils.get_param(metadata, 'rank')
		return self.add_file(full_path, expected_output, channel)

	def add_file(self, filename, expected_output, channel=None):
		"""
		@brief: adds a file to the dataset.
				if the file length is longer then specified, only the beginning is inspected
				if the file length is smaller then specified, the file wont be inspected
		"""

		data = wav_to_fft.wav_to_normalized_fft(filename, self._part_length, channel=channel)
		all_parts_data = []
		for part in data:
			all_parts_data = np.append(all_parts_data, part[:self._max_freq])

		self._dataset.addSample(all_parts_data, [expected_output])

	def train(self):
		trainer = BackpropTrainer(self._net, self._dataset)
		erros = trainer.trainUntilConvergence()
		return erros

