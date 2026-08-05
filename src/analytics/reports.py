from .queries import top_hiring_companies

def company_report():
    df = top_hiring_companies()
    
    print("\nTop Hiring Companies:\n")
    print(df)