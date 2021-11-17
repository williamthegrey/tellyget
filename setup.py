import setuptools

long_description = '''# TellyGet

A toolset for fetching and updating m3u playlist and xmltv guide from the IPTV network.

Please visit [TellyGet on GitHub](https://github.com/williamthegrey/tellyget) for detail.
'''

setuptools.setup(
    name='tellyget',
    version='1.0.0',
    author='William Lu',
    author_email='wy.william.lu@gmail.com',
    description='A toolset for fetching and updating m3u playlist and xmltv guide from the IPTV network',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/williamthegrey/tellyget',
    packages=setuptools.find_packages(),
    license='GPLv3',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Multimedia :: Video',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
    keywords='set-top-box iptv m3u xmltv',
    python_requires='>=3.6',
    install_requires=['beautifulsoup4', 'netifaces', 'pycryptodome', 'requests-toolbelt'],
    entry_points={
        'console_scripts': [
            'tellyget=tellyget.tellyget:main',
            'tellyget-config=tellyget.tellyget_config:main',
            'tellyget-decrypt=tellyget.tellyget_decrypt:main'
        ]
    }
)
