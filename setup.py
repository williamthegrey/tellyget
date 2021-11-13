import setuptools

setuptools.setup(
    name='tv-guide-updater-william-lu',
    version='1.0.0',
    author='William Lu',
    author_email='wy.william.lu@gmail.com',
    description='A tool for fetching and updating m3u playlist and xmltv guide from the IPTV network of China Telecom',
    url='https://github.com/williamthegrey/tv-guide-updater',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=['bs4', 'netifaces', 'pycryptodome', 'requests-toolbelt'],
    entry_points={
        'console_scripts': [
            'tv-guide-updater=tv_guide_updater.tv_guide_updater:main',
            'tv-config-generator=tv_guide_updater.tv_config_generator:main',
            'tv-encryption-key-finder=tv_guide_updater.tv_encryption_key_finder:main'
        ]
    },
    package_data={
        'tv_guide_updater': ['etc/tv-guide-updater.conf.example']
    }
)
