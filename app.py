from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# TODO: Task 1 - Define the Problem
# Create a new event from JSON input
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()
    if not data or not data.get("title"):
        return jsonify({"error":"Bad request"}),400
    else:
        new_id = max((e.id for e in events),default=0)+1
        new_event = Event(new_id,data["title"])
        events.append(new_event)
        return jsonify(new_event.to_dict()),201


# TODO: Task 1 - Define the Problem
# Update the title of an existing event
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()
    target = next((e for e in events if e.id == event_id),None)
    if not data or not data.get("title"):
        return jsonify({"error":"No title"}),400
    elif not target:
        return jsonify({"error":"No id matching"}),404
    else:
        target.title = data["title"]
        return jsonify(target.to_dict()), 200


# TODO: Task 1 - Define the Problem
# Remove an event from the list
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    global events
    target = next((e for e in events if e.id == event_id),None)
    if not target:
        return jsonify({"error":"No id matching"}),404
    else:
        events.remove(target)
        return jsonify(),204

if __name__ == "__main__":
    app.run(debug=True)
