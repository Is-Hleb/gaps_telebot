import setuptools

setuptools.setup(name="gaps_telebot",
                 author="is_hleb",
                 install_requires=["telebot", "xlsxwriter", "datetime", "time", "sqlite3", "os", "logging"],
                 packages=setuptools.find_packages()
                 )
