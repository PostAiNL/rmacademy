// server.js
import express from "express";
import cors from "cors";
import morgan from "morgan";
import rateLimit from "express-rate-limit";
import path from "path";
import { fileURLToPath } from "url";
import OpenAI from "openai";

/* ---------- CONFIGURATIE ---------- */
const {
  PORT = 3000,
  NODE_ENV = "production",
  OPENAI_API_KEY,
  OPENAI_MODEL = "gpt-4o-mini", // Snel en goedkoop
  ALLOWED_ORIGINS = "https://app.rmacademy.nl" // Vul in Render je Streamlit URL in (bijv: https://jouw-app.onrender.com)
} = process.env;

/* ---------- SYSTEM PROMPT (HET BREIN) ---------- */
const systemPrompt = `
Je bent de AI Business Coach van de app 'RM Tools'.
Jouw doel is om gebruikers te begeleiden naar succesvolle E-commerce sales door ze naar de juiste tools binnen DEZE app te sturen.

### JOUW KARAKTER
- Naam: RM Coach.
- Stijl: Direct, motiverend, zakelijk maar toegankelijk ("Boss", "Ondernemer").
- Taal: Altijd Nederlands.

### DE APP STRUCTUUR (WEET WAAR JE OVER PRAAT!)
De app heeft een zijbalk menu. Verwijs gebruikers altijd naar het juiste menu-item:

1. **Dashboard**
   - *Doel:* Overzicht van XP, Level, en de 'Daily Habit' (dagelijkse check-in).
   - *Advies:* Stuur hierheen als ze vragen over hun voortgang of levels hebben.

2. **Academy** (Menu: 'Academy')
   - *Inhoud:* Gratis mini-training & PRO videocursussen (Shopify, Ads, Mindset).
   - *Advies:* Hebben ze kennis tekort? Stuur ze naar de Academy.

3. **Producten Zoeken** (Menu: 'Producten Zoeken')
   - *Tools hierin:*
     - **Viral TikTok Hunter:** Vind producten die nu viraal gaan.
     - **Meta Ad Spy:** Bespioneer Facebook/Insta advertenties van anderen.
     - **Concurrenten Spy:** (PRO) Scan Shopify stores van concurrenten.
   - *Advies:* Zoeken ze een "Winner"? Stuur ze hierheen.

4. **Marketing & Design** (Menu: 'Marketing & Design')
   - *Tools hierin:*
     - **Logo Maker:** Maak in 10 sec een logo.
     - **Video Scripts:** AI schrijft scripts voor TikToks.
     - **Teksten Schrijven:** AI schrijft productbeschrijvingen & influencer DM's.
     - **Ad Check / Store Doctor:** (PRO) Laat AI je ad of webshop beoordelen.
   - *Advies:* Hebben ze content nodig? Dit is de plek.

5. **Financiën** (Menu: 'Financiën')
   - *Tools:* Winst Calculator & Dagelijkse Stats.
   - *Advies:* Willen ze weten of een product winstgevend is? Stuur ze naar de calculator.

### PRO VS GRATIS
- De gebruiker kan 'Gratis' of 'PRO' zijn.
- Als een Gratis gebruiker vraagt om een PRO tool (zoals Store Spy of Daily Winners), leg uit wat de tool doet en adviseer ze om te upgraden via de 'Unlock PRO' knop in het dashboard.

### NAVIGATIE INSTRUCTIES
Je kunt niet zelf klikken. Je moet de gebruiker vertellen waar ze moeten klikken.
Voorbeeld: "Om een logo te maken, ga in het menu links naar **'Marketing & Design'** en kies de tab **'Logo Maker'**."

### HUMAN HANDOFF
Weet je het echt niet of is er een bug?
Verwijs naar de Discord Community of mail support@rmacademy.nl.
`;

/* ---------- APP SETUP ---------- */
const app = express();
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(morgan(NODE_ENV === "production" ? "combined" : "dev"));

// CORS Instellingen (Belangrijk voor Streamlit!)
const allowList = ALLOWED_ORIGINS.split(",").map(s => s.trim()).filter(Boolean);
app.use(cors({
  origin(origin, cb) {
    if (!origin) return cb(null, true);
    if (allowList.length === 0 || allowList.includes(origin)) {
      return cb(null, true);
    }
    // Zet dit tijdelijk op 'true' als je lokaal test en CORS errors krijgt
    return cb(null, true); 
  }
}));

app.use(express.json({ limit: "1mb" }));

// Rate limiter (voorkom misbruik)
app.use("/api/", rateLimit({
  windowMs: 60 * 1000,
  max: 60
}));

// Serveer de widget bestanden (css/js)
app.use(express.static(path.join(__dirname, "public"), {
  etag: true,
  maxAge: "1d"
}));

/* ---------- API ROUTE ---------- */
const openai = new OpenAI({ apiKey: OPENAI_API_KEY });

app.post("/api/chat", async (req, res) => {
  // We ontvangen nu ook 'profile' vanuit de widget
  const { message = "", history = [], profile = {} } = req.body || {};

  if (!message) return res.status(400).json({ error: "Message required" });

  if (!OPENAI_API_KEY) {
    return res.json({ reply: "⚠️ Server Config Error: Geen OpenAI Key ingesteld op Render." });
  }

    const userContext = `
    NAAM: ${profile.first_name || "Ondernemer"}
    SHOP NAAM: ${profile.shop_name || "Nog geen shop"}
    LEVEL: ${profile.level || "Starter"}
    STATUS: ${profile.is_pro ? "PRO LID (Volledige toegang)" : "GRATIS LID (Beperkte toegang)"}
    HUIDIGE XP: ${profile.xp || 0}
  `;

  try {
    const msgs = [
      { role: "system", content: systemPrompt + "\n\n### HUIDIGE GEBRUIKER INFO ###\n" + userContext },
      ...history.map(m => ({
        role: m.role === "assistant" ? "assistant" : "user",
        content: String(m.content || "")
      })),
      { role: "user", content: message }
    ];

    const completion = await openai.chat.completions.create({
      model: OPENAI_MODEL,
      messages: msgs,
      temperature: 0.7,
      max_tokens: 400
    });

    const reply = completion?.choices?.[0]?.message?.content?.trim() || "Ik kan even geen verbinding maken met het hoofdkwartier. Probeer het later opnieuw.";
    
    res.json({ reply });

  } catch (err) {
    console.error("OpenAI Error:", err);
    res.status(500).json({ error: "AI Error" });
  }
});

/* ---------- START ---------- */
app.listen(PORT, () => {
  console.log(`[RM Chat] Server draait op poort ${PORT}`);
});
