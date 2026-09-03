import requests
from bs4 import BeautifulSoup


def extract_content(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        title = ""

        if soup.title:
            title = soup.title.text.strip()

        h1 = [
            item.get_text(strip=True)
            for item in soup.find_all("h1")
        ]

        h2 = [
            item.get_text(strip=True)
            for item in soup.find_all("h2")
        ]

        content = soup.get_text(
            separator=" ",
            strip=True
        )

        links = []

        for link in soup.find_all(
            "a",
            href=True
        ):

            links.append({
                "anchor":
                    link.get_text(strip=True),

                "href":
                    link["href"]
            })

        return {
            "url": url,
            "title": title,
            "h1": h1,
            "h2": h2,
            "content": content,
            "links": links
        }

    except Exception as error:

        return {
            "url": url,
            "error": str(error)
        }
