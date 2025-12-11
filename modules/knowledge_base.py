import os

def search_course_content(query):
    """
    Zoekt in het bestand 'course_content.txt' naar relevante informatie.
    Dit is een simpele vorm van RAG (Retrieval Augmented Generation).
    """
    file_path = "course_content.txt"
    
    if not os.path.exists(file_path):
        return "Geen cursusmateriaal gevonden. Vraag de admin om 'course_content.txt' te vullen."
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Simpele zoekfunctie: splitst tekst in paragrafen en kijkt of trefwoorden erin staan
        # In een productie-app zou je hier een Vector Database (Pinecone) gebruiken.
        paragraphs = content.split("\n\n")
        relevant_chunks = []
        
        keywords = query.lower().split()
        for p in paragraphs:
            # Als een van de keywords in de paragraaf zit, is het relevant
            if any(k in p.lower() for k in keywords if len(k) > 3):
                relevant_chunks.append(p)
                
        if not relevant_chunks:
            return ""
            
        # Geef de top 3 meest relevante stukken terug
        return "\n---\n".join(relevant_chunks[:3])
        
    except Exception as e:
        return f"Fout bij lezen cursusdata: {e}"