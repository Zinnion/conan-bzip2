#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, CMake, tools


class Bzip2Conan(ConanFile):
    name = "bzip2"
    version = "1.0.6"
    url = "https://github.com/zinnion/conan-bzip2"
    homepage = "https://github.com/Zinnion/bzip2"
    author = "Zinnion"
    license = "bzip2-1.0.6"
    description = "bzip2 is a free and open-source file compression program that uses the Burrows–Wheeler algorithm."
    topics = ("conan", "bzip2", "data-compressor", "file-compression")
    settings = "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False], "build_executable": [True, False]}
    default_options = "shared=False", "fPIC=True", "build_executable=True"
    exports = "LICENSE"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self): 
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        major = self.version.split(".")[0]
        cmake = CMake(self)
        cmake.definitions["BZ2_VERSION_STRING"] = self.version
        cmake.definitions["BZ2_VERSION_MAJOR"] = major
        cmake.definitions["BZ2_BUILD_EXE"] = "ON" if self.options.build_executable else "OFF"
        cmake.configure()
        return cmake

    def build(self):
        tools.replace_in_file(os.path.join(self._source_subfolder, "bzip2.c"), r"<sys\stat.h>", "<sys/stat.h>")
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ['bz2']
