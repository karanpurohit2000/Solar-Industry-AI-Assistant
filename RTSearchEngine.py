from googlesearch import search

def googlesearch(query):
    try:
        results = list(search(query + " solar energy", num_results=3))
        if not results:
            return "No search results found for solar energy."

        Answer = "Here are some relevant sources:\n"
        for result in results:
            Answer += f"- {result}\n"

        return Answer
    except Exception as e:
        return f"Search error: {e}"
