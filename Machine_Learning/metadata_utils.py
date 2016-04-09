
METADATA_PARAMETERS = {
	'filename' : str, 
	'rank' : float
}

def get_recording_data(csv_file, recording_file):
	str_data = None
	f = open(csv_file)
	line = f.readline()
	while line != '':
		if recording_file in line:
			str_data = line.split(',')

		line = f.readline()

	f.close()

	if str_data is None:
		raise Exception('File %s not found' %(recording_file))

	return [METADATA_PARAMETERS[param](str_data) for param in METADATA_PARAMETERS] 

