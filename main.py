from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["NOTION_DATABASE_ID"]

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

@app.route("/add-event", methods=["POST"])
def add_event():
    data = request.json
    title = data.get("title")
    date = data.get("date")
    description = data.get("description", "")

    notion_data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": title}}]},
            "Date": {"date": {"start": date}},
            "Description": {"rich_text": [{"text": {"content": description}}]}
        }
    }

    response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=notion_data)

    if response.status_code in [200, 201]:
        return jsonify({"success": True})
    return jsonify({"success": False, "error": response.text}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)