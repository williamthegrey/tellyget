from pathlib import Path

import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name='tv-guide-updater',
    version='1.0.0',
    author='William Lu',
    author_email='wy.william.lu@gmail.com',
    description='A toolset for fetching and updating m3u playlist and xmltv guide from the IPTV network',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/williamthegrey/tv-guide-updater',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=['beautifulsoup4', 'netifaces', 'pycryptodome', 'requests-toolbelt'],
    entry_points={
        'console_scripts': [
            'tv-guide-updater=tv_guide_updater.tv_guide_updater:main',
            'tv-config-generator=tv_guide_updater.tv_config_generator:main',
            'tv-encryption-key-finder=tv_guide_updater.tv_encryption_key_finder:main'
        ]
    }
)
