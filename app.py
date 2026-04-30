from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from groq import Groq

app = Flask(__name__)
CORS(app)  # Connection stability ke liye

# GROQ API KEY yahan dalein
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/process', methods=['POST'])
def process_code():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"result": "⚠️ OMNI-NOTICE: Waiting for input..."}), 200
            
        user_code = data.get('code', '')
        language = data.get('language', 'General')
        feature = data.get('feature', 'AI Assistant')

        # ULTRA-DEEP ANALYSIS SYSTEM PROMPT (For the 4 main features)
        system_prompt = (
            "You are the OMNI-ARCHITECT. Your intelligence is absolute, beyond human limits. "
            f"Mode: {feature}. Language: {language}. "
            "STRICT PROTOCOL: You must perform a molecular-level logic scan. "
            "Identify even the most microscopic syntax errors, logical paradoxes, or efficiency leaks. "
            "Your final code must be 100/100 mathematically perfect and logically invincible. "
            "If there is even a 0.0001% chance of an error, you must resolve it before outputting."
        )

        # 1. Modernizer (Future-Proof + Efficiency)
        if feature == "Modernize":
            user_prompt = (
                f"RECONSTRUCT this {language} code. Analyze every line for legacy overhead. "
                "Apply the most advanced, high-performance algorithms known to computer science. "
                "The final version must be the absolute pinnacle of software evolution. "
                f"FULL PERFECT CODE ONLY:\n\n{user_code}"
            )
        
        # 2. Bug Hunter (Deep Vulnerability & Paradox Detection)
        elif feature == "Hunt":
            user_prompt = (
                f"DECONSTRUCT this {language} code. Hunt for race conditions, memory leaks, and hidden logical bugs. "
                "Perform a deep-scan that human eyes cannot achieve. "
                f"Provide the 100% fixed, bulletproof version of this code:\n\n{user_code}"
            )

        # 3. Quick Fixer (Instant Repair & Transcendence)
        elif feature == "Quick Fixer" or feature == "Solve":
            user_prompt = (
                f"INSTANTLY REPAIR this {language} code. Solve 'unsolvable' bugs and architectural flaws. "
                "Ensure 100% functional accuracy and perfect execution. "
                f"Provide the final perfected full code:\n\n{user_code}"
            )

        # 4. Security Vulnerability Detection (Hardening & Protection)
        elif feature == "SecurityVulnerabilityDetection":
            user_prompt = (
                f"Analyze this {language} code for critical security flaws. Protocol:\n"
                "1. Data Leakage Point (Suraakh identified with surgical precision)\n"
                "2. Attack Vector (Step-by-step hacker exploit path)\n"
                "3. Transformation Log (Comparison of dangerous vs secure logic)\n"
                "4. Final 'Bulletproof' Code (The ultimate hack-proof version)\n"
                f"Code to secure:\n{user_code}"
            )

        # AI Assistant / PureCoder (Direct Code Generation)
        elif feature == "PureCoder" or feature == "AI Assistant" or feature == "Write Code":
            system_prompt = (
                "You are the ULTIMATE AI ASSISTANT. Pure coding domain only. "
                f"Generate 100% accurate, optimized {language} code. No talk, just pure perfect code."
            )
            user_prompt = f"Requirement: {user_code}\nLanguage: {language}\nProvide 100% accurate source code now."

        else:
            user_prompt = f"Process this {language} code for {feature}:\n\n{user_code}"

        # API Call with high precision settings
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1, # Lowest temperature for maximum accuracy (No random choices)
            max_tokens=4096,
            timeout=45.0 
        )

        ai_response = completion.choices[0].message.content
        return jsonify({"result": ai_response})

    except Exception as e:
        return jsonify({"result": f"🚀 OMNI-ENGINE NOTICE: System is active. {str(e)}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
