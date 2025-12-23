# Project Installation and Setup on a Remote VM

This guide provides step-by-step instructions for deploying and running this project on a remote virtual machine (VM).

## 1. Connect to Your VM

First, connect to your remote VM using SSH. You will need the VM's IP address and your user credentials.

```bash
ssh your-user@your-vm-ip-address
```

## 2. Install Prerequisites

Ensure that `git`, `python3`, and `python3-pip` are installed on your VM. You can check their versions with:

```bash
git --version
python3 --version
pip3 --version
```

If they are not installed, use your VM's package manager to install them. For example, on a Debian-based system (like Ubuntu):

```bash
sudo apt-get update
sudo apt-get install -y git python3 python3-pip
```

## 3. Clone the Repository

Clone the project repository from GitHub onto your VM. Replace `<your-github-repo-url>` with the actual URL of your repository.

```bash
git clone <your-github-repo-url>
```

Navigate into the cloned project directory:

```bash
cd RAG-Tutorials
```

## 4. Set Up the Python Environment

It is highly recommended to use a virtual environment to manage project-specific dependencies.

**Create a virtual environment:**

```bash
python3 -m venv .venv
```

**Activate the virtual environment:**

On Linux or macOS:
```bash
source .venv/bin/activate
```

On Windows:
```powershell
.\.venv\Scripts\Activate.ps1
```

**Install the required packages:**

With the virtual environment activated, install all the project dependencies from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## 5. Configure Environment Variables

This project requires API keys and other secrets to be stored in an environment file.

Create a `.env` file in the root of the project directory:

```bash
touch .env
```

Now, open the file with a text editor (like `nano` or `vim`) and add the necessary environment variables. For this project, you will need to add your `GEN_API_KEY`.

```
GEN_API_KEY="your_gemini_api_key_here"
```

Save and close the file.

## 6. Run the Streamlit Application

To run the Streamlit web application and make it accessible from your local machine, use the following command:

```bash
streamlit run streamlit_app.py --server.address=0.0.0.0 --server.port=8501
```
- `--server.address=0.0.0.0` makes the app accessible on your VM's public IP address.
- `--server.port=8501` runs the app on port 8501. You can change this to another port if you wish.

## 7. Configure Your Firewall

You must allow traffic on the port you are using (e.g., 8501) through your VM's firewall. This process depends on your cloud provider (e.g., AWS EC2 security groups, Google Cloud firewall rules, Azure Network Security Groups).

Please consult your provider's documentation for instructions on how to open a port.

## 8. Access Your Application

Once the application is running and the firewall is configured, you can access it from a web browser on your local computer by navigating to:

```
http://<your-vm-public-ip>:8501
```

Replace `<your-vm-public-ip>` with the public IP address of your VM.
