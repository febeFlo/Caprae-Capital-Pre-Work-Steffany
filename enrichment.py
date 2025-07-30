import time

def enrich_company(name, website):
    """
    Stubbed enrichment function.
    Replace with real API calls to:
      - Clearbit (firmographics)
      - Hunter.io (email verification)
      - TechStack.io (technology usage)
    """
    time.sleep(0.1)  # simulate network latency
    return {
        "employee_count": 100,
        "revenue_million_usd": 10.5,
        "funding_million_usd": 5.2,
        "email_validity": 0.85,
        "tech_score": 0.7
    }