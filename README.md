# IR-Sentinel: MCP-Native LLVM Vulnerability Researcher

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![LLVM](https://img.shields.io/badge/LLVM-14%2B-green)
![Status](https://img.shields.io/badge/status-Research%20Prototype-orange)

**IR-Sentinel** is an automated vulnerability research platform that combines **LLVM Static Analysis** with **Generative AI**. Unlike standard linters that rely on regex, IR-Sentinel compiles source code to **LLVM Intermediate Representation (IR)**, extracts semantic metrics (Control Flow Graph stats, complexity, memory ops), and exposes these as tools to an AI agent via the **Model Context Protocol (MCP)**.

<!-- It uses a multi-iteration reasoning loop to detect complex temporal bugs, such as **Use-After-Free (UAF)** and race conditions, which static analysis often misses. -->

## 🏗 Architecture

The project consists of three layers:

1.  **Low-Level Analysis (C++):** A custom LLVM Pass (`StatsCollector.so`) that extracts JSON metrics from IR.
2.  **Tooling Layer (MCP):** A `FastMCP` server that allows LLMs to "compile", "inspect", and "filter" code programmatically.
3.  **Reasoning Agent (Python):** An orchestrator that loops prompts against Gemini 2.0/3.0 or Groq to probabilistically verify vulnerabilities.

## ⚡ Prerequisites

*   **Linux/macOS** (Windows requires WSL2)
*   **LLVM & Clang** (Version 14 or higher recommended)
*   **Python 3.10+**
*   **API Keys:** Google GenAI (Gemini) or Groq

## 📦 Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/IR-Sentinel.git
    cd IR-Sentinel
    ```

2.  **Install Python Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Environment Variables**
    Create a `.env` file in the root directory:
    ```bash
    touch .env
    ```
    Add your keys:
    ```ini
    GOOGLE_API_KEY=your_gemini_key_here
    GROQ_API_KEY=your_groq_key_here
    ```

## 🛠️ Build the LLVM Pass

Before running the server, you must compile the C++ analyzer pass.

1. **Ensure `LLVM` is installed in `opt/llvm-22` directory.**

2.  **To build the pass library:**
    ```bash
    $ ./cmake_build.sh
    ```

    

## 🚀 Quickstart

### 1. Run the MCP Server
Start the tool server to expose compiler capabilities:
```bash
python server.py
```
### 2. Run **Gemini-cli** or an AI agent and configure it to use the `server`. 