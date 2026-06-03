#!/usr/bin/env python3
"""
IA Business Solutions - Systeme de Prospection Automatisee
Genere des leads qualifies et envoie des emails personnalises.
"""
import smtplib, ssl, os, json, random, time, csv, re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import List, Dict

# ============================================================
# CONFIG
# ============================================================
SENDER_NAME = "Dominiqk Mendy"
SENDER_EMAIL = "dominiqk29@gmail.com"
APP_PASSWORD_PATH = "~/.config/himalaya/.app_password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

DAILY_LIMIT = 200
MIN_INTERVAL = 90   # seconds between emails
MAX_INTERVAL = 180

# ============================================================
# EMAIL TEMPLATES (A/B/C)
# ============================================================

TEMPLATES = {
    "A_short": {
        "subjects": [
            "{company} => 3h pour transformer votre {department} avec l'IA",
            "Question rapide pour {company} (entreprises {sector})",
            "{first_name}, votre concurrent utilise deja l'IA",
        ],
        "body": """Bonjour {first_name},

Je me presente : Dominiqk Mendy, consultant IA avec +18 ans d'experience.
J'accompagne des entreprises {sector} comme {company} a automatiser leurs processus cles.

Resultat moyen : +300% de productivite, -70% de couts operationnels.

Exemple concret : j'ai recemment automatise la gestion des demandes clients pour une entreprise similaire => 80% des demandes traitees instantanement par un agent IA.

Seriez-vous disponible pour un appel de 15 minutes cette semaine ?
=> https://ai.dominiqkmendy.com

Bien a vous,
Dominiqk Mendy
+212 607 798 670
Expert IA & Transformation Digitale"""
    },
    "B_value": {
        "subjects": [
            "{company} : combien vous coute l'absence d'IA ?",
            "Etude de cas IA pour {sector} - ROI en 30 jours",
            "Peut-etre deja vu, mais pas par moi : votre {department} + IA",
        ],
        "body": """Bonjour {first_name},

Chaque mois sans IA, une entreprise comme {company} perd en moyenne :

- 40-60 heures de travail manuel repetitif
- 20-30% de revenus potentiels (leads non suivis, reponses tardives)
- Un desavantage face aux concurrents qui automatisent deja

Je suis Dominiqk Mendy. Depuis 18 ans, j'aide des entreprises {sector} a combler cet ecart avec des solutions IA sur mesure : chatbots, automatisation, analyse predictive.

Travail recent : une PME logistique qui a reduit de 70% ses couts operationnels en 6 semaines.

Sans pression - juste un diagnostic rapide. 15 minutes par visio ?
=> https://ai.dominiqkmendy.com

Dominiqk Mendy
+212 607 798 670
ia@dominiqkmendy.com"""
    },
    "C_social": {
        "subjects": [
            "3 entreprises de {sector} ont automatise ce mois-ci - prochain tour ?",
            "Ce que j'ai fait pour 3 entreprises {sector} (et ce que ca peut faire pour {company})",
            "Rapport : etat de l'IA dans le {sector} en 2026",
        ],
        "body": """Bonjour {first_name},

Ce trimestre, j'ai aide :

=> Un groupe logistique a automatiser 120h/mois de reporting
=> Un service client B2B a traiter 80% des demandes sans intervention humaine
=> Une PME industrielle a augmenter sa productivite de 40%

Tous en moins de 30 jours. Tous avec un ROI visible des le premier mois.

Votre entreprise {company} est dans le {sector}. Je suis convaincu que des gains similaires sont possibles.

Je vous propose 15 minutes d'echange pour identifier vos plus gros leviers IA.
=> https://ai.dominiqkmendy.com

Dominiqk Mendy
Expert IA & Automatisation
+212 607 798 670"""
    }
}

FOLLOW_UPS = {
    "day3": {
        "subject": "Re: {original_subject}",
        "body": """Bonjour {first_name},

Je me permets de revenir vers vous suite a mon message precedent.

Le marche evolue vite : dans le {sector}, les entreprises qui automatisent maintenant prendront une avance considerable dans les 6 prochains mois.

Si le timing n'est pas bon, pas de souci - je comprends. Mais si vous avez 15 minutes cette semaine, je suis disponible.
=> https://ai.dominiqkmendy.com

Bonne journee,
Dominiqk Mendy"""
    }
}

# ============================================================
# EMAIL SENDER
# ============================================================

def load_password():
    with open(os.path.expanduser(APP_PASSWORD_PATH)) as f:
        return f.read().strip()

def send_email(to_email, subject, body):
    """Send an email via Gmail SMTP"""
    password = load_password()
    ctx = ssl.create_default_context()
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(SENDER_EMAIL, password)
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
            msg["To"] = to_email
            msg.attach(MIMEText(body, "utf-8"))
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"  ERREUR envoi a {to_email}: {e}")
        return False

# ============================================================
# CAMPAIGN ENGINE
# ============================================================

def fill_template(text, prospect):
    """Replace placeholders with prospect data"""
    mapping = {
        "{first_name}": prospect.get("first_name", ""),
        "{last_name}": prospect.get("last_name", prospect.get("first_name", "")),
        "{company}": prospect.get("company", "votre entreprise"),
        "{sector}": prospect.get("sector", "votre secteur"),
        "{department}": prospect.get("department", "operations"),
        "{original_subject}": prospect.get("original_subject", ""),
    }
    result = text
    for key, val in mapping.items():
        result = result.replace(key, str(val))
    return result

def run_campaign(prospects_csv, campaign_name="default", max_emails=None):
    """Run a full prospecting campaign"""
    # Load prospects
    prospects = []
    with open(prospects_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            prospects.append(row)
    
    print(f"Campagne: {campaign_name}")
    print(f"Prospects: {len(prospects)}")
    
    # Load history
    history_dir = os.path.expanduser(f"~/.hermes/ia-boutique/campaigns/{campaign_name}")
    os.makedirs(history_dir, exist_ok=True)
    history_file = os.path.join(history_dir, "history.json")
    
    history = {"sent": [], "replied": [], "bounced": []}
    if os.path.exists(history_file):
        with open(history_file) as f:
            history = json.load(f)
    
    sent_emails = {h["email"] for h in history["sent"]}
    
    # Send
    sent_count = 0
    for i, prospect in enumerate(prospects):
        if max_emails and sent_count >= max_emails:
            print(f"Limite atteinte: {max_emails}")
            break
        
        email = prospect.get("email", "").strip()
        if not email or email in sent_emails:
            continue
        
        # Select template (rotation)
        templates = list(TEMPLATES.keys())
        template_key = templates[hash(email) % len(templates)]
        tpl = TEMPLATES[template_key]
        
        subject = random.choice(tpl["subjects"])
        subject = fill_template(subject, prospect)
        body = fill_template(tpl["body"], prospect)
        
        print(f"  [{i+1}/{len(prospects)}] Envoi a {email} ({prospect.get('company','')})...")
        success = send_email(email, subject, body)
        
        if success:
            history["sent"].append({
                "email": email,
                "name": f"{prospect.get('first_name','')} {prospect.get('last_name','')}",
                "company": prospect.get("company", ""),
                "template": template_key,
                "subject": subject,
                "sent_at": datetime.now().isoformat()
            })
            sent_count += 1
            with open(history_file, "w") as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            print(f"  OK ({sent_count} envoyes aujourd'hui)")
        else:
            print(f"  ECHEC")
        
        # Delay between emails
        if i < len(prospects) - 1 and sent_count > 0:
            delay = random.randint(MIN_INTERVAL, MAX_INTERVAL)
            print(f"  Pause {delay}s...")
            time.sleep(delay)
    
    total = len(history["sent"])
    print(f"\nCampagne terminee: {sent_count} envoyes (total: {total})")
    return sent_count

# ============================================================
# REPORTING
# ============================================================

def generate_report(campaign_name="default"):
    """Generate campaign report"""
    history_file = os.path.expanduser(f"~/.hermes/ia-boutique/campaigns/{campaign_name}/history.json")
    if not os.path.exists(history_file):
        return "Aucune donnee."
    with open(history_file) as f:
        history = json.load(f)
    sent = len(history.get("sent", []))
    replied = len(history.get("replied", []))
    rate = (replied / sent * 100) if sent else 0
    lines = []
    lines.append(f"\nRAPPORT CAMPAGNE: {campaign_name}")
    lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Emails envoyes: {sent}")
    lines.append(f"Reponses: {replied} ({rate:.1f}%)")
    lines.append(f"Rebonds: {len(history.get('bounced', []))}")
    return "\n".join(lines)

# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="IA Business - Prospection")
    parser.add_argument("action", choices=["send", "report", "test"], help="Action")
    parser.add_argument("--campaign", default="default", help="Nom campagne")
    parser.add_argument("--csv", help="Fichier CSV prospects")
    parser.add_argument("--max", type=int, default=None, help="Max emails")
    parser.add_argument("--test-email", help="Email de test")
    args = parser.parse_args()
    
    if args.action == "test":
        if not args.test_email:
            print("Usage: python3 prospect.py test --test-email email@test.com")
        else:
            ok = send_email(args.test_email, "Test systeme prospection IA", f"Test envoye le {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\nSi vous recevez ceci, le systeme fonctionne.")
            print("OK envoye" if ok else "ECHEC")
    elif args.action == "send":
        if not args.csv:
            print("ERREUR: --csv requis")
        else:
            run_campaign(args.csv, args.campaign, args.max)
    elif args.action == "report":
        print(generate_report(args.campaign))
