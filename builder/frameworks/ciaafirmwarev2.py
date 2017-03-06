# Copyright 2014-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
SAPI
"""

from os.path import isdir, isfile, join, dirname

from SCons.Script import DefaultEnvironment
from base64 import b64decode
import json

env = DefaultEnvironment()
platform = env.PioPlatform()

FRAMEWORK_DIR = platform.get_package_dir("framework-ciaafirmwarev2")
assert isdir(FRAMEWORK_DIR)


# If no modules where selected in the project use the default ones
if ARGUMENTS.get("CIAAFIRMWAREV2_MODULES", None) is not None:
    modules = [item.strip() for item in b64decode(ARGUMENTS.get("CIAAFIRMWAREV2_MODULES")).split(",")]
else:
    modules = ["base","board","chip","dsp","sapi"]

print ("Modules included for sapi: " + str(modules))


# Add include dirs of sapi modules to CPPPATH. This is later used to set -I for gcc
env.Append(
    CPPPATH=[join(FRAMEWORK_DIR, "modules", env.BoardConfig().get("build.core"), module_name, "inc") for module_name in modules]
)


# Add chip config to -I. This is required for the m0 core chip
try:
    chip_config = env.BoardConfig().get("build.chip_config")
    env.Append(
        CPPPATH=[join(FRAMEWORK_DIR, "modules", 
                 env.BoardConfig().get("build.core"), "chip", "inc", chip_config)]
    )
except KeyError:
    pass


# Copy environment
envsafe = env.Clone()


# Select ldscript
ldscript = env.BoardConfig().get("build.ldscript")
if isinstance(ldscript, basestring):
    ldscript = [ldscript]

for i, ldpath in enumerate(ldscript):
    if not isfile(ldpath):
        ldscript[i] = join(dirname(platform.manifest_path), "etc", "ld", ldpath)

env.Append(
    LINKFLAGS=['-Wl,-T' + ",-T".join(ldscript)]
)



# Compile SAPI libraries 
sapi_libs = [envsafe.BuildLibrary(
    join("$BUILD_DIR", module_name),
    join(FRAMEWORK_DIR, "modules", env.BoardConfig().get("build.core"), module_name)
) for module_name in modules]

libs = []
for sapi_lib in sapi_libs:
    libs.append(sapi_libs)
env.Append(LIBS=libs)



