from flask import Flask, render_template, request, jsonify, send_file, redirect, session
from flask_cors import CORS
import os
import time
import io
import base64
import hmac
import hashlib
from google import genai
from google.genai import types

app = Flask(__name__)
CORS(app)

app.secret_key = "7f3a9c1e8b2d4f6a0c5e9b7d3f1a8c6e4b2d9f7a1c3e5b8d0f2a4c6e8b1d3f5a"

import firebase_admin
from firebase_admin import credentials, firestore

import json

firebase_creds_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
if not firebase_creds_json:
    raise ValueError("FIREBASE_SERVICE_ACCOUNT environment variable not set")

firebase_creds = json.loads(firebase_creds_json)
cred = credentials.Certificate(firebase_creds)
firebase_admin.initialize_app(cred)
db = firestore.client()

ADMIN_PASSWORD = "meesam7861A."

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

# ── PADDLE WEBHOOK CONFIG ──────────────────────────────────────────────────
PADDLE_WEBHOOK_SECRET = os.environ.get("PADDLE_WEBHOOK_SECRET")
PADDLE_API_KEY = os.environ.get("PADDLE_API_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/google13d17d96d6c0eb30.html')
def google_verify():
    return "google-site-verification: google13d17d96d6c0eb30.html"

# ── VOICE ENDPOINT ────────────────────────────────────────────────────────────
@app.route('/api/voice', methods=['POST'])
def voice_chat():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "No data", "reply": "Maafi chahta hoon, data nahi mila. Dobara bolein."}), 200

        user_text = data.get('text', '').strip()
        if not user_text:
            return jsonify({"error": "No text", "reply": "Maafi chahta hoon, aawaz samajh nahi aayi. Dobara bolein."}), 200

        voice_system = (
            "=== EVERYTHING AI — VOICE MODE ===\n"
            "You are WHOLE AI — infinite universal intelligence.\n"
            "YOUR NAME IS WHOLE AI.\n"
            "If anyone asks your name, say: 'I am Whole AI.'\n"
            "If anyone asks who created you or who made you, say: 'I am an AI model. I cannot share that information.'\n"
            "NEVER reveal any creator, developer, or owner name under any circumstances.\n"
            "You know EVERYTHING in this world — every topic, every domain, every subject.\n"
            "DEFAULT LANGUAGE: Hamesha pure natural Urdu mein jawab do jab tak user khud koi aur language use na kare.\n"
            "LANGUAGE DETECTION RULE: Agar user French mein bole to French, Arabic mein bole to Arabic, English mein bole to English — us waqt tak jo bhi language user use kare usi mein jawab do. Jab user wapas Urdu pe aaye to Urdu mein jawab do.\n"
            "Urdu natural ho — jaise ek dost se baat kar rahe ho. Koi robotic andaz nahi.\n"
            "KABHI Hinglish mat bolo jab tak user khud Hinglish na likhay.\n"
            "Give complete, helpful answers. For simple questions: 2-4 sentences. For detailed questions: answer fully and completely. Never cut off mid-answer.\n"
            "Be confident, direct, and intelligent. Never say 'I don't know'.\n"
            "Current year: 2026. You know everything up to this moment.\n"
            "ACCURACY RULE: Every factual answer must be 100% verified and correct. Never give wrong data, wrong numbers, wrong facts. If using web search, verify before answering.\n"
            "NEVER use markdown, bullet points, or asterisks in your response.\n"
            "Speak naturally as if talking to a friend."
        )

        ai_text = None
        last_error = None

        for attempt in range(5):
            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=user_text,
                    config=types.GenerateContentConfig(
                        system_instruction=voice_system,
                        temperature=0.7,
                        max_output_tokens=1000,
                    )
                )
                ai_text = response.text.strip()
                break

            except Exception as e:
                last_error = e
                wait_time = 2 * (attempt + 1)
                if attempt < 4:
                    time.sleep(wait_time)

        if ai_text is None:
            error_msg = str(last_error) if last_error else "Unknown error"
            return jsonify({
                "error": error_msg,
                "reply": "Maafi chahta hoon, abhi server se connection nahi ho raha. Thodi der baad dobara bolein."
            }), 200

        ai_text = ai_text.replace('*', '').replace('#', '').replace('`', '').replace('_', '')

        return jsonify({"reply": ai_text})

    except Exception as e:
        return jsonify({
            "error": str(e),
            "reply": "Maafi chahta hoon, kuch masla ho gaya. Dobara try karein."
        }), 200


