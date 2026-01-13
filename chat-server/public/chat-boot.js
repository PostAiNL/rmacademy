(function (w, d) {
  var s = d.currentScript;
  // Dit pakt de URL waar dit bestand vandaan komt (jouw Render URL)
  var server = "";
  if (s) {
      var src = s.src;
      var url = new URL(src);
      server = url.origin;
  }
  
  // Als er handmatig een server is ingesteld via Python injectie, gebruik die
  if (w.BMS_CHAT_SERVER) server = w.BMS_CHAT_SERVER;

  if (!server) { console.error("[RM Chat] Server URL ontbreekt"); return; }

  w.BMS_CHAT_SERVER = server;
  
  // CSS Laden
  var link = d.createElement("link");
  link.rel = "stylesheet";
  link.href = server + "/chat-widget.css";
  d.head.appendChild(link);

  // JS Widget Laden
  var js = d.createElement("script");
  js.src = server + "/chat-widget.js";
  js.defer = true;
  d.head.appendChild(js);

})(window, document);
