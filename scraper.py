import cloudscraper
from bs4 import BeautifulSoup
import json
import time
import urllib3
import sys
import random

urllib3.disable_warnings()

competitions = {
    "IMO": range(2000, 2026),
    "USAMO": range(2000, 2026),
    "USAJMO": range(2010, 2026)
}

# EVAN CHEN MOHS DB
MOHS_DATA = {
    "IMO": {
        2000: ([10, 5, 35, 15, 15, 35], ['G', 'A', 'C', 'C', 'N', 'G']),
        2001: ([10, 20, 25, 5, 20, 25], ['G', 'A', 'C', 'A', 'G', 'A']),
        2002: ([5, 10, 35, 5, 15, 45], ['C', 'G', 'A', 'N', 'A', 'G']),
        2003: ([10, 35, 40, 10, 25, 35], ['C', 'N', 'G', 'G', 'A', 'N']),
        2004: ([5, 20, 35, 10, 20, 35], ['G', 'A', 'C', 'A', 'G', 'N']),
        2005: ([20, 10, 30, 10, 25, 35], ['G', 'A', 'A', 'N', 'G', 'C']),
        2006: ([5, 30, 35, 10, 30, 45], ['G', 'C', 'A', 'N', 'N', 'C']),
        2007: ([5, 15, 45, 5, 25, 50], ['A', 'G', 'C', 'G', 'N', 'A']),
        2008: ([10, 20, 30, 10, 15, 40], ['G', 'A', 'N', 'A', 'C', 'G']),
        2009: ([5, 15, 40, 15, 15, 45], ['N', 'G', 'A', 'G', 'A', 'C']),
        2010: ([10, 20, 40, 10, 35, 40], ['A', 'G', 'A', 'G', 'C', 'A']),
        2011: ([10, 45, 40, 5, 15, 45], ['N', 'C', 'A', 'C', 'N', 'G']),
        2012: ([5, 15, 45, 15, 25, 45], ['G', 'A', 'C', 'A', 'G', 'A']),
        2013: ([5, 20, 35, 10, 25, 45], ['N', 'C', 'G', 'G', 'A', 'C']),
        2014: ([5, 15, 40, 5, 30, 35], ['A', 'C', 'G', 'G', 'C', 'C']),
        2015: ([15, 30, 25, 15, 35, 30], ['C', 'N', 'G', 'G', 'A', 'A']),
        2016: ([15, 30, 40, 10, 25, 25], ['G', 'C', 'N', 'N', 'A', 'C']),
        2017: ([5, 40, 40, 15, 35, 40], ['N', 'A', 'C', 'G', 'C', 'N']),
        2018: ([10, 30, 40, 15, 20, 45], ['G', 'A', 'C', 'C', 'N', 'G']),
        2019: ([5, 25, 40, 10, 15, 35], ['A', 'G', 'C', 'N', 'C', 'G']),
        2020: ([10, 25, 40, 15, 20, 50], ['G', 'A', 'C', 'C', 'N', 'C']),
        2021: ([15, 45, 45, 15, 20, 35], ['A', 'A', 'G', 'G', 'C', 'A']),
        2022: ([10, 15, 40, 10, 20, 40], ['C', 'A', 'N', 'G', 'N', 'C']),
        2023: ([5, 25, 30, 10, 35, 45], ['N', 'G', 'A', 'A', 'C', 'G']),
        2024: ([5, 25, 45, 10, 35, 40], ['A', 'N', 'C', 'G', 'C', 'A']),
        2025: ([5, 20, 25, 15, 15, 50], ['C', 'G', 'N', 'N', 'A', 'C']),
    },
    "USAMO": {
        2000: ([10, 10, 15, 15, 10, 50], ['A', 'A', 'C', 'C', 'G', 'A']),
        2001: ([15, 10, 30, 5, 25, 35], ['C', 'G', 'A', 'G', 'N', 'C']),
        2002: ([5, 5, 30, 10, 10, 25], ['C', 'A', 'A', 'A', 'C', 'C']),
        2003: ([0, 25, 25, 5, 15, 35], ['N', 'G', 'A', 'G', 'A', 'C']),
        2004: ([5, 20, 35, 10, 25, 45], ['G', 'N', 'C', 'C', 'A', 'A']),
        2005: ([5, 10, 20, 0, 10, 35], ['C', 'N', 'G', 'C', 'C', 'N']),
        2006: ([5, 10, 35, 10, 35, 15], ['N', 'A', 'N', 'A', 'C', 'G']),
        2007: ([10, 15, 35, 25, 25, 35], ['A', 'G', 'C', 'C', 'N', 'G']),
        2008: ([10, 25, 35, 10, 25, 40], ['N', 'G', 'C', 'C', 'C', 'C']),
        2009: ([10, 15, 45, 10, 25, 25], ['G', 'C', 'C', 'A', 'G', 'N']),
        2010: ([5, 20, 45, 5, 15, 45], ['G', 'C', 'A', 'G', 'N', 'C']),
        2011: ([10, 15, 40, 5, 15, 10], ['A', 'C', 'G', 'N', 'G', 'C']),
        2012: ([0, 25, 35, 15, 20, 20], ['A', 'C', 'N', 'A', 'G', 'C']),
        2013: ([15, 25, 50, 10, 30, 25], ['G', 'C', 'C', 'A', 'N', 'G']),
        2014: ([10, 25, 30, 15, 25, 40], ['A', 'A', 'A', 'C', 'G', 'N']),
        2015: ([15, 15, 25, 15, 30, 30], ['N', 'G', 'C', 'C', 'N', 'A']),
        2016: ([15, 15, 45, 25, 45, 15], ['C', 'N', 'G', 'A', 'G', 'C']),
        2017: ([5, 40, 35, 10, 50, 30], ['N', 'C', 'G', 'C', 'C', 'A']),
        2018: ([10, 20, 45, 10, 25, 45], ['A', 'A', 'N', 'C', 'G', 'C']),
        2019: ([15, 25, 40, 5, 15, 25], ['A', 'G', 'N', 'C', 'N', 'A']),
        2020: ([5, 20, 40, 20, 30, 45], ['G', 'C', 'N', 'C', 'C', 'A']),
        2021: ([10, 20, 40, 10, 20, 40], ['G', 'C', 'C', 'C', 'A', 'G']),
        2022: ([25, 20, 40, 15, 35, 50], ['C', 'G', 'A', 'N', 'C', 'C']),
        2023: ([5, 25, 35, 10, 15, 35], ['G', 'A', 'C', 'N', 'C', 'G']),
        2024: ([5, 35, 40, 10, 40, 35], ['N', 'A', 'N', 'C', 'G', 'A']),
        2025: ([10, 30, 30, 5, 20, 45], ['N', 'A', 'C', 'G', 'N', 'C'])
    }
}

