# inotify_backup
A Python script to back up file modifications reported by inotify.
## Usage
Run it with `python -m inotify_backup watch_dir (Must have trailing slash "\".) backup_dir (Must have trailing slash "/".) wait (The duration between keeping an old backup of the same file in minutes.)`.
