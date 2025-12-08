# flower's Upload Assistant

This branch is for flower group members! Its modified for our use.

## Setup

Requirements:

* Python 3.9+ and pip3
* MediaInfo and ffmpeg installed on your system
  * Windows users: ffmpeg must be added to PATH. [Guide here](https://windowsloop.com/install-ffmpeg-windows-10/)
  * Alternatively, create a folder named ffmpeg within the Upload Assistant bin directory, and paste ffmpeg executables there.

* If you encounter ffmpeg issues (e.g., `max workers` errors), see this [wiki](https://github.com/Audionut/Upload-Assistant/wiki/ffmpeg---max-workers-issues)

Get the source:

* Clone the repository:

```bash
git clone -b flowerey --single-branch https://github.com/flowerey/Upload-Assistant.git
```
* Or download a ZIP of the source from the releases page and create/overwrite a local copy

Install Python modules:

```bash
pip3 install --user -U -r requirements.txt
```

Optional: Use a virtual environment (recommended if you receive errors about an externally managed environment or want to keep Upload Assistant Python separate):

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Configure Upload Assistant:

* Run the configuration generator:

```bash
python config-generator.py
```
* Or copy and rename `data/example-config.py` to `data/config.py`
* And edit `config.py` with your information (more details in the [wiki](https://github.com/Audionut/Upload-Assistant/wiki))

## Updating

1. Navigate to the Upload-Assistant directory:

```bash
cd Upload-Assistant
```

2. Pull the latest changes:

```bash
git pull
```
* Or download a fresh ZIP from the releases page and overwrite existing files

3. Update dependencies:

```bash
python -m pip install --user -U -r requirements.txt
```

4. Update your config options (or grab new options if added):

```bash
python config-generator.py
```
