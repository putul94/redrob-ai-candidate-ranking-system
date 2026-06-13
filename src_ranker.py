import json
import csv

# =====================================================
# CONFIG
# =====================================================

FILE_NAME = r"C:\Users\hibre\OneDrive\Desktop\candidates.jsonl"
OUTPUT_FILE = r"C:\Users\hibre\OneDrive\Desktop\final_submission.csv"

# =====================================================
# KEYWORDS
# =====================================================

AI_KEYWORDS = [
    "llm",
    "rag",
    "machine learning",
    "deep learning",
    "nlp",
    "transformers",
    "prompt engineering",
    "mlops",
    "fine-tuning",
    "hugging face",
    "openai",
    "langchain"
]

RETRIEVAL_KEYWORDS = [
    "retrieval",
    "ranking",
    "recommendation",
    "search",
    "semantic search",
    "relevance",
    "vector",
    "embedding",
    "embeddings",
    "bm25",
    "elasticsearch",
    "pinecone",
    "milvus",
    "faiss"
]

PRODUCT_KEYWORDS = [
    "software",
    "technology",
    "saas",
    "internet",
    "product",
    "startup"
]

GENUINE_AI_ROLES = [
    "ai engineer",
    "ml engineer",
    "machine learning engineer",
    "data scientist",
    "applied scientist",
    "nlp engineer",
    "research engineer"
]

# =====================================================
# TEXT EXTRACTION
# =====================================================

def get_candidate_text(candidate):

    text = ""

    profile = candidate.get("profile", {})

    text += str(profile.get("headline", "")) + " "
    text += str(profile.get("summary", "")) + " "

    for job in candidate.get("career_history", []):
        text += str(job.get("title", "")) + " "
        text += str(job.get("description", "")) + " "

    skills = candidate.get("skills", [])

    for skill in skills:

        if isinstance(skill, dict):
            text += str(skill.get("name", "")) + " "
        else:
            text += str(skill) + " "

    return text.lower()

# =====================================================
# TECHNICAL SCORE
# =====================================================

def technical_score(candidate):

    text = get_candidate_text(candidate)

    hits = 0

    for keyword in AI_KEYWORDS:
        if keyword in text:
            hits += 1

    return min(hits / 8, 1.0)

# =====================================================
# RETRIEVAL SCORE
# =====================================================

def retrieval_score(candidate):

    text = get_candidate_text(candidate)

    hits = 0

    for keyword in RETRIEVAL_KEYWORDS:
        if keyword in text:
            hits += 1

    return min(hits / 6, 1.0)

# =====================================================
# PRODUCT COMPANY SCORE
# =====================================================

def product_company_score(candidate):

    history = candidate.get("career_history", [])

    score = 0

    for job in history:

        industry = str(
            job.get("industry", "")
        ).lower()

        company = str(
            job.get("company_name", "")
        ).lower()

        blob = industry + " " + company

        for keyword in PRODUCT_KEYWORDS:

            if keyword in blob:
                score += 1

    return min(score / 3, 1.0)

# =====================================================
# EXPERIENCE SCORE
# =====================================================

def experience_score(candidate):

    profile = candidate.get("profile", {})

    exp = profile.get(
        "years_of_experience",
        0
    )

    try:
        exp = float(exp)
    except:
        exp = 0

    if 5 <= exp <= 9:
        return 1.0

    elif 3 <= exp < 5:
        return 0.8

    elif 9 < exp <= 12:
        return 0.6

    else:
        return 0.2

# =====================================================
# BEHAVIOR SCORE
# =====================================================

def behavior_score(candidate):

    signals = candidate.get(
        "redrob_signals",
        {}
    )

    profile_score = (
        signals.get(
            "profile_completeness_score",
            0
        ) / 100
    )

    recruiter_response = signals.get(
        "recruiter_response_rate",
        0
    )

    interview_completion = signals.get(
        "interview_completion_rate",
        0
    )

    saved = min(
        signals.get(
            "saved_by_recruiters_30d",
            0
        ) / 20,
        1
    )

    open_to_work = 1 if signals.get(
        "open_to_work_flag",
        False
    ) else 0

    return (
        profile_score
        + recruiter_response
        + interview_completion
        + saved
        + open_to_work
    ) / 5

# =====================================================
# LOCATION SCORE
# =====================================================

def location_score(candidate):

    profile = candidate.get("profile", {})
    signals = candidate.get("redrob_signals", {})

    score = 0

    country = str(
        profile.get("country", "")
    ).lower()

    if country == "india":
        score += 0.5

    if signals.get(
        "willing_to_relocate",
        False
    ):
        score += 0.5

    return score

# =====================================================
# SKILL STUFFING PENALTY
# =====================================================

def stuffing_penalty(candidate):

    text = get_candidate_text(candidate)

    ai_hits = 0

    for keyword in AI_KEYWORDS:
        if keyword in text:
            ai_hits += 1

    titles = []

    for job in candidate.get(
        "career_history",
        []
    ):
        titles.append(
            str(job.get("title", "")).lower()
        )

    title_text = " ".join(titles)

    genuine = False

    for role in GENUINE_AI_ROLES:

        if role in title_text:
            genuine = True

    if ai_hits >= 5 and not genuine:
        return 0.15

    return 0

# =====================================================
# FINAL SCORE
# =====================================================

def final_score(candidate):

    score = (
        0.35 * technical_score(candidate)
        + 0.20 * retrieval_score(candidate)
        + 0.15 * product_company_score(candidate)
        + 0.10 * experience_score(candidate)
        + 0.15 * behavior_score(candidate)
        + 0.05 * location_score(candidate)
    )

    score = score - stuffing_penalty(candidate)

    return round(score, 6)

# =====================================================
# REASONING
# =====================================================

def generate_reason(candidate):

    profile = candidate.get(
        "profile",
        {}
    )

    title = profile.get(
        "current_title",
        "Professional"
    )

    exp = profile.get(
        "years_of_experience",
        0
    )

    return (
        f"{title} | "
        f"{exp} years experience | "
        f"Strong AI relevance, retrieval/search exposure, "
        f"behavioral engagement and product-fit signals."
    )

# =====================================================
# LOAD DATA
# =====================================================

print("Loading dataset...")

candidates = []

with open(
    FILE_NAME,
    "r",
    encoding="utf-8"
) as file:

    for line in file:

        try:

            candidate = json.loads(line)

            candidates.append({
                "candidate_id":
                    candidate["candidate_id"],
                "score":
                    final_score(candidate),
                "reason":
                    generate_reason(candidate)
            })

        except Exception:
            pass

print(
    f"Loaded {len(candidates)} candidates"
)

# =====================================================
# SORT
# =====================================================

print("Ranking candidates...")

candidates.sort(
    key=lambda x: x["score"],
    reverse=True
)

# =====================================================
# EXPORT TOP 100
# =====================================================

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "candidate_id",
        "rank",
        "score",
        "reasoning"
    ])

    for rank, candidate in enumerate(
        candidates[:100],
        start=1
    ):

        writer.writerow([
            candidate["candidate_id"],
            rank,
            candidate["score"],
            candidate["reason"]
        ])

# =====================================================
# DISPLAY TOP 20
# =====================================================

print("\nTOP 20 CANDIDATES\n")

for rank, candidate in enumerate(
    candidates[:20],
    start=1
):

    print(
        rank,
        candidate["candidate_id"],
        candidate["score"]
    )

print("\nCompleted Successfully")
print("\nCSV Saved To:")
print(OUTPUT_FILE)