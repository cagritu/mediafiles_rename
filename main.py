#Renaming photo files in A FOLDER according to its 'date taken' attributes if exist.
#Does not run in subfolders. If there are photos in multiple folders/subfolders it needs to be run seperately.


import os
import exifread
import pathlib	


directoryInput = 'C:\\Users\\konko\\Python\\Project_Photo_Video_Rename\\Photos'
extension_list = ['.JPG','.jpg','','.jpeg']
prefix = ''	
									#DCIM or BT
os.chdir(directoryInput)



print(os.listdir())
i=0
for filename in os.listdir():

	i=i+1
	iStr=str(i).zfill(4)
	extension = pathlib.PurePosixPath(filename).suffix
	error_flag=0	

	if extension in extension_list:
			
		with open(filename, 'rb') as image:
			exif = exifread.process_file(image) #reading image file attributes
			
			try:								# try retrieving date_taken attribute
				dt = str(exif['EXIF DateTimeOriginal'])
			
			except:								#flag set on error
				error_flag = 1

			else:								#ıf no error, create new naming format
				day, dtime = dt.split(" ", 1)
				hour, minute, second = dtime.split(":", 2)
				year, month, day = day.split(":",2 )
				new_filename = prefix + year + "_" + month +  "_" + day + "__" + hour + "_" + minute + "_" + second + extension

 
		if error_flag ==1: 						#if error occured, print result and skip.
			print(iStr + "-" + filename + " --> has no date_taken attribute")

		elif filename != new_filename:			#if no error ,change the name and print result. 
			
			try:
				os.rename(filename, new_filename)
			except FileExistsError:
				print(iStr + "-" + filename + " -->  another file with new name already exist")
			except:
				print(iStr + "-" + filename + " -->  unkown error")	
			else:
				print(iStr + "-" + filename + "-- changed --> " + new_filename)

		else:									#no need for name change
			print(iStr + "-" + filename + " --> has correct naming")
	else:										#extension is not expected.
		print(iStr + "-" + filename + " --> has different extension")
	
