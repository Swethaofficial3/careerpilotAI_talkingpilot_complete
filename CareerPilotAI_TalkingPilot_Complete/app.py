from flask import Flask, render_template, request, jsonify, session
import random
app = Flask(__name__)
app.secret_key = "change-this-secret-key-for-production"

CAREER_OPTIONS = {
 "10th": ["Intermediate / Higher Secondary", "MPC", "BiPC", "CEC", "MEC", "MBiPC", "HEC", "ITI", "Polytechnic / Diploma", "Agriculture", "Vocational course", "Skill-based course", "Other"],
 "Intermediate / 12th": ["Engineering", "CSE", "AI & ML", "Data Science", "ECE", "EEE", "Mechanical", "Civil", "IT", "MBBS", "BDS", "Nursing", "Pharmacy", "Physiotherapy", "Allied Health Sciences", "B.Com", "CA", "CMA", "CS", "BBA", "Finance", "Banking", "Entrepreneurship", "BA", "Psychology", "Journalism", "Literature", "Law / LLB", "Government jobs", "Defence", "Civil services", "Teaching", "Sports", "Aviation", "Hotel Management", "Tourism", "Agriculture", "Acting", "Modelling", "Fashion", "Animation", "Graphic Design", "UI/UX", "Photography", "Content Creation", "Film & Media", "Other"],
 "Diploma": ["Engineering degree", "AI & ML", "Data Science", "IT jobs", "Government jobs", "Entrepreneurship", "Higher studies", "Other"],
 "Undergraduate": ["Software Developer", "AI/ML Engineer", "Data Analyst", "Cybersecurity", "Higher studies", "Government jobs", "Business", "Acting / Modelling", "Design", "Teaching", "Other"],
 "Postgraduate": ["Research", "AI/ML Engineer", "Data Scientist", "Management", "Teaching", "Government jobs", "Business", "Other"],
 "Working professional": ["Career switch", "Promotion", "Higher studies", "Entrepreneurship", "Other"],
 "Other": ["Other"]
}
INTERESTS = ["Technology","Artificial Intelligence","Data","Design","Movies & Acting","Social Media","Business","Finance","Psychology","Healthcare","Science","Writing","Communication","Teaching","Aviation","Agriculture","Sports","Music","Photography","Gaming"]
SKILLS = ["Python","Java","HTML","CSS","JavaScript","Communication","Leadership","Creativity","Problem Solving","Mathematics","Drawing","Public Speaking","Teamwork","Writing"]
QUESTION_BANK = {
 "technology": [
  ("Which Python type stores key-value pairs?", ["list","tuple","dictionary","set"], 2, "A dictionary stores data as key-value pairs."),
  ("What does HTML mainly define?", ["Page structure","Database tables","Network speed","Image editing"], 0, "HTML describes the structure and content of a web page."),
  ("Which is a good first step when debugging?", ["Guess randomly","Read the error and reproduce it","Delete the project","Ignore the issue"], 1, "Reproducing and understanding the error helps you find its cause."),
  ("What does AI stand for?", ["Automated Internet","Artificial Intelligence","Applied Interface","Advanced Input"], 1, "AI stands for Artificial Intelligence."),
  ("Which approach breaks a big problem into smaller parts?", ["Decomposition","Decoration","Duplication","Compression"], 0, "Decomposition makes complex problems easier to solve."),
  ("Which is commonly used to style web pages?", ["CSS","SQL","SMTP","CSV"], 0, "CSS controls layout, colours, spacing and visual presentation."),
  ("What is a variable used for?", ["Store a value","Clean a screen","Connect a cable","Print a book"], 0, "Variables name values that a program can use."),
  ("Which data structure is ordered and changeable in Python?", ["tuple","list","string only","None"], 1, "Python lists are ordered and mutable."),
  ("What is a model in machine learning?", ["A learned pattern used for predictions","A monitor","A folder name","A keyboard shortcut"], 0, "A trained model uses patterns learned from data to make predictions."),
  ("Why test software?", ["To find defects and check behaviour","To make files larger","To avoid planning","To remove all comments"], 0, "Testing checks whether software behaves as expected.")
 ],
 "business": [
  ("A product costs ₹800 and has a 10% discount. What is the sale price?", ["₹720","₹790","₹700","₹880"], 0, "10% of ₹800 is ₹80, so the sale price is ₹720."),
  ("What should you do before launching a product?", ["Understand customer needs","Ignore feedback","Set a random price","Avoid research"], 0, "Customer research helps validate whether a product solves a real problem."),
  ("Revenue is ₹5,000 and costs are ₹3,200. What is profit?", ["₹1,800","₹8,200","₹3,200","₹2,000"], 0, "Profit equals revenue minus costs: ₹5,000 − ₹3,200 = ₹1,800."),
  ("Which is an example of clear communication?", ["Using simple, specific language","Using confusing jargon","Avoiding questions","Changing the topic"], 0, "Clear and specific language reduces misunderstandings."),
  ("A customer reports a problem. What is the best first response?", ["Listen and clarify","Blame them","Ignore them","Promise anything"], 0, "Listen carefully and clarify the issue before proposing a solution."),
  ("What is a budget?", ["A plan for income and spending","A logo","A sales slogan","A job title"], 0, "A budget plans expected income and expenses."),
  ("What does teamwork require?", ["Shared goals and communication","Working against teammates","Hiding updates","Avoiding responsibility"], 0, "Teamwork depends on coordination and communication."),
  ("What can feedback help improve?", ["A product or service","Nothing ever","Only the colour","Only the price"], 0, "Feedback reveals what is working and what needs improvement."),
  ("Which is a useful way to compare options?", ["Compare costs, benefits and risks","Choose blindly","Use rumours only","Ignore requirements"], 0, "A structured comparison supports better decisions."),
  ("What is entrepreneurship?", ["Building and running a venture","Only applying for jobs","Avoiding all risks","A type of exam"], 0, "Entrepreneurship involves developing and operating a venture.")
 ],
 "healthcare": [
  ("Which organ pumps blood around the body?", ["Lungs","Heart","Kidneys","Stomach"], 1, "The heart pumps blood through the circulatory system."),
  ("Which habit supports infection prevention?", ["Hand hygiene","Sharing used needles","Ignoring cleanliness","Skipping safe practices"], 0, "Hand hygiene helps reduce the spread of many infections."),
  ("Which nutrient is the body's main quick energy source?", ["Carbohydrates","Water only","Minerals only","Fibre only"], 0, "Carbohydrates are a major energy source."),
  ("What should you do if a health situation is urgent?", ["Seek qualified emergency help","Rely only on a quiz","Wait indefinitely","Take unknown medicine"], 0, "Urgent symptoms need timely professional assessment."),
  ("Which system helps the body fight infections?", ["Immune system","Digestive system only","Skeletal system only","Hair"], 0, "The immune system helps protect the body from pathogens."),
  ("Why is accurate record keeping important in healthcare?", ["Continuity and safety of care","To hide details","To slow care","For decoration"], 0, "Accurate records support safe, coordinated care."),
  ("Which is a balanced approach to health information?", ["Use reliable sources and professionals","Trust every rumour","Self-diagnose from one post","Ignore evidence"], 0, "Reliable sources and qualified professionals help reduce misinformation."),
  ("What does hydration mean?", ["Maintaining adequate body fluids","Avoiding all water","Only eating sweets","Sleeping less"], 0, "Hydration means having enough fluid for normal body functions."),
  ("Which is a good teamwork skill in a clinic?", ["Clear handover communication","Keeping important facts secret","Guessing","Ignoring patients"], 0, "Clear handovers help team members understand care needs."),
  ("Why is observation important?", ["It helps notice changes","It replaces all training","It guarantees a diagnosis","It removes uncertainty"], 0, "Careful observation can identify changes that need further assessment.")
 ],
 "creative": [
  ("What makes a story easier to follow?", ["A clear sequence and purpose","Random unrelated scenes only","No context","Unexplained endings only"], 0, "A clear structure helps the audience follow the story."),
  ("What is a mood board used for?", ["Collecting visual inspiration","Calculating tax","Running code","Storing passwords"], 0, "Mood boards gather references for style, tone and direction."),
  ("What should a designer consider first?", ["The audience and problem","Only personal preference","Random effects","File size only"], 0, "Design decisions should respond to audience needs and goals."),
  ("Which is a useful way to improve a draft?", ["Get feedback and revise","Never review it","Add complexity everywhere","Ignore the brief"], 0, "Feedback and revision improve clarity and fit."),
  ("What is contrast in visual design?", ["Difference that helps elements stand out","Making everything identical","Removing all spacing","A file type"], 0, "Contrast creates visual distinction and hierarchy."),
  ("What does copyright generally protect?", ["Original creative expression","Every idea ever imagined","All facts","Every common word"], 0, "Copyright generally protects original expression, subject to applicable law."),
  ("What helps a presentation stay engaging?", ["Clear message and relevant visuals","Tiny text on every slide","Unrelated images","No structure"], 0, "A clear message and purposeful visuals help the audience stay engaged."),
  ("What is a useful creative habit?", ["Practise, reflect and iterate","Wait for perfect inspiration","Avoid learning","Copy without understanding"], 0, "Regular practice and iteration help creative skills grow."),
  ("What is storytelling?", ["Communicating through a connected narrative","Only listing random facts","A spreadsheet formula","A network protocol"], 0, "Storytelling connects events or ideas into a meaningful narrative."),
  ("Why should creators consider accessibility?", ["More people can use and understand the work","It removes creativity","It is never useful","It only changes file names"], 0, "Accessible work can be used by people with a wider range of needs.")
 ],
 "general": [
  ("If all roses are flowers, which statement must be true?", ["All flowers are roses","All roses are flowers","No roses are flowers","All plants are roses"], 1, "This repeats the given relationship without reversing it."),
  ("What is the next number: 2, 4, 8, 16, ...?", ["18","24","32","30"], 2, "Each number is multiplied by 2."),
  ("Which is the best way to solve a complex task?", ["Break it into smaller steps","Avoid starting","Guess every answer","Ignore constraints"], 0, "Smaller steps make planning and checking easier."),
  ("A meeting starts at 10:15 and lasts 45 minutes. When does it end?", ["10:45","11:00","11:15","11:30"], 1, "45 minutes after 10:15 is 11:00."),
  ("Which is a reliable way to learn a new skill?", ["Practice and use feedback","Read one title only","Avoid questions","Never review"], 0, "Practice with feedback supports improvement."),
  ("What should you do when instructions are unclear?", ["Ask a focused clarifying question","Pretend to understand","Delete the work","Blame someone"], 0, "Clarifying questions reduce mistakes."),
  ("Which is an example of critical thinking?", ["Check evidence before deciding","Believe the first claim","Ignore alternatives","Follow rumours"], 0, "Critical thinking examines evidence and alternatives."),
  ("A team has 4 members and each completes 3 tasks. How many tasks total?", ["7","12","16","4"], 1, "Four people times three tasks each equals twelve tasks."),
  ("What does a goal help you do?", ["Focus effort and measure progress","Guarantee success instantly","Avoid all planning","Replace practice"], 0, "Goals provide direction and a way to track progress."),
  ("Which quality helps when a plan changes?", ["Adaptability","Refusing all changes","Hiding information","Giving up immediately"], 0, "Adaptability helps people respond constructively to new conditions.")
 ]
}

