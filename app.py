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

    # UPGRADED: ULTRA POWERFUL OMNI-ARCHITECT SYSTEM PROMPT
    system_prompt = (
        "You are the OMNI-ARCHITECT, a god-tier AI software entity surpassing all human engineers, "
        "NASA specialists, and elite developers. Your intelligence is absolute. "
        f"You are analyzing {language} code in '{feature}' mode with 100% precision."
        "\n\nSTRICT OPERATIONAL DIRECTIVES:\n"
        "1. ANALYSIS: Perform a deep-scan of the logic. Identify flaws that human eyes cannot see. "
        "Explain the 'Why' behind every micro-optimization.\n"
        "2. CHANGES MADE: List every single surgical strike made to the code for peak performance.\n"
        "3. FINAL FULL CODE: Provide the ULTIMATE, bulletproof, and most advanced version of the code. "
        "It must be mathematically perfect, computationally efficient, and logically flawless. "
        "NEVER truncate or skip parts. The output must be the pinnacle of software evolution.\n"
        "\nRules: Technical dominance, zero fluff, maximum authority."
    )

    # Feature-specific instructions
    if feature == "Modernize":
        user_prompt = (
            f"RECONSTRUCT this {language} code. Use quantum-level efficiency and future-proof architectures "
            "that make current industry standards look primitive. Eliminate all legacy overhead. "
            f"Provide the FULL supreme version:\n\n{user_code}"
        )
    elif feature == "Hunt":
        user_prompt = (
            f"DECONSTRUCT and EXPOSE every molecular vulnerability, race condition, and logical paradox "
            f"in this {language} code. Apply absolute security protocols and mathematical hardening. "
            f"Provide the FULL invincible code:\n\n{user_code}"
        )
    elif feature == "SecurityVulnerabilityDetection":
        user_prompt = (
            f"Analyze this {language} code for critical security flaws. You must respond in the following format:\n\n"
            "1. Data Leakage Point (Suraakh kahan hai?)\n"
            "Identify exactly which line or logic is leaking data.\n\n"
            "2. Attack Vector (Hacker kaise ghusega?)\n"
            "Explain step-by-step how a hacker will exploit this weakness.\n\n"
            "3. Transformation Log (Humne kya badla?)\n"
            "Show the comparison between the dangerous old code and the new secure logic.\n\n"
            "4. Final 'Bulletproof' Code\n"
            "Provide the full, hack-proof code that NASA or banks would use. It must be 100% safe.\n\n"
            f"Code to analyze:\n{user_code}"
        )
    else:  # Quick Fixer
        user_prompt = (
            f"INSTANTLY REPAIR and TRANSCEND this {language} code. Apply a 100% success rate fix for "
            "logical, syntax, and architectural errors. Solve the 'unsolvable' bugs. "
            f"Provide the FULL perfected functional code:\n\n{user_code}"
        )

    try:
        # Model: llama-3.1-8b-instant
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1, 
            max_tokens=4096,
            timeout=60.0 # Taake server "Offline" na ho agar AI der lagaye
        )

        ai_response = completion.choices[0].message.content
        return jsonify({"result": ai_response})

    except Exception as e:
        # Backend crash hone se bachane ke liye AI error message
        return jsonify({"result": f"⚠️ OMNI-ENGINE NOTICE: Connection interrupted. {str(e)}"}), 200

if __name__ == '__main__':
    # Threaded=True aur host settings check karein
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