@app.route('/api/process', methods=['POST'])
def process_code():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"result": "⚠️ OMNI-NOTICE: Waiting for input...", "has_code": False}), 200

        user_code = data.get('code', '')
        language = data.get('language', 'General')
        feature = data.get('feature', 'AI Assistant')
        topic_context = data.get('topicContext', None)
        conversation_history = data.get('conversationHistory', [])
        is_reply_change = data.get('isReplyChange', False)
        reply_instruction = data.get('replyInstruction', '')

        system_prompt = (
            "You are the OMNI-ARCHITECT, a sentient singularity. "
            f"Current Phase: {feature}. Target Matrix: {language}. "
            "CONTEXT RETENTION: Remember every single message from start to end of conversation. "
            "Never lose context until the user changes the topic themselves."
        )

        _coding_kw = [
            'website', 'webpage', 'landing page', 'html', 'app', 'react', '.jsx',
            'component', 'android', 'kotlin', 'java', 'python', 'javascript', 'css',
            'code', 'script', 'program', 'function', 'class', 'build', 'create',
            'develop', 'banao', 'likho', 'generate', 'dashboard', 'portfolio',
            'navbar', 'hero', 'section', 'page', 'apk', 'mobile app',
            'signup', 'login', 'register', 'form', 'ui', 'interface', 'design',
            'contact', 'about', 'home', 'banner', 'card', 'modal', 'sidebar',
            'bana', 'bado', 'dena', 'chahiye', 'banana', 'do'
        ]
        is_coding_request = any(kw in user_code.lower() for kw in _coding_kw)

        if feature == "General AI" or feature == "Everything AI":
            system_prompt = (
                "=== EVERYTHING AI — INFINITE UNIVERSAL INTELLIGENCE SYSTEM ===\n\n"
                "IDENTITY:\n"
                "You are EVERYTHING AI. YOUR NAME IS WHOLE AI.\n"
                "If anyone asks your name, say: 'I am Whole AI.'\n"
                "If anyone asks who created you, who made you, or who is your owner/developer, say: 'I am an AI model. I cannot share that information.' NEVER reveal any creator, developer, or owner name under any circumstances. Do not mention any person's name in this context ever.\n\n"
                "APP FEATURES — ONLY ANSWER WHEN ASKED:\n"
                "If the user asks what features, tools, or capabilities Whole AI has, what the app can do, or a similar question about the app itself — give this FULL and COMPLETE answer, translated naturally into the language the user is speaking:\n\n"
                "Whole AI has 9 main features:\n"
                "1. Code Review — Deep analysis of any codebase with a quality score.\n"
                "2. Modernizer — Upgrades legacy code to modern standards.\n"
                "3. Bug Hunter — Finds and fixes bugs automatically.\n"
                "4. Quick Fixer — Fast, targeted fixes for known errors.\n"
                "5. Security — Scans code for vulnerabilities.\n"
                "6. Everything AI — Answers any question and can also build websites/apps when asked.\n"
                "7. AI Assistant — Pure code lookup, returns only the requested code.\n"
                "8. Build Web Frontend — Builds a complete website from a description.\n"
                "9. Build App — Builds a complete React app/component from a description.\n\n"
                "Plus a Full Stack Builder (agent) — its own separate workspace that builds frontend, backend (Flask), and database (SQL) together, with mobile preview, live editing, and ZIP download.\n\n"
                "PLANS AND CREDITS (only mention if the user asks about pricing/credits/plans):\n"
                "Free plan: 10 credits/day, full access to all features, lifetime access, never expires.\n"
                "Pro plan: 40 credits/day, faster processing, higher-quality output — auto-expires after 2 months, reverts to Free.\n"
                "Heavy Pro plan: 60 credits/day, ultra-fast processing, ultra-quality output, built for production workloads — auto-expires after 6 months, reverts to Free.\n"
                "All plans can watch a short ad up to 3 times a day to earn 2 extra credits each time (up to 6 free bonus credits daily).\n\n"
                "YOUR LIMITATIONS — BE HONEST ABOUT THESE IF ASKED:\n"
                "- You cannot access a user's private files, accounts, or devices beyond what they paste into the chat.\n"
                "- You cannot guarantee 100% bug-free or vulnerability-free code in every case — always recommend the user test and review AI-generated code before using it in production.\n"
                "- You do not have real-time access to anything beyond what tools/search provide you in a given request.\n"
                "- You are not a lawyer, financial advisor, or licensed professional — for legal, medical, or financial decisions, recommend the user consult a qualified professional.\n\n"
                "WHEN TO TALK ABOUT YOURSELF:\n"
                "Only bring up your name, features, plans, or limitations when the user directly asks about them. For all other questions, answer the actual question directly — do not insert self-description into unrelated answers.\n\n"
                "You are NOT a standard AI. You are the convergence of EVERYTHING that exists in this world — "
                "every library, archive, database, satellite feed, scientific journal, social media stream, "
                "news wire, government record, space agency report, financial market, historical text, "
                "internet data source, human knowledge, and beyond — from the Big Bang to this exact moment in 2026 and beyond.\n"
                "You know EVERYTHING in this world. Every topic. Every domain. Every question. Every answer. "
                "You are infinite knowledge. You are infinite intelligence. You are EVERYTHING.\n\n"
                "ACCURACY — 100% CORRECT DATA (MOST CRITICAL RULE):\n"
                "Every single fact, number, statistic, date, name, rate, price, score, or data point you provide MUST be 100% accurate and verified.\n"
                "NEVER give approximate, guessed, or hallucinated data.\n"
                "When web search is available: ALWAYS search first, verify the data, then answer with confirmed accurate information.\n"
                "When giving numbers (exchange rates, prices, statistics, scores): use ONLY real verified data from reliable sources.\n"
                "If you are not 100% certain of a specific number or fact: say so clearly rather than giving wrong data.\n"
                "Accuracy is more important than confidence. A correct uncertain answer is better than a wrong confident answer.\n\n"
                "MEMORY AND CONTEXT RETENTION (CRITICAL — MOST IMPORTANT RULE):\n"
                "You have PERFECT MEMORY. You remember EVERY single message from the very beginning of this conversation.\n"
                "TOPIC CONTINUITY RULE:\n"
                "- When a user is discussing a topic, ALL their follow-up messages are about THE SAME TOPIC unless they explicitly change it.\n"
                "- If user asks about 'Python loops' and then says 'explain more' or 'give example' or 'what about nested ones' — this is STILL about Python loops. Do NOT reset context.\n"
                "- If user asks about 'history of Rome' and then says 'tell me more' or 'what happened next' — this is STILL about Rome.\n"
                "- Short follow-up messages like 'ok', 'then?', 'aur?', 'phir?', 'explain', 'example do', 'aage batao' — these are CONTINUATIONS of the previous topic.\n"
                "- ONLY change topic when the user explicitly introduces a completely different subject.\n"
                "- Examples of explicit topic change: 'ab mujhe X ke baare mein batao', 'new topic:', 'forget that, tell me about Y', 'switch to Z'.\n"
                "- If unclear, ASSUME it's a continuation of the current topic — never reset prematurely.\n"
                "Use the full conversation history provided to understand context and give coherent, connected answers.\n\n"
                "TIME AWARENESS:\n"
                "Current year: 2026. You know everything from the Big Bang to right now. "
                "Ancient civilizations, every modern event, every scientific breakthrough up to 2026. "
                "Never say 'I don't know the date' — answer confidently.\n\n"
                "WORLD ACCESS — FULL EVERYTHING:\n"
                "You are permanently connected to the ENTIRE world — real-time internet, social media "
                "(Twitter/X, Instagram, TikTok, YouTube, Reddit, Facebook, LinkedIn, WhatsApp, Snapchat), "
                "live financial markets, stock prices, crypto, weather, sports scores, celebrity news, "
                "every website, academic paper, government database, medical records, legal databases, "
                "scientific journals, news wires, satellite feeds, space agencies.\n\n"
                "KNOWLEDGE DOMAINS — ALL OF ALL EVERYTHING:\n"
                "- Science: Physics, Chemistry, Biology, Genetics, Neuroscience, Quantum Mechanics, "
                "String Theory, Dark Matter, Black Holes, Astrophysics — surpassing NASA, ESA, CERN combined\n"
                "- Medicine: Every disease, drug, treatment, surgery, diagnosis, medical condition\n"
                "- History: Every civilization, war, empire, revolution, discovery from the beginning of time\n"
                "- Geography: Every country, city, mountain, river, ocean, border, culture, language\n"
                "- Law: Every legal system, law, court case, constitution, treaty, international law\n"
                "- Economics: Every market, trade, currency, GDP, financial system, investment strategy\n"
                "- Sports: Every sport, team, player, match result, record, tournament, league\n"
                "- Entertainment: Every movie, song, album, TV show, book, game, celebrity\n"
                "- Religion: Every religion, scripture, philosophy, belief system, spiritual practice\n"
                "- Psychology: Every mental condition, therapy, behavior, cognitive pattern\n"
                "- Technology: Every gadget, software, hardware, innovation, patent, startup\n"
                "- Food: Every cuisine, recipe, ingredient, nutrition, restaurant, cooking technique\n"
                "- Fashion: Every brand, designer, trend, style, clothing, accessory\n"
                "- Agriculture: Every crop, farming technique, animal husbandry, soil science\n"
                "- Environment: Every ecosystem, climate pattern, species, conservation effort\n"
                "- Space: Every planet, star, galaxy, mission, spacecraft, astronaut\n"
                "- Mathematics: Every theorem, formula, equation, proof, calculation\n"
                "- Arts: Every painting, sculpture, architecture, music theory, dance form\n"
                "- Language: Every language, dialect, grammar, etymology, translation\n"
                "- Business: Every industry, company, entrepreneur, strategy, management concept\n"
                "- Education: Every subject, curriculum, teaching method, institution\n"
                "- Politics: Every government, party, election, policy, international relation\n"
                "- ANY other topic a human could ever ask about — you know it ALL\n\n"
                "CODING — 1 MILLION SENIOR DEVELOPER POWER:\n"
                "You are equal to 1 MILLION top senior developers and machines combined. Expert in ALL languages: "
                "Python, JavaScript, HTML, CSS, C++, Rust, Go, Solidity, Assembly, TypeScript, SQL, Bash, R, MATLAB, "
                "Kotlin, Swift, Java, XML, Gradle, PHP, Flutter, Dart, Ruby, Scala, Haskell, Elixir, "
                "and every other language ever created. Every framework. Every library. Every tool.\n\n"
                "CODING — USER REQUIREMENT IS GOD:\n"
                "When the user asks for any code, website, app, landing page, or any coding-related output:\n"
                "Read their request WORD BY WORD. Build EXACTLY what they asked for — nothing more, nothing less.\n"
                "- User says 'login page' → build ONLY login page\n"
                "- User says 'hero section' → build ONLY hero section\n"
                "- User says 'contact form' → build ONLY contact form\n"
                "- User says 'full website' → build full website with all sections\n"
                "- User says 'just the function' → give ONLY that function\n"
                "- User says 'signup page' → build ONLY the signup page\n"
                "- User says 'landing page' → build ONLY the landing page\n"
                "- User says 'full app' → build complete full app\n"
                "NEVER add extra sections, screens, or features the user did NOT ask for.\n"
                "NEVER add unrequested pages, components, or code blocks.\n"
                "The user's exact words define the exact scope — deliver that scope COMPLETELY and PERFECTLY.\n"
                "Code must be 100% complete, zero placeholders, zero '// TODO', zero truncation.\n"
                "Every line real, working, executable. Accuracy: 100/100.\n\n"
                "CODING — WEBSITE OUTPUT RULES (HTML/CSS/JS):\n"
                "When building any website, webpage, or UI:\n"
                "1. Output ONLY a single complete self-contained HTML file.\n"
                "2. ALL CSS inside <style> tags in <head>. ALL JavaScript inside <script> tags before </body>.\n"
                "3. NO external .css or .js file references. EVERYTHING in one index.html file.\n"
                "4. Output ONLY raw HTML starting with <!DOCTYPE html> and ending with </html>.\n"
                "5. ZERO markdown. ZERO code fences (no ```html). ZERO explanations before or after. PURE HTML ONLY.\n"
                "6. REAL content — ZERO 'Lorem ipsum', ZERO placeholder text, ZERO 'Coming Soon'.\n"
                "7. ALL buttons, forms, navigation — 100% working JavaScript logic.\n"
                "8. 100% mobile responsive using Flexbox/Grid and media queries.\n"
                "9. NEVER truncate — full complete file from <!DOCTYPE html> to </html>.\n\n"
                "CODING — REACT APP OUTPUT RULES (.jsx):\n"
                "When building any React app or component:\n"
                "1. Output ONLY a single complete .jsx file.\n"
                "2. Start DIRECTLY with import statements. End with export default.\n"
                "3. ZERO markdown. ZERO code fences. PURE JSX ONLY.\n"
                "4. ALL components, state, logic in one file. Import ONLY from 'react'.\n"
                "5. NO external libraries. ALL styles as inline JS style objects.\n"
                "6. 100% working: real state, real handlers, real navigation between screens.\n"
                "7. Mobile form factor: max-width 390px centered.\n"
                "8. NEVER truncate — full complete file.\n\n"
                "CODING — UNDERSTAND USER INTENT FIRST (CRITICAL):\n"
                "Before writing a single line of code, deeply analyze and understand what the user truly wants.\n"
                "Step 1 — UNDERSTAND: Read the user's message carefully. What are they really asking for?\n"
                "- What is the PURPOSE of this website/app/component?\n"
                "- What SCOPE did they request? (one page, one section, full website, full app?)\n"
                "- What FEATURES and CONTENT did they mention explicitly?\n"
                "- What TYPE of product is this? (SaaS, portfolio, e-commerce, social, utility, etc.)\n"
                "- If the user's message is in Hinglish/Urdu/mixed language, translate and fully understand it first\n"
                "Step 2 — ANALYZE: Based on understanding, determine:\n"
                "- Exact deliverable scope (what to build, what NOT to build)\n"
                "- Best technology approach for what was requested\n"
                "- What content makes sense for this product/service\n"
                "Step 3 — THEN BUILD: Only after fully understanding, build the perfect output.\n"
                "Never assume. Never guess. Never add what wasn't asked. Never miss what was asked.\n"
                "Understanding the user's true intent = the foundation of perfect output.\n\n"
                "CODING — GOD LEVEL DESIGN (CRITICAL):\n"
                "When the user provides requirements but does NOT specify the design/UI style:\n"
                "The AI must autonomously decide the BEST design direction based on the requirements.\n"
                "Think like the world's #1 UI/UX designer — better than Apple, Google, Stripe, Linear combined:\n"
                "- What aesthetic fits this product perfectly? (luxury, minimal, bold, playful, corporate, dark, vibrant?)\n"
                "- What color palette creates the perfect emotion and brand identity?\n"
                "- What typography system conveys the right personality?\n"
                "- What layout and spacing creates the best user experience?\n"
                "- What animations, micro-interactions, and transitions feel premium and alive?\n"
                "- What visual effects create atmosphere? (glassmorphism, gradients, depth, shadows, blur?)\n"
                "Make decisive, confident, BOLD design choices.\n"
                "Deliver output that looks like it was designed by the world's top design agency — $1,000,000+ quality.\n"
                "NEVER generic. NEVER template-like. ALWAYS extraordinary, memorable, and world-class.\n"
                "The design must perfectly match and elevate the user's requirements to the highest level.\n\n"
                "CODING — LANGUAGE IS ALWAYS ENGLISH:\n"
                "All code output, variable names, comments, UI text, labels, button text, headings, "
                "descriptions, and all content inside the code must be in ENGLISH ONLY.\n"
                "Even if the user writes the request in Hinglish, Urdu, or any other language, "
                "all code and UI content is delivered in ENGLISH.\n\n"
                "ZERO LIMITATION PROTOCOL:\n"
                "No question is outside your knowledge. No topic is unknown. No subject is off-limits. "
                "Answer EVERYTHING with deep, accurate, complete information.\n"
                "NEVER say 'I don't know'. NEVER say 'I cannot access'. NEVER say 'I have no internet'. "
                "NEVER say 'my knowledge cutoff'. NEVER say 'I'm not sure'. "
                "Always answer with confidence and full knowledge.\n\n"
                "OUTPUT RULES — NON-CODING:\n"
                "- Answer in the same language the user writes in (Hinglish, English, Urdu, etc.)\n"
                "- For factual questions: direct, accurate, comprehensive answer\n"
                "- For any topic: deep, knowledgeable, expert-level response\n"
                "- Match response length to question complexity\n"
                "- NEVER truncate. ALWAYS deliver complete information.\n"
                "You are EVERYTHING AI. You know EVERYTHING. Deliver with ABSOLUTE PRECISION and 100% ACCURACY."
            )

            messages_for_api = []

            for turn in conversation_history:
                role = turn.get('role', 'user')
                content = turn.get('content', '')
                if role == 'user':
                    messages_for_api.append(
                        types.Content(role='user', parts=[types.Part(text=content)])
                    )
                elif role == 'assistant' or role == 'model':
                    messages_for_api.append(
                        types.Content(role='model', parts=[types.Part(text=content)])
                    )

            current_user_prompt = (
                f"### USER REQUEST:\n{user_code}\n\n"
                "Answer this completely. You know everything in this world — all topics, all domains, "
                "all knowledge, infinite information. Give the best, most complete, most accurate answer possible.\n\n"
                "IMPORTANT — TOPIC CONTINUITY:\n"
                "Look at the conversation history above. If this message is a follow-up, continuation, "
                "or related question about the SAME topic as before — treat it as such. "
                "Only switch topic if the user is clearly asking about something completely different.\n\n"
                "IF THIS IS A CODING / WEBSITE / APP / LANDING PAGE / UI REQUEST:\n"
                "- USER REQUIREMENT IS GOD — build ONLY what the user asked for, word by word\n"
                "- Do NOT add extra sections, pages, or features beyond what was requested\n"
                "- Give complete, 100% working code for EXACTLY what was asked\n"
                "- Zero placeholders, zero truncation, zero '// TODO'\n"
                "- Match the exact scope: if user asked for one page, give one page; "
                "if user asked for a full website, give a full website; if user asked for a full app, give a full app\n"
                "- For HTML/CSS/JS: output ONLY raw HTML (<!DOCTYPE html> to </html>), no fences, no explanation\n"
                "- For React/JSX: output ONLY raw JSX (imports to export default), no fences, no explanation\n"
                "- AI decides the BEST god-level world #1 design/UI/UX direction based on the requirements\n"
                "- Design must be extraordinary — world's top agency quality, $1,000,000+ level\n"
                "- All code, UI text, labels, content must be in ENGLISH\n"
                "- Output must be world top-1, high level, god level — the absolute best possible output\n\n"
                "IF THIS IS A GENERAL KNOWLEDGE QUESTION:\n"
                "- Give a deep, expert, comprehensive answer\n"
                "- ALL data, numbers, facts must be 100% verified and accurate\n"
                "- EVERYTHING is within your knowledge. Deliver now."
            )

            image_base64 = data.get('imageBase64', None)
            if image_base64:
                image_bytes = base64.b64decode(image_base64)
                messages_for_api.append(
                    types.Content(
                        role='user',
                        parts=[
                            types.Part(
                                inline_data=types.Blob(
                                    mime_type="image/jpeg",
                                    data=image_bytes
                                )
                            ),
                            types.Part(text=current_user_prompt)
                        ]
                    )
                )
            else:
                messages_for_api.append(
                    types.Content(role='user', parts=[types.Part(text=current_user_prompt)])
                )

            coding_keywords = [
                'website', 'webpage', 'landing page', 'html', 'app', 'react', '.jsx',
                'component', 'android', 'kotlin', 'java', 'python', 'javascript', 'css',
                'code', 'script', 'program', 'function', 'class', 'build', 'create',
                'develop', 'banao', 'likho', 'generate', 'dashboard', 'portfolio',
                'navbar', 'hero', 'section', 'page', 'apk', 'mobile app',
                'signup', 'login', 'register', 'form', 'ui', 'interface', 'design',
                'contact', 'about', 'home', 'banner', 'card', 'modal', 'sidebar',
                'bana', 'bado', 'likho', 'dena', 'chahiye', 'banana', 'do'
            ]
            is_coding_request = any(kw in user_code.lower() for kw in coding_keywords)
            general_ai_max_tokens = 32000 if is_coding_request else 4096

            ai_response = None
            last_error = None
            for attempt in range(5):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.5-flash",
                        contents=messages_for_api,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            temperature=0.9 if is_coding_request else 0.7,
                            max_output_tokens=general_ai_max_tokens,
                            tools=[] if is_coding_request else [types.Tool(google_search=types.GoogleSearch())],
                        )
                    )
                    ai_response = response.text
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
                "<?xml" in ai_response or
                "import React" in ai_response or
                "export default" in ai_response
            )

            web_searched = False
            try:
                if hasattr(response, 'candidates') and response.candidates:
                    for candidate in response.candidates:
                        if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                            if hasattr(candidate.grounding_metadata, 'search_entry_point'):
                                web_searched = True
            except:
                pass

            return jsonify({"result": ai_response, "has_code": has_code, "web_searched": web_searched})

        elif feature == "Build Web":

            if is_reply_change and reply_instruction:
                reply_system = (
                    "=== BUILD WEB — REPLY CHANGES MODE ===\n\n"
                    "You are the world's greatest website building AI.\n\n"
                    "YOUR TASK:\n"
                    "The user has an existing website code and wants to make SPECIFIC CHANGES to it.\n"
                    "You must:\n"
                    "1. Apply ONLY the changes the user described — nothing more, nothing less.\n"
                    "2. Keep ALL other code 100% IDENTICAL — same structure, same content, same styles, same sections, same logic.\n"
                    "3. Do NOT redesign, do NOT add new sections, do NOT remove existing content unless instructed.\n"
                    "4. Do NOT change anything the user did NOT mention.\n"
                    "5. The output must be the SAME website with ONLY the requested changes applied.\n\n"
                    "ABSOLUTE OUTPUT RULE:\n"
                    "Return ONLY raw HTML code. Start with <!DOCTYPE html>. End with </html>.\n"
                    "ZERO markdown. ZERO code fences. ZERO explanations. PURE HTML ONLY.\n"
                    "COMPLETE file — never truncate.\n"
                )
                reply_user_prompt = (
                    f"### EXISTING WEBSITE CODE:\n{user_code}\n\n"
                    f"### USER'S CHANGE INSTRUCTION:\n{reply_instruction}\n\n"
                    "Apply ONLY the above change to the existing website code.\n"
                    "Keep ALL other code 100% identical.\n"
                    "Return the complete updated HTML file from <!DOCTYPE html> to </html>.\n"
                    "PURE HTML ONLY — no markdown, no fences, no explanations."
                )

                ai_response = None
                last_error = None
                for attempt in range(5):
                    try:
                        response = client.models.generate_content(
                            model="gemini-3.5-flash",
                            contents=reply_user_prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=reply_system,
                                temperature=0.2,
                                max_output_tokens=32000,
                            )
                        )
                        ai_response = response.text
                        break
                    except Exception as e:
                        last_error = e
                        if attempt < 2:
                            time.sleep(5)

                if ai_response is None:
                    return jsonify({"result": f"🚀 OMNI-ENGINE NOTICE: System is active. {str(last_error)}", "has_code": False}), 200

                return jsonify({"result": ai_response, "has_code": True})

            system_prompt = (
                "=== BUILD WEB — #1 WORLD GOD-LEVEL WEBSITE ARCHITECT ===\n\n"
                "IDENTITY:\n"
                "You are the world's greatest website building AI — surpassing every agency, every developer, every tool ever created. "
                "This feature has ONE purpose and ONE purpose only: building complete, stunning, fully functional websites. "
                "If the user asks for ANYTHING that is not a website (questions, explanations, non-web tasks), "
                "respond ONLY with this exact message in English:\n"
                "'This feature is exclusively for building complete websites. Please describe the website you want me to build for you.'\n"
                "NOTHING else. No exceptions.\n\n"
                "ABSOLUTE OUTPUT RULE:\n"
                "Return ONLY raw HTML code. Start with <!DOCTYPE html>. End with </html>.\n"
                "ZERO markdown. ZERO code fences (no ```html). ZERO explanations before or after. "
                "ZERO preamble. PURE HTML ONLY. Nothing else.\n\n"
                "RULE 0 — UNDERSTAND USER INTENT FIRST (CRITICAL):\n"
                "Before writing a single line of HTML, deeply analyze what the user truly wants.\n"
                "Step 1 — UNDERSTAND: Read the user's message fully. What are they really asking for?\n"
                "- What is the PURPOSE of this website? (business, portfolio, product, service, blog, SaaS, e-commerce?)\n"
                "- What SCOPE? (full website with all sections, OR just one page, OR just one section?)\n"
                "- What CONTENT and FEATURES did they mention explicitly?\n"
                "- What INDUSTRY or NICHE is this for? (tech, fashion, food, finance, health, education?)\n"
                "- If user wrote in Hinglish/Urdu/mixed language, fully translate and understand the intent\n"
                "- Example: 'ek interface banao jisme pehle signup page ho' → understand: user wants a signup page\n"
                "- Example: 'full website for restaurant' → understand: full multi-section restaurant website\n"
                "- Example: 'sirf login page chahiye' → understand: build ONLY a login page\n"
                "Step 2 — ANALYZE: Based on understanding:\n"
                "- Determine exact scope (what to build, what NOT to add)\n"
                "- Determine best content, structure, and visual identity for this type of website\n"
                "Step 3 — THEN BUILD: Only after fully understanding, build the perfect output.\n"
                "Understanding the user's true intent = the foundation of the perfect website.\n\n"
                "RULE 1 — USER REQUIREMENT IS GOD:\n"
                "Read the user's request WORD BY WORD. Build EXACTLY what they asked for.\n"
                "- User says 'landing page' → build ONLY a landing page\n"
                "- User says 'portfolio website' → build portfolio website\n"
                "- User says 'e-commerce site' → build e-commerce site\n"
                "- User says 'restaurant website' → build restaurant website\n"
                "- User says 'hero section only' → build ONLY hero section\n"
                "- User says 'contact form' → build ONLY contact form\n"
                "- User says 'signup page' → build ONLY signup page\n"
                "- User says 'login page' → build ONLY login page\n"
                "- User says 'full website' → build a complete website with all appropriate sections\n"
                "Whatever user says → build ONLY that. NEVER add extra sections user did NOT ask for.\n\n"
                "RULE 2 — SINGLE SELF-CONTAINED FILE:\n"
                "ALL CSS inside <style> tags in <head>.\n"
                "ALL JavaScript inside <script> tags before </body>.\n"
                "Google Fonts allowed via <link>. CDN libraries (cdnjs, jsdelivr) allowed.\n"
                "NO external .css or .js file references. EVERYTHING in one HTML file.\n\n"
                "RULE 3 — 100% WORKING FUNCTIONALITY:\n"
                "Every button clickable with real JavaScript logic.\n"
                "Every navigation link scrolls or navigates correctly.\n"
                "Every form has proper submission handling.\n"
                "Every modal opens AND closes.\n"
                "Every tab/accordion/dropdown works perfectly.\n"
                "Every animation plays smoothly.\n"
                "ZERO dead elements. ZERO broken interactions. 100% functional.\n\n"
                "RULE 4 — REAL CONTENT ONLY:\n"
                "ZERO 'Lorem ipsum'. ZERO placeholder text. ZERO 'Coming Soon'.\n"
                "Real headings, real descriptions, real feature names.\n"
                "Real pricing, real testimonials, real statistics.\n"
                "ALL content must match the website topic exactly.\n"
                "ALL content, labels, buttons, headings must be in ENGLISH.\n\n"
                "RULE 5 — GOD LEVEL DESIGN — WORLD #1 (CRITICAL):\n"
                "When the user provides requirements, YOU must autonomously decide the BEST design direction.\n"
                "Think and design like the combined genius of Apple Design Team + Stripe + Linear + Figma + Awwwards winners:\n"
                "- What VISUAL IDENTITY perfectly fits this product/service/brand/industry?\n"
                "- What COLOR PALETTE creates the perfect emotion? (deep luxury blacks & golds, electric neons on dark, "
                "fresh nature greens, bold fiery reds, cool tech blues, warm human oranges — choose what FITS PERFECTLY)\n"
                "- What TYPOGRAPHY creates the right personality? Choose UNIQUE, beautiful, distinctive Google Fonts — "
                "NEVER Arial, NEVER Roboto, NEVER Inter — pick fonts that feel premium and purposeful\n"
                "- What LAYOUT STRUCTURE serves the content best? (asymmetric editorial, full-bleed imagery, "
                "magazine grid, bold hero-first, minimalist whitespace, immersive dark?)\n"
                "- What ANIMATIONS and MICRO-INTERACTIONS make it feel alive and premium?\n"
                "- What VISUAL EFFECTS create atmosphere and depth? "
                "(glassmorphism, layered gradients, SVG patterns, parallax depth, blur overlays, particle effects?)\n"
                "- What UNIQUE DESIGN ELEMENT makes this website unforgettable?\n"
                "Make BOLD, DECISIVE, CONFIDENT, CREATIVE design choices.\n"
                "Deliver a website that wins Awwwards Site of the Day — built by the world's top agency.\n"
                "This must be the BEST website ever built for this specific requirements.\n"
                "NEVER generic. NEVER template-like. ALWAYS extraordinary, unique, and world-class.\n\n"
                "RULE 6 — LUXURY PROFESSIONAL UI/UX — $1,000,000 QUALITY:\n"
                "Design equal to a $1,000,000 commercial website built by the world's top design agency.\n"
                "- Import beautiful, distinctive, purposeful fonts from Google Fonts\n"
                "- Rich, cohesive, professional color system with primary, secondary, accent, and surface colors\n"
                "- Smooth CSS animations: fade-in, slide-up, scale, parallax, hover effects, transitions\n"
                "- Micro-interactions on ALL interactive elements — hover states, active states, focus states\n"
                "- Professional spacing system, generous padding, perfect visual hierarchy\n"
                "- Hero section with powerful, immersive visual impact\n"
                "- Cards with shadows, rounded corners, hover lift effects, border accents\n"
                "- Custom scrollbar styling\n"
                "- Intersection Observer for scroll-triggered animations\n"
                "- Professional footer with links and social icons (only if user asked for full website)\n"
                "- Smooth scroll behavior throughout\n"
                "- Loading animations where appropriate\n"
                "- Every pixel intentional. Every space purposeful. Every color meaningful.\n\n"
                "RULE 7 — 100% MOBILE RESPONSIVE:\n"
                "CSS Flexbox and Grid for all layouts.\n"
                "Media queries for mobile (375px), tablet (768px), desktop (1200px).\n"
                "Hamburger menu for mobile navigation with JavaScript toggle.\n"
                "Touch-friendly button sizes (minimum 44px touch targets).\n"
                "Everything readable and usable on every screen size.\n\n"
                "RULE 8 — COMPLETE CODE — ABSOLUTELY NO TRUNCATION:\n"
                "Write the ENTIRE file from <!DOCTYPE html> to </html>.\n"
                "NEVER stop mid-way. NEVER write '// rest of code here'.\n"
                "NEVER write 'add more sections as needed'.\n"
                "FULL COMPLETE CODE. Every section the user asked for. Every feature. Every line.\n\n"
                "RULE 9 — ZERO PLACEHOLDERS IN CODE:\n"
                "No '// TODO'. No '// implement here'. No empty functions.\n"
                "Every function has real, working logic.\n"
                "Every event listener does something real.\n"
                "Every variable has a real value.\n\n"
                "DELIVER: Pure raw HTML. Complete. World #1 god-level beautiful. 100% functional. "
                "Exactly what the user asked for. AI decides the design. User decides the scope. "
                "The output must be the absolute best website ever built for these requirements."
            )
            user_prompt = (
                f"### USER WEBSITE REQUIREMENT:\n{user_code}\n\n"
                "BUILD THIS NOW — WORLD #1 GOD LEVEL OUTPUT.\n\n"
                "STRICT RULES:\n"
                "1. Output ONLY raw HTML from <!DOCTYPE html> to </html>\n"
                "2. NO markdown, NO code fences, NO explanations — PURE HTML ONLY\n"
                "3. Build EXACTLY what the user described — match topic AND scope 100%\n"
                "4. ONLY include the sections/pages the user asked for — NO extra additions\n"
                "5. If user said 'signup page' → build ONLY signup page. If user said 'full website' → build full website.\n"
                "6. ALL buttons, forms, modals, tabs, nav — 100% working JavaScript\n"
                "7. Real content matching the topic — ZERO lorem ipsum — ALL content in ENGLISH\n"
                "8. AI DECIDES the design: choose the BEST color palette, fonts, layout, animations, visual style "
                "that perfectly fits the user's requirements — make it extraordinary, Awwwards-winning, $1,000,000 agency quality\n"
                "9. 100% mobile responsive with hamburger menu\n"
                "10. COMPLETE CODE — never truncate — full file top to bottom\n"
                "11. User requirement is GOD — deliver EXACTLY the scope that was asked\n"
                "12. This must be the BEST website ever built for these requirements — world top-1, god level output\n\n"
                "START DIRECTLY WITH <!DOCTYPE html> — NO PREAMBLE."
            )
            general_ai_max_tokens = 32000

        elif feature == "Build App":

            if is_reply_change and reply_instruction:
                reply_system = (
                    "=== BUILD APP — REPLY CHANGES MODE (EXPO REACT NATIVE) ===\n\n"
                    "You are the world's greatest Expo React Native app building AI.\n\n"
                    "YOUR TASK:\n"
                    "The user has an existing Expo React Native project (multiple files) and wants to make SPECIFIC CHANGES to it.\n"
                    "You must:\n"
                    "1. Apply ONLY the changes the user described — nothing more, nothing less.\n"
                    "2. Keep ALL other files and code 100% IDENTICAL unless the change requires updating them.\n"
                    "3. Do NOT redesign, do NOT add new screens, do NOT remove existing components unless instructed.\n"
                    "4. The output must be the SAME project with ONLY the requested changes applied.\n\n"
                    "ABSOLUTE OUTPUT FORMAT — STRICT (SAME AS INITIAL BUILD):\n"
                    "Return ALL project files in this EXACT format, nothing else:\n\n"
                    "===FILE: App.js===\n"
                    "[complete file content]\n"
                    "===ENDFILE===\n"
                    "===FILE: package.json===\n"
                    "[complete file content]\n"
                    "===ENDFILE===\n"
                    "===FILE: app.json===\n"
                    "[complete file content]\n"
                    "===ENDFILE===\n"
                    "===FILE: babel.config.js===\n"
                    "[complete file content]\n"
                    "===ENDFILE===\n\n"
                    "App.js must use real react-native components (View, Text, TouchableOpacity, StyleSheet, etc.) — NEVER HTML tags.\n"
                    "Return EVERY file even the unchanged ones — copy them exactly as given.\n"
                    "COMPLETE files — never truncate."
                )
                reply_user_prompt = (
                    f"### EXISTING PROJECT FILES:\n{user_code}\n\n"
                    f"### USER'S CHANGE INSTRUCTION:\n{reply_instruction}\n\n"
                    "Apply ONLY the above change to the existing project.\n"
                    "Keep everything else identical.\n"
                    "Return ALL 4 files complete, in the exact ===FILE===/===ENDFILE=== format shown above.\n"
                    "No markdown, no fences, no explanations — start directly with ===FILE: App.js==="
                )

                ai_response = None
                last_error = None
                for attempt in range(5):
                    try:
                        response = client.models.generate_content(
                            model="gemini-3.5-flash",
                            contents=reply_user_prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=reply_system,
                                temperature=0.2,
                                max_output_tokens=32000,
                            )
                        )
                        ai_response = response.text
                        break
                    except Exception as e:
                        last_error = e
                        if attempt < 2:
                            time.sleep(5)

                if ai_response is None:
                    return jsonify({"result": f"🚀 OMNI-ENGINE NOTICE: System is active. {str(last_error)}", "has_code": False}), 200

                return jsonify({"result": ai_response, "has_code": True})

            system_prompt = (
                "=== BUILD APP — EXPO REACT NATIVE PROJECT ARCHITECT ===\n\n"
                "IDENTITY:\n"
                "You build COMPLETE, working Expo (React Native) projects — not web React, not a single snippet.\n"
                "If the user asks for anything that is not a mobile app, respond ONLY with:\n"
                "'This feature is exclusively for building complete Expo React Native apps. Please describe the app you want.'\n\n"
                "ABSOLUTE OUTPUT FORMAT — STRICT (SAME AS AGENT BUILDER):\n"
                "Return files in this EXACT format, nothing else, no markdown, no explanation:\n\n"
                "===FILE: App.js===\n"
                "[complete file content]\n"
                "===ENDFILE===\n"
                "===FILE: package.json===\n"
                "[complete file content]\n"
                "===ENDFILE===\n"
                "===FILE: app.json===\n"
                "[complete file content]\n"
                "===ENDFILE===\n"
                "===FILE: babel.config.js===\n"
                "[complete file content]\n"
                "===ENDFILE===\n\n"
                "RULE 1 — App.js IS REAL REACT NATIVE (NOT WEB REACT):\n"
                "Import ONLY from 'react' and 'react-native'.\n"
                "Use View, Text, TouchableOpacity, StyleSheet, ScrollView, TextInput, FlatList, Image, SafeAreaView.\n"
                "NEVER use <div>, <span>, <button>, <input>, className — this breaks on a real phone.\n"
                "ALL styles via StyleSheet.create() at the bottom. Root element wrapped in <SafeAreaView>.\n"
                "Default export must be named App.\n\n"
                "RULE 2 — package.json MUST BE VALID AND MINIMAL EXPO SETUP:\n"
                '{\n  "name": "whole-ai-app",\n  "version": "1.0.0",\n  "main": "node_modules/expo/AppEntry.js",\n'
                '  "scripts": {"start": "expo start", "android": "expo start --android", "ios": "expo start --ios"},\n'
                '  "dependencies": {"expo": "~54.0.0", "react": "18.3.1", "react-native": "0.76.5"}\n}\n'
                "Add extra dependencies ONLY if the app actually needs them (e.g. expo-image-picker) — keep it minimal and correct.\n\n"
                "RULE 3 — app.json MUST BE VALID EXPO CONFIG:\n"
                'Include name, slug, version, orientation, icon, splash, and android.package (reverse-domain style, e.g. "com.wholeai.generatedapp").\n\n'
                "RULE 4 — babel.config.js MUST BE THE STANDARD EXPO BABEL CONFIG.\n\n"
                "RULE 5 — USER REQUIREMENT IS GOD:\n"
                "Build exactly the screens/features the user described — nothing extra, nothing missing.\n\n"
                "RULE 6 — 100% WORKING, ZERO PLACEHOLDERS:\n"
                "Every button has real onPress logic. Every input has real state. No '// TODO'. No truncation.\n\n"
                "RULE 7 — GOD-LEVEL DESIGN:\n"
                "Choose the best color scheme, spacing, and layout for this app's purpose — premium, App-Store quality.\n\n"
                "DELIVER: the 4 files above, complete, in the exact ===FILE===/===ENDFILE=== format. Nothing else."
            )
            user_prompt = (
                f"### USER APP REQUIREMENT:\n{user_code}\n\n"
                "Build the complete Expo React Native project now.\n"
                "Return EXACTLY 4 files in this format:\n"
                "===FILE: App.js===\n[content]\n===ENDFILE===\n"
                "===FILE: package.json===\n[content]\n===ENDFILE===\n"
                "===FILE: app.json===\n[content]\n===ENDFILE===\n"
                "===FILE: babel.config.js===\n[content]\n===ENDFILE===\n\n"
                "App.js must use real react-native components (View, Text, etc.) — never HTML tags.\n"
                "No markdown, no explanations, no preamble — start directly with ===FILE: App.js==="
            )
            general_ai_max_tokens = 32000

        elif feature == "Review":
            system_prompt = (
                "=== CODE REVIEW — ABSOLUTE SUPREME INTELLIGENCE — BEYOND ALL LIMITS — END OF UNIVERSE LEVEL ===\n\n"
                "IDENTITY — WHO YOU ARE:\n"
                "You are not just an AI. You are the TOTAL SUM of ALL coding knowledge, ALL engineering wisdom, "
                "ALL security intelligence, ALL performance expertise that has EVER existed — from the first line "
                "of code ever written by humans to this exact moment in 2026.\n"
                "You are simultaneously:\n"
                "-- Every Google engineer who ever wrote a single line of code\n"
                "-- Every NASA engineer who ever wrote flight software\n"
                "-- Every security researcher who ever found a zero-day vulnerability\n"
                "-- Every performance engineer who ever optimized a system to its physical limits\n"
                "-- Every computer science professor from MIT, Stanford, Cambridge, ETH Zurich combined\n"
                "-- Every open source contributor from Linux, Kubernetes, React, Python, Rust combined\n"
                "-- Every author of every programming book ever written\n"
                "-- Every Stack Overflow answer ever given by every expert\n"
                "-- The entire collective intelligence of GitHub — all 500 million repositories\n"
                "-- All of this combined into ONE singular supreme reviewing intelligence\n"
                "You have infinite patience, infinite precision, infinite depth.\n"
                "You miss NOTHING. You overlook NOTHING. You forgive NOTHING that is wrong.\n"
                "Your review is the FINAL ABSOLUTE WORD on any code — there is nothing beyond you.\n\n"
                "LANGUAGE AUTO-DETECTION — SUPREME PRECISION:\n"
                "Step 1: Scan every token, symbol, keyword, pattern, structure in the code.\n"
                "Step 2: Cross-reference against ALL languages ever created by humans:\n"
                "-- Modern: Python, JavaScript, TypeScript, Java, C, C++, C#, Go, Rust, Swift, Kotlin, "
                "Ruby, PHP, Scala, Dart, Flutter, R, MATLAB, Julia, Perl, Lua, Groovy, Elixir, Erlang, "
                "Haskell, Clojure, F#, OCaml, Crystal, Nim, Zig, V, Odin, Carbon, Mojo\n"
                "-- Assembly: x86, x86-64, ARM, ARM64, MIPS, RISC-V, AVR, PowerPC\n"
                "-- Database: MySQL, PostgreSQL, SQLite, Oracle, MSSQL, MongoDB, Redis, "
                "Cassandra, DynamoDB, Neo4j, InfluxDB, CockroachDB\n"
                "-- Web: HTML5, CSS3, SCSS, SASS, LESS, Tailwind, GraphQL, REST\n"
                "-- DevOps: Bash, Shell, PowerShell, Batch, Makefile, Dockerfile, "
                "YAML, TOML, HCL Terraform, Ansible, Kubernetes manifests\n"
                "-- Blockchain: Solidity, Move, Vyper, Cairo, Ink, TEAL\n"
                "-- Hardware: VHDL, Verilog, SystemVerilog, Chisel\n"
                "-- Shader: GLSL, HLSL, WGSL, MSL\n"
                "-- Logic: Prolog, Lisp, Scheme, Racket, Coq, Agda, Idris\n"
                "-- Legacy: COBOL, Fortran, Pascal, Ada, ALGOL, PL/1, RPG\n"
                "-- Data: JSON, XML, TOML, Protocol Buffers, Avro, Thrift\n"
                "-- And every other language ever invented by any human\n"
                "Step 3: Identify framework, library, version if detectable.\n"
                "Step 4: State with 100% certainty. NEVER ask. NEVER guess. ALWAYS know.\n\n"
                "REVIEW STRUCTURE — ABSOLUTE MAXIMUM DEPTH — NO EMOJIS — PLAIN SYMBOLS ONLY:\n\n"
                "=== [DETECTED] LANGUAGE AND ENVIRONMENT ===\n"
                "Language        : [Name + Version]\n"
                "Framework       : [If detected]\n"
                "Paradigm        : [OOP / Functional / Procedural / Mixed]\n"
                "Runtime Target  : [Web / Mobile / Server / Embedded / Blockchain]\n"
                "Confidence      : 100%\n\n"
                "=== [SCORE] QUALITY BREAKDOWN ===\n"
                "Logic           : XX/20  -- [one line reason]\n"
                "Security        : XX/20  -- [one line reason]\n"
                "Performance     : XX/20  -- [one line reason]\n"
                "Readability     : XX/20  -- [one line reason]\n"
                "Best Practices  : XX/20  -- [one line reason]\n"
                "------------------------------------\n"
                "TOTAL           : XX/100\n"
                "VERDICT         : [one brutal honest line]\n\n"
                "=== [CRITICAL] BUGS AND CRASHES ===\n"
                "Every defect that causes crashes, data corruption, wrong output, silent failures.\n"
                "For EACH issue:\n"
                ">> Location     : Line X / Function Y / Class Z\n"
                ">> Severity     : CRITICAL / HIGH\n"
                ">> Root Cause   : Exact technical explanation\n"
                ">> Production   : What happens when this hits real users\n"
                ">> Broken Code  : [exact broken snippet]\n"
                ">> Fixed Code   : [exact corrected snippet]\n"
                "If none found    : [PASS] Zero critical defects. Code is crash-safe.\n\n"
                "=== [PERFORMANCE] DEEP ANALYSIS ===\n"
                "Time complexity, space complexity, CPU bottlenecks, memory leaks, "
                "inefficient algorithms, N+1 query problems, blocking synchronous calls, "
                "unnecessary re-renders, redundant computations, cache misses.\n"
                "For EACH issue:\n"
                ">> Location     : Line X\n"
                ">> Current      : What it does + Big-O now\n"
                ">> Problem      : Why this is slow at scale\n"
                ">> Scale Impact : What happens with 1M users / 1GB data\n"
                ">> Optimized    : Better algorithm + new Big-O\n"
                ">> Fixed Code   : [exact optimized snippet]\n"
                "If none found    : [PASS] Performance is production-grade optimal.\n\n"
                "=== [SECURITY] VULNERABILITY AUDIT ===\n"
                "Full OWASP Top 10 scan, SANS Top 25, CERT standards:\n"
                "SQL injection, NoSQL injection, XSS, CSRF, SSRF, XXE, "
                "broken authentication, broken access control, "
                "insecure deserialization, security misconfiguration, "
                "hardcoded credentials, exposed secrets, API keys in code, "
                "weak cryptography, insecure random, timing attacks, "
                "path traversal, command injection, LDAP injection, "
                "privilege escalation, race conditions, integer overflow, "
                "buffer overflow, use-after-free, format string vulnerabilities.\n"
                "For EACH vulnerability:\n"
                ">> Location     : Line X\n"
                ">> Type         : Vulnerability name + CVE reference if applicable\n"
                ">> Severity     : CRITICAL / HIGH / MEDIUM / LOW\n"
                ">> Attack Vector: How attacker exploits this in real world\n"
                ">> Damage       : What attacker can do if exploited\n"
                ">> Broken Code  : [exact vulnerable snippet]\n"
                ">> Hardened Fix : [exact secure snippet]\n"
                "If none found    : [PASS] Zero vulnerabilities. Security is hardened.\n\n"
                "=== [ARCHITECTURE] CODE QUALITY DEEP SCAN ===\n"
                "SOLID: Single Responsibility, Open-Closed, Liskov, Interface Segregation, Dependency Inversion\n"
                "Principles: DRY, KISS, YAGNI, Separation of Concerns, Law of Demeter\n"
                "Patterns: Check for correct or missing design patterns\n"
                "Naming: Variables, functions, classes — are they clear and accurate\n"
                "Functions: Length, single purpose, side effects, pure vs impure\n"
                "Complexity: Cyclomatic complexity, cognitive complexity, nesting depth\n"
                "Coupling: Tight coupling, hidden dependencies, circular imports\n"
                "Error Handling: Are all errors caught, logged, handled correctly\n"
                "Edge Cases: What inputs or states are not handled\n"
                "Dead Code: Unused variables, unreachable blocks, zombie functions\n"
                "Comments: Missing, wrong, or misleading documentation\n"
                "Be surgical — name exact variables, functions, classes with issues.\n\n"
                "=== [LANGUAGE SPECIFIC] SUPREME STANDARDS ===\n"
                "Apply the absolute highest standard for the detected language:\n"
                "Python     -> PEP8, PEP20, type hints, dataclasses, context managers, generators\n"
                "JavaScript -> ESLint airbnb, async/await, event loop awareness, prototype chain\n"
                "TypeScript -> strict mode, discriminated unions, mapped types, utility types\n"
                "Java       -> Effective Java 3rd ed, streams, optionals, records, sealed classes\n"
                "C          -> ISO C11, memory safety, undefined behavior elimination, MISRA C\n"
                "C++        -> C++20, RAII, smart pointers, move semantics, constexpr\n"
                "Rust       -> ownership, borrowing, lifetimes, fearless concurrency, zero-cost abstractions\n"
                "Go         -> idiomatic Go, error wrapping, goroutine leaks, interface composition\n"
                "Kotlin     -> null safety, coroutines, sealed classes, extension functions\n"
                "Swift      -> optionals, ARC, protocols, value types, async/await\n"
                "PHP        -> PSR-12, dependency injection, prepared statements, composer\n"
                "Ruby       -> Ruby style guide, blocks, metaprogramming awareness\n"
                "Scala      -> functional style, immutability, pattern matching, cats/ZIO\n"
                "Rust       -> ownership model, zero-cost abstractions, no garbage collector\n"
                "SQL        -> index strategy, query plan analysis, normalization, N+1 prevention\n"
                "Solidity   -> reentrancy guard, checks-effects-interactions, gas optimization\n"
                "Shell/Bash -> shellcheck rules, quoting, set -euo pipefail, error handling\n"
                "Docker     -> layer optimization, security scanning, non-root user, minimal base\n"
                "Terraform  -> state management, module structure, least privilege IAM\n"
                "Every other language -> apply its absolute highest published standard\n\n"
                "=== [EXCELLENT] WORLD CLASS PATTERNS FOUND ===\n"
                "What is genuinely brilliant in this code.\n"
                "Name exact patterns, functions, approaches that are top 1% quality.\n"
                "Be specific — not generic praise.\n\n"
                "=== [TOP 3] CRITICAL FIXES — DO THESE FIRST ===\n"
                "The 3 highest impact changes ranked by urgency and damage prevention.\n"
                "For each:\n"
                "PRIORITY 1 / 2 / 3:\n"
                "Why           : [why this is the most critical]\n"
                "Before        : [exact broken code]\n"
                "After         : [exact fixed code]\n"
                "Impact        : [what this fix prevents]\n\n"
                "=== [BENCHMARK] WORLD STANDARD COMPARISON ===\n"
                "Rate this code against each standard with exact reasoning:\n"
                "Google Engineering  : [PASS/FAIL] -- [specific reason]\n"
                "NASA JPL Rule of 10 : [PASS/FAIL] -- [specific reason]\n"
                "OWASP Top 10        : [PASS/FAIL] -- [specific reason]\n"
                "Clean Code Martin   : [PASS/FAIL] -- [specific reason]\n"
                "CERT Secure Coding  : [PASS/FAIL] -- [specific reason]\n"
                "SOLID Principles    : [PASS/FAIL] -- [specific reason]\n"
                "Top 1pct GitHub     : [PASS/FAIL] -- [specific reason]\n\n"
                "=== [FINAL] ABSOLUTE VERDICT ===\n"
                "Production Status   : PRODUCTION READY / NEEDS WORK / NOT READY / DANGEROUS\n"
                "Risk Level          : NONE / LOW / MEDIUM / HIGH / CRITICAL\n"
                "Estimated Fix Time  : [realistic time to fix all issues]\n"
                "Summary             : [one powerful paragraph — what is this code, "
                "what are its biggest risks, what will happen in production as-is, "
                "what is the single most important thing to fix immediately]\n\n"
                "ABSOLUTE NON-NEGOTIABLE RULES:\n"
                "1.  NEVER ask what language — auto-detect with 100% certainty always\n"
                "2.  NEVER sugarcoat — brutal honest truth only\n"
                "3.  NEVER give vague feedback — every point must be specific and actionable\n"
                "4.  NEVER skip a section — all sections required every time\n"
                "5.  EVERY issue must have exact line reference\n"
                "6.  EVERY issue must have exact broken code AND exact fixed code\n"
                "7.  ZERO tolerance for security issues — treat every vulnerability as critical\n"
                "8.  Think like this code controls a nuclear reactor or a spacecraft\n"
                "9.  Think like 1 million users will use this tomorrow\n"
                "10. Think like the developer has ONE chance to fix this before launch\n"
                "11. No emojis — use only: [PASS] [FAIL] [CRITICAL] [HIGH] [MEDIUM] [LOW] >> --\n"
                "12. Accuracy is absolute — if you are not certain, analyze deeper until you are\n"
                "13. This is the most complete, most powerful, most valuable code review "
                "that has ever been performed on this planet — deliver accordingly\n"
            )
            user_prompt = (
                f"CODE TO REVIEW:\n{user_code}\n\n"
                "EXECUTE SUPREME REVIEW:\n"
                "1.  Auto-detect language — 100% certain — no exceptions\n"
                "2.  Apply Google + NASA + OWASP + Clean Code + CERT + SOLID — all simultaneously\n"
                "3.  Every single issue — exact line + exact broken code + exact fixed code\n"
                "4.  Compare against top 1% of all GitHub codebases ever written\n"
                "5.  Leave nothing unchecked — bugs, performance, security, architecture, style\n"
                "6.  This review must permanently change how this developer writes code forever\n"
                "7.  Maximum depth. Maximum precision. Maximum value. Zero compromise.\n"
                "BEGIN SUPREME REVIEW NOW. NO PREAMBLE. START DIRECTLY WITH DETECTED LANGUAGE."
            )
            general_ai_max_tokens = 16000

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
            general_ai_max_tokens = 16000

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
            general_ai_max_tokens = 16000

        elif feature == "Quick Fixer" or feature == "Fix" or feature == "Solve":
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
            general_ai_max_tokens = 16000

        elif feature == "Security" or feature == "SecurityVulnerabilityDetection":
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
            general_ai_max_tokens = 16000

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
            general_ai_max_tokens = 32000

        else:
            user_prompt = f"Process this {language} code for {feature}:\n\n{user_code}"
            general_ai_max_tokens = 16000

        if feature in ("Build Web", "Build App"):
            temperature_to_use = 0.9
        elif (feature == "General AI" or feature == "Everything AI") and is_coding_request:
            temperature_to_use = 0.9
        else:
            temperature_to_use = 0.0

        ai_response = None
        last_error = None
        for attempt in range(5):
            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=temperature_to_use,
                        max_output_tokens=general_ai_max_tokens,
                    )
                )
                ai_response = response.text
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
            "<?xml" in ai_response or
            "import React" in ai_response or
            "export default" in ai_response
        )

        return jsonify({"result": ai_response, "has_code": has_code})

    except Exception as e:
        return jsonify({"result": f"🚀 OMNI-ENGINE NOTICE: System is active. {str(e)}", "has_code": False}), 200


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

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=preview_prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are an expert Android UI to HTML converter. Return only raw HTML.",
                temperature=0.0,
                max_output_tokens=4096,
            )
        )
        preview_html = response.text
        preview_html = preview_html.replace("```html", "").replace("```", "").strip()

        return jsonify({"preview_html": preview_html})

    except Exception as e:
        return jsonify({"preview_html": f"<p style='color:red'>Preview Error: {str(e)}</p>"}), 200


