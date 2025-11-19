import os
import io
import requests
import pandas as pd
from flask import Flask, request, render_template, send_file
from openai import OpenAI

app = Flask(__name__)

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def search_linkedin(full_name: str):
    query = f'"{full_name}" site:linkedin.com/in'
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "n_results": 3
    }
    resp = requests.post("https://api.tavily.com/search", json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()


def analyze_with_openai(full_name: str, tavily_results: dict):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that identifies LinkedIn profiles from web "
                "search results.\n"
                "You receive a full name and Tavily search results.\n"
                "Your tasks:\n"
                "1. Choose the single best LinkedIn profile URL for this person, "
                "only if it clearly matches.\n"
                "2. Extract the person's role (job title) from the title/snippet.\n"
                "3. Return a confidence score between 0 and 100.\n"
                "If no clear linkedin.com/in profile is found: "
                "linkedin_profile = 'Not found', role = '', confidence = 0.\n"
                "Respond ONLY in JSON with keys: linkedin_profile, role, confidence."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Full name: {full_name}\n"
                f"Tavily results JSON: {tavily_results}"
            ),
        },
    ]

    response = client.chat.completions.create(
        model="gpt-5.1",
        messages=messages,
        temperature=0,
    )

    import json
    try:
        data = json.loads(response.choices[0].message.content)
        return (
            data.get("linkedin_profile", "Not found"),
            data.get("role", ""),
            data.get("confidence", 0),
        )
    except Exception:
        return "Not found", "", 0


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    uploaded_file = request.files.get("file")
    if not uploaded_file:
        return "No file uploaded", 400

    try:
        df = pd.read_excel(uploaded_file)
    except Exception as e:
        return f"Error reading Excel file: {e}", 400

    if "Full Name" not in df.columns:
        return "Excel file must contain a 'Full Name' column.", 400

    df["LinkedIn Profile"] = ""
    df["Role"] = ""
    df["Confidence"] = 0

    for idx, row in df.iterrows():
        full_name = str(row["Full Name"]).strip()
        if not full_name:
            continue

        try:
            tavily_results = search_linkedin(full_name)
            linkedin_profile, role, confidence = analyze_with_openai(
                full_name, tavily_results
            )
        except Exception:
            linkedin_profile, role, confidence = "Not found", "", 0

        if not linkedin_profile:
            linkedin_profile = "Not found"

        df.at[idx, "LinkedIn Profile"] = linkedin_profile
        df.at[idx, "Role"] = role
        df.at[idx, "Confidence"] = confidence

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="lead_profile_results.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)
