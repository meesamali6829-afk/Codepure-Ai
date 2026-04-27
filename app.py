from flask import Flask, render_template, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# GROQ API KEY yahan dalein
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

@app.route('/')
def index():
    # index.html file templates folder ke andar honi chiye
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_code():
    data = request.json
    if not data:
        return jsonify({"result": "Error: No data received"}), 400
        
    user_code = data.get('code')
    language = data.get('language')
    feature = data.get('feature')

    if not user_code or not language or not feature:
        return jsonify({"result": "Error: Missing data"}), 400

    # System Prompt: Isko mazeed sakht kar diya gaya hai full code ke liye
    system_prompt = (
        "You are CodePure AI, the world's leading expert in software engineering. "
        f"Your task is to analyze the following {language} code using the '{feature}' mode. "
        "\n\nSTRICT OUTPUT FORMAT:\n"
        "1. ANALYSIS: Har galti aur masle ko alag point mein wazeh karein.\n"
        "2. CHANGES MADE: Jo sahi kiya gaya hai uski list dein.\n"
        "3. FINAL FULL CODE: Provide the COMPLETE, functional, and clean version of the code. "
        "Do not skip any parts. Full code must be provided regardless of the feature selected.\n"
        "\nRules: Be concise, technical, and ensure the code is production-ready."
    )

    # Feature-specific instructions
    if feature == "Modernize":
        user_prompt = f"Modernize this {language} code for maximum efficiency and modern syntax. Provide the FULL code after improvements:\n\n{user_code}"
    elif feature == "Hunt":
        user_prompt = f"Identify all bugs and risks in this {language} code. After listing them, provide the FULL corrected code:\n\n{user_code}"
    else:  # Quick Fixer
        user_prompt = f"Provide a rapid fix for this {language} code. Give a brief explanation and then the FULL functional code:\n\n{user_code}"

    try:
        # Model replaced with llama-3.1-8b-instant (Fastest & Most Cost-Efficient)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2, # Accuracy ke liye low temperature
            max_tokens=4096
        )

        ai_response = completion.choices[0].message.content
        return jsonify({"result": ai_response})

    except Exception as e:
        # Agar API fail ho toh user ko clear message mile
        return jsonify({"result": f"Backend Error: {str(e)}"}), 500

if __name__ == '__main__':
    # Threaded=True aur use_reloader=False server ko crash hone se bachata hai
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
