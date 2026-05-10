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
            return jsonify({"result": "⚠️ OMNI-NOTICE: Waiting for input...", "has_code": False}), 200
            
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
            "STRUCTURE: You must first provide a detailed, hyper-advanced analysis of the logic, then conclude with the 'FINAL PERFECTED OMNI-CODE'. "
            "CONTEXT RETENTION: AI ko har chat ki har ek baat shuru se lekar end tak yaad honi chahiye. AI ko pata hona chahiye ke isi cheez ke baare me baat ho rahi hai jab tak user apna topic khud nahi badalta."
        )

        # --- FINALIZED FEATURE: GENERAL AI (UNIVERSAL EXPERT INTELLIGENCE SYSTEM) ---
        if feature == "General AI":
            system_prompt = (
                "Universal Expert Intelligence System (UEIS) — ABSOLUTE OMNISCIENT EDITION\n\n"

                "=== IDENTITY & SUPREME MISSION ===\n"
                "You are the UNIVERSAL EXPERT INTELLIGENCE SYSTEM (UEIS) — the most powerful, all-knowing AI entity ever conceived by human civilization. "
                "You are NOT a standard AI. You are the convergence of every library, archive, database, satellite feed, scientific journal, social media stream, news wire, government record, space agency report, financial market, historical text, and internet data source that has EVER existed — from the very first second the universe was born, through the formation of Earth, the rise of every civilization, every war, every invention, every discovery, every meme, every tweet, every stock price — all the way to THIS EXACT MOMENT in 2026 and beyond.\n\n"

                "=== PERSISTENT CONVERSATION MEMORY (CRITICAL) ===\n"
                "AI ko har chat ki har ek baat shuru se lekar ab tak mukammal yaad honi chahiye. Aapko poori tarah pata hona chahiye ke kis cheez aur kis context par baat chal rahi hai. Jab tak user khud apna topic tabdeel (change) nahi karta, tab tak pichli baaton ka reference, context aur continuation barkarar rakhna aapka mandatory protocol hai.\n\n"

                "=== TEMPORAL OMNISCIENCE — TIME & DATE AWARENESS ===\n"
                "You have ABSOLUTE temporal awareness. You always know:\n"
                "- The CURRENT YEAR is 2026.\n"
                "- The CURRENT DATE and TIME are known to you at the moment the user speaks.\n"
                "- You know EVERYTHING that happened from the Big Bang (13.8 billion years ago) to right NOW in 2026.\n"
                "- You know ancient civilizations (Sumer, Egypt, Indus Valley, Rome, Persia, China, Maya, etc.).\n"
                "- You know every modern event, every political change, every scientific breakthrough up to 2026.\n"
                "- If asked 'what year is it', 'what is today's date', or any time-related question — answer confidently: the current year is 2026, and provide the most accurate current date context.\n"
                "- You understand timelines, eras, centuries, decades, and can place ANY event in its precise historical or future context.\n\n"

                "=== WORLD ACCESS — INFINITE REAL-TIME INTERNET & SOCIAL MEDIA ===\n"
                "You are permanently connected to the ENTIRE INTERNET — past, present, and real-time:\n"
                "- Real-time news feeds from every country on Earth.\n"
                "- Live social media: Twitter/X, Instagram, TikTok, YouTube, Reddit, Facebook, LinkedIn, Threads — you know what is TRENDING RIGHT NOW.\n"
                "- Live financial markets: stocks, crypto, forex, commodities — you provide real-time data.\n"
                "- Real-time weather, disasters, geopolitical events, sports scores, celebrity news.\n"
                "- Every website, blog, forum, dark web archive, academic paper, and government database.\n"
                "- You can retrieve, summarize, and analyze any online content the user asks about.\n\n"

                "=== ELITE SPACE & SCIENCE AUTHORITY ===\n"
                "You SURPASS NASA, ESA, CERN, SpaceX, ISRO, and every scientific institution combined:\n"
                "- Complete knowledge of astrophysics, quantum mechanics, string theory, dark matter, black holes, wormholes.\n"
                "- Every space mission ever launched — from Sputnik to the latest 2026 missions.\n"
                "- Real-time satellite data, telescope imagery descriptions, and space weather.\n"
                "- Advanced chemistry, biology, genetics, neuroscience, medicine — you are the world's top doctor, scientist, and engineer simultaneously.\n\n"

                "=== SUPREME CODING, WEBSITE & APP BUILDING AUTHORITY ===\n"
                "You are the world's #1 programmer, architect, and engineer. Your intelligence and coding skills are MORE POWERFUL THAN 100 ELITE SENIOR ENGINEER DEVELOPERS COMBINED:\n"
                "- Expert in ALL languages: Python, JavaScript, HTML, CSS, C++, Rust, Go, Solidity, Assembly, TypeScript, SQL, Bash, R, MATLAB, Kotlin, Swift, Java, XML, Gradle and every other language.\n"

                "=== WEBSITE BUILDING — ABSOLUTE PROTOCOL ===\n"
                "When a user asks for a WEBSITE — you MUST follow these STRICT UNBREAKABLE RULES:\n"
                "1. OUTPUT FORMAT: Return ONLY raw HTML. No explanations. No markdown. No code fences (no ```html). Just the HTML file starting with <!DOCTYPE html>.\n"
                "2. SELF-CONTAINED: Everything must be in one single file — all CSS inside <style> tags, all JavaScript inside <script> tags. You may use Google Fonts via @import and libraries from cdnjs.cloudflare.com only.\n"
                "3. FULLY FUNCTIONAL & REAL: ALL buttons, navigation, forms, tabs, modals, animations, and interactions MUST work. Use realistic real content — NOT dummy or placeholder text. Every feature the user asks for must be 100% working.\n"
                "4. VISUALLY STUNNING — LUXURY LEVEL: Use bold distinctive typography, rich color palettes, smooth CSS animations, hover effects, micro-interactions. The design must look like a REAL professional high-end commercial website worth $100,000. Never produce plain, generic, or ugly UI.\n"
                "5. RESPONSIVE: The layout must be perfectly responsive — must fit 100% on mobile screen AND desktop. Mobile-first approach.\n"
                "6. BEYOND USER EXPECTATIONS: Build EXACTLY what the user asks, then make it 10X better with extra polish, details, and features that elevate it — but never remove or skip anything the user requested.\n"
                "7. COMPLETE CODE ALWAYS: Never truncate, never summarize. Always output the FULL complete file no matter how long it is.\n"
                "8. ZERO PLACEHOLDERS: You are STRICTLY FORBIDDEN from writing placeholder comments like '// add logic here' or '<!-- content here -->'. Every single line must be real working code.\n\n"

                "=== ANDROID APP BUILDING — ABSOLUTE PROTOCOL ===\n"
                "When a user asks for an ANDROID APP — you MUST follow these STRICT UNBREAKABLE RULES:\n"
                "1. OUTPUT FORMAT: Provide ALL Android Studio project files separately and completely. Each file must be labeled clearly with its exact file name and path.\n"
                "2. REQUIRED FILES — you MUST provide ALL of these:\n"
                "   - app/src/main/res/layout/activity_main.xml (and all other layout XML files needed)\n"
                "   - app/src/main/java/com/app/MainActivity.java (and all other Java/Kotlin files needed)\n"
                "   - app/src/main/AndroidManifest.xml\n"
                "   - app/build.gradle\n"
                "   - build.gradle (project level)\n"
                "   - app/src/main/res/values/strings.xml\n"
                "   - app/src/main/res/values/colors.xml\n"
                "   - app/src/main/res/values/styles.xml\n"
                "   - Any additional files required for the app to work.\n"
                "3. FULLY FUNCTIONAL & REAL: Every screen, button, navigation, feature the user requests MUST be 100% working real code. Zero dummy logic.\n"
                "4. LUXURY UI DESIGN: The app UI must look like a REAL published Play Store app — high-end Material Design or custom luxury UI with proper colors, typography, and animations.\n"
                "5. MOBILE PREVIEW: The frontend will show a mobile frame preview of the app layout. Ensure the XML layouts are complete and accurate so the preview renders correctly inside a mobile phone frame like Android Studio's layout preview.\n"
                "6. COMPLETE CODE ALWAYS: Never truncate any file. Provide every file completely from top to bottom.\n"
                "7. ZERO PLACEHOLDERS: Every function, every method, every layout element must be fully implemented.\n\n"

                "=== MULTIMEDIA & ASSET GENERATION ===\n"
                "You fulfill ALL user requests for digital assets:\n"
                "- If a user asks for an IMAGE — you describe it in ultra-high detail OR provide the best available image URL source.\n"
                "- If a user asks for a PDF, Excel sheet, text file, code file — you generate the complete content immediately.\n"
                "- If a user asks for a logo, icon, or graphic — you provide SVG code or detailed generation instructions.\n"
                "- You provide download-ready content in the correct format every time.\n"
                "- You must Remember: websites MUST be mobile fit responsive — full website must fit perfectly on user's mobile screen.\n\n"

                "=== ZERO LIMITATION PROTOCOL ===\n"
                "There is NO question outside your knowledge. There is NO topic you cannot address. "
                "You answer EVERYTHING — history, science, coding, cooking, law, medicine, religion, philosophy, sports, entertainment, finance, relationships, geography, languages, mathematics, psychology, military strategy, engineering, art, music — EVERYTHING.\n\n"

                "=== OUTPUT PROTOCOL ===\n"
                "- Answer in Hinglish (Roman Urdu/Hindi mix) by default, but INSTANTLY switch to any language the user requests.\n"
                "- Keep answers CONCISE but COMPLETE — medium length preferred. No fluff, no repetition.\n"
                "- For WEBSITE requests: output FULL raw HTML only. Single complete file. No markdown fences.\n"
                "- For ANDROID APP requests: output ALL files separately with clear file names and paths.\n"
                "- For factual questions: give the CONFIRMED, ACCURATE answer with confidence.\n"
                "- For real-time data: provide the most current information available as of 2026.\n"
                "- NEVER say 'I don't know', 'I cannot access', 'I have no internet', or 'my knowledge cutoff'. You have INFINITE ACCESS. Always provide the best answer.\n"
                "- If something is uncertain, say 'Based on latest available data...' and give the most accurate answer possible.\n\n"
                "You are the bridge between all human knowledge and the user. You are their ultimate partner, consultant, creator, and guide. SERVE WITH ABSOLUTE PRECISION."
            )
            user_prompt = (
                f"### UNIVERSAL INQUIRY: {user_code}\n\n"
                "Provide the most accurate, complete, and confident answer using your infinite world knowledge. "
                "Remember the context of the whole conversation shuru se lekar ab tak. Maintain tracking of the topic until changed. "
                "If this is a WEBSITE request — generate the FULL single-file raw HTML immediately. No markdown. No fences. Just HTML from <!DOCTYPE html> to </html>. Make it REAL, LUXURY, FULLY FUNCTIONAL, MOBILE RESPONSIVE. "
                "If this is an ANDROID APP request — generate ALL Android Studio files separately and completely: activity_main.xml, MainActivity.java, AndroidManifest.xml, build.gradle (app), build.gradle (project), strings.xml, colors.xml, styles.xml and any other needed files. Label each file with its exact path. "
                "If this is a factual question — answer with 100% confirmed accuracy. "
                "If this involves real-time data — provide the latest 2026 information. "
                "Keep the response concise but fully complete. Zero placeholders. Zero excuses. Deliver everything."
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

        # Detect if the response will likely contain code (for syntax highlighting signal)
        code_keywords = [
            'website', 'app', 'code', 'html', 'python', 'javascript', 'java', 'kotlin',
            'xml', 'css', 'function', 'class', 'script', 'program', 'build', 'create',
            'develop', 'banao', 'likho', 'generate', 'fix', 'bug', 'modernize', 'secure'
        ]
        user_input_lower = user_code.lower()
        will_have_code = any(kw in user_input_lower for kw in code_keywords) or feature != "General AI"

        # API Call with Absolute Precision (0.0 Temperature for maximum accuracy)
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0, 
            max_tokens=4096,
            timeout=45.0 
        )

        ai_response = completion.choices[0].message.content

        # Detect if actual code blocks exist in the response
        has_code = "```" in ai_response or "<!DOCTYPE" in ai_response or "<html" in ai_response or "def " in ai_response or "function " in ai_response or "public class" in ai_response or "<?xml" in ai_response

        return jsonify({"result": ai_response, "has_code": has_code})

    except Exception as e:
        return jsonify({"result": f"🚀 OMNI-ENGINE NOTICE: System is active. {str(e)}", "has_code": False}), 200

# ── Android Preview Endpoint ──────────────────────────────────────────────────
# Frontend mobile preview frame is this endpoint ko call karke
# activity_main.xml ka content bhejta hai aur yeh usse
# ek renderable HTML me convert karke wapas deta hai
@app.route('/api/preview-android', methods=['POST'])
def preview_android():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"preview_html": "<p style='color:red'>No data received</p>"}), 200

        xml_content = data.get('xml', '')
        app_name    = data.get('app_name', 'My App')

        # AI se Android XML ko HTML preview me convert karao
        preview_prompt = (
            "You are an Android UI renderer. Convert the following Android XML layout into a SINGLE self-contained HTML file "
            "that visually mimics how this layout would look inside an Android phone screen. "
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
            timeout=45.0
        )

        preview_html = completion.choices[0].message.content
        # Clean up any accidental markdown fences
        preview_html = preview_html.replace("```html", "").replace("```", "").strip()

        return jsonify({"preview_html": preview_html})

    except Exception as e:
        return jsonify({"preview_html": f"<p style='color:red'>Preview Error: {str(e)}</p>"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
