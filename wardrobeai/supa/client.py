from supabase import create_client

# Supabase project URL
SUPABASE_URL = "https://zfonywjyfbuygzsxrzox.supabase.co"

# Secret key (server-side only, do not expose in frontend)
SUPABASE_KEY = "sb_secret_Gw49L1PfkcKddoUUYW37kA_T88ECJyZ"

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
