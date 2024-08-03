import platform
from setuptools import setup, Extension
from sys import platform as sys_platform
from pathlib import Path

root_path = Path(__file__).parent
BASE_PATH = Path("cpqa/native")

print(root_path)


def include_dirs():
    if sys_platform == "linux" or sys_platform == "linux2":
        return ["/usr/local/include"]
    elif sys_platform == "win32":
        return [str(BASE_PATH / "external" / "include")]
    elif sys_platform == "darwin":
        raise Exception("MacOS is not supported")
    else:
        raise Exception("Unsupported sys_platform")


def library_dirs():
    if sys_platform == "linux" or sys_platform == "linux2":
        pass
    elif sys_platform == "win32":
        if platform.architecture()[0] == "32bit":
            return [str(BASE_PATH / "external" / "lib" / "FTD2XX" / "i386")]
        elif platform.architecture()[0] == "64bit":
            return [str(BASE_PATH / "external" / "lib" / "FTD2XX" / "amd64")]
        else:
            raise Exception("Unsupported architecture")
    elif sys_platform == "darwin":
        raise Exception("MacOS is not supported")
    else:
        raise Exception("Unsupported sys_platform")


def libraries():
    if sys_platform == "linux" or sys_platform == "linux2":
        return ["ftd2xx"]
    elif sys_platform == "win32":
        return ["ftd2xx"]
    elif sys_platform == "darwin":
        raise Exception("MacOS is not supported")
    else:
        raise Exception("Unsupported sys_platform")


def extra_compile_args():
    if sys_platform == "linux" or sys_platform == "linux2":
        return ["-Wno-error=format-security"]
    elif sys_platform == "win32":
        return ["/std:c++20"]
    elif sys_platform == "darwin":
        raise Exception("MacOS is not supported")
    else:
        raise Exception("Unsupported sys_platform")


def depends():
    if sys_platform == "linux" or sys_platform == "linux2":
        pass
    elif sys_platform == "win32":
        all_deps = library_dirs() + include_dirs()
        return [str(f) for d in all_deps for f in Path(d).glob("**/*")]
    elif sys_platform == "darwin":
        raise Exception("MacOS is not supported")
    else:
        raise Exception("Unsupported sys_platform")


setup(
    ext_modules=[
        Extension(
            name="cpqa.native.mut",
            sources=[
                str(BASE_PATH / "mut.cc"),
            ],
            include_dirs=include_dirs(),
            library_dirs=library_dirs(),
            libraries=libraries(),
            extra_compile_args=extra_compile_args(),
            depends=depends(),
        )
    ],
    include_package_data=False,
)
