from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["flask"],
    "include_files": [
        ("templates", "templates"),
        ("static", "static"),          #You can add your own directory with files to be added to the build process
    ],
    "include_msvcr": True
}

exe = Executable(
    script="app.py",
    base="Console",  
    target_name="PyHTTP.exe",          #Set a convenient name for the application
)

setup(
    name="PythonHTTP",
    version="0.4",
    description="Simple HTTP Python server",
    options={"build_exe": build_exe_options},
    executables=[exe],
)
