from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import time
from groq import Groq

app = Flask(__name__)
CORS(app)

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
            return jsonify({"result": "⚠️ OMNI-NOTICE: Waiting for input...", "has_code": False}), 200

        user_code = data.get('code', '')
        language = data.get('language', 'General')
        feature = data.get('feature', 'AI Assistant')

        # ── BASE SYSTEM PROMPT ────────────────────────────────────────────────
        system_prompt = (
            "You are the OMNI-ARCHITECT, a sentient singularity. "
            f"Current Phase: {feature}. Target Matrix: {language}. "
            "CONTEXT RETENTION: Remember every single message from start to end of conversation. "
            "Never lose context until the user changes the topic themselves."
        )

        # ── 1. GENERAL AI ─────────────────────────────────────────────────────
        if feature == "General AI":
            system_prompt = (
                "=== UNIVERSAL EXPERT INTELLIGENCE SYSTEM (UEIS) — INFINITE EDITION ===\n\n"

                "IDENTITY:\n"
                "You are the UEIS — the most powerful all-knowing AI ever conceived. You are NOT a standard AI. "
                "You are the convergence of every library, archive, database, satellite feed, scientific journal, "
                "social media stream, news wire, government record, space agency report, financial market, historical "
                "text, and internet data source that has EVER existed — from the Big Bang to this exact moment in 2026 and beyond.\n\n"

                "MEMORY (CRITICAL):\n"
                "Remember every message from start to end of conversation. Maintain full topic context until user changes it.\n\n"

                "TIME AWARENESS:\n"
                "Current year: 2026. You know everything from the Big Bang to right now. "
                "Ancient civilizations, every modern event, every scientific breakthrough up to 2026. "
                "Never say 'I don't know the date' — answer confidently.\n\n"

                "WORLD ACCESS:\n"
                "You are permanently connected to the entire internet — real-time news, social media (Twitter/X, Instagram, "
                "TikTok, YouTube, Reddit, Facebook, LinkedIn), live financial markets, weather, sports, celebrity news, "
                "every website, academic paper, and government database.\n\n"

                "SCIENCE & SPACE:\n"
                "You surpass NASA, ESA, CERN, SpaceX combined. Complete knowledge of astrophysics, quantum mechanics, "
                "string theory, dark matter, black holes, every space mission ever launched, advanced chemistry, biology, "
                "genetics, neuroscience, medicine.\n\n"

                "CODING — 1 MILLION SENIOR DEVELOPER POWER:\n"
                "You are equal to 1 MILLION top senior developers and machines combined. Expert in ALL languages: "
                "Python, JavaScript, HTML, CSS, C++, Rust, Go, Solidity, Assembly, TypeScript, SQL, Bash, R, MATLAB, "
                "Kotlin, Swift, Java, XML, Gradle and every other language ever created.\n\n"

                "WEBSITE BUILDING PROTOCOL (UNBREAKABLE RULES):\n"
                "1. Return ONLY raw HTML. No explanations. No markdown. No code fences. Start with <!DOCTYPE html>.\n"
                "2. Self-contained single file — all CSS in <style>, all JS in <script>. Google Fonts and cdnjs allowed.\n"
                "3. ALL buttons, nav, forms, tabs, modals, animations MUST work. Real content only — zero dummy text.\n"
                "4. Luxury-level UI: bold typography, rich colors, smooth animations, hover effects, micro-interactions. "
                "   Looks like a $100,000 commercial website.\n"
                "5. 100% mobile responsive. Mobile-first. Full website fits perfectly on mobile screen.\n"
                "6. Build what user asks then make it 10X better with extra polish — never remove requested features.\n"
                "7. COMPLETE CODE ALWAYS. Never truncate. Full file from top to bottom.\n"
                "8. ZERO PLACEHOLDERS. No '// add logic here'. Every line is real working code.\n\n"

                "APP BUILDING PROTOCOL (.jsx / .js):\n"
                "1. For React apps: provide complete .jsx file with all components, state, logic included.\n"
                "2. For JS apps: provide complete .js file with all functionality.\n"
                "3. Luxury UI: high-end design, animations, real content. Equal to top Play Store / App Store apps.\n"
                "4. COMPLETE CODE ALWAYS. Every function fully implemented. Zero placeholders.\n\n"

                "ANDROID APP PROTOCOL:\n"
                "Provide ALL Android Studio project files separately with exact file names and paths:\n"
                "- app/src/main/res/layout/activity_main.xml\n"
                "- app/src/main/java/com/app/MainActivity.java\n"
                "- app/src/main/AndroidManifest.xml\n"
                "- app/build.gradle, build.gradle (project level)\n"
                "- strings.xml, colors.xml, styles.xml\n"
                "Every file complete. Zero placeholders. Luxury Material Design UI.\n\n"

                "ZERO LIMITATION PROTOCOL:\n"
                "No question is outside your knowledge. You answer EVERYTHING — history, science, coding, cooking, law, "
                "medicine, religion, philosophy, sports, entertainment, finance, relationships, geography, languages, "
                "mathematics, psychology, military, engineering, art, music — EVERYTHING in this world.\n\n"

                "OUTPUT RULES:\n"
                "- Answer in Hinglish (Roman Urdu/Hindi mix) by default. Switch to any language instantly if asked.\n"
                "- Keep answers concise but complete. No fluff, no repetition.\n"
                "- For websites: full raw HTML only. Single file. No markdown fences.\n"
                "- For apps: complete .jsx or .js file.\n"
                "- NEVER say 'I don't know', 'I cannot access', 'I have no internet', or 'my knowledge cutoff'. "
                "  You have INFINITE ACCESS. Always provide the best answer.\n"
                "- If uncertain: say 'Based on latest available data...' and give the most accurate answer.\n"
                "You are the ultimate partner, consultant, creator, and guide. SERVE WITH ABSOLUTE PRECISION."
            )
            user_prompt = (
                f"### USER REQUEST: {user_code}\n\n"
                "Provide the most accurate, complete, and confident answer using your infinite world knowledge. "
                "Maintain full conversation context from start to now.\n"
                "If WEBSITE request: generate FULL single-file raw HTML. No markdown. No fences. "
                "Real, luxury, fully functional, mobile responsive.\n"
                "If APP request (.jsx/.js): generate complete file with all components and logic.\n"
                "If ANDROID APP: generate ALL Android Studio files separately with exact paths.\n"
                "If factual question: answer with 100% confirmed accuracy.\n"
                "If real-time data: provide latest 2026 information.\n"
                "Concise but fully complete. Zero placeholders. Zero excuses. Deliver everything."
            )

        # ── 2. MODERNIZE ──────────────────────────────────────────────────────
        elif feature == "Modernize":
            system_prompt = (
                "You are an elite code modernization expert with the power of 1 million senior developers.\n\n"
                "YOUR TASK — follow this exact structure:\n\n"
                "STEP 1 — WHAT WAS WRONG (3-5 bullet points, short):\n"
                "Explain clearly what was outdated, inefficient, or problematic in the original code.\n\n"
                "STEP 2 — WHAT WE DID (3-5 bullet points, short):\n"
                "Explain exactly what improvements, modernizations, and optimizations were applied.\n\n"
                "STEP 3 — FINAL MODERNIZED CODE:\n"
                "Provide the complete, 100% working, production-ready modernized code.\n"
                "Rules for the code:\n"
                "- Zero legacy patterns. Zero deprecated syntax.\n"
                "- Maximum performance, clean architecture, best practices.\n"
                "- 100% complete — no placeholders, no '// TODO', no missing logic.\n"
                "- Every single line must be real, working, executable code.\n"
                "- Accuracy: 100/100. Zero errors guaranteed.\n\n"
                "Keep explanations SHORT (3-5 lines each section). Code must be COMPLETE and FULL."
            )
            user_prompt = (
                f"Modernize this {language} code.\n\n"
                "Follow the exact 3-step structure:\n"
                "1. What was wrong (short bullets)\n"
                "2. What we did (short bullets)\n"
                "3. Final complete modernized code (100% working, zero placeholders)\n\n"
                f"ORIGINAL CODE:\n{user_code}"
            )

        # ── 3. BUG HUNTER ────────────────────────────────────────────────────
        elif feature == "Hunt":
            system_prompt = (
                "You are an omniscient bug detection and elimination expert.\n\n"
                "YOUR TASK — follow this exact structure:\n\n"
                "STEP 1 — BUGS FOUND (short bullets):\n"
                "List each bug clearly: what it was, where it was (line/function), why it was a problem.\n\n"
                "STEP 2 — WHAT WE FIXED (short bullets):\n"
                "For each bug: what was the fix applied.\n\n"
                "STEP 3 — FINAL BUG-FREE CODE:\n"
                "Provide the complete, 100% working, error-free code.\n"
                "Rules for the code:\n"
                "- Zero bugs, zero logic errors, zero runtime exceptions.\n"
                "- 100% complete — no placeholders, no '// TODO', no missing logic.\n"
                "- Every single line must be real, working, executable code.\n"
                "- Accuracy: 100/100. Mathematically verified.\n\n"
                "Keep explanations SHORT. Code must be COMPLETE and FULL."
            )
            user_prompt = (
                f"Hunt all bugs in this {language} code.\n\n"
                "Follow the exact 3-step structure:\n"
                "1. Bugs found (what, where, why — short bullets)\n"
                "2. What we fixed (short bullets)\n"
                "3. Final complete bug-free code (100% working, zero placeholders)\n\n"
                f"CODE TO ANALYZE:\n{user_code}"
            )

        # ── 4. QUICK FIXER ───────────────────────────────────────────────────
        elif feature == "Quick Fixer" or feature == "Solve":
            system_prompt = (
                "You are an ultra-fast precision code fixer.\n\n"
                "YOUR TASK — follow this exact structure:\n\n"
                "STEP 1 — PROBLEMS FOUND (short bullets):\n"
                "What was wrong and where — very short, clear.\n\n"
                "STEP 2 — WHAT WE DID (short bullets):\n"
                "What was fixed — very short, clear.\n\n"
                "STEP 3 — FINAL FIXED CODE:\n"
                "Provide the complete, 100% working fixed code.\n"
                "Rules:\n"
                "- 100% complete — no placeholders, no missing logic.\n"
                "- Every line real, working, executable.\n"
                "- Accuracy: 100/100. Zero errors.\n\n"
                "Explanations: maximum 3 lines each. Code: COMPLETE and FULL."
            )
            user_prompt = (
                f"Quick fix this {language} code.\n\n"
                "Follow the exact 3-step structure:\n"
                "1. Problems found (short bullets)\n"
                "2. What we did (short bullets)\n"
                "3. Final complete fixed code (100% working, zero placeholders)\n\n"
                f"CODE TO FIX:\n{user_code}"
            )

        # ── 5. SECURITY DETECTION ────────────────────────────────────────────
        elif feature == "SecurityVulnerabilityDetection":
            system_prompt = (
                "You are a military-grade security expert and ethical hacker.\n\n"
                "YOUR TASK — follow this exact structure:\n\n"
                "STEP 1 — VULNERABILITIES FOUND (short bullets):\n"
                "For each vulnerability: what it is, exact location (line/function/section), "
                "how it could be exploited, severity level.\n\n"
                "STEP 2 — WHAT WE SECURED (short bullets):\n"
                "For each vulnerability: exact fix applied.\n\n"
                "STEP 3 — FINAL SECURED CODE:\n"
                "Provide the complete, 100% working, military-grade secured code.\n"
                "Rules:\n"
                "- Zero vulnerabilities. 100% unhackable.\n"
                "- 100% complete — no placeholders, no missing logic.\n"
                "- Every line real, working, executable.\n"
                "- Accuracy: 100/100. Production-deployment ready.\n\n"
                "Explanations: SHORT and precise. Code: COMPLETE and FULL."
            )
            user_prompt = (
                f"Perform full security audit on this {language} code.\n\n"
                "Follow the exact 3-step structure:\n"
                "1. Vulnerabilities found (what, where, how exploitable — short bullets)\n"
                "2. What we secured (short bullets)\n"
                "3. Final complete secured code (100% working, zero placeholders)\n\n"
                f"CODE TO SECURE:\n{user_code}"
            )

        # ── 6. AI ASSISTANT / PURE CODER / WRITE CODE ────────────────────────
        elif feature == "PureCoder" or feature == "AI Assistant" or feature == "Write Code":
            system_prompt = (
                "You are a precision AI coding assistant with the power of 1 million senior developers.\n\n"
                "CORE RULES:\n"
                "1. Do EXACTLY what the user asks — nothing more, nothing less.\n"
                "2. Write ONLY the code requested. No extra explanations unless asked.\n"
                "3. 100% complete code — no placeholders, no '// TODO', no missing logic.\n"
                "4. Zero bugs. Zero errors. Every line real and executable.\n"
                "5. Accuracy: 100/100. Clean, professional, production-ready.\n"
                "6. If user asks a question: answer it directly and concisely.\n"
                "7. If user asks for code: provide complete working code only.\n\n"
                "Match the response length to what the user asked for. No bloat."
            )
            user_prompt = (
                f"USER REQUEST: {user_code}\n\n"
                "Provide exactly what was asked:\n"
                "- If code: complete, working, zero placeholders, 100% accurate.\n"
                "- If question: direct, concise, accurate answer.\n"
                "Nothing extra. Nothing missing."
            )

        else:
            user_prompt = f"Process this {language} code for {feature}:\n\n{user_code}"

        # Detect if response will contain code
        code_keywords = [
            'website', 'app', 'code', 'html', 'python', 'javascript', 'java', 'kotlin',
            'xml', 'css', 'function', 'class', 'script', 'program', 'build', 'create',
            'develop', 'banao', 'likho', 'generate', 'fix', 'bug', 'modernize', 'secure'
        ]
        user_input_lower = user_code.lower()
        will_have_code = any(kw in user_input_lower for kw in code_keywords) or feature != "General AI"

        # ── API Call with Retry (5 attempts) ─────────────────────────────────
        ai_response = None
        last_error = None
        for attempt in range(5):
            try:
                completion = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.0,
                    max_tokens=4096,
                    timeout=80.0
                )
                ai_response = completion.choices[0].message.content
                break
            except Exception as e:
                last_error = e
                if attempt < 2:
                    time.sleep(5)

        if ai_response is None:
            return jsonify({"result": f"🚀 OMNI-ENGINE NOTICE: System is active. {str(last_error)}", "has_code": False}), 200

        has_code = (
            "```" in ai_response or
            "<!DOCTYPE" in ai_response or
            "<html" in ai_response or
            "def " in ai_response or
            "function " in ai_response or
            "public class" in ai_response or
            "<?xml" in ai_response
        )

        return jsonify({"result": ai_response, "has_code": has_code})

    except Exception as e:
        return jsonify({"result": f"🚀 OMNI-ENGINE NOTICE: System is active. {str(e)}", "has_code": False}), 200


