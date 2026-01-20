import os
import zipfile
import requests
from pathlib import Path

# Minimalistic search implementation based on minsearch
class Index:
    def __init__(self, text_fields, keyword_fields=None):
        self.text_fields = text_fields
        self.keyword_fields = keyword_fields or []
        self.docs = []
        self.df = None
        self.vectorizer = None
        self.matrix = None
    
    def fit(self, docs):
        from sklearn.feature_extraction.text import TfidfVectorizer
        import pandas as pd
        
        self.docs = docs
        self.df = pd.DataFrame(docs)
        
        # Combine text fields for TF-IDF
        combined_text = self.df[self.text_fields].apply(
            lambda row: ' '.join(row.values.astype(str)), axis=1
        )
        
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.matrix = self.vectorizer.fit_transform(combined_text)
    
    def search(self, query, filter_dict=None, boost_dict=None, num_results=10):
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np
        
        # Transform query
        query_vec = self.vectorizer.transform([query])
        
        # Calculate similarity
        scores = cosine_similarity(query_vec, self.matrix).flatten()
        
        # Apply filters
        if filter_dict:
            mask = np.ones(len(self.df), dtype=bool)
            for field, value in filter_dict.items():
                if field in self.df.columns:
                    mask &= (self.df[field] == value).values
            scores = scores * mask
        
        # Get top results
        top_indices = np.argsort(scores)[::-1][:num_results]
        
        results = []
        for idx in top_indices:
            if scores[idx] > 0:
                result = self.docs[idx].copy()
                result['score'] = float(scores[idx])
                results.append(result)
        
        return results


def download_and_extract_zip(url, extract_to='./data'):
    """Download and extract zip file if not already present"""
    zip_path = os.path.join(extract_to, 'fastmcp.zip')
    
    # Create directory if it doesn't exist
    os.makedirs(extract_to, exist_ok=True)
    
    # Check if already extracted
    extracted_path = os.path.join(extract_to, 'fastmcp-main')
    if os.path.exists(extracted_path):
        print(f"✓ Archive already extracted at {extracted_path}")
        return extracted_path
    
    # Download if not exists
    if not os.path.exists(zip_path):
        print(f"Downloading {url}...")
        response = requests.get(url)
        response.raise_for_status()
        
        with open(zip_path, 'wb') as f:
            f.write(response.content)
        print(f"✓ Downloaded to {zip_path}")
    else:
        print(f"✓ Zip file already exists at {zip_path}")
    
    # Extract
    print("Extracting...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"✓ Extracted to {extract_to}")
    
    return extracted_path


def read_md_files(root_path):
    """Read all .md and .mdx files from the extracted archive"""
    documents = []
    root = Path(root_path)
    
    for file_path in root.rglob('*'):
        if file_path.suffix in ['.md', '.mdx']:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Remove the first part of the path (fastmcp-main/)
                relative_path = str(file_path.relative_to(root))
                
                documents.append({
                    'filename': relative_path,
                    'content': content
                })
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    print(f"✓ Read {len(documents)} markdown files")
    return documents


def create_search_function(index):
    """Create a search function that retrieves 5 most relevant documents"""
    def search(query, num_results=5):
        return index.search(query, num_results=num_results)
    return search


def main():
    # Step 1: Download and extract
    url = "https://github.com/jlowin/fastmcp/archive/refs/heads/main.zip"
    extracted_path = download_and_extract_zip(url)
    
    # Step 2: Read markdown files
    documents = read_md_files(extracted_path)
    
    # Step 3: Index with minsearch
    print("\nIndexing documents...")
    index = Index(text_fields=['content', 'filename'])
    index.fit(documents)
    print("✓ Indexing complete")
    
    # Step 4: Create search function
    search = create_search_function(index)
    
    # Step 5: Test with query "demo"
    print("\n" + "="*60)
    print("Testing search with query: 'demo'")
    print("="*60)
    
    results = search("demo", num_results=5)
    
    print(f"\nFound {len(results)} results:\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['filename']}")
        print(f"   Score: {result['score']:.4f}")
        print()
    
    # Answer the question
    if results:
        first_file = results[0]['filename']
        print("="*60)
        print(f"The first file returned with query 'demo' is:")
        print(f"  → {first_file}")
        print("="*60)
        
        return first_file
    else:
        print("No results found!")
        return None


if __name__ == "__main__":
    first_result = main()