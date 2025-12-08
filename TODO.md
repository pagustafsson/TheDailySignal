# The Daily Signal - To Do

## 2025-12-09 (Imorgon)

### Lägg till bildgenerering med Imagen API

**Problem:** Artiklar uppdateras automatiskt, men bilden förblir densamma.

**Lösning:** Integrera Google Imagen API för att generera relevanta bilder till varje artikel.

**Steg:**
1. [ ] Sätt upp Google Cloud-projekt med Imagen API aktiverat
2. [ ] Skapa service account och ladda ner JSON-nyckel
3. [ ] Lägg till `GOOGLE_CLOUD_CREDENTIALS` secret i GitHub repo
4. [ ] Uppdatera `scripts/generate_article.py` för att:
   - Generera bildprompt baserat på artikelns ämne
   - Anropa Imagen API för att skapa bild
   - Spara bild som `article-image.webp`
   - Uppdatera `alt`-text i HTML
5. [ ] Testa workflowen manuellt
6. [ ] Verifiera att nya bilder genereras vid varje körning

**Dokumentation:**
- [Imagen API docs](https://cloud.google.com/vertex-ai/docs/generative-ai/image/generate-images)
