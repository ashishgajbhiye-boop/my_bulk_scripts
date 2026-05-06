from playwright.sync_api import sync_playwright

base_url = "https://www.justice.gov/epstein/files/DataSet%202/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    # Open page and manually pass age verification ONCE
    page.goto("https://www.justice.gov/epstein/doj-disclosures/data-set-2-files")

    input("Press ENTER after you pass age verification...")

    for i in range(3159, 3208):
        filename = f"EFTA{i:08d}.pdf"
        url = base_url + filename

        print("Downloading", filename)

        response = page.goto(url)

        if response and "pdf" in response.headers.get("content-type", ""):
            with open(filename, "wb") as f:
                f.write(response.body())
        else:
            print("❌ Failed:", filename)

    browser.close()