# THEOREM EXTRACTION DICTIONARY
THEOREM_MAP = {
    "AM-GM": ["am-gm", "arithmetic mean", "geometric mean"],
    "Cauchy-Schwarz": ["cauchy-schwarz", "cauchy", "cs inequality"],
    "Pigeonhole Principle": ["pigeonhole", "php", "dirichlet's box"],
    "LTE Lemma": ["lte", "lifting the exponent"],
    "Vieta Jumping": ["vieta jumping", "root flipping", "vieta's formulas"],
    "Chinese Remainder Theorem": ["chinese remainder", "crt"],
    "Fermat's Little Theorem": ["fermat's little", "flt"],
    "Euler's Totient Theorem": ["euler's totient", "euler's theorem"],
    "Ceva's Theorem": ["ceva's", "ceva "],
    "Menelaus's Theorem": ["menelaus"],
    "Power of a Point": ["power of a point", "pop"],
    "Ptolemy's Theorem": ["ptolemy"],
    "Jensen's Inequality": ["jensen"],
    "Hölder's Inequality": ["holder's", "hölder's"],
    "Muirhead's Inequality": ["muirhead"],
    "Principle of Inclusion-Exclusion": ["inclusion-exclusion", "pie"],
    "Shoelace Formula": ["shoelace"],
    "Newton's Sums": ["newton's sums"],
    "Bézout's Identity": ["bezout", "bézout"],
    "Dirichlet's Theorem": ["dirichlet's theorem"],
    "Hall's Marriage Theorem": ["hall's marriage", "hall's condition"],
    "Zsigmondy's Theorem": ["zsigmondy"],
    "Lucas' Theorem": ["lucas' theorem"],
    "Schur's Inequality": ["schur's"],
    "Minkowski's Theorem": ["minkowski"],
    "Desargues' Theorem": ["desargues"],
    "Pascal's Theorem": ["pascal's theorem"],
    "Radical Axis Theorem": ["radical axis"],
    "Homothety": ["homothety", "spiral similarity"],
    "Inversion": ["inversion geometry", "circle inversion"]
}

