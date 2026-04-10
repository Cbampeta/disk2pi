# disk2pi

disk2pi is a tool that processes various types of documents. 

## Features

- Supports multiple input formats:
  - PDF documents
  - Videos (`.mp4`)
  - Images (`.png`)
- Simple interface using PySide6
- Fast build and execution using `uv`

> ⚠️ Audio files are not supported yet.

---

## Getting Started


### Installation

1. Install `uv`:

   Follow the official instructions:  
   https://docs.astral.sh/uv/getting-started/installation/

2. Clone the repository:

   ```bash
   git clone https://github.com/Cbampeta/disk2pi.git
   cd disk2pi

3. Build the project:
    ```bash
    uv build
    ```


### Usage

Run the project from the root directory:

```bash
    uv run main.py "path/to/your/file"
```

Format supported : video, pdf and image