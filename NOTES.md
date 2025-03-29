# Step-by-Step Agno Deployment on Azure

## Step 1. Create a VM

-Resource group: agno-rg
-Name: agno-vm
-Image: Ubuntu Server 24.04 LTS
-Size: D2ads v5 (2 vCPUs, 8 GiB RAM)
-Inboud Ports: 22 (SSH), 80 (HTTP), 7777 (Playground), 3000 (Agent UI)

## Step 2. Connect to VM

ssh -i ~/agno-vm_key.pem azureuser@172.178.45.177

## Step 3. Install Dependencies

Update
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-venv python3-pip git curl -y

Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

Install Docker and Docker Compose
sudo apt install docker.io docker-compose -y
sudo usermod -aG docker $USER
newgrp docker

Install Node.js and pnpm (for Agent UI)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
npm install -g pnpm

Install tmux
sudo apt install tmux

## Step 4. Set up Agno App

mkdir agno-server && cd agno-server
python3.10 -m venv .venv && source .venv/bin/activate

git clone https://github.com/agno-agi/agent-ui.git
cd agent-ui
pnpm install
pnpm dev

echo 'export OPENAI_API_KEY=""' >> ~/.bashrc
source ~/.bashrc

## Usefull commands

sudo reboot
ssh -i ~/agno-vm_key.pem azureuser@172.178.45.177
cd ~/agno-server/agent-ui
pnpm start
cd agno-server
source AgnoVenv/bin/activate
deactivate (venv)
cd ~/agno-server/playground
python playground.py

html_server
tmux new -s html-server
cd ~/agno-server/playground/public
python3 -m http.server 8080
ctr+b d

tmux commands:
tmux new -s <session_name> - create a tmux session
ctr+B % - split vertically
ctr+B / - split horizontally
ctr+b d - detach
tmux attach -t agno - reattach
tmux ls - list sessions

sessions:
agno
html_server
playground
