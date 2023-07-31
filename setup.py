import cx_Freeze  # pip install cx_freeze

# base = "Win32GUI" allows your application to open without a console window
executables = [cx_Freeze.Executable('main.py', base="Win32GUI")]
excludes = []

cx_Freeze.setup(
    name="Pac-man",
    options={"build_exe":
                 {'include_msvcr': True,
                  "packages": ["pygame", "sqlalchemy", "pygame_gui"],
                  "zip_include_packages": ["pygame/", "SQLAlchemy", 'pygame_gui', 'pygame-ce', 'sqlite3',
                                           'sqlalchemy.dialects.sqlite', 'pygame_gui/', 'pygame_gui.data',
                                           'pygame_gui.data/', 'pygame_gui.core.ui_font_dictionary'],
                  "include_files": ['data/', 'data_db/', 'data_level/', 'db/', 'sounds/', 'readme.md', 'const.py',
                                    'game.py', 'level_game.py', 'load.py', 'sprites_class.py'],
                  "excludes": excludes}},
    executables=executables
)
