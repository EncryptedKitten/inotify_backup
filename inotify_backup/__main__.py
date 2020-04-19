#EncryptedKitten\'s Python script to back up file modifications reported by inotify. You will need to install inotify with pip. All single quotes have been escaped "\'", so you can paste this into a shell surrounded by single quotes.
import inotify.adapters, shutil, datetime, os, sys
from pathlib import Path

def utcnow_time_function():
	return datetime.datetime.utcnow()

#wait exists so it doesn\'t rapidly backup the same file and waste all of your disk space.
def inotify_backup(watch_dir, backup_dir, time_function, wait):
	i = inotify.adapters.InotifyTree(watch_dir)
	
	recent_files = {}
	
	for event in i.event_gen(yield_nones=False):
		if ("IN_ISDIR" not in event[1]) and ("IN_MODIFY" in event[1]):
			#If the file doesn\'t exist when it tries to copy the file, it will error.
			try:
				path = ""
				for path_segment in event[3:]:
					path += path_segment + "/"
				
				path = path[:-1]

				
				current_time = time_function()
				
				Path(backup_dir + path + "/" + str(current_time)).mkdir(parents=True, exist_ok=True)
				shutil.copyfile(watch_dir + path, backup_dir + path + "/" + str(current_time) + "/" + os.path.basename(path))
				
				print(backup_dir + path + "/" + str(datetime.datetime.utcnow()))
				
				if path in recent_files:
					if current_time - recent_files[path][0] < wait:
						shutil.rmtree(backup_dir + path + "/" + str(recent_files[path][1]), ignore_errors=True)
						recent_files[path][1] = current_time
					else:
						recent_files[path] = [current_time, current_time]
				else:
					recent_files[path] = [current_time, current_time]
				
				#To avoid recent_files getting too big and taking up all of your memory.
				if len(recent_files) > 1000:
					if current_time - recent_files[path] > wait:
						del(recent_files[path])
			except FileNotFoundError:
				pass

def main():
	if len(sys.argv) == 4:
		watch_dir = sys.argv[1]
		backup_dir = sys.argv[2]
		
		time_function = utcnow_time_function
		
		wait = datetime.timedelta(minutes=int(sys.argv[3]))
		
		i = inotify.adapters.InotifyTree(watch_dir)
		
		inotify_backup(watch_dir, backup_dir, time_function, wait)
	else:
		print(sys.argv[0] + " watch_dir (Must have trailing slash \"/\".) backup_dir (Must have trailing slash \"/\".) wait (The duration between keeping an old backup of the same file in minutes.)")
	
if __name__ == "__main__":
	main()