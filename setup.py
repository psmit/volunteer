import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'docutils',
    'WTForms',
    'alembic',
    'boto',
    ]

setup(name='volunteer',
    version='0.0.6',
    description='volunteer',
    long_description=README + '\n\n' +  CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
    author='Peter Smit',
    author_email='peter@smitmail.eu',
    url='',
    keywords='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='volunteer',
    install_requires=requires,
    entry_points="""\
      [paste.app_factory]
      main = volunteer:main
      [console_scripts]
      initialize_volunteer_db = volunteer.scripts.initializedb:main
      send_notifications = volunteer.scripts.send_notifications:main
      send_test_sms = volunteer.scripts.send_test_sms:main
      fix_delivery_message_links = volunteer.scripts.fix_delivery_message_links:main
      """,
)

