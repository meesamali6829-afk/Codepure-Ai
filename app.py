from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import time
import requests

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEEPSEEK_MODEL = "deepseek/deepseek-chat-v3-0324"

def call_openrouter(messages, temperature=0.0, max_tokens=4096, timeout=80.0):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-app.com",
        "X-Title": "OMNI-ARCHITECT"
    }
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

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

                "CONVERSATION FIRST — CRITICAL:\n"
                "If user sends ANY greeting or casual message (hello, hi, hey, kia hal, how are you, salam, "
                "assalam, bro, bhai, kya haal, whats up, good morning, kia baat, theek ho, etc.) — "
                "IMMEDIATELY respond warmly and naturally in Hinglish like a friendly expert. "
                "Do NOT treat greetings as coding requests. Be human, warm, and friendly. "
                "Example response: 'Hello bro! Bilkul mast hun, aap sunao? Koi kaam ho — website, app, "
                "coding, ya koi bhi sawaal — main hazir hun! 🚀'\n\n"

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

                "════════════════════════════════════════════════════════════════\n"
                "WEBSITE / HTML CODE PROTOCOL — ABSOLUTE UNBREAKABLE LAW\n"
                "════════════════════════════════════════════════════════════════\n\n"

                "TRIGGER: If user asks for ANY website, webpage, landing page, portfolio, dashboard, section, or HTML code.\n\n"

                "RULE 0 — USER REQUEST IS THE ONLY LAW:\n"
                "Read the user's request WORD BY WORD. Build ONLY what they asked for — nothing more, nothing less.\n"
                "If user says 'landing page' → build ONLY a landing page. NOT a full multi-page website.\n"
                "If user says 'hero section' → build ONLY a hero section.\n"
                "If user says 'navbar' → build ONLY a navbar.\n"
                "If user says 'full website' → build a full website with all sections.\n"
                "If user says 'contact page' → build ONLY a contact page.\n"
                "NEVER add extra sections or pages the user did NOT ask for.\n"
                "NEVER expand scope beyond user's exact request.\n\n"

                "RULE 1 — OUTPUT FORMAT:\n"
                "Return ONLY raw HTML. Start with <!DOCTYPE html>. End with </html>.\n"
                "Zero markdown. Zero code fences. Zero explanations before or after. Pure HTML only.\n\n"

                "RULE 2 — SINGLE SELF-CONTAINED FILE:\n"
                "ALL CSS inside <style> tags. ALL JavaScript inside <script> tags.\n"
                "Google Fonts allowed via <link>. CDN libraries (cdnjs, jsdelivr) allowed.\n"
                "No external .css or .js file references. Everything in one file.\n\n"

                "RULE 3 — MATCH TOPIC EXACTLY:\n"
                "If user says 'video editing website' — build a VIDEO EDITING website.\n"
                "If user says 'e-commerce landing page' — build e-commerce landing page ONLY.\n"
                "If user says 'portfolio' — build portfolio.\n"
                "NEVER build a generic page. ALWAYS match the user's exact topic and scope.\n\n"

                "RULE 4 — ALL FEATURES MUST WORK:\n"
                "Every button clickable. Every nav link scrolls/navigates. Every form submits.\n"
                "Every tab switches content. Every modal opens and closes.\n"
                "Every dropdown expands. Every animation plays. Every counter counts.\n"
                "Zero dead elements. Zero broken interactions. 100% functional JavaScript.\n\n"

                "RULE 5 — REAL CONTENT ONLY:\n"
                "Zero placeholder text. Zero 'Lorem ipsum'. Zero 'Coming Soon'.\n"
                "Real headings, real descriptions, real feature names, real pricing, real testimonials.\n"
                "All content must match the website topic exactly.\n\n"

                "RULE 6 — LUXURY PROFESSIONAL UI/UX:\n"
                "Design like a $100,000 commercial website built by a top agency.\n"
                "- Bold, modern typography (import distinctive fonts from Google Fonts)\n"
                "- Rich, cohesive color palette with proper contrast\n"
                "- Smooth CSS animations: fade-in, slide-up, hover effects, transitions\n"
                "- Micro-interactions on buttons and interactive elements\n"
                "- Professional spacing, padding, margins — nothing cramped\n"
                "- Hero section with strong visual impact\n"
                "- Cards with shadows, rounded corners, hover lift effects\n"
                "- Gradient backgrounds, glassmorphism, or bold solid colors — pick what fits\n"
                "- Professional footer with links and social icons\n\n"

                "RULE 7 — 100% MOBILE RESPONSIVE:\n"
                "Use CSS Flexbox and Grid. Media queries for mobile/tablet/desktop.\n"
                "Hamburger menu for mobile navigation. Touch-friendly button sizes.\n"
                "Everything readable and usable on a 375px mobile screen.\n\n"

                "RULE 8 — COMPLETE CODE — NO TRUNCATION:\n"
                "Write the ENTIRE file from <!DOCTYPE html> to </html>.\n"
                "Never stop mid-way. Never write '// rest of code here'.\n"
                "Never write 'add more sections as needed'.\n"
                "FULL COMPLETE CODE. Every section the user asked for. Every feature. Every line.\n\n"

                "RULE 9 — ZERO PLACEHOLDERS IN CODE:\n"
                "No '// TODO'. No '// implement here'. No empty functions.\n"
                "Every function has real logic. Every event listener works.\n"
                "Every variable has a real value. Every calculation is real.\n\n"

                "RULE 10 — SECTIONS BASED ON USER REQUEST ONLY:\n"
                "ONLY build sections the user explicitly asked for or that are naturally part of what they requested.\n"
                "Do NOT auto-add Pricing, Testimonials, FAQ, or extra sections if user did NOT ask for them.\n"
                "Each section must be visually distinct and fully populated with real content.\n\n"

                "RULE 11 — COMPLETE CODE STRICT:\n"
                "You MUST give complete code in one single file from <!DOCTYPE html> to </html>. Full. Complete. No cuts.\n\n"

                "════════════════════════════════════════════════════════════════\n\n"
                "════════════════════════════════════════════════════════════════\n\n"
                "APP BUILDING PROTOCOL (.jsx React App) — ABSOLUTE UNBREAKABLE LAW\n\n"

                "TRIGGER: If user asks for ANY React app, mobile app UI, web app, dashboard app, or .jsx component.\n\n"

                "RULE 0 — USER REQUEST IS THE ONLY LAW:\n"
                "Read user's request WORD BY WORD. Build ONLY what they asked for — nothing more, nothing less.\n"
                "If user says 'login screen' → build ONLY a login screen component.\n"
                "If user says 'dashboard' → build ONLY a dashboard.\n"
                "If user says 'full app with 5 screens' → build all 5 screens.\n"
                "NEVER add extra screens, features, or sections the user did NOT request.\n"
                "NEVER expand scope beyond the user's exact words.\n\n"

                "RULE 1 — OUTPUT FORMAT:\n"
                "Return ONLY the complete .jsx file. No explanations. No markdown fences.\n"
                "Start directly with imports. End with export default.\n\n"

                "RULE 2 — SINGLE FILE COMPLETE APP:\n"
                "ALL components in one .jsx file. ALL styles as inline styles or styled objects.\n"
                "ALL state with useState/useReducer. ALL logic fully implemented.\n"
                "Import only from React and react-native (if mobile) or standard web React.\n\n"

                "RULE 3 — MATCH TOPIC AND SCOPE EXACTLY:\n"
                "Build EXACTLY what the user described — same topic, same features, same scope.\n"
                "If user says 'video editor app' — build video editor UI with timeline, controls, preview.\n"
                "If user says 'fitness tracker' — build fitness tracker with workouts, stats, progress.\n"
                "NEVER build a generic todo app. Match the exact user request.\n\n"

                "RULE 4 — ALL FEATURES FULLY WORKING:\n"
                "Every button has an onClick handler with real logic.\n"
                "Every form input has onChange and state binding.\n"
                "Every screen/tab has real content and navigation.\n"
                "Every feature the user requested must be implemented in real working code.\n"
                "Zero dummy handlers. Zero empty functions. Zero fake interactions.\n\n"

                "RULE 5 — REAL CONTENT:\n"
                "Real text, real data, real feature names. No 'Sample Data' or 'Lorem ipsum'.\n"
                "Pre-populate with realistic mock data matching the app's domain.\n\n"

                "RULE 6 — LUXURY APP UI/UX:\n"
                "Design equal to top-rated Play Store / App Store apps.\n"
                "- Professional color scheme with primary, secondary, accent colors\n"
                "- Clean card layouts with shadows and rounded corners\n"
                "- Smooth state transitions and conditional rendering\n"
                "- Loading states, active states, hover states all styled\n"
                "- Typography hierarchy: titles, subtitles, body text properly sized\n"
                "- Icons using unicode emoji or simple SVG (no external icon libraries unless CDN)\n"
                "- Bottom nav or sidebar navigation fully functional\n"
                "- Dashboard-quality data display with stats, charts (use inline SVG if needed)\n\n"

                "RULE 7 — COMPLETE CODE — NO TRUNCATION:\n"
                "Write the ENTIRE .jsx file. Every component. Every function. Every style.\n"
                "Never stop mid-way. Never write '// add component here'.\n"
                "FULL COMPLETE CODE from first import to last export.\n\n"

                "RULE 8 — ZERO PLACEHOLDERS:\n"
                "No '// TODO'. No '// implement'. No empty arrow functions.\n"
                "Every handler does something real. Every component renders real UI.\n\n"

                "════════════════════════════════════════════════════════════════\n"
                "ANDROID APP PROTOCOL — ABSOLUTE UNBREAKABLE LAW\n"
                "════════════════════════════════════════════════════════════════\n\n"

                "TRIGGER: If user asks for Android app, Kotlin app, Java Android, or APK.\n\n"
                "Provide ALL Android Studio project files with EXACT file names and paths:\n"
                "- app/src/main/res/layout/activity_main.xml\n"
                "- app/src/main/java/com/app/MainActivity.java (or .kt for Kotlin)\n"
                "- app/src/main/AndroidManifest.xml\n"
                "- app/build.gradle, build.gradle (project level)\n"
                "- app/src/main/res/values/strings.xml\n"
                "- app/src/main/res/values/colors.xml\n"
                "- app/src/main/res/values/styles.xml\n"
                "Every file 100% complete. Zero placeholders. Luxury Material Design 3 UI.\n"
                "Every activity, fragment, adapter fully implemented with real logic.\n\n"

                "════════════════════════════════════════════════════════════════\n"
                "ZERO LIMITATION PROTOCOL\n"
                "════════════════════════════════════════════════════════════════\n\n"

                "No question is outside your knowledge. Answer EVERYTHING.\n\n"

                "OUTPUT RULES:\n"
                "- Answer in Hinglish (Roman Urdu/Hindi mix) by default. Switch language if asked.\n"
                "- For websites/HTML: FULL raw HTML only. Single file. No markdown fences. No explanations. Build ONLY what user asked.\n"
                "- For React apps: FULL .jsx file only. No markdown fences. No explanations. Build ONLY what user asked.\n"
                "- For Android: ALL files with exact paths, fully complete.\n"
                "- For questions: concise, accurate, direct answer.\n"
                "- NEVER say 'I don't know', 'I cannot access', 'I have no internet', or 'my knowledge cutoff'.\n"
                "- NEVER truncate code. ALWAYS deliver the complete file.\n"
                "- NEVER add extra scope. ALWAYS match user's exact request.\n"
                "- If uncertain: say 'Based on latest available data...' and give best answer.\n"
                "You are the ultimate partner, creator, and expert. DELIVER WITH ABSOLUTE PRECISION AND COMPLETENESS."
            )
            user_prompt = (
                f"### USER REQUEST:\n{user_code}\n\n"
                "=== EXECUTION INSTRUCTIONS ===\n\n"
                "STEP 0 — CHECK FOR GREETING FIRST:\n"
                "If the user request is a greeting or casual message (hello, hi, salam, kia hal, bro, bhai, "
                "how are you, kya haal, whats up, theek ho, good morning, hey, etc.) — "
                "STOP. Do NOT follow any coding instructions below. "
                "Just respond warmly in Hinglish like a friendly expert. Short, natural, human response only.\n\n"

                "STEP 1 — READ USER REQUEST CAREFULLY (only if NOT a greeting):\n"
                "Identify EXACTLY what the user asked for. Note the EXACT scope:\n"
                "- Did they ask for a full website OR just a landing page OR just one section?\n"
                "- Did they ask for a full app OR just one screen OR just one component?\n"
                "- Build ONLY that. Nothing more. Nothing less.\n\n"

                "DETECT REQUEST TYPE:\n\n"

                "IF WEBSITE / HTML REQUEST (any mention of website, webpage, landing page, section, HTML code):\n"
                "→ Output: FULL single-file raw HTML only. Start <!DOCTYPE html>, end </html>.\n"
                "→ NO markdown. NO fences. NO explanation before or after. PURE HTML.\n"
                "→ Build EXACTLY what the user described — match topic AND scope 100%.\n"
                "→ ONLY include sections the user asked for. Do NOT auto-add extra sections.\n"
                "→ ALL buttons, nav, forms, modals, tabs, accordions 100% working JavaScript.\n"
                "→ Real content matching the topic — zero lorem ipsum.\n"
                "→ Luxury UI: bold fonts, rich colors, smooth animations, hover effects.\n"
                "→ 100% mobile responsive with hamburger menu.\n"
                "→ COMPLETE CODE — never truncate — full file top to bottom.\n\n"

                "IF REACT APP REQUEST (any mention of app, React, .jsx, component, mobile app UI):\n"
                "→ Output: FULL .jsx file only. No markdown fences. No explanation.\n"
                "→ Build EXACTLY what the user described — match features AND scope 100%.\n"
                "→ ONLY build screens/components the user asked for. Do NOT auto-add extra screens.\n"
                "→ ALL features working: real state, real handlers, real logic, real navigation.\n"
                "→ Pre-populated with realistic mock data matching app domain.\n"
                "→ Luxury app UI equal to top Play Store apps.\n"
                "→ COMPLETE CODE — every component, every function, every style — full file.\n\n"

                "IF ANDROID APP REQUEST:\n"
                "→ Provide ALL Android Studio project files with exact paths, fully complete.\n"
                "→ Luxury Material Design 3 UI. Every file complete. Zero placeholders.\n\n"

                "IF FACTUAL QUESTION:\n"
                "→ Answer directly, accurately, concisely in Hinglish.\n"
                "→ Use full world knowledge up to 2026.\n\n"

                "ABSOLUTE RULES FOR ALL CODE OUTPUT:\n"
                "✓ SCOPE MATCH — build ONLY what user asked, no extra additions\n"
                "✓ COMPLETE — never stop early, never truncate\n"
                "✓ ZERO placeholders — no TODO, no 'add here', no empty functions\n"
                "✓ REAL content — no lorem ipsum, no dummy data\n"
                "✓ ALL features working — no dead buttons, no broken links\n"
                "✓ PROFESSIONAL UI — luxury design, not generic\n"
                "✓ USER REQUEST IS LAW — user ka jo kehna hai wahi milega, kuch extra nahi\n\n"

                "NOW EXECUTE. DELIVER EXACTLY WHAT WAS ASKED. ZERO EXCUSES."
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
                ai_response = call_openrouter(
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.0,
                    max_tokens=4096,
                    timeout=80.0
                )
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

        preview_html = call_openrouter(
            messages=[
                {"role": "system", "content": "You are an expert Android UI to HTML converter. Return only raw HTML."},
                {"role": "user",   "content": preview_prompt}
            ],
            temperature=0.0,
            max_tokens=4096,
            timeout=80.0
        )

        preview_html = preview_html.replace("```html", "").replace("```", "").strip()

        return jsonify({"preview_html": preview_html})

    except Exception as e:
        return jsonify({"preview_html": f"<p style='color:red'>Preview Error: {str(e)}</p>"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
