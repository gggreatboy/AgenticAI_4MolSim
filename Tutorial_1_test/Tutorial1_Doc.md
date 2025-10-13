# Tutorial 1 — AI Agents with Custom Tools  
### *(LangChain + MoSDEF + LAMMPS)*

Welcome to the first tutorial in the **Agentic AI Tutorials** series!  
In this lesson, we’ll explore how to build an **LLM-powered agent** using **LangChain** that can call your own Python functions to automate molecular simulation workflows.

By the end of this tutorial, you’ll understand how to:
- Turn regular Python functions into **LangChain tools**.
- Build an **agent** that can reason about which tool to call and in what order.
- Automate a real-world workflow involving **molecular setup, simulation, and analysis**.

---

## 🧭 Overview

This tutorial demonstrates how to integrate **custom scientific tools** into an LLM workflow using LangChain.  
As a case study, we’ll build an agent that can:

1. **Generate molecular configurations** (e.g., a solvent box).  
2. **Run a short molecular dynamics (MD) simulation** using LAMMPS.  
3. **Analyze the resulting trajectory** to extract physical properties.  
4. **Summarize and report results** back to the user.

Each of these tasks will be implemented as a **separate Python function** that the agent can call when appropriate.

---

## ⚙️ What You’ll Learn

By completing this tutorial, you’ll learn how to:

- Design and document tool functions for agents.
- Integrate tools into a LangChain-based workflow.
- Pass data between tools (e.g., configuration → simulation → analysis).
- Handle results and provide interpretable outputs for scientific tasks.

This will give you a strong foundation for building **AI-driven automation** in computational chemistry, materials science, or other simulation-based fields.

---

## 🧩 Prerequisites

Before running this tutorial, ensure your environment is properly configured.

- Activate the provided conda environment:  
  ```bash
  conda activate /groups/ycolon/group-envs/agentic-tutorials

- or install everything from scratch
```bash 
    ./install_from_scratch.sh
```

- Make sure LangChain and Ollama or another supported LLM backend are installed and available.
    - If using Ollama, start the server before running LangChain:

```bash
    ollama serve
```

## Chatbot vs Agent Notebook
It is recommended to run this notebook to familiarize with essential concepts of this workflow and test installations. 


### Development and testing
Inside the `dev_test` directory you will find the `Agent_1_dev.ipynb` notebook wich is used to test pure python functions (No LLM) and make sure they are producing the epected results. You can use this notebook to test your custom functions, so later only a copy and paste task is required for enabling it as a tool with an agent. 


# Overview of example tools
**IMPORTANT NOTE:** There are two notebooks for this tutorial. One using the OpenAI APi and one using Ollama models. FOr this specific workflow the open sorce models are not as successful in calling and using tools in comparison to OpenAI models. However, this is a good introduction to essential components on building AI agents. If using the OpenAI API make sure to copy yor API key in the .env file. 


## 🧰 Tool 1: `molnum` — Determine Number of Solvent Molecules for a Simulation Box
The `molnum` function estimates how many **solvent molecules** are needed to fill a cubic simulation box at a given **density** and **molecular mass**.  

This calculation is useful for preparing molecular simulations, ensuring that the number of molecules in the box is consistent with a realistic physical density.  
For example, if you are building a solvent box for ethanol or water, `molnum` helps determine the number of molecules that should be packed in to match experimental conditions. This function is a good example of a deterministic, physics-based tool that the agent can call when it needs to estimate system composition.


## 🧰 Tool 2: `create_lammps_data_file` — Generate a LAMMPS Data File from a SMILES String

The `create_lammps_data_file` function automates the creation of a **LAMMPS-compatible data file** directly from a **SMILES string** representing a molecule.  

It uses the **MoSDEF ecosystem** — specifically the `mbuild` and `foyer` libraries — to:
1. Interpret the SMILES structure.
2. Pack multiple copies of that molecule into a simulation box.
3. Apply a classical force field (OPLS-AA by default).
4. Export a fully parameterized LAMMPS `.data` file ready for simulation.

This function bridges **chemical representation** (SMILES) and **simulation setup**, allowing the agent to generate input files for MD automatically. This tool provides the core link between molecular structure representation and molecular dynamics simulation.

## 🧰 Tool 3: `create_lammps_input_file`

### **Overview**
This function automatically generates a **LAMMPS input file** (`.in`) designed for running a **basic NPT (constant Number, Pressure, Temperature)** molecular dynamics simulation.  
It provides a ready-to-run simulation setup using typical settings suitable for organic and small-molecule systems, assuming the user already has a parameterized **LAMMPS data file** from `Tool 2`.

### **Function Purpose**
- To create a standardized LAMMPS input file that performs:
  - **Energy minimization**
  - **NPT equilibration**
  - **Trajectory output**
- It allows users to specify key simulation parameters such as **temperature** and **pressure**, while all other parameters (integration styles, cutoffs, and thermo settings) are handled automatically.


### **Key Features**
- **Energy minimization** before equilibration for structural relaxation.  
- **NPT ensemble** control using the `fix npt` command with isotropic pressure coupling.  
- **Automatic velocity initialization** with a Gaussian distribution.  
- **Thermo output and DCD trajectory writing** for monitoring and analysis.  
- Suitable for small-molecule systems generated with the **OPLS-AA** force field (default from Tool 2).
- The ouput is a  formatted `.in` file ready for direct use in LAMMPS:
- This tools highlights how a specific input file for a third-party code or enggine can be generated and modified by a function.


## 🧰 Tool 4: `ensemble_average`

### **Overview**
The `ensemble_average` tool is a **robust convergence analysis utility** that evaluates whether a given property (e.g., energy, density, pressure) from a **LAMMPS log file** has reached equilibrium.  
It computes cumulative and rolling averages over time, detects convergence based on a user-defined **tolerance threshold**, and produces clear **diagnostic plots** to visualize system equilibration.

This function is essential for automating the **post-processing stage** of molecular dynamics workflows — enabling agents to quantitatively determine when a simulation property becomes statistically stable.

---

### **Function Purpose**
- Parse LAMMPS log files and extract time-series data for any thermodynamic property.
- Calculate the **cumulative running average (CRA)** and **rolling running average (RRA)** of the property.
- Determine **when (if at all)** the property converges within a specified **tolerance**.
- Produce a **diagnostic plot** showing the property trajectory, averages, and the identified equilibration point.


### **Methodology**
1. **Log Parsing:**  
   Extracts all numerical data from the LAMMPS log file’s `Step` block and organizes it into a structured table.
2. **Cumulative and Rolling Averages:**  
   Computes two running averages to smooth fluctuations and track long-term behavior.
3. **Convergence Detection:**  
   Iteratively compares average values over fixed windows; convergence is detected when percent change falls below the specified tolerance.
4. **Visualization:**  
   Generates a dual-axis plot showing:
   - Property trajectory
   - Cumulative and rolling averages
   - Percentage change curve
   - Convergence cutoff (if found)

---


