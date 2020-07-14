from setuptools import setup

setup(
    name = 'webtron-AWS automation',
    version = '0.1',
    author = 'Laljit Suri',
    author_email = 'laljitssuri@yahoo.com',
    description = 'Tool to automate deployment of static website to AWS S3',
    license = '',
    packages = ['webtron'],
    url = 'https://github.com/laljitsuri/automating-aws-with-python',
    install_requires = ['boto3', 'click'],
    entry_points = '''
        [console_scripts]
        webtron = webtron.webtron:cli
    '''
)
