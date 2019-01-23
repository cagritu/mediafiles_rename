#Renaming photo and files in given A FOLDER according to its 'date taken(photos)' and 'media_created(videos)' attributes if exist.
#Does not run in subfolders. If there are photos/videos in multiple folders/subfolders it needs to be run seperately.


import os
import pathlib
import exifread	
import exiftool 	#exiftool cmd-line tool needs to be installed. https://sno.phy.queensu.ca/~phil/exiftool/
import hashlib		


directoryInput = 'C:\\Users\\konko\\Google Drive\\Python\\Project_Photo_Video_Rename\\Photos'
prefix = ''	 #DCIM or BT or blank
extension_photos = ['.JPG','.jpg', '.PNG']  
extension_videos = [ '.mp4' , '.MP4', '.MOV']
extension_list = extension_photos + extension_videos 



def hash_file(filename): 
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()



def get_date(media_file, ext):
	metadata = "" ;	media_date = "" ;	error=0
		
	try:	# try retrieving date_taken attribute
		if ext in extension_photos:
			with open(filename, 'rb') as image:
				exif = exifread.process_file(image) #reading image file attributes
				media_date = str(exif['EXIF DateTimeOriginal'])

		if ext in extension_videos:
			with exiftool.ExifTool() as et:  
				metadata = et.get_metadata(media_file) #reading video file attributes
				media_date= metadata['QuickTime:MediaCreateDate']

	except:	#flag set on error
		error = 1		

	else:
		error = 0	

	return str(media_date) , error

def change_name(change_from, change_to):
		try:								
			os.rename(change_from, change_to)
		except PermissionError:				#Permission Error
			print(iStr + "-" + change_from + " --> " + change_to + " :Permission Error - Access Denied.")
		except:								#Other Errors
			print(iStr + "-" + change_from + " --> " + change_to + "  unknown error.")
		else:								#print on name change
			print(iStr + "-" + change_from + "-- changed --> " + change_to)



def get_file_index(newname, ext):
	last_file_index = 0
	for i in range(99):
		if os.path.isfile(new_name + "_" +str(i).zfill(2) + extension):
			last_file_index = i
	return last_file_index


hasher = hashlib.md5()
i=0									
os.chdir(directoryInput)

for filename in os.listdir():

	i+=1
	iStr=str(i).zfill(4)
	extension = pathlib.PurePosixPath(filename).suffix
	error_flag=0	

	if extension not in extension_list:
		#file extension is not defined in list.
		print(iStr + "-" + filename + " --> has different extension.")
	else:										
		dt , error_flag = get_date(filename,extension)

		if error_flag==0:
			day, dtime = dt.split(" ", 1)
			hour, minute, second = dtime.split(":", 2)
			year, month, day = day.split(":",2 )
			new_name = prefix + year + "_" + month +  "_" + day + "__" + hour + "_" + minute + "_" + second
			new_filename = new_name + extension


		if error_flag ==1 : 						#if error occured, print result and skip.
			print(iStr + "-" + filename + " --> has no date_taken attribute")

		elif filename != new_filename:			#if no error ,change the name and print result. 
			
			if not os.path.isfile(new_name + "_00" + extension) and not os.path.isfile(new_filename) :
				change_name(filename, new_filename)
				pfix = 0 
			
			elif not os.path.isfile(new_name + "_00" + extension) or os.path.isfile(new_filename):
				
				if hash_file(filename) != hash_file(new_filename):
					print('test ')
					change_name(new_filename, new_name + "_" + str(pfix).zfill(2) + extension)
					pfix=pfix+1
					change_name(filename, new_name + "_" + str(pfix).zfill(2) + extension)		
				else:
					print(iStr + "-" + filename + " -->  same file with new name(" + new_filename + ") already exist.")

			elif os.path.isfile(new_name + "_01" + extension):
					pfix = get_file_index(new_name, extension) + 1
					change_name(filename, new_name + "_" + str(pfix).zfill(2) + extension)	

		else:									#no need for name change
			print(iStr + "-" + filename + " --> has correct naming.")


	
