from collections import OrderedDict

"""
It is assumes that the first parameter is the filename
changing that will cause bugs
"""
METADATA_PARAMETERS = OrderedDict([
	('filename', str),
	('rank', float)
])

def get_recording_data(csv_file, recording_file):
	str_data = None
	f = open(csv_file)
	line = f.readline()
	while line != '':
		if recording_file in line:
			str_data = line[:-1].split(',')

		line = f.readline()

	f.close()

	if str_data is None:
		raise Exception('File %s not found' %(recording_file))

	return_data = []
	for param in range(len(str_data)):
		param_type = METADATA_PARAMETERS[METADATA_PARAMETERS.keys()[param]]
		str_param = str_data[param]
		return_data.append(param_type(str_param))

	return return_data

def get_param(data, param_name):
	#find param name index
	c = 0
	for param in data:
		if param == param_name:
			return data[param_name]

		c+=1

	raise Exception('param {0} not found in {1}'.format(param_name, data))