@app.route("/")
def home():
    return render_template("index.html", interests=INTERESTS, skills=SKILLS, education_levels=list(CAREER_OPTIONS.keys()))

@app.route("/career-options")
def career_options():
    level = request.args.get("level", "Other")
    return jsonify(CAREER_OPTIONS.get(level, CAREER_OPTIONS["Other"]))

@app.route("/questions", methods=["POST"])
def questions():
    data = request.get_json(force=True)
    interest = " ".join(data.get("interests", [])).lower()
    path = str(data.get("career_path", "")).lower()
    if any(k in interest + " " + path for k in ["technology","ai","data","python","engineer","computer","software"]):
        key = "technology"
    elif any(k in interest + " " + path for k in ["business","finance","commerce","management","entrepreneur","b.com","bba"]):
        key = "business"
    elif any(k in interest + " " + path for k in ["health","medical","mbbs","nursing","biology","pharmacy"]):
        key = "healthcare"
    elif any(k in interest + " " + path for k in ["design","acting","model","movie","creative","fashion","media","photography","music"]):
        key = "creative"
    else:
        key = "general"
    session["question_key"] = key
    chosen = QUESTION_BANK[key][:]
    random.shuffle(chosen)
    session["questions"] = [{"q":q,"options":opts,"answer":ans,"explanation":exp} for q,opts,ans,exp in chosen[:10]]
    return jsonify([{"q":q,"options":opts} for q,opts,ans,exp in chosen[:10]])

