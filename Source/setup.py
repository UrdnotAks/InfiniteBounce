from cx_Freeze import setup, Executable

base = None

executables = [Executable("InfiniteBounce.py", base=base)]

packages = ["pygame", "random", "sys", "math", "time"]
options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    name="InfiniteBounce",
    options=options,
    version="1.2.0",
    description='<any description>',
    executables=executables, requires=['pygame']
)
