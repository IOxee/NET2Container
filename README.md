# .NET to Python Converter

This Python script allows you to convert .NET projects to Python, performing the following actions:

- Changing relative paths to absolute paths in the source code.
- Creating backups of modified files.
- Automatically generating a Dockerfile to facilitate project containerization.

## Requirements

Before using this script, make sure you have the following installed:

- Python 3.x: [Download and install Python](https://www.python.org/downloads/)
- Additional dependencies: `Visual Studio 2017 -> 2022`

## Usage

1. Clone the repository or download the project files.
2. Run the `dotnet2container.py` script in your Python environment.
3. Provide the location of the .NET project you want to convert.
4. The script will automatically perform the following tasks:
   - Change relative paths to absolute paths in the source code.
   - Create backups of modified files in the `backups` folder.
   - Generate a Dockerfile in the project root.
5. Once the conversion is complete, you will have a Python project ready to use.


## Contributions

Contributions are welcome. If you want to improve this script or add new features, feel free to do so. Open an issue or submit a pull request with your changes.

## License
Copyright (c) 2023 IOxee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
