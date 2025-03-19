# Detailed Setup Guide for PDF Chat Application

This guide provides detailed instructions for setting up and troubleshooting the Chat with Multiple PDFs application.

## Prerequisites

Before installing the application, ensure you have:

1. **Python 3.9+** installed on your system
2. **OpenAI API key** - Get from [OpenAI Platform](https://platform.openai.com/)
3. **Hugging Face API token** (optional, for alternative embeddings) - Get from [Hugging Face](https://huggingface.co/settings/tokens)

## Step-by-Step Installation

### 1. Clone or download the repository

If using git:

```bash
git clone <repository-url>
cd multi-chat
```

Or simply download and extract the zip file to a folder named `multi-chat`.

### 2. Set up a virtual environment

Creating a virtual environment is recommended to avoid package conflicts:

```bash
# Create virtual environment
python -m venv myenv

# Activate on Windows
myenv\Scripts\activate

# Activate on macOS/Linux
source myenv/bin/activate
```

### 3. Install required packages

```bash
pip install -r requirements.txt
```

If you encounter any errors during installation, try:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file in the project root directory with your API keys:
