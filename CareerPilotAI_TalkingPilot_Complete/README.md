# Career Pilot AI — Talking Pilot Edition

A friendly, responsive Flask career-discovery demo with an animated pilot companion.

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Create and activate a virtual environment:
   - Windows: `python -m venv venv` then `venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv venv` then `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Start the app: `python app.py`
6. Open http://127.0.0.1:5000

## Included
- Animated welcome/boarding page with a consistent CSS-drawn pilot mascot
- Optional synthesized browser speech and optional gentle audio tone
- Education-level-specific career path options
- Interest and skill selection
- Career-area-aware 10-question quiz
- Results, wrong answers, explanations and a learning roadmap
- Friendly local doubt assistant fallback
- Browser-local streak/history tracking

## Honest limitations
This is a working educational prototype, not a validated career prediction system. The quiz selects a topic set based on the student's stated interests/path; it does not diagnose aptitude or guarantee a career outcome. The assistant is a local rule-based fallback, not a connected external LLM. Browser speech depends on device/browser voices. Progress history is stored in the browser on that device.
