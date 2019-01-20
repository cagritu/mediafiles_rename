#Renaming photo and files in given A FOLDER according to its 'date taken(photos)' and 'media_created(videos)' attributes if exist.
#Does not run in subfolders. If there are photos/videos in multiple folders/subfolders it needs to be run seperately.


import os
import pathlib
import exifread	
import exiftool 	#exiftool cmd-line tool needs to be installed. https://sno.phy.queensu.ca/~phil/exiftool/




def get_date(media_file, ext):
	metadata = "" ;	media_date = "" ;	error=0
		
	try:	# try retrieving date_taken attribute
		if ext in extension_photos:

			with open(filename, 'rb') as image:
				exif = exifread.process_file(image) #reading image file attributes
				media_date = str(exif['EXIF DateTimeOriginal'])

		if ext in extension_videos:
			with exiftool.ExifTool() as et:  
				metadata = et.get_metadata(media_file)
				media_date= metadata['QuickTime:MediaCreateDate']	
	except:	#flag set on error
		error = 1		
	else:
		error = 0	

	return str(media_date) , error




directoryInput = 'C:\\Users\\konko\\Python\\Project_Photo_Video_Rename\\Videos'
prefix = ''	 #DCIM or BT or blank
i=0
extension_photos = ['.JPG','.jpg']  
extension_videos = [ '.mp4']
extension_list = extension_photos + extension_videos 


									
os.chdir(directoryInput)

for filename in os.listdir():

	i+=1
	iStr=str(i).zfill(4)
	extension = pathlib.PurePosixPath(filename).suffix
	error_flag=0	

	if extension in extension_list:

		dt , error_flag = get_date(filename,extension)

		if error_flag==0:
			day, dtime = dt.split(" ", 1)
			hour, minute, second = dtime.split(":", 2)
			year, month, day = day.split(":",2 )
			new_filename = prefix + year + "_" + month +  "_" + day + "__" + hour + "_" + minute + "_" + second + extension

		if error_flag ==1: 						#if error occured, print result and skip.
			print(iStr + "-" + filename + " --> has no date_taken attribute")

		elif filename != new_filename:			#if no error ,change the name and print result. 
			
			try:								#Change
				os.rename(filename, new_filename)
			except FileExistsError:				#A file with same name already exist
				print(iStr + "-" + filename + " -->  another file with new name(" + new_filename + ") already exist.")
			except PermissionError:				#Permission Error
				print(iStr + "-" + filename + " -->  Permission Error - Access Denied.")
			except:								#Other Errors
				print(iStr + "-" + filename + " -->  unkown error.")	
			else:								#print on name change
				print(iStr + "-" + filename + "-- changed --> " + new_filename)

		else:									#no need for name change
			print(iStr + "-" + filename + " --> has correct naming.")

	else:										#file extension is not defined in list.
		print(iStr + "-" + filename + " --> has different extension.")
	