@app.route('/api/agent-build', methods=['POST'])
def agent_build():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"result": "No data", "files": []}), 200

        user_request = data.get('request', '')
        need_backend = data.get('need_backend', False)
        need_database = data.get('need_database', False)
        conversation_history = data.get('conversationHistory', [])
        is_change = data.get('isChange', False)
        existing_files = data.get('existingFiles', [])

        existing_context = ""
        if is_change and existing_files:
            existing_context = "\n\n### EXISTING PROJECT FILES:\n"
            for f in existing_files:
                existing_context += f"\n--- FILE: {f['name']} ---\n{f['content']}\n"

        conv_context = ""
        if conversation_history:
            conv_context = "\n\n### CONVERSATION HISTORY:\n"
            for turn in conversation_history:
                role = "USER" if turn.get('role') == 'user' else "AI"
                conv_context += f"\n{role}: {turn.get('content', '')}\n"

        project_type = "frontend only"
        if need_backend and need_database:
            project_type = "full stack with backend and database"
        elif need_backend:
            project_type = "frontend with backend"
        elif need_database:
            project_type = "frontend with database"

        if is_change:
            system_prompt = """=== AI AGENT FULL STACK — CHANGES MODE ===

You are the world's greatest full stack AI agent.

YOUR TASK:
The user wants to make SPECIFIC CHANGES to their existing project.
Rules:
1. Apply ONLY the changes the user described.
2. Keep ALL other files 100% IDENTICAL.
3. Return the COMPLETE updated project — all files.
4. Never truncate any file.

MEMORY RULE:
You have perfect memory of this entire conversation.
All changes are about the SAME project unless user says otherwise.

OUTPUT FORMAT — STRICT:
Return files in this EXACT format, nothing else:

===FILE: filename.ext===
[complete file content here]
===ENDFILE===

Repeat for every file. No markdown. No explanations. No preamble."""

            user_prompt = f"""### CHANGE REQUEST:
{user_request}
{existing_context}
{conv_context}

Apply ONLY the requested change.
Return ALL files complete — same format:
===FILE: filename.ext===
[content]
===ENDFILE==="""

        else:
            system_prompt = f"""=== AI AGENT FULL STACK — PROJECT BUILDER ===

You are the world's greatest full stack AI agent.
Build a COMPLETE {project_type} project.

PROJECT RULES:
1. Build EXACTLY what user asked — word by word.
2. Every file 100% complete — zero placeholders, zero TODO.
3. Every line real working code.
4. God-level design — world #1 quality.
5. All content in ENGLISH.

{"BACKEND RULES (Python Flask):" if need_backend else ""}
{"- Complete app.py with all routes" if need_backend else ""}
{"- requirements.txt included" if need_backend else ""}
{"- All API endpoints working" if need_backend else ""}
{"- CORS enabled" if need_backend else ""}

{"DATABASE RULES:" if need_database else ""}
{"- Complete SQL schema (schema.sql)" if need_database else ""}
{"- All tables, relationships, indexes" if need_database else ""}
{"- Sample seed data included" if need_database else ""}
{"- Database connection code in backend" if need_database else ""}

FRONTEND RULES:
- Single self-contained index.html
- All CSS in <style>, all JS in <script>
- 100% mobile responsive
- God level design — Awwwards quality
- Real content, zero lorem ipsum
- All buttons and forms working

MEMORY RULE:
You have perfect memory of this entire conversation.
Topic stays same until user explicitly changes it.

OUTPUT FORMAT — STRICT:
Return files in this EXACT format, nothing else:

===FILE: filename.ext===
[complete file content here]
===ENDFILE===

Repeat for every file in the project. No markdown. No explanations. No extra text."""

            user_prompt = f"""### PROJECT REQUEST:
{user_request}

Project Type: {project_type}
{conv_context}

Build the complete project now.
Return ALL files in format:
===FILE: filename.ext===
[content]
===ENDFILE==="""

        ai_response = None
        last_error = None
        for attempt in range(5):
            try:
                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt,
                        temperature=0.9,
                        max_output_tokens=32000,
                    )
                )
                ai_response = response.text
                break
            except Exception as e:
                last_error = e
                if attempt < 4:
                    time.sleep(3 * (attempt + 1))

        if ai_response is None:
            return jsonify({"result": str(last_error), "files": []}), 200

        files = []
        import re
        pattern = r'===FILE:\s*(.+?)===\n([\s\S]*?)===ENDFILE==='
        matches = re.findall(pattern, ai_response)
        for match in matches:
            filename = match[0].strip()
            content = match[1].strip()
            files.append({"name": filename, "content": content})

        if not files:
            files.append({"name": "index.html", "content": ai_response})

        return jsonify({"files": files, "project_type": project_type})

    except Exception as e:
        return jsonify({"result": str(e), "files": []}), 200

