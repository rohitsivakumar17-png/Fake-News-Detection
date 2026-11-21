import re

FAKE_NEWS_KEYWORDS = [
    "shocking",
    "you won't believe",
    "miracle",
    "secret",
    "doctor says",
    "guaranteed",
    "click here",
    "scientists stunned",
    "exposed",
    "cure",
    "unbelievable",
    "breakthrough",
    "worst",
    "best",
    "crisis",
    "truth",
    "scandal",
    "fake news",
    "conspiracy",
    "busted",
]

REAL_NEWS_KEYWORDS = [
    "report",
    "study",
    "according to",
    "announced",
    "survey",
    "official",
    "confirmed",
    "research",
    "data",
    "government",
    "policy",
    "minister",
    "scientists",
    "economy",
]

SAMPLE_ARTICLES = [
    {
        "title": "Shocking secret cure exposed by top doctor",
        "content": "A top doctor reveals a shocking secret cure that the medical industry does not want you to know."
    },
    {
        "title": "Government announces new education policy for 2026",
        "content": "The ministry announced a new education policy today designed to improve student outcomes and teacher training."
    },
    {
        "title": "You won't believe how this man made $10,000 in one day",
        "content": "A viral post claims a man made ten thousand dollars in a single day using a simple online trick."
    },
    {
        "title": "Study finds clean-air initiatives cut city pollution by 40%",
        "content": "Researchers published a report showing that targeted clean-air programs reduced pollution levels and improved public health."
    },
    {
        "title": "Experts confirm emergency response keeps hospitals ready",
        "content": "An official report confirms that the emergency response system is maintaining preparedness across city hospitals."
    },
]


def normalize_text(text: str) -> str:
    return re.sub(r"[^a-z0-9\s]", "", text.lower())


def score_article(title: str, content: str) -> dict:
    text = normalize_text(title + " " + content)
    fake_score = 0
    real_score = 0

    for keyword in FAKE_NEWS_KEYWORDS:
        if keyword in text:
            fake_score += 1

    for keyword in REAL_NEWS_KEYWORDS:
        if keyword in text:
            real_score += 1

    # Extra risk for aggressive claims, clickbait style, and all-caps text in the original title
    if title.isupper() and len(title) > 10:
        fake_score += 2
    if re.search(r"\b(you|your) won't believe\b", text):
        fake_score += 2
    if re.search(r"\b(guaranteed|miracle|cure|secret)\b", text):
        fake_score += 1

    total_signals = fake_score + real_score
    if total_signals == 0:
        confidence = 0.5
    else:
        confidence = fake_score / total_signals

    verdict = "Fake or Suspicious" if confidence >= 0.6 else "Likely Real"

    return {
        "fake_score": fake_score,
        "real_score": real_score,
        "confidence": round(confidence, 2),
        "verdict": verdict,
    }


def analyze_articles(articles):
    results = []
    for article in articles:
        result = score_article(article["title"], article["content"])
        results.append({
            "title": article["title"],
            "content": article["content"],
            **result,
        })
    return results


import argparse


def print_analysis(results):
    print("Fake News Detection Report")
    print("""==============================================================""")
    for index, item in enumerate(results, start=1):
        print(f"Article {index}: {item['title']}")
        print(f"  Verdict: {item['verdict']}")
        print(f"  Fake score: {item['fake_score']}")
        print(f"  Real score: {item['real_score']}")
        print(f"  Confidence of fake news: {item['confidence'] * 100:.0f}%")
        print(f"  Excerpt: {item['content'][:80]}...")
        print("""--------------------------------------------------------------""")


def classify_one_article(title: str, content: str):
    result = score_article(title, content)
    print("Fake News Check")
    print("""==============================================================""")
    print(f"Title: {title}")
    print(f"Verdict: {result['verdict']}")
    print(f"Fake score: {result['fake_score']}")
    print(f"Real score: {result['real_score']}")
    print(f"Confidence of fake news: {result['confidence'] * 100:.0f}%")
    print(f"Excerpt: {content[:120]}...")
    print("""--------------------------------------------------------------""")
    return result


def prompt_and_classify():
    print("Enter news text to check. Leave the title blank to exit.")

    while True:
        title = input("Title: ").strip()
        if not title:
            print("Exiting news checker.")
            break

        content = input("Content: ").strip()
        if not content:
            print("Please provide the article content. Try again.\n")
            continue

        classify_one_article(title, content)


def main():
    parser = argparse.ArgumentParser(description="Simple fake news checker")
    parser.add_argument("--sample", action="store_true", help="Run the built-in sample articles instead of interactive mode")
    args = parser.parse_args()

    if args.sample:
        results = analyze_articles(SAMPLE_ARTICLES)
        print_analysis(results)
    else:
        prompt_and_classify()


if __name__ == "__main__":
    main()
