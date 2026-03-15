"""
Command-line interface (CLI) entry point for the DVD collection app.

This is your original CLI - kept for backup and reference.
The new web version is in app/main.py
"""

from dvd_repo import insert_dvd, remove_dvd, get_all_dvds

def main():
    """
    Menu-driven CLI:
    - Add a movie
    - Remove a movie
    - View collection
    - Exit
    """

    print("Starting DVD CLI...")

    while True:
        print("\n--- DVD Collection Menu ---")
        print("1. Add a movie")
        print("2. Remove a movie")
        print("3. View collection")
        print("4. Exit")

        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            title = input("Movie title: ").strip()
            location = input("Purchase location: ").strip()
            message = insert_dvd(title, location)
            print(message)

        elif choice == "2":
            title = input("Movie title to remove: ").strip()
            message = remove_dvd(title)
            print(message)

        elif choice == "3":
            df = get_all_dvds()
            if df.empty:
                print("Collection is empty.")
            else:
                print()
                print(df.to_string(index=False))
                print(f"\nTotal DVDs: {len(df)}")

        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()