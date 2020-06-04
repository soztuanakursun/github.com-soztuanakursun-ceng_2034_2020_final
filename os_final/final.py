import os
import requests
import uuid
import signal
import hashlib
from os import walk
# Until child process finishes downloading files, this function
# check directory for new downloaded files and calculates checksums
# After child process has ended, it defines same-content files
def directory_check():

	while is_running():
		for [_, _, filenames] in walk(os.getcwd()):
			for file in filenames:
				if file not in checked_list:
					print("File found : ", file)
					checked_list.append(file)
					content = open(file, "rb").read()
					checksum_number = checksum(content)
					checksum_list.append([checksum_number, checked_list[-1]])

	checked = []
	for i in range(len(checksum_list)):
		for j in range(len(checksum_list)):
			if checksum_list[i][0] == checksum_list[j][0] and i!=j and checksum_list[i][0] not in checked:
				checksum_list[i].append(checked_list[j])
		checked.append(checksum_list[i][0])

# this function return True, if child process is still running
# otherwise returns false
def is_running():
	try:
		os.waitpid(0, os.WNOHANG)
	except:
		return  False
	return True

# This function makes calculation for checksum
def checksum(data):
	return hashlib.md5(data).hexdigest()

# This function downloads the file for the given url
def download_file(url, file_name=None):
	r = requests.get(url, allow_redirects=True)
	file = file_name if file_name else str(uuid.uuid4().hex)
	extension = url.split(".")
	file = file + "." + extension[len(extension)-1]
	fptr = open(file, 'wb')
	fptr.write(r.content)
	fptr.close()
	print("File Downloaded : ", file)

# list of files which have been checked
# this means detcted in directory and calculated checksum
checked_list = []

# all directory item checksums
checksum_list = []

# file urls to be downloaded
url_list = ["http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
			"https://upload.wikimedia.org/wikipedia/tr/9/98/Mu%C4%9Fla_S%C4%B1tk%C4%B1_Ko%C3%A7man_%C3%9Cniversitesi_logo.png",
			"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg",
			"http://wiki.netseclab.mu.edu.tr/images/thumb/f/f7/MSKU-BlockchainResearchGroup.jpeg/300px-MSKU-BlockchainResearchGroup.jpeg",
			"https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hawai%27i.jpg/1024px-Hawai%27i.jpg"]

# process id - [a number] for parent - [zero] for child
pid = os.fork()

# if child process, download files
if pid == 0:
	print("child pid : ", os.getpid())
	download_file(url_list[0], None)
	download_file(url_list[1], None)
	download_file(url_list[2], None)
	download_file(url_list[3], None)
	download_file(url_list[4], None)

	# child process ends
	exit()

#parent keep checking directory files
directory_check()

# parent prints out the detected files of same content
print("\nFiles have same content\n")
for x in checksum_list:
	if len(x) > 2:
		print(len(x)-1, " files have same content : \n")
		for f in x[1:]:
			print(f)
		print("\n")

