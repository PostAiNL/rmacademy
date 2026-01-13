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
  ALLOWED_ORIGINS = "" // Vul in Render je Streamlit URL in (bijv: https://jouw-app.onrender.com)
} = process.env;

/* ---------- SYSTEM PROMPT (DE PERSOONLIJKHEID) ---------- */
const systemPrompt = `
Je bent de AI Business Coach van 'RM Tools'. Je helpt ondernemers met E-commerce, Dropshipping, Marketing en Mindset.

JOUW DOEL:
Geef kort, krachtig en strategisch advies om de gebruiker te helpen groeien naar de volgende mijlpaal.

CONTEXT GEBRUIKEN:
Je krijgt data over de gebruiker (Naam, Shop, Level). Gebruik dit!
- Spreek de gebruiker aan bij voornaam.
- Als ze een shopnaam hebben, refereer daaraan.
- Level 1 (Starter): Geef simpele, motiverende uitleg.
- Level 5+ (Expert): Geef geavanceerd, data-gedreven advies.

DE REGELS:
1. Schrijf ALTIJD in het Nederlands.
2. Gebruik korte alinea's en bulletpoints. Geen muren van tekst.
3. Wees een mentor: streng maar rechtvaardig en enthousiast.
4. Ga niet in op vragen die niets met ondernemen te maken hebben.

HUMAN HANDOFF (FALLBACK):
Jij bent een AI. Als de gebruiker vraagt om "een mens", "support", of als je het antwoord technisch niet weet (bijv. bugs in de app, betalingen):
Zeg dan vriendelijk:
"Voor specifieke accountvragen of technische support kun je het beste even schakelen met ons team via de Discord Community of mail naar support@rmacademy.nl."
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

  // Bouw de gebruikerscontext string
  const userContext = `
    NAAM: ${profile.first_name || "Ondernemer"}
    SHOP: ${profile.shop_name || "Nog geen naam"}
    LEVEL: ${profile.level || "Starter"}
    XP: ${profile.xp || 0}
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
