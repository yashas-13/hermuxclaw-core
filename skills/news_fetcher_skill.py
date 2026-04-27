# skills/news_fetcher_skill.py
import requests
from skills.base_skill import BaseSkill

class NewsFetcherSkill(BaseSkill):
    """
    Sovereign News Aggregator.
    Fetches real-time headlines for a specific region.
    """
    META = {
        "name": "news_fetcher_skill",
        "version": "1.0.0",
        "inputs": ["region", "limit"],
        "outputs": ["headlines", "source"],
        "dependencies": ["requests"]
    }

    def run(self, input_data):
        region = input_data.get("region", "India")
        limit = input_data.get("limit", 5)
        
        # Using a public RSS-to-JSON or search-based API for demonstration
        # In production, this targets the Pravidhi Data Hive
        url = f"https://news.google.com/rss/search?q={region}+today&hl=en-IN&gl=IN&ceid=IN:en"
        
        try:
            print(f"[*] NewsFetcher: Sourcing data for {region}...")
            # We fetch the raw RSS and perform a light parse
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            
            # Simple keyword extraction from the RSS (Deterministic Logic)
            content = r.text
            items = content.split("<item>")[1:limit+1]
            headlines = []
            
            for item in items:
                title = item.split("<title>")[1].split("</title>")[0]
                headlines.append(title)
                
            return {"status": "success", "headlines": headlines, "source": "Google News RSS"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    nf = NewsFetcherSkill()
    print(nf.run({"region": "India", "limit": 5}))
