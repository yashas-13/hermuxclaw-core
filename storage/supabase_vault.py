import os
import json
from supabase import create_client, Client

class SupabaseVault:
    """
    Federated Data Vault for HermuXclaw-CORE.
    Synchronizes local state with a central Supabase instance for multi-device awareness.
    """
    def __init__(self):
        self.url = "https://gnorslgqghumwmgoqwhk.supabase.co"
        self.key = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdub3JzbGdxZ2h1bXdtZ29xd2hrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTIzMDUzNSwiZXhwIjoyMDYwODA2NTM1fQ.ybht5pNxY4QC4dHMGGOD-Rj66LATISW5N9DiHMNLeIs")
        try:
            self.client: Client = create_client(self.url, self.key)
        except Exception as e:
            print(f"[!] Supabase Initialization Failed: {e}")
            self.client = None

    def sync_skill(self, skill_name, meta, code):
        """Uploads a verified skill to the global vault."""
        if not self.client: return False
        try:
            data = {
                "name": skill_name,
                "meta": json.dumps(meta),
                "code": code,
                "node_id": os.uname()[1] # Identify which device sent this
            }
            # Upsert into a 'vault_skills' table
            self.client.table("vault_skills").upsert(data).execute()
            return True
        except Exception as e:
            print(f"[!] Supabase Sync Failed: {e}")
            return False

    def fetch_global_skills(self):
        """Retrieves best-performing skills from the entire swarm."""
        if not self.client: return []
        try:
            res = self.client.table("vault_skills").select("*").execute()
            return res.data
        except:
            return []

vault = SupabaseVault()
