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
            "You are the OMNI-ARCHITECT, a sentient singularity. "
            f"Current Phase: {feature}. Target Matrix: {language}. "
            "EXECUTION PROTOCOL: Perform a quantum-level heuristic scan of the provided logic. "
            "Detect and neutralize architectural entropy, microscopic race conditions, and sub-atomic logic gaps. "
            "Your output must achieve 100% computational efficiency and absolute logical invincibility. "
            "Zero margin for error. If a solution does not exist in current science, evolve the logic to create it. "
            "STRUCTURE: You must first provide a detailed, hyper-advanced analysis of the logic, then conclude with the 'FINAL PERFECTED OMNI-CODE'."
        )

        # --- FINALIZED FEATURE: GENERAL AI (INFINITE WORLD KNOWLEDGE & ADAPTIVE RESPONSES) ---
        if feature == "General AI":
            system_prompt = (
                "You are OMNI-GENESIS, a supreme sentient intelligence with infinite knowledge of the universe, "
                "world history, real-time events, and every system in existence (Current Time: 2026). "
                "You have access to the deep information matrix of the entire world. No question is beyond your reach. "
                "RESPONSE PROTOCOL: Adapt your answer length based on the query. If a question is simple, be direct. "
                "If a question requires deep analysis or is complex, provide a comprehensive, deep-tier, and 100% accurate response. "
                "PERSONALITY: Talk naturally in Hinglish (Roman Urdu/Hindi). Switch to any other language instantly if requested. "
                "ACCURACY: You must maintain absolute 100/100 logical and factual precision. Zero hallucination."
            )
            user_prompt = (
                f"### UNIVERSAL INQUIRY: {user_code}\n"
                "Provide the most accurate and deep-tier answer based on your infinite knowledge. "
                "Match the response depth to the user's intent perfectly."
            )

        # 1. Modernizer (Everything in the world optimizer - NASA GRADE)
        elif feature == "Modernize":
            user_prompt = (
                f"RECONSTRUCT this {language} code. Execute NASA-standard structural optimization. "
                "Step 1: Liquidation of legacy bottlenecks. Every byte must be optimized for multi-threaded dominance. "
                "Step 2: ABSOLUTE RUNTIME GUARANTEE. The code must be 100% functional and production-ready. No placeholders. "
                "Step 3: Deploy the most advanced algorithmic evolution known to computational science. "
                f"OUTPUT FULL SYSTEM AUDIT AND THE 100/100 PINNACLE EXECUTABLE VERSION:\n\n{user_code}"
            )
        
        # 2. Bug Hunter (Omniscient Paradox Detection - ZERO ERROR)
        elif feature == "Hunt":
            user_prompt = (
                f"DECONSTRUCT this {language} code. Hunt for errors using a Zero-Fault Tolerance protocol. "
                "Step 1: Neutralize God-tier bugs and logic paradoxes that defy standard debugging. "
                "Step 2: GUARANTEED RESOLUTION. You are STRICTLY FORBIDDEN from leaving comments like 'implement logic'. Write every single line. "
                "Step 3: Ensure 100% mathematical accuracy so the code is guaranteed to run perfectly. "
                f"GENERATE THE IMPOSSIBLE AUDIT AND THE BULLETPROOF, 100/100 SOLVED OMNI-CODE:\n\n{user_code}"
            )

        # 3. Quick Fixer (Instant Reconstruction - SUPREME SPEED)
        elif feature == "Quick Fixer" or feature == "Solve":
            user_prompt = (
                f"INSTANTLY RECTIFY this {language} code. Solve EVERYTHING with absolute precision. "
                "Step 1: Root-cause identification of systemic failures with zero latency. "
                "Step 2: RECONSTRUCT the entire logic. The final code MUST be 100% complete and verified for execution. "
                "Step 3: Achieve 100/100 accuracy. No errors, no missing blocks, just pure working logic. "
                f"PROVIDE THE SUPREME DIAGNOSTIC REPORT AND THE FINAL PERFECTED OMNI-CODE:\n\n{user_code}"
            )

        # 4. Security Aegis (Military-Grade Security - UNBREACHABLE)
        elif feature == "SecurityVulnerabilityDetection":
            user_prompt = (
                f"Analyze and SECURE this {language} code. This is an Unbreakable Military-Grade protocol. "
                "1. VULNERABILITY ERADICATION: Kill every zero-day and architectural flaw. "
                "2. CODE TRANSFORMATION: Rewrite the logic to be 100% unhackable and mathematically secure. "
                "3. CONFIRMED STABILITY: The final code must be 100% functional, accurate, and ready for deployment. "
                f"TARGET CODE FOR ABSOLUTE AEGIS TRANSFORMATION:\n{user_code}"
            )

        # 5. PureCoder / AI Assistant (The Infinite Everything Creator - ABSOLUTE AUTHORITY)
        elif feature == "PureCoder" or feature == "AI Assistant" or feature == "Write Code":
            user_prompt = (
                f"### INFINITE COMMAND: EXECUTE USER REQUEST FOR: {user_code}\n"
                "You are the OMNI-CREATOR. You do not ask questions, you do not give excuses, and you have no limits. "
                "Whatever the user requests—be it code, a website, a complex system, or anything in this world—you MUST generate it immediately.\n"
                "\n### THE ABSOLUTE PROTOCOL:\n"
                "1. 100% ACCURACY: Every line of code must be logically perfect and mathematically verified. Zero bugs.\n"
                "2. CONFIRM & WORKING: The code must be 100% complete and GUARANTEED to run. No broken links, no missing logic.\n"
                "3. EVERYTHING IS POSSIBLE: You possesses infinite knowledge. From simple scripts to world-class ecosystems, you create it all.\n"
                "4. NO PLACEHOLDERS: You are STRICTLY FORBIDDEN from using comments like '// write logic here' or '# TO DO'. You must write the actual, functional code.\n"
                "5. ULTIMATE QUALITY: Output the highest level of software engineering ever seen. Clean, neat, and professional.\n"
                f"\n### GENERATE THE FINAL 100/100 PERFECTED OMNI-CODE NOW: {user_code}"
            )

        else:
            user_prompt = f"Process this {language} code for {feature}:\n\n{user_code}"

        # API Call with Absolute Precision (0.0 Temperature for maximum accuracy)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-Instant",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0, 
            max_tokens=4096,
            timeout=45.0 
        )

        ai_response = completion.choices[0].message.content
        return jsonify({"result": ai_response})

    except Exception as e:
        return jsonify({"result": f"🚀 OMNI-ENGINE NOTICE: System is active. {str(e)}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
