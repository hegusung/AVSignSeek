# AVSignSeek
Tool written in python3 to determine where the AV signature is located in a binary/payload

## Usage 

Zip (with a password) your binary/payload caught by an AV so it won't be detected when placed in an environment protected by an AntiVirus.
Launch the tool and specify the zip password and filename in the zip with the -p and -f options (infected/infected.bin by default)

This tool won't work for complex signatures

```
./avsignseek.py zipfile.zip
```

The tool will drop multiple files on the disk to determine on which pattern the signature is based on. It will obviously generate a lot of AV alerts, might be a good idea to run this on an host with no internet connection.

Once done, the result will be printed in stdout and a file (output.txt by default) containing the result will be generated

## Help

```
Automatically detects AV Signatures

positional arguments:
  zip_file

optional arguments:
  -h, --help       show this help message and exit
  -w SLEEP         waiting time between 2 tests (default: 20)
  -p ZIP_PASSWORD  zip password (default: infected)
  -f FILENAME      file name contained in the zip (default: infected.bin)
  -l LIMIT_SIGN    signature limit (default: 64)
  -d SUBDIV        subdiv per step (default: 4)
  -o OUTPUT_FILE   output_file (default: output.txt)
  -s START         start byte (default: 0)
  -e END           end byte
```

## Output example

```
=== AVSignSeek ===
[+] Signature between bytes 88220 and 88284
[+] Bytes:
4d 61 6c 77 61 72 65 54 65 73 74 2e 64 6c 6c 00 	MalwareTest.dll.
52 65 66 6c 65 63 74 69 76 65 4c 6f 61 64 65 72 	ReflectiveLoader
00 66 75 6e 63 5f 74 65 73 74 00 00 00 00 00 00 	.func_test......
00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 	................
[+] Strings:
> MalwareTest.dll
> ReflectiveLoader
> func_test
```
