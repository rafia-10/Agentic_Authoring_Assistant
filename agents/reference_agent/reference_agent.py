import requests
import xml.etree.ElementTree as ET

def search_arxiv(query: str, max_results: int = 5):
    """
    Search arXiv API for papers related to the query.
    Returns a list of references with title, authors, year, link.
    """
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"arXiv API error: {response.status_code}")

    root = ET.fromstring(response.text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}

    references = []
    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns).text.strip()
        link = entry.find("atom:id", ns).text.strip()
        published = entry.find("atom:published", ns).text[:4]  # year only

        authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]

        references.append({
            "title": title,
            "authors": authors,
            "year": published,
            "link": link
        })

    return references


def generate_references(description: str, tags=None, max_results=5):
    """
    Generate references for a project description using arXiv.
    Uses description + tags to build search query.
    """
    if tags:
        query = " ".join(tags)
    else:
        query = description

    return search_arxiv(query, max_results=max_results)
