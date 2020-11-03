
DEBUG = True
LOG_TO_FILE = False
filename = "dbg_log.txt"

def debug(s):
    if DEBUG:
        print (s)
	if LOG_TO_FILE:
        file_handler = open(filename, 'w')
		file_handler.write(s)
		file_handler.close()

	