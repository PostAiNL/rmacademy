(function (global) {
    "use strict";

    var SERVER = global.BMS_CHAT_SERVER || "";
    var DOC = global.document;

    // --- 1. USER DATA OPHALEN (Uit Streamlit injectie) ---
    // Dit is de cruciale stap. Als Python data heeft klaargezet, gebruiken we die.
    var USER_PROFILE = global.RM_USER_DATA || null;

    // Elementen aanmaken
    var launcher = DOC.createElement("div");
    launcher.id = "bms-chat-launcher";
    launcher.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>';
    
    var chat = DOC.createElement("div");
    chat.id = "bms-chat";
    chat.innerHTML = `
        <div class="hdr">
            <div class="avatar">🚀</div>
            <div class="titles">
                <h3>RM Coach</h3>
                <p>Jouw AI Business Partner</p>
            </div>
            <button class="close" id="bms-close">×</button>
        </div>
        <div id="bms-body"></div>
        <div class="bms-suggestions" id="bms-suggestions"></div>
        <div class="inp">
            <input id="bms-input" type="text" placeholder="Stel je vraag..." autocomplete="off" />
            <button id="bms-send">➤</button>
        </div>
    `;

    DOC.body.appendChild(launcher);
    DOC.body.appendChild(chat);

    // Variabelen
    var bodyEl = DOC.getElementById("bms-body");
    var inputEl = DOC.getElementById("bms-input");
    var sendBtn = DOC.getElementById("bms-send");
    var closeBtn = DOC.getElementById("bms-close");
    var suggestionsEl = DOC.getElementById("bms-suggestions");
    
    var history = [];

    // --- FUNCTIES ---

    function toggleChat() {
        chat.classList.toggle("open");
        if (chat.classList.contains("open")) {
            inputEl.focus();
            if (history.length === 0) startConversation();
        }
    }

    function startConversation() {
        // Welkomstbericht op basis van User Data
        var greeting = "Hi! Ik ben de RM Coach. Waar loop je tegenaan?";
        
        if (USER_PROFILE) {
            var name = USER_PROFILE.first_name || "Ondernemer";
            var shop = USER_PROFILE.shop_name ? "met " + USER_PROFILE.shop_name : "met je business";
            greeting = `Hi ${name}! 👋 Goed bezig ${shop}. Waar kan ik je vandaag mee helpen?`;
            
            // Suggesties op maat (simpel voorbeeld)
            var suggestions = [];
            if (USER_PROFILE.level < 2) {
                suggestions = ["Hoe vind ik een product?", "Wat is de volgende stap?", "Help me met mijn shop naam"];
            } else {
                suggestions = ["Hoe schaal ik mijn ads?", "Analyseer mijn conversie", "Geef me een marketing strategie"];
            }
            setSuggestions(suggestions);
        } else {
            // Geen user data (fallback)
            setSuggestions(["Hoe begin ik?", "Wat is een winnend product?", "Help met marketing"]);
        }

        addMessage(greeting, "bot");
    }

    function addMessage(text, sender) {
        var div = DOC.createElement("div");
        div.className = "bms-msg " + sender;
        
        // Simpele formatting voor bot berichten
        if (sender === "bot") {
            // Bold
            text = text.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
            // Links
            text = text.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
            // Headings
            text = text.replace(/^(.*?:)/gm, '<span class="bms-heading">$1</span>');
            // Newlines
            text = text.replace(/\n/g, '<br>');
        }

        div.innerHTML = `<div class="bubble">${text}</div>`;
        bodyEl.appendChild(div);
        bodyEl.scrollTop = bodyEl.scrollHeight;

        // History bijhouden (voor API)
        history.push({ role: sender === "user" ? "user" : "assistant", content: text });
    }

    function setSuggestions(list) {
        suggestionsEl.innerHTML = "";
        list.forEach(function(txt) {
            var btn = DOC.createElement("button");
            btn.textContent = txt;
            btn.onclick = function() { 
                inputEl.value = txt; 
                handleSend(); 
            };
            suggestionsEl.appendChild(btn);
        });
    }

    function showTyping() {
        var div = DOC.createElement("div");
        div.id = "bms-typing";
        div.className = "bms-msg bot";
        div.innerHTML = '<div class="bubble typing-dots"></div>';
        bodyEl.appendChild(div);
        bodyEl.scrollTop = bodyEl.scrollHeight;
    }

    function hideTyping() {
        var el = DOC.getElementById("bms-typing");
        if (el) el.remove();
    }

    function handleSend() {
        var txt = inputEl.value.trim();
        if (!txt) return;

        addMessage(txt, "user");
        inputEl.value = "";
        suggestionsEl.innerHTML = ""; // Suggesties weg na typen
        showTyping();

        // DE API CALL
        fetch(SERVER + "/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: txt,
                history: history.slice(0, -1).slice(-6), // Laatste 6 berichten context
                profile: USER_PROFILE // STUUR DE RM DATA MEE!
            })
        })
        .then(res => res.json())
        .then(data => {
            hideTyping();
            addMessage(data.reply, "bot");
        })
        .catch(err => {
            hideTyping();
            addMessage("⚠️ Oeps, ik kan even geen verbinding maken. Probeer het later.", "bot");
            console.error(err);
        });
    }

    // Event Listeners
    launcher.onclick = toggleChat;
    closeBtn.onclick = toggleChat;
    sendBtn.onclick = handleSend;
    inputEl.onkeypress = function(e) { if(e.key === "Enter") handleSend(); };

// --- NUDGE LOGICA (Punt 3) ---
    // Als de gebruiker nieuw is (weinig XP) en de chat nog niet open is...
    if (USER_PROFILE && USER_PROFILE.xp < 50) {
        // ... wacht dan 4 seconden en open de chat automatisch
        setTimeout(function() {
            var chatBox = DOC.getElementById("bms-chat");
            // Check of hij niet al open is
            if (chatBox && !chatBox.classList.contains("open")) {
                toggleChat(); // Open de chat
                // Speel eventueel een zacht geluidje af of laat de knop wiebelen (optioneel)
                console.log("🔔 Auto-Nudge geactiveerd voor nieuwe gebruiker.");
            }
        }, 4000); 
    }
    
})(window);
