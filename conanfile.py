from conans import ConanFile, CMake, tools


class PortableconcurrencyConan(ConanFile):
    name = "portable_concurrency"
    version = "0.0.1"
    license = "Public Domain"
    url = "https://github.com/kmaragon/conan-portable_concurrency"
    description = "Conan package for VestniK's portable_concurrency implementation"
    settings = "os", "compiler", "build_type", "arch"
    options = {
            "shared": [True, False],
            "strict_ts": [True, False]
    }
    default_options = "shared=False","strict_ts=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/kmaragon/portable_concurrency.git")

    def build(self):
        # check out the appropriate branch
        if self.options.strict_ts:
            self.run('cd portable_concurrency && git reset --hard && git checkout strict-ts')
        else:
            self.run('cd portable_concurrency && git reset --hard && git checkout master')


        # let test_package test the package
        tools.replace_in_file('portable_concurrency/CMakeLists.txt', 'add_subdirectory(test)', '')

        cmake = CMake(self)
        cmake.configure(source_folder="portable_concurrency")
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.configure(source_folder="portable_concurrency")
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["portable_concurrency"]
        if self.settings.os != "Windows":
            self.cpp_info.libs.append("pthread")
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
