import setuptools


with open('README.md', 'r') as fh:
	long_description = fh.read()

setuptools.setup(
	name="inotiy_backup",
	version="0.0.1",
	author="EncryptedKitten",
	description="A Python script to back up file modifications reported by inotify.",
	long_description=long_description,
	long_description_content_type='text/markdown',
	url="https://github.com/EncryptedKitten/inotify_backup",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
	],
	python_requires=">=3.4",
	install_requires=[
		  "inotify"
	  ],
)