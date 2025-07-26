<div align="center">

# RawTextCheck

 software tool to proofread text in any file formats.

</div>

## Overview

RawTextCheck is a Python-based integration of LanguageTool, built with PyQt5. Its purpose is to proofread texts found in non-standard formats such as XML, Excel, CSV, JSON, and other structured files. These files often contain code elements, markup, or special characters that are not part of the actual text, but are essential for the logic or styling of scripts, especially in video games.

This tool was originally designed for fan translation of video games, but it can be adapted to many other use cases where structured text needs linguistic analysis.

To analyze a file, a parser first extracts the relevant text lines. Several generic parsers are already included, and custom parsers can be plugged in for specific formats. The parser itself doesn’t need to clean the text, as that can be handled by a dedicated filtering system afterward.

Each file is analyzed within the context of a project, which defines parameters such as:

- The language of the text
- A list of valid characters
- Words to flag as errors (e.g., banned words)
- Custom dictionary entries to ignore false positives
- Filters to exclude code fragments, either by defining specific tokens or start/end delimiters

RawTextCheck provides a flexible and extensible environment for proofreading structured text embedded in various formats, ensuring cleaner and more accurate translations or content validation.



![main window](resources/readme_app_1.png)

![project config window](resources/readme_app_2.png)