#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)


namespace_imports = [
    'device/samsung/s5e8825-common',
    'hardware/samsung',
    'hardware/samsung_slsi-linaro/exynos',
    'hardware/samsung_slsi-linaro/graphics',
]

blob_fixups: blob_fixups_user_type = {
    # Camera - Dependecies
    'vendor/lib64/libsensorlistener.so': blob_fixup().add_needed('libsensorndkbridge_shim.samsung.so'),
    # GNSS
    'vendor/bin/hw/gpsd': blob_fixup().binary_regex_replace(b'libcrypto.so', b'libcryptx.so'),
    'vendor/etc/init/init.gps.rc': blob_fixup().regex_replace('.sh', 'd /vendor/etc/gnss/gps.cfg'),
    (
        'vendor/etc/init/init.gps.rc',
        'vendor/etc/init/vendor.samsung.hardware.gnss-service.rc',
    ): blob_fixup().regex_replace(r'\n.*:[\s\S]*', ''),
    # Neural Networks
    'vendor/lib64/libeden_ud_gpu.so': blob_fixup()
        .add_needed('libeden_ud_cpu.so')
        .replace_needed('libOpenCL.so', 'libGLES_mali.so'),
    'vendor/lib64/libeden_wrapper_sdk.so': blob_fixup().add_needed('libc++_ndk.samsung.so'),
    # RIL
    'vendor/etc/init/init.vendor.rilcommon.rc': blob_fixup().regex_replace('\n.*\n.*n}\n', ''),
    # Sensors
    (
        'vendor/lib64/sensors.inputvirtual.so',
        'vendor/lib64/sensors.sensorhub.so',
    ): blob_fixup().remove_needed('libhidltransport.so'),
}  # fmt: skip

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    # Security - TEEGRIS
    'libuuid': lambda lib, *_: f'{lib}.vendor'
}  # fmt: skip

module = ExtractUtilsModule(
    's5e8825-common',
    'samsung',
    namespace_imports=namespace_imports,
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
)

module.add_proprietary_file(
    'products/ril/proprietary-files.txt'
).add_copy_files_guard('TARGET_HAS_RIL', 'true')

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
