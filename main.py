import csv
import asyncio
from playwright.async_api import async_playwright


# Function to read data from CSV file
def read_csv(file_path):
    authors = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            first_name = ""
            last_name = ""

            # Check if Author_Last_Name_First_Name exists and is properly formatted
            if row["Author_Last_Name_First_Name"]:
                name_parts = row["Author_Last_Name_First_Name"].split(", ")
                if len(name_parts) == 2:  # Properly formatted as "Last, First"
                    last_name = name_parts[0]
                    first_name = name_parts[1]
                else:
                    print(f"Warning: Name format is incorrect for: {row['Author_Last_Name_First_Name']}")

            # Extract birth year and death year
            birth_year = row["Birth_Date"][:4] if row["Birth_Date"] else ""
            death_year = row["Death_Date"][:4] if row["Death_Date"] else ""

            # Add to authors list
            authors.append((first_name, last_name, birth_year, death_year))
    return authors


# Function to automate the form submission to FindAGrave using Playwright
async def submit_to_findagrave(first_name, last_name, birth_year, death_year):
    async with async_playwright() as p:
        # Launch the Chromium browser (set headless=True to run in background)
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Navigate to FindAGrave search page
        await page.goto("https://www.findagrave.com/memorial/search")

        # Fill out the search form with the author's data
        await page.locator('label[for="First Name"]').fill(first_name)
        await page.locator('label[for="Last Name(s)"]').fill(last_name)
        # await page.locator('label[for="Middle Name"]').fill(middle_name)
        await page.locator('label[for="Year Born"]').fill(birth_year)
        await page.locator('label[for="Year Died"]').fill(death_year)

        # Submit the form and search
        await page.get_by_role("button", name="SEARCH", exact=True).click()


        # Wait for the results page to load (adjust selector as needed)
        await page.wait_for_selector('h2', timeout=5000)  # Waiting for the results heading

        # Optionally, take a screenshot of the results (for debugging purposes)
        await page.screenshot(path=f'{first_name}_{last_name}_results.png')

        # Close the browser once done
        await browser.close()


# Main function to loop through authors and submit their data
async def main(file_path):
    authors = read_csv(file_path)

    # Iterate through each author and submit their details to FindAGrave
    for first_name, last_name, birth_year, death_year in authors:
        if first_name and last_name and birth_year and death_year:
            print(f"Submitting: {first_name} {last_name} ({birth_year} - {death_year})")
            await submit_to_findagrave(first_name, last_name, birth_year, death_year)
        else:
            print(f"Skipping incomplete data for {first_name} {last_name}")


# Run the script with the local authors.csv file
if __name__ == '__main__':
    file_path = 'authors.csv'  # Path to your local CSV file
    asyncio.run(main(file_path))