subj_map = {'A': 'Algebra', 'C': 'Combinatorics', 'G': 'Geometry', 'N': 'Number Theory'}
all_problems = []
problem_id = 1
total_pages = sum(len(years) * 6 for years in competitions.values())
pages_checked = 0

print("==================================================")
print("📚 Starting INTELLIGENT scraper with Theorems & MOHS...")
print(f"📊 Total pages to check: {total_pages}")
print("==================================================\n")

scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'darwin', 'desktop': True})


def save_progress():
    with open('problems_output.json', 'w', encoding='utf-8') as f:
        json.dump(all_problems, f, indent=4, ensure_ascii=False)


def NLP_junior_categorize(text):
    text_lower = text.lower()
    scores = {
        "Geometry": sum(text_lower.count(w) for w in ['triangle', 'circle', 'angle', 'circumcenter']),
        "Number Theory": sum(text_lower.count(w) for w in ['integer', 'prime', 'divide', 'modulo']),
        "Algebra": sum(text_lower.count(w) for w in ['real number', 'polynomial', 'function', 'inequality']),
        "Combinatorics": sum(text_lower.count(w) for w in ['grid', 'color', 'graph', 'ways', 'game'])
    }
    prob_type = max(scores, key=scores.get)
    if scores[prob_type] == 0: prob_type = "Algebra"

    tags = []
    if 'polynomial' in text_lower: tags.append('Polynomials')
    if 'function' in text_lower or 'f(x)' in text_lower: tags.append('Functional Equations')
    if 'prime' in text_lower: tags.append('Primes')
    if 'triangle' in text_lower: tags.append('Euclidean Geometry')
    if 'color' in text_lower: tags.append('Coloring')
    if 'inequality' in text_lower: tags.append('Inequalities')
    if not tags: tags.append(prob_type)
    return prob_type, tags


def extract_theorems(full_solution_text):
    """Scans the entire solution string against the Theorem Map aliases"""
    found_theorems = []
    text_lower = full_solution_text.lower()
    for theorem_name, aliases in THEOREM_MAP.items():
        for alias in aliases:
            if alias in text_lower:
                found_theorems.append(theorem_name)
                break  # Move to next theorem once found
    return found_theorems


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
                if response.status_code != 200: continue

                soup = BeautifulSoup(response.text, 'html.parser')
                content_div = soup.find('div', {'class': 'mw-parser-output'})
                if not content_div: continue

                for img in content_div.find_all('img'):
                    alt_text = img.get('alt', '')
                    if 'latex' in img.get('class', []) or '\\' in alt_text or '$' in alt_text:
                        img.replace_with(alt_text)

                statement_paras, solution_paras = [], []
                current_section = "statement"

                for child in content_div.children:
                    if child.name in ['h2', 'h3', 'h4'] and 'solution' in child.get_text().lower():
                        current_section = "solution"
                        continue
                    if child.name == 'p':
                        text = child.get_text().strip()
                        if text:
                            if current_section == "statement":
                                statement_paras.append(text)
                            elif current_section == "solution":
                                solution_paras.append(text)

                statement = "\n\n".join(statement_paras)
                if not statement or "stub" in statement.lower()[:50]: continue

                # Combine ALL solution text to aggressively hunt for theorems
                full_solution_str = " ".join(solution_paras)
                key_theorems = extract_theorems(full_solution_str)

                strategy = solution_paras[0] if solution_paras else "See official AoPS link for full solutions."
                if len(strategy) > 400: strategy = strategy[:397] + "..."

                if comp in ["IMO", "USAMO"] and year in MOHS_DATA[comp]:
                    idx = prob_num - 1
                    difficulty = f"{MOHS_DATA[comp][year][0][idx]}M"
                    prob_type = subj_map[MOHS_DATA[comp][year][1][idx]]
                    _, tags = NLP_junior_categorize(statement)
                else:
                    difficulty = "Unrated"
                    prob_type, tags = NLP_junior_categorize(statement)

                problem_data = {
                    "id": problem_id, "competition": comp, "year": year, "number": prob_num,
                    "type": prob_type, "difficulty": difficulty, "tags": tags,
                    "key_theorems": key_theorems,
                    "statement": statement, "strategy": strategy, "link": url
                }

                all_problems.append(problem_data)
                problem_id += 1
                save_progress()

                print(f"\n✅ ADDED: {comp} {year} P{prob_num} | Theorems: {len(key_theorems)}")

            except Exception as e:
                print(f"\n❌ Error on {comp} {year} P{prob_num}: {e}")

print(f"\n\n🎉 Finished! Scraped {len(all_problems)} problems with Theorems & Ratings.")