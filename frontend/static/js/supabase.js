import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm'

// Access global variables set in the HTML templates
const supabaseUrl = window.SUPABASE_URL;
const supabaseKey = window.SUPABASE_KEY;

export const supabase = createClient(supabaseUrl, supabaseKey);