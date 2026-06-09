import cloudscraper
from bs4 import BeautifulSoup
import json
import time
import urllib3
import sys
import random

urllib3.disable_warnings()

competitions = {
    "IMO": range(2000, 2027),
    "USAMO": range(2000, 2027),
    "USAJMO": range(2010, 2027)
}

all_problems = []
problem_id = 1
total_pages = sum(len(years) * 6 for years in competitions.values())
pages_checked = 0

print("==================================================")
print("🧠 Starting INTELLIGENT web scraper for AoPS...")
print(f"📊 Total pages to check: {total_pages}")
print("==================================================\n")

scraper = cloudscraper.create_scraper(
    browser={'browser': 'chrome', 'platform': 'darwin', 'desktop': True}
)


def save_progress():
    with open('problems_output.json', 'w', encoding='utf-8') as f:
        json.dump(all_problems, f, indent=4, ensure_ascii=False)


def auto_categorize(text):
    """Mini NLP Engine: Analyzes text keywords to determine Type and Tags."""
    text_lower = text.lower()

    # Keyword scoring system
    scores = {
        "Geometry": sum(text_lower.count(w) for w in
                        ['triangle', 'circle', 'angle', 'circumcenter', 'incenter', 'intersect', 'line', 'polygon',
                         'cyclic', 'tangent', 'perpendicular']),
        "Number Theory": sum(text_lower.count(w) for w in
                             ['integer', 'prime', 'divide', 'modulo', 'perfect square', 'gcd', 'coprime', 'rational',
                              'digit']),
        "Algebra": sum(text_lower.count(w) for w in
                       ['real number', 'polynomial', 'function', 'inequality', 'equation', 'roots', 'f(x)']),
        "Combinatorics": sum(text_lower.count(w) for w in
                             ['grid', 'color', 'graph', 'ways', 'game', 'player', 'subset', 'permutation', 'choose',
                              'coin', 'board'])
    }

    # Highest score wins the Category (Default to Algebra if tied at 0)
    prob_type = max(scores, key=scores.get)
    if scores[prob_type] == 0:
        prob_type = "Algebra"

        # Generate Tags based on specific keyword triggers
    tags = []
    if 'polynomial' in text_lower: tags.append('Polynomials')
    if 'function' in text_lower or 'f(x)' in text_lower: tags.append('Functional Equations')
    if 'prime' in text_lower: tags.append('Primes')
    if 'triangle' in text_lower or 'circle' in text_lower: tags.append('Euclidean Geometry')
    if 'color' in text_lower or 'grid' in text_lower: tags.append('Coloring')
    if 'inequality' in text_lower or '\\ge' in text_lower or '\\le' in text_lower or '>' in text_lower: tags.append(
        'Inequalities')
    if 'player' in text_lower or 'game' in text_lower or 'alice' in text_lower: tags.append('Combinatorial Games')
    if 'sequence' in text_lower: tags.append('Sequences')

    if not tags:
        tags.append(prob_type)  # Fallback tag

    return prob_type, tags


for comp, years in competitions.items():
    for year in years:
        for prob_num in range(1, 7):
            pages_checked += 1
            url = f"https://artofproblemsolving.com/wiki/index.php/{year}_{comp}_Problems/Problem_{prob_num}"

            sys.stdout.write(f"\r⏳ Progress: [{pages_checked}/{total_pages}] Checking {comp} {year} P{prob_num}...   ")
            sys.stdout.flush()

            try:
                time.sleep(random.uniform(1.2, 2.5))
                response = scraper.get(url, timeout=15)

                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')
                content_div = soup.find('div', {'class': 'mw-parser-output'})
                if not content_div: continue

                # FIX 1: LATEX RECOVERY
                # Find all images. If it's a math image, replace the <img> tag with its raw LaTeX alt text
                for img in content_div.find_all('img'):
                    alt_text = img.get('alt', '')
                    if 'latex' in img.get('class', []) or '\\' in alt_text or '$' in alt_text:
                        img.replace_with(alt_text)

                # FIX 2: SMART SPLITTING (Statement vs Strategy)
                statement_paras = []
                solution_paras = []
                current_section = "statement"

                # Read elements in chronological order
                for child in content_div.children:
                    # If we hit a header with "Solution", switch modes
                    if child.name in ['h2', 'h3', 'h4'] and 'solution' in child.get_text().lower():
                        current_section = "solution"
                        continue

                    if child.name == 'p':
                        text = child.get_text().strip()
                        if text:
                            if current_section == "statement":
                                statement_paras.append(text)
                            elif current_section == "solution" and len(solution_paras) < 1:
                                # Grab ONLY the very first paragraph of the solution to use as the Strategy
                                solution_paras.append(text)

                statement = "\n\n".join(statement_paras)
                if not statement or "stub" in statement.lower()[:50]:
                    continue

                # Format the Strategy
                strategy = solution_paras[0] if solution_paras else "See official AoPS link for full solutions."
                if len(strategy) > 400:
                    strategy = strategy[:397] + "..."  # Truncate if it's too long

                # FIX 3: AUTO CATEGORIZATION
                prob_type, tags = auto_categorize(statement)
                difficulty = "Easy" if prob_num in [1, 4] else "Medium" if prob_num in [2, 5] else "Hard"

                problem_data = {
                    "id": problem_id,
                    "competition": comp,
                    "year": year,
                    "number": prob_num,
                    "type": prob_type,
                    "difficulty": difficulty,
                    "tags": tags,
                    "statement": statement,
                    "strategy": strategy,
                    "link": url
                }

                all_problems.append(problem_data)
                problem_id += 1
                save_progress()

                print(f"\n✅ ADDED: {comp} {year} P{prob_num} | {prob_type} | Tags: {tags}")

            except Exception as e:
                print(f"\n❌ Error on {comp} {year} P{prob_num}: {e}")

print(f"\n\n🎉 Finished! Scraped {len(all_problems)} problems with full MathJax and Tags.")