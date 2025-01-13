from utils.database import (
    connect_to_db, get_all_jobs, get_job_by_id, 
    search_jobs_by_title, get_recent_jobs, clear_database
)


def print_job_details(job):
    """Helper function to print job details in a formatted way"""
    print("\n" + "="*50)
    print(f"Job ID: {job[1]}")
    print(f"Title: {job[3]}")
    print(f"Posted Date: {job[4]}")
    print(f"URL: {job[2]}")
    print(f"Tags: {job[6]}")
    print(f"Proposals: {job[7]}")
    print("Description Preview: " + job[5][:500] + "...")  # First 500 chars of description
    print("="*50 + "\n")


def confirm_action(message):
    """Helper function to confirm dangerous actions"""
    response = input(f"{message} (yes/no): ").lower().strip()
    return response == 'yes'


def main():
    # Connect to the database
    conn, cursor = connect_to_db()
    
    try:
        while True:
            print("\nUpwork Jobs Database Viewer")
            print("1. View all jobs")
            print("2. Search jobs by title")
            print("3. Get job by ID")
            print("4. View recent jobs")
            print("5. Clear database")
            print("6. Exit")
            
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == "1":
                jobs = get_all_jobs(cursor)
                print(f"\nFound {len(jobs)} jobs:")
                for job in jobs:
                    print_job_details(job)
                    
            elif choice == "2":
                keyword = input("Enter search keyword: ")
                jobs = search_jobs_by_title(cursor, keyword)
                print(f"\nFound {len(jobs)} jobs matching '{keyword}':")
                for job in jobs:
                    print_job_details(job)
                    
            elif choice == "3":
                job_id = input("Enter job ID: ")
                job = get_job_by_id(cursor, job_id)
                if job:
                    print("\nFound job:")
                    print_job_details(job)
                else:
                    print("\nNo job found with that ID")
                    
            elif choice == "4":
                limit = input("How many recent jobs to show? (default 10): ")
                limit = int(limit) if limit.isdigit() else 10
                jobs = get_recent_jobs(cursor, limit)
                print(f"\nShowing {len(jobs)} most recent jobs:")
                for job in jobs:
                    print_job_details(job)
            
            elif choice == "5":
                if confirm_action("WARNING: This will delete ALL jobs from the database. Are you sure?"):
                    if clear_database(conn, cursor):
                        print("\nDatabase cleared successfully!")
                    else:
                        print("\nFailed to clear database.")
                else:
                    print("\nDatabase clear cancelled.")
                    
            elif choice == "6":
                print("\nGoodbye!")
                break
                
            else:
                print("\nInvalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        # Always close the connection
        conn.close()


if __name__ == "__main__":
    main() 