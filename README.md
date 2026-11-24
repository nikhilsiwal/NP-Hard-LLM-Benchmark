# 

# \# NP-Hard Problem with LLM Benchmarking

# 

# A Python-based benchmarking framework designed to evaluate how Large Language Models (LLMs) solve classical NP-hard problems.

# 

# The framework generates problem instances, sends them to an LLM, validates generated solutions against reference solvers, evaluates performance metrics, and stores experimental results in SQLite.

# 

# \## Key Features

# 

# \- Five classical NP-hard problem implementations.

# \- Brute-force reference solvers.

# \- Gemini AI integration through REST API.

# \- Automated prompt generation and response parsing.

# \- Solution validation.

# \- Performance evaluation using accuracy, optimality gap, and latency.

# \- SQLite-based experiment storage.

# \- Interactive Streamlit dashboard.

# \- Automated test suite using Pytest.

# 

# \## Supported NP-Hard Problems

# 

# | Problem | Description |

# |---|---|

# | Travelling Salesman Problem (TSP) | Finds a minimum-distance tour |

# | 0/1 Knapsack | Maximizes value within a weight capacity |

# | Graph Coloring | Minimizes the number of colors |

# | 3-SAT | Finds a satisfying Boolean assignment |

# | Subset Sum | Finds a subset matching a target sum |

# 

# \## Technology Stack

# 

# \- Python

# \- Google Gemini API

# \- SQLite

# \- Streamlit

# \- Pandas, NumPy

# \- Plotly

# \- NetworkX

# \- Pytest

# 

# \## Initial Gemini Benchmark Results

# 

# | Problem | Validity | Exact-Match Accuracy | Optimality Gap | Latency |

# |---|---:|---:|---:|---:|

# | Subset Sum | Valid | 100% | 0% | 34.06 sec |

# | TSP | Valid | 0% | 1.07% | 54.73 sec |

# | 0/1 Knapsack | Valid | 100% | 0% | 50.41 sec |

# | Graph Coloring | Valid | 100% | 0% | 22.98 sec |

# | 3-SAT | Valid | 100% | 0% | 12.93 sec |

# 

# \*\*Note:\*\* These are preliminary results from small, fixed problem instances, not a comprehensive performance evaluation. Exact-match accuracy checks whether the objective value matches the reference optimum. TSP produced a valid but slightly non-optimal route.

# 

# \## Dashboard

# 

# The Streamlit dashboard provides:

# \- Overall benchmark statistics.

# \- Latest Gemini experiment results.

# \- Accuracy comparison.

# \- Response latency comparison.

# \- Optimality gap comparison.

# \- Experiment history.

# 

# \## Installation and Setup

# 

# \### 1. Clone the repository

# 

# ```bash

# git clone https://github.com/nikhilsiwal/NP-Hard-LLM-Benchmark.git

# cd NP-Hard-LLM-Benchmark

# ```

# 

# \### 2. Create a virtual environment

# 

# ```bash

# python -m venv .venv

# ```

# 

# \### 3. Activate the environment (Windows PowerShell)

# 

# ```powershell

# .\\.venv\\Scripts\\Activate.ps1

# ```

# 

# \### 4. Install dependencies

# 

# ```bash

# python -m pip install -r requirements.txt

# ```

# 

# \### 5. Configure Gemini API

# 

# Create a `.env` file in the project root:

# 

# ```env

# GEMINI\_API\_KEY=your\_api\_key\_here

# ```

# 

# Never upload your `.env` file or expose your API key publicly.

# 

# \### 6. Run the dashboard

# 

# ```bash

# streamlit run app/dashboard/dashboard.py

# ```

# 

# \## Run Tests

# 

# ```bash

# python -m pytest -v

# ```

# 

# Current test status: \*\*84 tests passed\*\*.

# 

# \## Project Status

# 

# \- \[x] Five NP-hard problem generators.

# \- \[x] Brute-force reference solvers.

# \- \[x] Prompt manager and response parser.

# \- \[x] Gemini REST API integration.

# \- \[x] Evaluation metrics.

# \- \[x] SQLite experiment database.

# \- \[x] Generic benchmark runner.

# \- \[x] Gemini benchmark integration for all five problems.

# \- \[x] Streamlit dashboard.

# \- \[x] Automated tests.

# 

# \## Future Improvements

# 

# \- Benchmark additional LLM providers.

# \- Support larger and more diverse problem instances.

# \- Track token usage and API cost.

# \- Add advanced evaluation metrics.

# \- Implement repeated experiments and statistical analysis.

# \- Improve dashboard comparisons.

# \- Explore hybrid and advanced LLM solving strategies.

# 

# \## Author

# 

# \*\*Nikhil Siwal\*\*

# 

# GitHub: \[nikhilsiwal](https://github.com/nikhilsiwal)

# 

# \---

# 

# This project is developed for studying and evaluating the problem-solving capabilities of Large Language Models on classical NP-hard problems.

# 

