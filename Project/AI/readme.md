step 1. install miniconda
1-1.
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh

1-2.
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3

1-3.
rm ~/miniconda3/miniconda.sh 

step 2. install Ollama

2-1.
curl -fsSL https://ollama.com/install.sh | sh

2-2.
ollama run gemma3:4b
ollama run gemma3:12b
ollama run gemma3:27b



step 3
create env
conda env create -f environment.yaml