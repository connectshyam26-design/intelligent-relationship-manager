# Intelligent Relationship Manager (IRM)

IRM is a banking AI product prototype that helps relationship managers
check a customer's eligibility for a banking product and identify
alternatives when the customer does not qualify.

## How it works

1. The relationship manager enters a customer ID and a product name.
2. The agent looks up the customer profile through an MCP tool and
   retrieves relevant product policy.
3. The agent checks eligibility using explicit business rules and
   can look for eligible alternatives.

## Design decision

The prototype separates policy retrieval from eligibility checks.
The agent retrieves the relevant policy, while explicit business
rules determine whether the customer meets the eligibility criteria.

## Run locally

With the project dependencies installed and `GEMINI_API_KEY` configured
in a local `.env` file, run these commands from the project root:

    source .venv/bin/activate
    adk web --port 8000

Open http://localhost:8000 and select `app`.