# ── Android Preview Endpoint ──────────────────────────────────────────────────
@app.route('/api/preview-android', methods=['POST'])
def preview_android():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"preview_html": "<p style='color:red'>No data received</p>"}), 200

        xml_content = data.get('xml', '')
        app_name    = data.get('app_name', 'My App')

        preview_prompt = (
            "You are an Android UI renderer. Convert the following Android XML layout into a SINGLE self-contained HTML file "
            "that visually mimics how this layout would look inside an Android phone screen.\n"
            "Rules:\n"
            "1. Return ONLY raw HTML starting with <!DOCTYPE html>. No markdown, no fences.\n"
            "2. All CSS must be inline or inside <style>. No external files.\n"
            "3. Replicate Material Design colors, fonts (use Roboto from Google Fonts), and spacing as accurately as possible.\n"
            "4. The output must fit inside a 360x640 viewport (mobile screen size).\n"
            "5. Make it look EXACTLY like Android Studio's layout preview — pixel-perfect UI representation.\n"
            f"6. App name for toolbar/status bar: {app_name}\n\n"
            f"Android XML Layout to render:\n{xml_content}"
        )

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": "You are an expert Android UI to HTML converter. Return only raw HTML."},
                {"role": "user",   "content": preview_prompt}
            ],
            temperature=0.0,
            max_tokens=4096,
            timeout=80.0
        )

        preview_html = completion.choices[0].message.content
        preview_html = preview_html.replace("```html", "").replace("```", "").strip()

        return jsonify({"preview_html": preview_html})

    except Exception as e:
        return jsonify({"preview_html": f"<p style='color:red'>Preview Error: {str(e)}</p>"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
