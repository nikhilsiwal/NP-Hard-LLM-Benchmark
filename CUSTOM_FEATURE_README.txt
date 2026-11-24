CUSTOM NP-HARD BENCHMARK UPDATE

Files in this ZIP use paths relative to your NP-Hard-LLM-Benchmark project root.
Extract these files into the project root and choose Replace for dashboard.py.

Features added:
- Custom Travelling Salesman Problem input (2-9 cities)
- Custom 0/1 Knapsack input (1-18 items)
- Custom Graph Coloring input (1-8 vertices)
- Gemini or Groq provider selection
- Exact solver comparison, validation, metrics, and SQLite saving
- Existing dashboard and Random Benchmark history remain in place

After extraction, activate your existing .venv and run:
  pytest -q
  streamlit run app/dashboard/dashboard.py

Do not replace or upload your .env file. The update ZIP does not contain API keys.
