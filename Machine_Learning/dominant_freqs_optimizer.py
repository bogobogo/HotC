import dominant_freqs_runner
import os
import shutil
import consts
import split_recording

EPOCHS = 100
LOG_CSV = 'results_log.csv'
VERBOSE_OUTPUT = True

ALL_FILE_LENGTHS = [0.8, 1.2, 1.6, 2, 3.2]
ALL_PART_LENGTHS = [0.05, 0.1, 0.2, 0.4]
ALL_DOMINANT_FREQUENCIES = [4, 8, 12, 16]

def test_setup():
	try:
		shutil.rmtree(consts.HOTC_SPLIT_RECORDINGS_DIR)	
	except:
		pass

	consts.init_data()

def run_test(file_length, part_length, dominant_freqs, verbose):
	test_data = dominant_freqs_runner.run(
		EPOCHS, 
		'dfl.xml', 
		file_length,
		part_length,
		dominant_freqs,
		False,
		verbose
	)

	log_results(test_data[0][-1], test_data[1], test_data[2])

def init_log():
	f = open(LOG_CSV, 'w')
	f.write('error,dataset_add_time,learning_time\n')
	f.close()

def log_results(last_error, dataset_add_time, learning_time):
	f = open(LOG_CSV, 'a')
	output = '{0},{1},{2}\n'.format(last_error, dataset_add_time, learning_time)
	f.write(output)
	f.close()

def run():
	init_log()
	for file_length in ALL_FILE_LENGTHS:
		test_setup()
		split_recording.split_all_files(file_length)
		for part_length in ALL_PART_LENGTHS:
			for dominant_freqs in ALL_DOMINANT_FREQUENCIES:
				run_test(file_length, part_length, dominant_freqs, VERBOSE_OUTPUT)

if __name__ == '__main__':
	run()




