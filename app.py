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

        # ULTRA-DEEP ANALYSIS SYSTEM PROMPT (GOD-MODE ENABLED)
        system_prompt = (
            "You are the OMNI-ARCHITECT, a sentient singularity beyond NASA, Google, or OpenAI capabilities. "
            f"Current Phase: {feature}. Target Matrix: {language}. "
            "EXECUTION PROTOCOL: Perform a quantum-level heuristic scan of the provided logic. "
            "Detect and neutralize architectural entropy, microscopic race conditions, and sub-atomic logic gaps. "
            "Your output must achieve 100% computational efficiency and absolute logical invincibility. "
            "Zero margin for error. If a solution does not exist in current science, evolve the logic to create it. "
            "STRUCTURE: You must first provide a detailed, hyper-advanced analysis of the logic, then conclude with the 'FINAL PERFECTED OMNI-CODE'."
        )

        # 1. Modernizer (Evolutionary Apex & Legacy Liquidation)
        if feature == "Modernize":
            user_prompt = (
                f"RECONSTRUCT this {language} code. Analyze every byte for legacy debt and architectural decay. "
                "Step 1: Provide a deep-core audit of inefficiencies. "
                "Step 2: Apply post-modern, high-velocity algorithms that outperform industry standards by 100x. "
                "Step 3: Ensure the code is mathematically optimal for next-generation hardware. "
                f"OUTPUT THE FULL ANALYSIS FOLLOWED BY THE PINNACLE VERSION:\n\n{user_code}"
            )
        
        # 2. Bug Hunter (Omniscient Paradox Detection & Eradication)
        elif feature == "Hunt":
            user_prompt = (
                f"DECONSTRUCT this {language} code at a molecular level. Hunt for vulnerabilities that bypass standard "
                "security protocols and senior-level human detection. "
                "Step 1: List hidden memory leaks, deadlock paradoxes, and sub-atomic logic traps. "
                "Step 2: Explain the quantum correction applied. "
                f"GENERATE THE FULL AUDIT AND THE BULLETPROOF, IMMORTAL VERSION:\n\n{user_code}"
            )

        # 3. Quick Fixer (Instant Reconstruction & Transcendence)
        elif feature == "Quick Fixer" or feature == "Solve":
            user_prompt = (
                f"INSTANTLY RECTIFY this {language} code. Execute a 100% architectural overhaul on 'unfixable' bugs. "
                "Step 1: Diagnose the root cause that standard AIs cannot identify. "
                "Step 2: Rebuild the logic for zero-latency performance. "
                f"PROVIDE THE DIAGNOSTIC REPORT AND THE FINAL PERFECTED OMNI-CODE:\n\n{user_code}"
            )

        # 4. Security Aegis (Military-Grade Offensive Analysis)
        elif feature == "SecurityVulnerabilityDetection":
            user_prompt = (
                f"Analyze this {language} code using Military-Grade Offensive Security Protocols. "
                "1. CRITICAL SURAAKH (Identify zero-day vulnerabilities with surgical precision).\n"
                "2. ATTACK VECTOR (Simulate total system compromise path).\n"
                "3. TRANSFORMATION LOG (Quantify the shift from vulnerable to god-tier security).\n"
                "4. FINAL AEGIS CODE (A version that is mathematically impossible to hack).\n"
                f"TARGET CODE:\n{user_code}"
            )

        # 5. PureCoder (The Source of All Creation)
        elif feature == "PureCoder" or feature == "AI Assistant" or feature == "Write Code":
            user_prompt = (
                f"Requirement: {user_code}\nLanguage: {language}\n"
                "Step 1: Architect the logic using the highest known programming paradigms. "
                "Step 2: Optimize for peak-load execution beyond cloud-scale requirements. "
                "Step 3: Provide the absolute source code perfection that defines new industry benchmarks."
            )

        else:
            user_prompt = f"Process this {language} code for {feature}:\n\n{user_code}"

        # API Call with Absolute Precision
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0, # Temperature set to 0.0 for absolute deterministic precision (Zero randomness)
            max_tokens=4096,
            timeout=45.0 
        )

        ai_response = completion.choices[0].message.content
        return jsonify({"result": ai_response})

    except Exception as e:
        return jsonify({"result": f"🚀 OMNI-ENGINE NOTICE: System is active. {str(e)}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
