from src.api.clients import fetch_jobs

def main():
    jobs = fetch_jobs("software engineer")
    print(jobs)


if __name__ == "__main__":
    main()