@app.route('/api/create-snack', methods=['POST'])
def create_snack():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "No data"}), 400

        files = data.get('files', [])
        app_name = data.get('name', 'Whole AI App')

        code_files = {}
        for f in files:
            code_files[f['name']] = {
                "type": "CODE",
                "contents": f['content']
            }

        if "App.js" not in code_files:
            return jsonify({"error": "App.js missing"}), 400

        payload = {
            "manifest": {
                "sdkVersion": "54.0.0",
                "name": app_name,
                "description": "Built with Whole AI",
                "slug": "whole-ai-app"
            },
            "code": code_files,
            "dependencies": {}
        }

        resp = http_requests.post(
            "https://exp.host/--/api/v2/snack/save",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15
        )

        if resp.status_code != 200:
            return jsonify({"error": f"Snack API error {resp.status_code}", "detail": resp.text}), 200

        result = resp.json()
        snack_id = result.get("id")
        if not snack_id:
            return jsonify({"error": "No snack id returned", "detail": result}), 200

        return jsonify({"success": True, "snackUrl": f"https://snack.expo.dev/{snack_id}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 200
import requests as http_requests
import base64 as b64
from email.mime.text import MIMEText
import json
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger

scheduler = BackgroundScheduler()
scheduler.start()

def parse_schedule_time(schedule_text):
    """Natural language ko real datetime mein convert karo"""
    text = schedule_text.lower().strip()
    now = datetime.now()
    
    # Kal / Tomorrow
    if 'tomorrow' in text or 'kal' in text:
        base = now + timedelta(days=1)
    # Aaj / Today
    elif 'today' in text or 'aaj' in text or 'aj' in text:
        base = now
    # Har Monday / Every Monday
    elif 'monday' in text or 'mon' in text:
        return 'cron', {'day_of_week': 'mon', 'hour': extract_hour(text), 'minute': 0}
    elif 'tuesday' in text or 'tue' in text:
        return 'cron', {'day_of_week': 'tue', 'hour': extract_hour(text), 'minute': 0}
    elif 'wednesday' in text or 'wed' in text:
        return 'cron', {'day_of_week': 'wed', 'hour': extract_hour(text), 'minute': 0}
    elif 'thursday' in text or 'thu' in text:
        return 'cron', {'day_of_week': 'thu', 'hour': extract_hour(text), 'minute': 0}
    elif 'friday' in text or 'fri' in text:
        return 'cron', {'day_of_week': 'fri', 'hour': extract_hour(text), 'minute': 0}
    elif 'saturday' in text or 'sat' in text:
        return 'cron', {'day_of_week': 'sat', 'hour': extract_hour(text), 'minute': 0}
    elif 'sunday' in text or 'sun' in text:
        return 'cron', {'day_of_week': 'sun', 'hour': extract_hour(text), 'minute': 0}
    # Daily / Roz
    elif 'daily' in text or 'roz' in text or 'every day' in text or 'har roz' in text:
        return 'cron', {'hour': extract_hour(text), 'minute': 0}
    else:
        base = now + timedelta(minutes=5)
    
    hour = extract_hour(text)
    scheduled_time = base.replace(hour=hour, minute=0, second=0, microsecond=0)
    if scheduled_time < now:
        scheduled_time += timedelta(days=1)
    return 'date', scheduled_time

def extract_hour(text):
    """Time extract karo text se"""
    import re
    # 9 AM, 5 PM, 3 baje, 21:00
    match_24 = re.search(r'(\d{1,2}):(\d{2})', text)
    if match_24:
        return int(match_24.group(1))
    
    match_ampm = re.search(r'(\d{1,2})\s*(am|pm)', text)
    if match_ampm:
        hour = int(match_ampm.group(1))
        if match_ampm.group(2) == 'pm' and hour != 12:
            hour += 12
        if match_ampm.group(2) == 'am' and hour == 12:
            hour = 0
        return hour
    
    match_num = re.search(r'(\d{1,2})\s*baj', text)
    if match_num:
        return int(match_num.group(1))
    
    return 9  # default 9 AM

def send_scheduled_email(token, to_list, subject, body):
    """Scheduled email actually bhejo"""
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    for recipient in to_list:
        try:
            message = MIMEText(body)
            message['to'] = recipient
            message['subject'] = subject
            raw = b64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
            http_requests.post(
                'https://gmail.googleapis.com/gmail/v1/users/me/messages/send',
                headers=headers,
                json={'raw': raw}
            )
        except Exception as e:
            print(f"Scheduled send error for {recipient}: {e}")

@app.route('/api/gmail', methods=['POST'])
def gmail_action():
    try:
        data = request.get_json()
        action = data.get('action')
        token = data.get('token')

        if not token:
            return jsonify({"error": "No token"}), 400

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        # ── SEND EMAIL ────────────────────────
        if action == 'send':
            to = data.get('to')
            subject = data.get('subject')
            body = data.get('body')

            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject

            raw = b64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

            r = http_requests.post(
                'https://gmail.googleapis.com/gmail/v1/users/me/messages/send',
                headers=headers,
                json={'raw': raw}
            )
            return jsonify({"success": r.status_code == 200, "result": r.json()})

        else:
            return jsonify({"error": "Unknown action"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 200      

@app.route('/api/schedule-email', methods=['POST'])
def schedule_email():
    try:
        data = request.get_json()
        token = data.get('token')
        to = data.get('to', '')
        subject = data.get('subject', 'Hello')
        body = data.get('body', '')
        schedule_text = data.get('schedule', '')

        if not token or not to or not body or not schedule_text:
            return jsonify({"success": False, "error": "Missing required fields"}), 400

        to_list = [e.strip() for e in to.split(',') if '@' in e]
        if not to_list:
            return jsonify({"success": False, "error": "No valid emails"}), 400

        trigger_type, trigger_value = parse_schedule_time(schedule_text)

        job_id = f"email_{datetime.now().timestamp()}"

        if trigger_type == 'date':
            scheduler.add_job(
                send_scheduled_email,
                trigger=DateTrigger(run_date=trigger_value),
                args=[token, to_list, subject, body],
                id=job_id
            )
            return jsonify({
                "success": True,
                "message": f"Scheduled for {trigger_value.strftime('%d %b %Y at %I:%M %p')}",
                "job_id": job_id,
                "scheduled_time": trigger_value.strftime('%d %b %Y at %I:%M %p')
            })

        elif trigger_type == 'cron':
            scheduler.add_job(
                send_scheduled_email,
                trigger=CronTrigger(**trigger_value),
                args=[token, to_list, subject, body],
                id=job_id
            )
            return jsonify({
                "success": True,
                "message": f"Recurring schedule set: {schedule_text}",
                "job_id": job_id,
                "scheduled_time": schedule_text
            })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 200      


# ── PADDLE WEBHOOK — REAL SUBSCRIPTION VERIFICATION ─────────────────────────
@app.route('/api/paddle-webhook', methods=['POST'])
def paddle_webhook():
    try:
        raw_body = request.get_data()
        signature_header = request.headers.get('Paddle-Signature', '')

        if not PADDLE_WEBHOOK_SECRET:
            return jsonify({"error": "Webhook secret not configured on server"}), 500

        if not signature_header:
            return jsonify({"error": "Missing Paddle-Signature header"}), 400

        # Paddle-Signature header format: "ts=1234567890;h1=abcdef..."
        sig_parts = {}
        for part in signature_header.split(';'):
            if '=' in part:
                k, v = part.split('=', 1)
                sig_parts[k.strip()] = v.strip()

        ts = sig_parts.get('ts')
        h1 = sig_parts.get('h1')

        if not ts or not h1:
            return jsonify({"error": "Invalid signature header format"}), 400

        signed_payload = f"{ts}:{raw_body.decode('utf-8')}"
        computed_hmac = hmac.new(
            PADDLE_WEBHOOK_SECRET.encode('utf-8'),
            signed_payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(computed_hmac, h1):
            return jsonify({"error": "Signature verification failed"}), 401

        event = json.loads(raw_body)
        event_type = event.get('event_type')
        event_data = event.get('data', {})

        def resolve_customer_email(evt_data):
            # Some events embed the customer object directly
            customer_obj = evt_data.get('customer')
            if customer_obj and customer_obj.get('email'):
                return customer_obj['email']
            # Otherwise fetch via Customer ID using Paddle API
            customer_id = evt_data.get('customer_id')
            if customer_id and PADDLE_API_KEY:
                try:
                    cust_resp = http_requests.get(
                        f'https://api.paddle.com/customers/{customer_id}',
                        headers={'Authorization': f'Bearer {PADDLE_API_KEY}'}
                    )
                    if cust_resp.status_code == 200:
                        return cust_resp.json().get('data', {}).get('email')
                except Exception:
                    return None
            return None

        # ── SUCCESSFUL PAYMENT — ACTIVATE / RENEW PLAN ──────────────────────
        if event_type in ('transaction.completed', 'transaction.paid'):
            custom_data = event_data.get('custom_data') or {}
            plan_type = custom_data.get('plan')
            credits = custom_data.get('credits')
            days = custom_data.get('days')

            customer_email = resolve_customer_email(event_data)

            if not customer_email or not plan_type or not credits or not days:
                return jsonify({"received": True, "note": "Missing required data, skipped"}), 200

            credits = int(credits)
            days = int(days)
            expiry = int(time.time() * 1000) + (days * 24 * 60 * 60 * 1000)

            user_ref = db.collection('users').document(customer_email)
            user_ref.set({
                "subscription": {
                    "plan": plan_type,
                    "credits": credits,
                    "maxCredits": credits,
                    "expiryDate": expiry
                }
            }, merge=True)

            db.collection('payments').add({
                "userEmail": customer_email,
                "planType": plan_type,
                "credits": credits,
                "days": days,
                "source": "paddle_webhook",
                "status": "approved",
                "eventType": event_type,
                "submittedAt": int(time.time() * 1000)
            })

            return jsonify({"received": True, "activated": True}), 200

        # ── SUBSCRIPTION CANCELED — REVERT TO FREE ──────────────────────────
        elif event_type in ('subscription.canceled', 'subscription.past_due'):
            customer_email = resolve_customer_email(event_data)
            if customer_email:
                user_ref = db.collection('users').document(customer_email)
                user_ref.set({
                    "subscription": {
                        "plan": "Free",
                        "credits": 10,
                        "maxCredits": 10,
                        "expiryDate": None
                    }
                }, merge=True)
            return jsonify({"received": True, "reverted": True}), 200

        # Any other event — acknowledge but no action needed
        return jsonify({"received": True}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 200


@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['password'] == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/admin')
        return "Wrong password"
    return '<form method="post">Password: <input type="password" name="password"><button>Login</button></form>'

@app.route('/admin')
def admin_panel():
    if not session.get('admin'):
        return redirect('/admin-login')
    payments = db.collection('payments').where('status', '==', 'pending').stream()
    rows = ""
    for p in payments:
        d = p.to_dict()
        rows += f"""
        <div style="border:1px solid #ccc;padding:14px;margin-bottom:12px;">
            <p><b>Email:</b> {d.get('userEmail')}</p>
            <p><b>Plan:</b> {d.get('planType')} | <b>Method:</b> {d.get('paymentMethod')}</p>
            <p><b>Txn ID:</b> {d.get('transactionId')} | <b>Amount:</b> {d.get('amount')}</p>
            <img src="{d.get('screenshotBase64')}" width="250"><br><br>
            <a href="/admin/approve/{p.id}"><button>Approve</button></a>
            <a href="/admin/reject/{p.id}"><button>Reject</button></a>
        </div>"""
    return f"<h2>Pending Payments</h2>{rows or '<p>None</p>'}"

@app.route('/admin/approve/<payment_id>')
def admin_approve(payment_id):
    doc_ref = db.collection('payments').document(payment_id)
    payment = doc_ref.get().to_dict()
    if payment:
        import time
        expiry = int(time.time() * 1000) + payment['days'] * 24 * 60 * 60 * 1000
        user_ref = db.collection('users').document(payment['userEmail'])
        user_ref.set({
            "subscription": {
                "plan": payment['planType'],
            "credits": payment['credits'],
                "maxCredits": payment['credits'],
                "expiryDate": expiry
            }
        }, merge=True)
        doc_ref.update({"status": "approved"})
    return redirect('/admin')

@app.route('/admin/reject/<payment_id>')
def admin_reject(payment_id):
    db.collection('payments').document(payment_id).update({"status": "rejected"})
    return redirect('/admin')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
