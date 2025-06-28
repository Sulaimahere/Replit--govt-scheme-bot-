

from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the CSV
df = pd.read_csv("attached_assets/CenterSectorScheme2021-22[1]_1751106824256.csv")

# DEBUG: Show columns to verify they are correct
print("CSV Columns:", df.columns)

@app.route("/", methods=["GET", "POST"])
def home():
    user_type = ""
    matched_schemes = []

    if request.method == "POST":
        user_type = request.form.get("user_type", "").strip()
        print("🔍 User entered:", user_type)

        filtered = df.copy()

        if user_type:
            # Case-insensitive filtering on both Ministry/Department and Scheme
            filtered = filtered[
                filtered["Ministry/Department"].str.contains(user_type, case=False, na=False) |
                filtered["Scheme"].str.contains(user_type, case=False, na=False)
            ]

        print("✅ Matched rows:", len(filtered))

        matched_schemes = filtered.to_dict(orient="records")

        return render_template("result.html", user_type=user_type, schemes=matched_schemes)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
