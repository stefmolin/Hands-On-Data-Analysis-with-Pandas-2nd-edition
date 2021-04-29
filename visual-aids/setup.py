from distutils.core import setup
from glob import glob

setup(
    name='visual_aids',
    version='2.0',
    description='Visual aids for Hands-On Data Analysis with Pandas.',
    author='Stefanie Molin',
    author_email='24376333+stefmolin@users.noreply.github.com',
    license='MIT',
    url='https://github.com/stefmolin/Hands-On-Data-Analysis-with-Pandas-2nd-edition',
    packages=['visual_aids'],
    install_requires=[
        'matplotlib>=3.0.2',
        'numpy>=1.15.2',
        'pandas>=0.23.4',
        'seaborn>=0.9.0',
        'statsmodels>=0.9.0',
        'stock_analysis @ git+https://github.com/stefmolin/stock-analysis.git@2nd_edition'
    ],
    package_data={'data': glob('data/*')},
    include_package_data=True
)
