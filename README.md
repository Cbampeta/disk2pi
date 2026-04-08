# disk2pi

disk2pi is a tool that processes various types of documents and prepares them for use on a Raspberry Pi.

## Features

- Supports multiple input formats:
  - PDF documents
  - Videos (`.mp4`)
  - Images (`.png`)
- Simple command-line interface
- Fast build and execution using `uv`

> ⚠️ Audio files are not supported yet.

---

## Getting Started

### Prerequisites

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed

---

### Installation

1. Install `uv`:

   Follow the official instructions:  
   https://docs.astral.sh/uv/getting-started/installation/

2. Clone the repository:

   ```bash
   git clone https://github.com/your-username/disk2pi.git
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