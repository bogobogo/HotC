import dominant_freqs_learner
import consts
import os
import sys
import argparse
import time
from pybrain.tools.customxml import NetworkWriter
from pybrain.tools.customxml import NetworkReader
import matplotlib.pyplot as plt

PROGRAM_DESCRIPTION = 'Runs the domianant frequencies learner'
EPOCHS_HELP = 'For how many epochs to run the learner'
NETWORK_FILE_HELP = 'The file to save the network to'

def parse_args(args):
	parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
	parser.add_argument('-e', type=int, required=True, metavar='epochs', help=EPOCHS_HELP)
	parser.add_argument('-f', type=str, required=False, default='dfl.xml', metavar='network_file', help=NETWORK_FILE_HELP)
	parser.add_argument('-l', type=int, required=True, metavar='file length')
	parser.add_argument('-p', type=float, required=True, metavar='part length')
	parser.add_argument('-df', type=int, required=True, metavar='dominant frequencies', help='number of domianant frequencies')
	parser.add_argument('-g', action='store_true', help='Display error graph')
	parser.add_argument('-v', action='store_true', help='Verbose output')

	return parser.parse_args()

def get_all_split_files():
	all_files = os.listdir(consts.HOTC_SPLIT_RECORDINGS_DIR)
	for f in all_files:
		if not f.endswith('.wav'):
			all_files.remove(f)

	return all_files

def plot_graph(erros):
	plt.plot(erros)
	plt.xlabel('epoch')
	plt.ylabel('error')
	plt.show()

def run(epochs, network_file, file_length, part_length, dominant_frequncies, show_graph, verbose_output):
	learner = dominant_freqs_learner.DominantFreqsLearner(file_length, part_length ,dominant_frequncies)
	all_files = get_all_split_files()
	if verbose_output:
		print 'started adding files to dataset at ' + time.ctime()

	for f in all_files:
		try:
			learner.add_split_file(f, channel=None, verbose=verbose_output)
		except:
			pass

	if verbose_output:
		print 'finished adding file to dataset at ' + time.ctime()

	errors = []
	for epoch in range(epochs):
		error = learner.train_single_epoch()
		if verbose_output:
			print '{0}: epoch {1} : {2}'.format(time.ctime(), epoch, error)

		errors.append(error)

	NetworkWriter.writeToFile(learner._net, network_file)
	if show_graph:
		plot_graph(errors)

	return errors

def main(arguments):
	args = parse_args(arguments)
	run(args.e, args.f, args.l, args.p, args.df, args.g, args.v)

if __name__ == '__main__':
	main(sys.argv[1:])

