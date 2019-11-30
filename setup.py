from distutils.core import setup
setup(
  name = 'mountainproject',
  packages = ['mountainproject', 'mountainproject.models', 'mountainproject.resources', 'mountainproject.util'],   # Chose the same as "name"
  version = '1.0.1',      
  license='MIT',        
  description = 'MountainProject API Python wrapper',
  author = 'Caleb Wang',                   # Type in your name
  author_email = 'caleb@caleb.wang',
  url = 'https://github.com/calebwang/mountainproject',
  download_url = 'https://github.com/calebwang/mountainproject/archive/v1.0.0.tar.gz',
  keywords = ['mountainproject'],
  requires=[            # I get to this in a second
    'requests',
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
