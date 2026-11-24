#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from pathlib import Path

from extract_utils import fixups_blob

# The appended firmware starts immediately after the
# ELF section headers at file offset 0x2daa30.
ELF_END = 0x2DAA30

OPEN_PATCHES = (
    fixups_blob.blob_fixup()
    # Open the external firmware to find the selected chip's image.
    # Before: [
    #  bl getpid@plt
    #  adrp x3, 0x30000
    #  mov w4, w0
    #  add x3, x3, #0xa76  // "/proc/%d/exe"
    #  add x0, sp, #0x200
    #  mov w1, #0x40
    #  mov w2, #0x40
    #  bl 0x8a234  // format the proc path
    #  add x0, sp, #0x200
    #  mov x1, sp
    #  mov w2, #0x200
    #  bl readlink@plt
    #  cmn x0, #0x1
    #  b.eq 0x8a638
    # ]
    # After: [
    #  mov x0, sp
    #  adr x1, 0x8a530  // "/vendor/firmware/gnss.bin"
    #  mov w2, #0x1a
    #  bl memcpy@plt
    #  b 0x8a554  // original fopen setup, past the path literal
    # ]
    .sig_replace(
        '25 2a 09 94 23 fd ff d0 e4 03 00 2a 63 d8 29 91 '
        'e0 03 08 91 01 08 80 52 02 08 80 52 3f ff ff 97 '
        'e0 03 08 91 e1 03 00 91 02 40 80 52 3e 2a 09 94 '
        '1f 04 00 b1 40 07 00 54',
        'e0 03 00 91 81 00 00 10 42 03 80 52 e2 29 09 94 0a 00 00 14 '
        + b'/vendor/firmware/gnss.bin\0'.hex(' ')
        + ' 00' * 10,
    )
    # Reopen the same firmware when reading the chip configuration.
    # Before: [
    #  bl getpid@plt
    #  adrp x3, 0x30000
    #  mov w4, w0
    #  add x3, x3, #0xa76  // "/proc/%d/exe"
    #  add x0, sp, #0x200
    #  mov w1, #0x40
    #  mov w2, #0x40
    #  bl 0x8a234  // format the proc path
    #  add x0, sp, #0x200
    #  mov x1, sp
    #  mov w2, #0x200
    #  bl readlink@plt
    # ]
    # After: [
    #  mov x0, sp
    #  adr x1, 0x8a530  // "/vendor/firmware/gnss.bin"
    #  mov w2, #0x1a
    #  bl memcpy@plt
    #  b 0x8a730  // original fopen setup
    # ]
    .sig_replace(
        'ac 29 09 94 23 fd ff d0 e4 03 00 2a 63 d8 29 91 '
        'e0 03 08 91 01 08 80 52 02 08 80 52 c6 fe ff 97 '
        'e0 03 08 91 e1 03 00 91 02 40 80 52 c5 29 09 94',
        'e0 03 00 91 61 f1 ff 10 42 03 80 52 69 29 09 94 08 00 00 14'
        + ' 00' * 28,
    )
)


def validate_firmware(data, start):
    end = len(data)
    if end <= start:
        raise ValueError('gpsd firmware is missing')

    while end > start:
        trailer_offset = end - 42
        # Chip family, decimal image size, configuration offset, RFIC ID.
        fields = data[trailer_offset:end].split(b'-')
        if (
            [len(field) for field in fields] != [4, 11, 16, 8]
            or not fields[0].startswith(b'K')
            or not fields[0][1:].isdigit()
            or not fields[1].isdigit()
        ):
            raise ValueError(
                f'invalid gpsd firmware trailer at {trailer_offset:#x}'
            )

        size = int(fields[1])
        end = trailer_offset - size
        if size == 0 or end < start:
            raise ValueError(
                f'invalid gpsd firmware size at {trailer_offset:#x}'
            )


def blob_fixup(ctx, file, file_path, **_kwargs):
    path = Path(file_path)
    data = path.read_bytes()

    validate_firmware(data, ELF_END)
    firmware = path.parents[2] / 'firmware/gnss.bin'
    firmware.parent.mkdir(parents=True, exist_ok=True)
    firmware.write_bytes(data[ELF_END:])
    path.write_bytes(data[:ELF_END])
    OPEN_PATCHES.run(ctx, file, file_path)
