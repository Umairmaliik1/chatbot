/*
 * Embeddable one‑liner widget
 * <script src="https://your‑cdn.com/chatbot.js" data-endpoint="https://api.yourdomain.com/chat"></script>
 */
(function () {
  const endpoint = document.currentScript.dataset.endpoint || "/chat";

  // Create launcher button
  const btn = Object.assign(document.createElement("button"), {
    innerText: "💬 Chat",
    style: `
      position:fixed; bottom:20px; right:20px; z-index:9999;
      background:#4f46e5; color:#fff; border:none; border-radius:50%;
      width:56px; height:56px; font-size:24px; cursor:pointer;
      box-shadow:0 2px 6px rgba(0,0,0,.3);
    `,
  });

  const iframe = document.createElement("iframe");
  Object.assign(iframe.style, {
    position: "fixed",
    bottom: "90px",
    right: "20px",
    width: "360px",
    height: "500px",
    border: "1px solid #ccc",
    borderRadius: "8px",
    display: "none",
    zIndex: "9999",
  });

  document.body.appendChild(btn);
  document.body.appendChild(iframe);

  btn.onclick = () => {
    if (iframe.style.display === "none") {
      // The chat UI is served from the root path ("/") via StaticFiles.
      if (!iframe.src) iframe.src = "/";
      iframe.style.display = "block";
    } else iframe.style.display = "none";
  };
})();
