#!/bin/bash

# Use:
#   source "./LLM Tests/setup_qwen_env.sh"

# Qwen2.5-3B Environment Setup for WSL / Linux
# - Won't work if Miniconda if missing
# - Creates conda env with CUDA PyTorch 
# - Installs python packasges (Jupyter, Transformers & BitsAndBytes)

# Detect if script is being sourced
(return 0 2>/dev/null) && SOURCED=1 || SOURCED=0

set -e # Stop on error

echo "Initializing Conda..."

# If Conda is missing: 
# (WSL Shelll) 
#   wget https://repo.anaconda.com/miniconda/Miniconda3-py312_24.5.0-0-Linux-x86_64.sh -O ~/miniconda312.sh 
#   bash ~/miniconda.sh -p -u ~/miniconda3 
# You may need to follow prompts. Default install to $HOME/miniconda3.
export PATH="$HOME/miniconda3/bin:$PATH"

if [ ! -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    echo "ERROR: Conda not found at ~/miniconda3"
    echo "Install Miniconda first."
    return 1 2>/dev/null || exit 1
fi

source "$HOME/miniconda3/etc/profile.d/conda.sh"

ENV_NAME="qwen-env"

# Check if env already exists
if conda env list | grep -q "^$ENV_NAME "; then
    echo "Environment '$ENV_NAME' already exists. Removing."
    conda deactivate 2>/dev/null || true
    conda remove -n qwen-env --all -y # In case broken   
fi
echo "Creating conda environment '$ENV_NAME' (Python 3.11)..."
conda create -n qwen-env python=3.11 -y

echo "Activating environment..."
conda activate "$ENV_NAME"

echo "Installing CUDA-enabled PyTorch..."
conda clean --all -y

# Conda installation does not work
#conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia --strict-channel-priority -y;
python -m pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121

echo "Installing Python packages..."
python -m pip install --upgrade pip
python -m pip install --upgrade transformers accelerate bitsandbytes sentencepiece safetensors ipykernel ipywidgets notebook


echo "Registering Jupyter kernel..."
python -m ipykernel install --user --name "$ENV_NAME" --display-name "Python ($ENV_NAME)"

echo
echo "Setup complete."
echo "Environment '$ENV_NAME' is now active in this shell."
echo "You can verify with: which python"
echo
echo "For future shells:"
echo "- Run once: 'conda init bash'"
echo "- Then restart terminal or run: 'exec bash'"
echo "Then the environment can be activated with: 'conda activate qwen-env'"
echo
echo "If VS Code doesn't see it:"
echo " - Run (from WSL):              code ."
echo " - Select interpreter manually: Ctrl+Shift+P > Python: Select Interpreter"
echo " - Refresh the kernel:          Ctrl+Shift+P > Developer: Reload Window"

# If discoverability issue in VS Code/Jupter:
# 0. Make sure the Jupyter extension is installed in WSL. 
# 1. Get VSC to run inside WSL to see it. In WSL terminal, run: code .
# 2. Ctrl+Shift+P > Python: Select Interpreter > /home/you/miniconda3/envs/qwen-env/bin/python
#    If you're not sure about the path: "conda activate qwen-env" and "which python"
# 3. Refresh the kernel: Ctrl+Shift+P > Developer: Reload Window

echo