from fastmcp import FastMCP

mcp = FastMCP("demo")


def _download_content_logic(url: str) -> str:
    """Internal logic for downloading content."""
    import requests
    prefix = "https://r.jina.ai/"
    if url.startswith(prefix):
        jina_url = url
    else:
        jina_url = f"{prefix}{url}"
    
    response = requests.get(jina_url)
    response.raise_for_status()
    return response.text

@mcp.tool
def download_content(url: str) -> str:
    """Download content from any website using Jina Reader.
    
    Args:
        url: The website URL to download content from.
    """
    return _download_content_logic(url)

@mcp.tool
def count_characters(text: str) -> int:
    """Count the exact number of characters in a text string.
    
    Args:
        text: The text string to count characters in.
    
    Returns:
        The exact number of characters in the text.
    """
    return len(text)


if __name__ == "__main__":
    mcp.run()