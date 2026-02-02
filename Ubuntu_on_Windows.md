# This Documentation is for setting up Ubuntu with Windows Subsystem for Linux
### Includes setup for UrbanWatch

## WSL2 Requirements:
- 64-bit Windows 10 or 11
- x64 or ARM processor

## UrbanWatch Requirements:
- OS: Ubuntu 20.04 or later (22.04 or later recommended)
- GPU: NVIDIA GPU w/ CUDA support, >= 8 GB GPU memory (>=12 GB recommended)
- Python: version 3.8+ (3.9+ recommended)
- CUDA Toolkit: Compatible with GPU and PyTorch (11.8+ recommended)
- NVIDIA Driver: Latest stable version
    - locate the correct one for your device here: [nvidia drivers](https://www.nvidia.com/en-us/drivers/).

### Open PowerShell and run:
```
wsl --install
```

You may be required to reboot.

### Confirm WSL2 is being used
```
wsl --status
```

Expected result:
```
Default Version: 2
```

If it is not, in Powershell run:
```
wsl --set-default-version 2
```

### If Ubuntu did **not** install automatically, run:
```
wsl --install -d Ubuntu-22.04
```
### Launch Ubuntu
Locate in the Start Menu.
When it opens, if you want to check the version, run:
```
cat /etc/os-release
```

### Create username and password
**Note:** Linux does **not** display any characters when typing a password.
You will be asked to retype your password to confirm. 
If they do not match, you will reprompted to create it.

### Verify GPU access inside Ubuntu
```
nvidia-smi
```
---
## UrbanWatch setup
---

### Update System
```
sudo apt update && sudo apt upgrade -y
```

### Install explicit tools for Python
Ubuntu 22.04 already includes Python 3.10
```
sudo apt install -y python3-venv python3-dev python3-pip
```

### Create project directory (shared with Windows)
```
mkdir -p /mnt/c/UrbanWatch
cd /mnt/c/UrbanWatch
```

### Create virtual environment
```
python3 -m venv urbanwatch_env
source urbanwatch_env/bin/activate
```

### With venv active, install PyTorch with CUDA
Example with 11.8
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Verify that GPU is available to PyTorch
```
python - <<EOF
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
EOF
```

### Install UrbanWatch dependencies
```
pip install torch torchvision numpy pandas opencv-python scikit-learn matplotlib tqdm

```

### Place UrbanWatchModel folder with all files inside the project directory
Change directory to the model folder and run the program
```
cd /mnt/c/UrbanWatch/UrbanWatchModel
./urbanwatch
```

**Note:** If you get this error when running UrbanWatch:
- Could not load library libcudnn_cnn_infer.so.8.
Run the following to make libcuda.so visible to non-Python binaries:
```
source urbanwatch_env/bin/activate
echo 'export LD_LIBRARY_PATH=/usr/lib/wsl/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```
And run the program:
```
./urbanwatch
```

## Running UrbanWatch after initial setup
- Open Ubuntu terminal
- Change directory to the model location
    - `cd /mnt/c/UrbanWatch/UrbanWatchModel` 
- Activate Python venv
    - `source urbanwatch_env/bin/activate`
- Run the program
    - `./urbanwatch`
