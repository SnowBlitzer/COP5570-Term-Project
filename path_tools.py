import os, concurrent.futures

file_paths = []

def qualify(file_path):
	"""
	Approves files to be included in analysis.
	"""
	return os.path.isfile(file_path) and (file_path.endswith(".lorien"))

def collect(file_path):
	global file_paths
	if qualify(file_path):
		file_paths.append(file_path)


def get_filenames_from_path(path):

	# Add missing / if needed
	if not path.endswith("/"):
		path += "/"

	# Select qualifying files.
	files = (path + filename for filename in os.listdir(path) if qualify(path + filename)) # single thread approach

	# code from stack_overflow
	# executor = concurrent.futures.ThreadPoolExecutor(10)
	# futures = [executor.submit(collect, path + filename) for filename in os.listdir(path)]
	# concurrent.futures.wait(futures)

	global file_paths
	return file_paths
