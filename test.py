"""
Test script for MCP tools.
This directly calls the tool functions to test them locally.
"""

from main import _download_content_logic


def count_characters(text: str) -> int:
    """Local version of count_characters for testing."""
    return len(text)



def test_count_characters():
    """Test the character counting tool."""
    print("=" * 60)
    print("Testing count_characters tool")
    print("=" * 60)
    
    test_cases = [
        "Hello World",
        "MCP is awesome!",
        "12345",
        "Special chars: !@#$%^&*()",
        "Multi\nline\ntext",
    ]
    
    for text in test_cases:
        count = count_characters(text)
        print(f"Text: {repr(text)}")
        print(f"Character count: {count}")
        print()


def test_download_content():
    """Test the download content tool."""
    print("=" * 60)
    print("Testing download_content tool")
    print("=" * 60)
    
    url = "https://example.com"
    print(f"Downloading content from: {url}")
    
    try:
        content = _download_content_logic(url)
        print(f"Downloaded {len(content)} characters")
        print(f"First 200 characters:\n{content[:200]}...")
    except Exception as e:
        print(f"Error: {e}")



if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("MCP Tools Test Suite")
    print("=" * 60 + "\n")
    
    test_count_characters()
    test_download_content()
    
    print("=" * 60)
    print("All tests completed!")
    print("=" * 60)
