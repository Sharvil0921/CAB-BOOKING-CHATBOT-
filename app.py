

import random
from flask import Flask, jsonify, render_template, request, session

app = Flask(__name__)
app.secret_key = "change-this-secret-key"  # needed for Flask sessions

# ---------- Predefined data ----------
CABS = {1: ("Auto", 12), 2: ("Sedan", 18), 3: ("SUV", 25)}
ROUTES = {
    1: ("Pune Station", "Shivajinagar", 5),
    2: ("Swargate", "Kothrud", 8),
    3: ("Hinjawadi", "Wakad", 10),
}


def opts(pairs):
    return [{"value": v, "label": l} for v, l in pairs]


def menu_reply(prefix=None):
    """Main menu (state = menu)."""
    session["state"] = "menu"
    msgs = list(prefix or [])
    msgs.append({"type": "text", "text": "Main menu. What would you like to do?"})
    return {"messages": msgs, "options": opts([(1, "Book Ride"), (2, "Exit")])}


def cab_reply(prefix=None):
    session["state"] = "cab"
    msgs = list(prefix or [])
    msgs.append({"type": "text", "text": "Which cab would you like?"})
    return {"messages": msgs, "options": opts(
        [(k, f"{n} · ₹{r}/km") for k, (n, r) in CABS.items()])}


def route_reply(prefix=None):
    session["state"] = "route"
    msgs = list(prefix or [])
    msgs.append({"type": "text", "text": "Pick your route."})
    return {"messages": msgs, "options": opts(
        [(k, f"{s} to {d} · {km} km") for k, (s, d, km) in ROUTES.items()])}


def confirm_reply(prefix=None):
    session["state"] = "confirm"
    msgs = list(prefix or [])
    msgs.append({"type": "text",
                 "text": "You can still cancel for free. Once the OTP is shared, the ride is locked."})
    return {"messages": msgs, "options": opts(
        [(1, "Confirm & Share OTP"), (2, "Cancel Ride")])}


def error(text, reply_fn):
    return reply_fn([{"type": "error", "text": text}])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/start", methods=["POST"])
def start():
    session.clear()
    return jsonify(menu_reply([{"type": "text",
                                "text": "Hi, I'm your cab booking assistant."}]))


@app.route("/api/choose", methods=["POST"])
def choose():
    raw = str((request.get_json(silent=True) or {}).get("choice", "")).strip()
    choice = int(raw) if raw.isdigit() else None
    state = session.get("state", "menu")

    if state == "menu":
        if choice == 1:
            return jsonify(cab_reply())
        if choice == 2:
            session.clear()
            return jsonify({
                "messages": [{"type": "text",
                              "text": "Thank you for using the Cab Booking Chatbot. Goodbye!"}],
                "options": opts([(0, "Start again")]), "ended": True})
        return jsonify(error("Invalid choice. Please pick 1 or 2.", menu_reply))

    if state == "cab":
        if choice not in CABS:
            return jsonify(error("Invalid cab choice. Please pick 1, 2 or 3.", cab_reply))
        session["cab"] = choice
        return jsonify(route_reply())

    if state == "route":
        if choice not in ROUTES:
            return jsonify(error("Invalid route. Please pick 1, 2 or 3.", route_reply))
        session["route"] = choice
        cab_name, rate = CABS[session["cab"]]
        src, dst, km = ROUTES[choice]
        summary = {"type": "summary", "cab": cab_name, "source": src,
                   "destination": dst, "distance": km, "rate": rate,
                   "fare": rate * km}
        return jsonify(confirm_reply([summary]))

    if state == "confirm":
        if choice == 2:  # cancelled BEFORE otp -> allowed, no OTP generated
            return jsonify(menu_reply([{
                "type": "cancel",
                "text": "Your ride has been cancelled. No OTP was shared."}]))
        if choice == 1:
            otp = random.randint(1000, 9999)
            session["state"] = "locked"
            msgs = [
                {"type": "otp", "otp": str(otp)},
                {"type": "lock",
                 "text": "Cancellation is now locked. A ride cannot be cancelled after the OTP is shared."},
                {"type": "text",
                 "text": "Booking confirmed! Your driver is on the way. Share the OTP at pickup."},
            ]
            return jsonify(menu_reply(msgs))
        return jsonify(error("Invalid choice. Please pick 1 or 2.", confirm_reply))

    return jsonify(menu_reply())


if __name__ == "__main__":
    app.run(debug=True)