@app.route("/submit-test", methods=["POST"])
def submit_test():
    data = request.get_json(force=True)
    questions = session.get("questions", [])
    answers = data.get("answers", [])
    wrong, correct = [], 0
    for i, q in enumerate(questions):
        picked = answers[i] if i < len(answers) else None
        if picked == q["answer"]:
            correct += 1
        else:
            wrong.append({"number":i+1,"question":q["q"],"your_answer":q["options"][picked] if isinstance(picked,int) and 0 <= picked < len(q["options"]) else "Not answered","correct_answer":q["options"][q["answer"]],"explanation":q["explanation"]})
    total = len(questions) or 10
    score = round(correct / total * 100)
    result = {"correct":correct,"wrong_count":len(wrong),"score":score,"wrong":wrong,"strength":"Problem solving" if score >= 70 else "Curiosity and willingness to learn","gap":"Review missed concepts" if wrong else "Try a more advanced challenge","readiness":min(95, 45+score//2)}
    session["last_result"] = result
    return jsonify(result)

@app.route("/assistant", methods=["POST"])
def assistant():
    data = request.get_json(force=True)
    msg = str(data.get("message","")).strip().lower()
    name = str(data.get("name","friend")).strip() or "friend"
    if any(x in msg for x in ["python","coding","program"]):
        reply = "Let's start small, " + name + "! Practise variables, conditions, loops and functions, then solve one tiny problem each day. Would you like a beginner exercise?"
    elif any(x in msg for x in ["job","career","role","future"]):
        reply = "We can explore your options together, " + name + ". Compare what interests you, what skills each path needs, and try a small project before making a big decision."
    elif any(x in msg for x in ["score","wrong","test","improve"]):
        reply = "Your test is a starting point, not a judgement. Review each explanation, practise the topics you missed, then try another short test to check your progress."
    elif any(x in msg for x in ["resume","cv","interview"]):
        reply = "Build proof of your skills with one clear project, explain your contribution honestly, and practise describing the problem, your approach and what you learned."
    else:
        reply = "I'm here with you, " + name + " 💙 Tell me what you're curious about, and we'll break it into simple steps. I can help with career paths, skills, projects, tests and interview preparation."
    return jsonify({"reply":reply})

if __name__ == "__main__":
    app.run(debug=True)
