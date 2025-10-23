# 🧠 Agentic Authoring Assistant

Multi-Agent System for Automated Metadata, Reference Retrieval & Content Refinement

Agentic Authoring Assistant is a multi-agent AI system built with LangGraph that automates content understanding and enhancement tasks — including metadata generation, web reference retrieval, and content refinement — using specialized, role-based agents.

## 🧩 Project Description

This repository implements a multi-agent orchestration system that enables modular and intelligent processing of written content.
Each agent performs a specialized role and communicates through a LangGraph pipeline to collaboratively produce refined metadata and knowledge references.

The system was designed following the “Agentic AI” pattern: a collection of autonomous yet cooperative agents that process a shared state through structured graph execution.

## Core Capabilities:

🪄 Metadata Agent – Extracts titles, summaries, and tags from raw text descriptions.

🧹 Refiner Agent – Polishes and optimizes metadata for clarity and consistency.

🔍 Reference Agent – Retrieves real-world supporting references using Tavily Search API.

⚙️ LangGraph Orchestration – Manages communication and state transitions between agents.

## 📁 Project Structure
    Agentic_Authoring_Assistant/
    │
    ├── agents/
    │   ├── metadata_agent/
    │   │   ├── metadata_agent_langgraph.py      # Metadata graph and generation pipeline
        |   ├──summary_agent.py
        |   ├──tag_agent.py
        |   ├──title_agent.py                 
    │   │   └── test_metadata.py                 # Test file for metadata generation
    │   │
    │   ├── refiner_agent/
    │   │   ├── refiner_agent_langgraph.py       # Refines metadata (titles, summary, tags)
    │   │   └── test_refiner.py                  # Unit test for refinement
    │   │
    │   ├── reference_agent/
    │       ├── reference_agent.py               # Web reference fetching via Tavily API
    │       └── test_reference.py                # Testing script for references
    │   
    │  
    │
    ├── tools/
    │   ├── nlp_tool.py                     # Metadata extraction logic
    │   ├── refiner_tool.py                      # Metadata refinement logic
    │   ├── web_search_tool.py                   # Tavily-based web search tool
    │   
    │
    ├── main.py                                  # LangGraph orchestration (entry point)
    ├── requirements.txt                         # Dependencies
    └── README.md                                # This file

## ⚙️ Setup Instructions
### 1. Clone the Repository

        git clone https://github.com/rafia-10/Agentic_Authoring_Assistant.git
        cd Agentic_Authoring_Assistant

### 2. Create a Virtual Environment
        python3 -m venv venv
        source venv/bin/activate    # On Windows: venv\Scripts\activate

### 3. Install Dependencies

    `pip install -r requirements.txt`

### 4. Set Up Environment Variables

    Create a .env file or export directly in your shell:
        export OPENAI_API_KEY="your_openai_api_key"
        export TAVILY_API_KEY="your_tavily_api_key"

## 🚀 Usage
🧠 Run the Full Multi-Agent Orchestration

The main entry point (main.py) orchestrates the metadata → refinement → reference pipeline.

        `python main.py`


### Sample Interaction:
    Enter your project description:
    "Agentic AI systems are transforming the way freelancers automate content workflows."

    🪄 Generating Metadata...
    🧹 Refining Metadata...
    🔍 Fetching References...
    ✅ Completed: titles, summaries, tags, and web references generated successfully!
    
    All agents communicate through a shared LangGraph state that ensures deterministic flow and reproducibility.


## 🧩 Roles and Communication Flow

    | **Agent**       | **Role**                 | **Input**        | **Output**            | **Depends On** |
    | --------------- | ------------------------ | ---------------- | --------------------- | -------------- |
    | Metadata Agent  | Extract initial metadata | Description text | Titles, tags, summary | —              |
    | Refiner Agent   | Refine metadata          | Raw metadata     | Cleaned metadata      | Metadata Agent |
    | Reference Agent | Search & rank references | Refined summary  | Reference links       | Refiner Agent  |



## 🧪 Testing

Each agent can be tested individually using its corresponding test script.

### Example:

    python agents/metadata_agent/test_metadata.py
    python agents/refiner_agent/test_refiner.py
    python agents/reference_agent/test_reference.py

## 🧰 Future Enhancements

     Add ImageGenerationAgent (once NanoBanana API is public)
    Integrate vector-based memory (via Qdrant or FAISS)

🪪 License

This project is released under the MIT License.
See the LICENSE
 file for details.

## 👩‍💻 Author

Developed by: Rafia Kedir — Agentic AI Developer & Automation expert
Contact: rafiakedir22@gmail.com
 


