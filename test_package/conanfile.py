from conans import ConanFile, CMake, tools
import os

class PortableconcurrencyTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def configure(self):
        self.requires("googletest/1.8.0@kmaragon/stable")


    def build(self):
        self.run("git clone https://github.com/VestniK/portable_concurrency.git")
         
        # check out the appropriate branch
        if self.options['portable_concurrency'].strict_ts:
            self.run('cd portable_concurrency && git reset --hard && git checkout strict-ts')
        else:
            self.run('cd portable_concurrency && git reset --hard && git checkout master')
        
        self.run('mv portable_concurrency/test%s* .' % os.sep)
        tools.replace_in_file('CMakeLists.txt', 'find_package(GTest REQUIRED)', '''include("${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()''')

        tools.replace_in_file('CMakeLists.txt', 'target_link_libraries(unit_tests portable_concurrency GTest::GTest GTest::Main', 'target_link_libraries(unit_tests ${CONAN_LIBS}')

        cmake = CMake(self)
        cmake.configure(source_folder=self.build_folder)
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        if not tools.cross_building(self.settings):
            os.chdir("bin")
            self.run(".%sunit_tests" % os.sep)
