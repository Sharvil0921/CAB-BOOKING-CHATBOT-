// ---------- Chat behaviour (talks to the Flask API) ----------
const chat = document.getElementById("chat");
const optionsBox = document.getElementById("options");
const typed = document.getElementById("typed");

// Escape text so user input can't inject HTML
const esc = s => String(s).replace(/[&<>"]/g, c =>
  ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

// Add one bubble/card to the chat
function add(cls, html) {
  const d = document.createElement("div");
  d.className = cls;
  d.innerHTML = html;
  chat.appendChild(d);
  chat.scrollTop = chat.scrollHeight;
}

// Draw the bot's reply and the option buttons
function render(data) {
  data.messages.forEach(m => {
    if (m.type === "text") add("msg bot", esc(m.text));
    else if (m.type === "error") add("msg error", esc(m.text));
    else if (m.type === "cancel") add("msg cancel", esc(m.text));
    else if (m.type === "lock") add("msg lock", "🔒 " + esc(m.text));
    else if (m.type === "summary") {
      add("ticket", `
        <div class="top">Ride summary</div>
        <dl>
          <dt>Cab type</dt><dd>${esc(m.cab)}</dd>
          <dt>From</dt><dd>${esc(m.source)}</dd>
          <dt>To</dt><dd>${esc(m.destination)}</dd>
          <dt>Distance</dt><dd>${m.distance} km</dd>
          <dt>Rate</dt><dd>₹${m.rate}/km</dd>
        </dl>
        <div class="fare"><span>Total fare (${m.distance} × ${m.rate})</span><span>₹${m.fare}</span></div>`);
    } else if (m.type === "otp") {
      const boxes = m.otp.split("").map((d, i) =>
        `<span class="pop" style="animation-delay:${i * 120}ms">${d}</span>`).join("");
      add("otp", `<small>OTP shared with you</small><div class="digits">${boxes}</div>`);
    }
  });

  optionsBox.innerHTML = "";
  data.options.forEach(o => {
    const b = document.createElement("button");
    b.textContent = o.label;
    if (o.label === "Cancel Ride") b.className = "danger";
    b.onclick = () => send(o.value, o.label);
    optionsBox.appendChild(b);
  });
  const first = optionsBox.querySelector("button");
  if (first) first.focus();
}

// Send the user's choice to the server
async function send(value, label) {
  if (value === 0) return start();          // "Start again" after goodbye
  add("msg user", esc(label || value));
  const res = await fetch("/api/choose", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ choice: value })
  });
  render(await res.json());
}

// Reset the chat and show the main menu
async function start() {
  chat.innerHTML = "";
  const res = await fetch("/api/start", { method: "POST" });
  render(await res.json());
}

document.getElementById("form").addEventListener("submit", e => {
  e.preventDefault();
  const v = typed.value.trim();
  if (!v) return;
  typed.value = "";
  send(v, v);
});
document.getElementById("restart").onclick = start;

start();
