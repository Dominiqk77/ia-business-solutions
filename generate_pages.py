#!/usr/bin/env python3
"""
IA Business Solutions - Page Generator
Genere les 10 landing pages produits + dashboard + pages annexes
"""
import os, json

OUTPUT_DIR = "/home/dom/ia-boutique/dist"

# ── TEMPLATE DE BASE ──
BASE_HEAD = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="https://ai.dominiqkmendy.com/{slug}/">
<style>
:root{{--bg:#08080c;--bg2:#0e0e14;--card:#12121c;--border:#1e1e2e;--accent:#6C5CE7;--accent2:#a29bfe;--glow:rgba(108,92,231,.15);--green:#00b894;--text:#e8e8f0;--text2:#9090a8;--grad:linear-gradient(135deg,#6C5CE7,#a29bfe,#fd79a8)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.7;overflow-x:hidden}}
a{{color:inherit;text-decoration:none}}
header{{position:fixed;top:0;left:0;right:0;z-index:100;padding:14px 0;background:rgba(8,8,12,.88);backdrop-filter:blur(20px);border-bottom:1px solid var(--border)}}
.hi{{max-width:1200px;margin:0 auto;padding:0 24px;display:flex;justify-content:space-between;align-items:center}}
.logo{{font-size:1.2rem;font-weight:800;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.logo small{{font-size:.6rem;display:block;font-weight:400;color:var(--text2);-webkit-text-fill-color:var(--text2)}}
.back{{color:var(--text2);font-size:.85rem;padding:8px 16px;border-radius:8px;border:1px solid var(--border);transition:.3s}}
.back:hover{{border-color:var(--accent);color:var(--text)}}
.hero{{padding:140px 24px 80px;text-align:center;position:relative;z-index:1}}
.hero h1{{font-size:clamp(2rem,5vw,3.5rem);font-weight:800;line-height:1.15;margin-bottom:20px;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.hero p{{max-width:650px;margin:0 auto;font-size:1.1rem;color:var(--text2)}}
section{{position:relative;z-index:1}}
.wrap{{max-width:1000px;margin:0 auto;padding:80px 24px}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center}}
.grid3{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:24px}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:28px}}
.card h3{{margin-bottom:10px}}
.card p{{font-size:.9rem;color:var(--text2)}}
.feature-list{{list-style:none;margin:20px 0}}
.feature-list li{{padding:10px 0;font-size:.9rem;color:var(--text2);border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px}}
.feature-list li:last-child{{border-bottom:none}}
.feature-list li::before{{content:"✓";color:var(--green);font-weight:700;flex-shrink:0}}
.btn{{display:inline-flex;align-items:center;gap:8px;padding:14px 32px;border-radius:12px;font-size:.95rem;font-weight:700;border:none;cursor:pointer;transition:.3s}}
.btn-p{{background:var(--accent);color:#fff;box-shadow:0 4px 30px rgba(108,92,231,.3)}}
.btn-p:hover{{background:var(--accent2);transform:translateY(-2px)}}
.btn-g{{background:transparent;color:var(--text);border:1px solid var(--border)}}
.btn-g:hover{{border-color:var(--accent);background:var(--glow)}}
.btn-w{{background:#25D366;color:#fff;margin-top:10px}}
.price-card{{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:36px;text-align:center;position:relative}}
.price-card.f{{border-color:var(--accent);background:linear-gradient(135deg,rgba(108,92,231,.05),transparent)}}
.pop{{position:absolute;top:-10px;right:16px;background:var(--accent);color:#fff;padding:4px 14px;border-radius:20px;font-size:.7rem;font-weight:700}}
.pname{{font-size:1.2rem;font-weight:700;margin:8px 0}}
.pfrom{{font-size:.8rem;color:var(--text2);margin-bottom:4px}}
.pamount{{font-size:2.4rem;font-weight:800;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.pperiod{{font-size:.8rem;color:var(--text2)}}
.pfeat{{list-style:none;margin:20px 0;text-align:left}}
.pfeat li{{padding:6px 0;font-size:.85rem;color:var(--text2);display:flex;align-items:center;gap:8px}}
.pfeat li::before{{content:"✓";color:var(--green);font-weight:700}}
.pay-sec{{background:linear-gradient(135deg,rgba(108,92,231,.08),rgba(0,184,148,.05));border:1px solid var(--accent);border-radius:20px;padding:36px;margin-top:40px}}
.pay-sec h3{{text-align:center;margin-bottom:20px}}
.pay-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}}
.pay-card{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:20px}}
.pay-card h4{{color:var(--accent);margin-bottom:8px;font-size:.95rem}}
.pay-card p{{font-size:.8rem;color:var(--text2);margin:2px 0}}
.rib{{font-family:'Courier New',monospace;background:var(--bg2);padding:10px;border-radius:6px;font-size:.75rem;margin:6px 0;word-break:break-all}}
.testimonial{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:24px;margin-bottom:16px}}
.testimonial .stars{{color:#ffd700;font-size:.9rem;margin-bottom:8px}}
.testimonial .text{{font-size:.88rem;color:var(--text2);margin-bottom:10px;font-style:italic}}
.testimonial .author{{font-weight:700;font-size:.85rem}}
.testimonial .role{{font-size:.78rem;color:var(--text2)}}
.faq-item{{background:var(--card);border:1px solid var(--border);border-radius:12px;margin-bottom:8px;overflow:hidden}}
.faq-q{{width:100%;padding:16px 20px;background:none;border:none;color:var(--text);font-size:.9rem;font-weight:600;text-align:left;cursor:pointer;display:flex;justify-content:space-between;align-items:center}}
.faq-open .faq-a{{max-height:300px;padding:0 20px 16px}}
.faq-a{{max-height:0;overflow:hidden;transition:max-height .3s ease;font-size:.85rem;color:var(--text2)}}
.demo-box{{background:var(--bg2);border:1px solid var(--border);border-radius:16px;padding:24px;margin:20px 0}}
.demo-box .chat-window{{background:var(--card);border-radius:12px;overflow:hidden;max-width:500px;margin:0 auto}}
.demo-box .chat-header{{background:var(--accent);padding:12px 16px;font-weight:700;font-size:.9rem;display:flex;align-items:center;gap:8px}}
.demo-box .chat-body{{padding:16px;max-height:300px;overflow-y:auto}}
.demo-box .msg{{margin:8px 0;padding:10px 14px;border-radius:12px;font-size:.85rem;line-height:1.5}}
.demo-box .msg.bot{{background:var(--bg2);border:1px solid var(--border)}}
.demo-box .msg.user{{background:var(--accent);color:#fff;text-align:right}}
footer{{border-top:1px solid var(--border);padding:36px 24px;text-align:center;font-size:.78rem;color:var(--text2);position:relative;z-index:1}}
footer a{{color:var(--accent)}}
@media(max-width:768px){{.grid2{{grid-template-columns:1fr}}.hero{{padding:110px 24px 50px}}}}
</style>
</head>
<body>
<header><div class="hi">
<a href="https://ai.dominiqkmendy.com/" class="logo">IA Business Solutions<small>by Dominiqk Mendy</small></a>
<a href="https://ai.dominiqkmendy.com/" class="back">← Retour</a>
</div></header>
"""

BASE_FOOT = """
<footer>
<p>© 2026 Dominiqk Mendy — IA Business Solutions | <a href="https://ai.dominiqkmendy.com">ai.dominiqkmendy.com</a> | <a href="mailto:ia@dominiqkmendy.com">ia@dominiqkmendy.com</a></p>
</footer>
<script>
document.querySelectorAll('.faq-q').forEach(btn=>{
btn.addEventListener('click',()=>{
const item=btn.parentElement;
item.classList.toggle('faq-open');
});
});
</script>
</body></html>"""

# ── PRODUITS ──
PRODUCTS = {
    "chatbot-ia": {
        "title": "Chatbot IA Intelligent — Agent Conversationnel 24/7",
        "description": "Chatbot IA clé en main pour site web, WhatsApp, Messenger. Entraîné sur vos données. Déploiement en 1 clic. Dès 29€/mois.",
        "h1": "Un agent IA qui répond à vos clients 24/7",
        "h2": "Ne perdez plus jamais un client par manque de réponse",
        "tagline": "10 messages/jour gratuit — 29€/mois Pro — 99€/mois Business",
        "emoji": "🤖",
        "features": [
            "Compréhension langage naturel multilingue",
            "Formation automatique sur vos PDF, FAQ, site web",
            "Déploiement en 1 clic via widget JS",
            "Intégration WhatsApp, Messenger, site web",
            "Collecte automatique de leads (emails)",
            "Analytics complet et export des conversations",
            "Escalade humaine automatique",
            "Multi-langues : FR, EN, AR, ES"
        ],
        "steps": [
            ("📍", "Vous choisissez votre plan", "Gratuit (10 msg/jour), Pro (29€/mois) ou Business (99€/mois)"),
            ("📄", "Vous uploadez vos données", "PDF, FAQ, site web — le bot apprend automatiquement"),
            ("🔗", "Vous copiez le code widget", "Un simple script-à coller sur votre site. 30 secondes."),
            ("🚀", "Votre bot est en ligne", "Il répond instantanément à vos clients. 24/7. Sans interruption."),
        ],
        "testimonials": [
            ("★★★★★", "Notre bot gère 80% des demandes sans humain. Temps de réponse passé de 48h à 3 secondes.", "Directeur Général", "E-commerce, Maroc"),
            ("★★★★★", "Meilleur investissement de l'année. Nos leads ont augmenté de 45% grâce à la collecte automatique.", "Head of Marketing", "SaaS, France"),
            ("★★★★★", "Le bot comprend vraiment nos clients. On a réduit le support de 60%.", "Customer Success Manager", "Fintech, Sénégal"),
        ],
        "prices": [
            ("free", "Gratuit", "0€", "mois", "10 messages/jour, watermark", False),
            ("pro", "Pro", "29€", "mois", "5,000 messages/mois, pas de watermark", True),
            ("business", "Business", "99€", "mois", "50,000 messages, multi-langues, analytics avancés", False),
        ],
        "faq": [
            ("Comment le bot apprend-il ?", "Vous uploadez vos documents (PDF, FAQ, URL de votre site). Le bot extrait automatiquement la connaissance et l'utilise pour répondre."),
            ("Quels langages sont supportés ?", "Français, Anglais, Arabe, Espagnol et plus. Le bot détecte automatiquement la langue du visiteur."),
            ("Combien de temps pour le déployer ?", "Moins de 30 secondes pour le widget. 1-2 heures si vous voulez personnaliser la base de connaissances."),
            ("Puis-je l'intégrer à WhatsApp ?", "Oui. L'intégration WhatsApp Business API est disponible en plan Business (99€/mois)."),
            ("Que se passe-t-il si le bot ne sait pas répondre ?", "Il escalade automatiquement vers un humain avec le contexte complet de la conversation."),
        ],
        "demo_bubbles": [
            ("bot", "Bonjour ! Je suis l'assistant virtuel. Comment puis-je vous aider ? En quoi consiste votre projet ?"),
            ("user", "J'aurais besoin d'un chatbot pour mon site e-commerce"),
            ("bot", "Excellent ! Je peux vous aider avec ça. Voulez-vous un devis gratuit ? Je peux analyser votre site et vous proposer une solution sur mesure en quelques minutes."),
        ]
    },

    "assistant-seo": {
        "title": "Assistant Rédaction SEO IA — Articles, Fiches Produits, Meta",
        "description": "Générez des articles SEO optimisés, fiches produits et meta descriptions. Inclut analyse mots-clés et suivi positionnement. Dès 19€/mois.",
        "h1": "Du contenu SEO optimisé en quelques clics",
        "h2": "Arrêtez de payer des rédacteurs 500€/article. L'IA fait mieux, plus vite.",
        "emoji": "✍️",
        "tagline": "19€/mois (10 articles) — 49€/mois (50 articles) — 99€/mois (illimité)",
        "features": [
            "Génération articles de blog optimisés SEO",
            "Fiches produits e-commerce multilingues",
            "Meta descriptions et title tags automatiques",
            "Analyse des mots-clés et concurrence",
            "Suggestion de structure H2/H3 optimisée",
            "Détection de content gaps vs concurrents",
            "Score SEO en temps réel",
            "Export direct vers WordPress, Shopify, Notion"
        ],
        "steps": [
            ("🎯", "Décrivez votre objectif", "Produit, service, article — l'IA vous pose les bonnes questions"),
            ("📝", "L'IA génère le contenu", "Article optimisé de 1500+ mots avec structure SEO complète"),
            ("⚡", "Optimisez et éditez", "Score SEO, suggestions d'amélioration, reformulation en 1 clic"),
            ("📤", "Publiez directement", "Export WordPress, Shopify, Notion, Google Docs"),
        ],
        "testimonials": [
            ("★★★★★", "On publie 3x plus de contenu pour 10x moins cher. Notre trafic organique a doublé en 4 mois.", "Responsable SEO", "Agence digitale, France"),
            ("★★★★★", "Les fiches produits générées convertissent mieux que celles de nos rédacteurs humains.", "E-commerçant", "Mode, Maroc"),
            ("★★★★★", "Le score SEO en temps réel m'a fait gagner des heures de relecture.", "Blogueur", "Tech, Sénégal"),
        ],
        "prices": [
            ("starter", "Starter", "19€", "mois", "10 articles/mois, 1500 mots max", False),
            ("pro", "Pro", "49€", "mois", "50 articles/mots illimités, export WP/Shopify", True),
            ("business", "Business", "99€", "mois", "Articles illimités, multi-utilisateurs, API", False),
        ],
        "faq": [
            ("Le contenu généré est-il unique ?", "Oui. Chaque article est généré from scratch avec vos paramètres. Pas de duplication."),
            ("Est-ce que Google détecte le contenu IA ?", "Le contenu est rédigé pour être naturel et passer les détections. Nous incluons des optimisations humaines."),
            ("Puis-je utiliser les articles directement ?", "Oui, ils sont prêts à publier. Un éditeur intégré permet de personnaliser si besoin."),
        ],
        "demo_bubbles": None,
    },

    "agent-support": {
        "title": "Agent Support Client IA — Automatisez 80% de vos Tickets",
        "description": "IA qui lit vos emails, tickets, chats et répond automatiquement. Escalade si nécessaire. Dès 99€/mois.",
        "h1": "Vos clients obtiennent des réponses en secondes, pas en jours",
        "h2": "Réduisez votre coût support de 70% sans perdre la qualité",
        "emoji": "🎧",
        "tagline": "99€/mois (500 résolutions) — 299€/mois (5000) — Sur devis entreprise",
        "features": [
            "Réponse automatique emails, tickets et chat",
            "Formation sur vos précédents échanges et FAQ",
            "Escalade intelligente vers un humain si nécessaire",
            "Détection d'urgence et priorisation",
            "Multi-canal unifié : email, chat, WhatsApp",
            "Analytics : temps de résolution, satisfaction",
            "Multi-langues automatique",
            "Intégration Zendesk, Freshdesk, Help Scout"
        ],
        "steps": [
            ("🔌", "Connectez vos canaux", "Email, ticket, Slack, WhatsApp — quelques clics pour intégrer"),
            ("📚", "L'IA apprend de vos données", "Historique des tickets, FAQ, procédures — tout est analysé"),
            ("🤖", "L'IA commence à répondre", "80% des demandes traitées sans intervention humaine"),
            ("📊", "Suivez les résultats", "Temps de résolution, taux d'automatisation, satisfaction"),
        ],
        "testimonials": [
            ("★★★★★", "Notre temps de réponse moyen est passé de 18h à 12 minutes. Nos clients sont ravis.", "VP Support", "SaaS, France"),
            ("★★★★★", "70% des tickets résolus sans humain. L'équipe se concentre sur les cas complexes.", "CTO", "E-commerce, Belgique"),
        ],
        "prices": [
            ("starter", "Starter", "99€", "mois", "500 résolutions/mois, email uniquement", False),
            ("pro", "Pro", "299€", "mois", "5,000 résolutions, multi-canal", True),
            ("enterprise", "Enterprise", "Sur devis", "", "Volume illimité, SLA, dédié humain", False),
        ],
        "faq": [
            ("Comment l'IA sait quoi répondre ?", "Elle est entraînée sur l'historique de vos tickets résolus et votre base de connaissances."),
            ("Que se passe-t-elle face à un problème inconnu ?", "Elle escalade automatiquement vers un agent humain avec tout le contexte de la conversation."),
        ],
        "demo_bubbles": None,
    },

    "analyse-contrats": {
        "title": "Analyseur de Contrats IA — Extraction & Alertes Automatiques",
        "description": "Uploadez un contrat PDF, l'IA extrait les clauses clés, résume et alerte sur les risques. Pour avocats, immobilier, PME.",
        "h1": "Comprenez un contrat de 50 pages en 30 secondes",
        "h2": "Plus jamais d'erreur cachée dans vos clauses",
        "emoji": "⚖️",
        "tagline": "Pay-per-use: 9€/document — 29€/mois (20 docs) — 99€/mois (illimité)",
        "features": [
            "Upload PDF, extraction automatique du texte",
            "Identification des clauses importantes",
            "Détection des risques et anomalies",
            "Résumé exécutif en langage simple",
            "Comparaison entre deux versions d'un contrat",
            "Alertes sur les dates clés et échéances",
            "Export Word, PDF annoté",
            "Confidentialité : données supprimées après analyse"
        ],
        "steps": [
            ("📄", "Uploadez votre document", "PDF, Word, ou photo — l'IA extrait tout le texte"),
            ("🔍", "L'IA analyse le document", "Clauses, risques, obligations — tout est identifié"),
            ("📋", "Recevez le rapport", "Résumé exécutif, alertes, recommandations"),
            ("✏️", "Exportez et partagez", "PDF annoté, Word, ou partage"),
        ],
        "testimonials": [
            ("★★★★★", "J'ai repéré une clause abusive dans un bail que 3 avocats avaient raté. Incroyable.", "Agent immobilier", "Paris, France"),
            ("★★★★★", "Je gère 200+ contrats/mois. Cet outil m'a fait gagner 80% de temps.", "Directrice Juridique", "PME, Maroc"),
        ],
        "prices": [
            ("payperuse", "Pay-per-use", "9€", "document", "Occasionnel, sans abonnement", False),
            ("pro", "Pro", "29€", "mois", "20 documents/mois, historique", True),
            ("business", "Business", "99€", "mois", "Documents illimités, API, équipe", False),
        ],
        "faq": [
            ("Mes documents sont-ils confidentiels ?", "Oui. Chaque document est supprimé 24h après l'analyse. Nous ne stockons rien."),
            ("Quels types de documents sont supportés ?", "Contrats, baux, CGV, NDA, devis, factures — tout document juridique ou commercial."),
        ],
        "demo_bubbles": None,
    },

    "videos-courtes-ia": {
        "title": "Générateur Vidéos Courtes IA TikTok/Reels Automatique",
        "description": "À partir d'un script ou article, généré des vidéos avec avatar IA, sous-titres et musique. Pour créateurs et marques.",
        "h1": "Créez des vidéos virales sans caméra",
        "h2": "Un script → une vidéo publiée en 60 secondes",
        "emoji": "🎬",
        "tagline": "19€/mois (5 vidéos) — 49€/mois (30 vidéos) — 99€/mois (illimité)",
        "features": [
            "Avatar IA réaliste (homme/femme, 20+ voix)",
            "Génération automatique de sous-titres",
            "Publication directe TikTok/Reels/Shorts",
            "Templates de hooks viraux",
            "Musique libre de droits intégrée",
            "Format vertical 9:16 optimisé",
            "Batch creation : 10 vidéos d'un coup",
            "Script to video automatique"
        ],
        "testimonials": [
            ("★★★★★", "Ma page TikTok est passée de 0 à 50K abonnés en 3 mois. Sans montrer mon visage !", "Créateur de contenu", "France"),
            ("★★★★★", "Nos Reels générés par IA ont 3x plus d'engagement que nos vidéos produites manuellement.", "Community Manager", "Mode, Maroc"),
        ],
        "prices": [
            ("starter", "Starter", "19€", "mois", "5 vidéos/mois, 60 sec max", False),
            ("pro", "Pro", "49€", "mois", "30 vidéos/mois, HD, publication auto", True),
            ("business", "Business", "99€", "mois", "Vidéos illimitées, API, multi-comptes", False),
        ],
        "faq": None,
        "demo_bubbles": None,
    },

    "analyste-donnees": {
        "title": "Analyste de Données IA — Dashboard Automatique",
        "description": "Connectez Supabase, Sheets ou CSV. L'IA génère dashboards, rapports et réponses en langage naturel.",
        "h1": "Vos données parlent enfin. Sans développeur.",
        "h2": "Posez une question, obtenez un graphique. En 10 secondes.",
        "emoji": "📊",
        "tagline": "Freemium (100 requêtes/mois) — 49€/mois — 149€/mois",
        "features": [
            "Connexion Supabase, Google Sheets, CSV",
            "Requêtes en langage naturel",
            "Graphiques automatiques",
            "Rapports périodiques automatiques",
            "Alertes sur anomalies",
            "Dashboard partageable",
            "Export PNG, PDF, PowerPoint",
            "Multi-sources de données"
        ],
        "testimonials": [
            ("★★★★★", "Plus besoin d'un data analyst à 5K€/mois. L'IA fait 80% du travail.", "CEO Startup", "France"),
            ("★★★★★", "Nos rapports mensuels auto-générés nous font gagner 20h/mois.", "Directeur Financier", "PME, Maroc"),
        ],
        "prices": [
            ("free", "Gratuit", "0€", "mois", "100 requêtes/mois, 2 sources", False),
            ("pro", "Pro", "49€", "mois", "2,000 requêtes, toutes sources", True),
            ("business", "Business", "149€", "mois", "Illimité, équipe, API", False),
        ],
        "faq": None,
        "demo_bubbles": None,
    },

    "agent-recrutement": {
        "title": "Agent Recrutement IA — Tri de CV Automatique",
        "description": "Uploadez une fiche de poste + CVs, l'IA classe les candidats, identifie les meilleurs, génère des questions d'entretien.",
        "h1": "Trouvez le bon candidat en minutes, pas en semaines",
        "h2": "Plus de tri manuel. L'IA lit, évalue, classe.",
        "emoji": "👔",
        "tagline": "49€/offre d'emploi — 149€/mois (offres illimitées)",
        "features": [
            "Upload fiche de poste + CVs (PDF, Word)",
            "Classement automatique des candidats",
            "Scores de compatibilité poste/candidat",
            "Questions d'entretien personnalisées",
            "Détection des incohérences dans les CV",
            "Résumé de chaque candidat en 3 lignes",
            "Multi-langues : FR, EN, AR",
            "Export vers votre ATS"
        ],
        "testimonials": [
            ("★★★★★", "On a réduit notre temps de recrutement de 6 semaines à 8 jours.", "DRH", "Groupe, Sénégal"),
            ("★★★★★", "L'IA repère des talents qu'on aurait zappés en tri manuelle.", "Talent Acquisition", "Scale-up, France"),
        ],
        "prices": [
            ("unit", "Par offre", "49€", "offre", "Jusqu'à 50 CV, analyse complète", False),
            ("pro", "Mensuel", "149€", "mois", "Offres illimitées, jusqu'à 200 CV/offre", True),
            ("enterprise", "Enterprise", "Sur devis", "", "ATS dédié, SLA, multi-utilisateurs", False),
        ],
        "faq": None,
        "demo_bubbles": None,
    },

    "traducteur-ia": {
        "title": "Traducteur Automatique Spécialisé IA — Sites & Documents",
        "description": "Traduisez des sites entiers ou documents en conservant le contexte métier. Pas Google Translate.",
        "h1": "Traduisez votre site en 30 langues. Sans faux sens.",
        "h2": "Vos clients méritent de lire dans leur langue. Sans erreur.",
        "emoji": "🌍",
        "tagline": "19€/mois (10K mots) — 49€/mois (50K mots) — 99€/mois (illimité)",
        "features": [
            "Traduction contextuelle (pas mot-à-mot)",
            "30+ langues supportées",
            "Conservation du ton et du style",
            "Glossaire métier personnalisable",
            "API pour traduction en temps réel",
            "Bulk : traduisez 100 pages d'un coup",
            "Intégration WordPress, Shopify, Notion",
            "QA automatique (détection d'erreurs)"
        ],
        "testimonials": [
            ("★★★★★", "Notre expansion en Afrique de l'Ouest a été multipliée par 5 grâce à la traduction automatique.", "VP International", "EdTech, France"),
            ("★★★★★", "Les traductions sont bien meilleures que Google Translate. Le glossaire métier fait la différence.", "Responsable Export", "Agro, Maroc"),
        ],
        "prices": [
            ("starter", "Starter", "19€", "mois", "10,000 mots/mois", False),
            ("pro", "Pro", "49€", "mois", "50,000 mots, glossaire, API", True),
            ("business", "Business", "99€", "mois", "Mots illimités, priority, SLA", False),
        ],
        "faq": None,
        "demo_bubbles": None,
    },

    "landing-pages-ia": {
        "title": "Générateur Landing Pages IA — Copywriting + Design",
        "description": "Décrivez votre produit, l'IA crée une landing page complète. Prête à publier. Pour entrepreneurs et agences.",
        "h1": "Une landing page qui convertit. En 60 secondes.",
        "h2": "Plus besoin de designer. Plus besoin de copywriter.",
        "emoji": "🚀",
        "tagline": "29€/page — 99€/mois (10 pages) — Pack agence 199€/mois",
        "features": [
            "Description produit → landing page complète",
            "Copywriting persuasif généré par IA",
            "Design responsive premium",
            "A/B testing automatique des headlines",
            "Intégration Mailchimp, Stripe, Formspree",
            "Export HTML ou publication directe",
            "Templates par secteur (SaaS, e-commerce, service)",
            "Optimisation taux de conversion intégrée"
        ],
        "testimonials": [
            ("★★★★★", "J'ai lancé 12 landing pages en un week-end. Les taux de conversion sont excellents.", "Growth Hacker", "Startup, France"),
            ("★★★★★", "Nos agences clientes adorent. Elles génèrent des pages client en 5 minutes.", "Fondateur Agence", "Digital, Maroc"),
        ],
        "prices": [
            ("unit", "Par page", "29€", "page", "1 section, export HTML", False),
            ("pro", "Mensuel", "99€", "mois", "10 pages/mois, publication auto", True),
            ("agency", "Agence", "199€", "mois", "Pages illimitées, multi-clients, API", False),
        ],
        "faq": None,
        "demo_bubbles": None,
    },

    "resumeur-reunions": {
        "title": "Résumeur de Réunions IA — Audio/Vidéo en Résumé Écrit",
        "description": "Uploadez un enregistrement, obtenez transcription, résumé, points d'action et compte-rendu. Dès 9€/mois.",
        "h1": "Ne prenez plus de notes. L'IA s'en charge.",
        "h2": "Upload minutes → Recevez le compte-rendu → Partagez",
        "emoji": "📝",
        "tagline": "9€/mois (5 heures) — 29€/mois (20 heures) — 49€/mois (illimité)",
        "features": [
            "Upload audio ou vidéo (MP3, MP4, WAV, Zoom)",
            "Transcription automatique (95%+ précision)",
            "Résumé exécutif en 5 bullets",
            "Extraction des points d'action (qui fait quoi)",
            "Identification des décisions prises",
            "Export Word, PDF, Notion, Google Docs",
            "Intégration Zoom, Google Meet, Teams",
            "Confidentialité : données supprimées après traitement"
        ],
        "testimonials": [
            ("★★★★★", "Fini les notes de réunion illisibles. L'IA produit un compte-rendu parfait à chaque fois.", "CEO", "Consulting, France"),
            ("★★★★★", "On économise 3h/semaine en compte-rendus. Toute l'équipe est alignée.", "VP Operations", "SaaS, Maroc"),
        ],
        "prices": [
            ("starter", "Starter", "9€", "mois", "5 heures/mois", False),
            ("pro", "Pro", "29€", "mois", "20 heures, Notion/Slack intégrés", True),
            ("business", "Business", "49€", "mois", "Heures illimitées", False),
        ],
        "faq": None,
        "demo_bubbles": None,
    },
}

def slug_to_name(slug):
    return slug.replace("-", " ").title()

def generate_product_page(slug, p):
    """Generate a full product landing page"""
    title = p["title"]
    desc = p["description"]
    emoji = p["emoji"]
    
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://ai.dominiqkmendy.com/products/{slug}/">
<style>
:root{{--bg:#08080c;--bg2:#0e0e14;--card:#12121c;--border:#1e1e2e;--accent:#6C5CE7;--accent2:#a29bfe;--glow:rgba(108,92,231,.15);--green:#00b894;--text:#e8e8f0;--text2:#9090a8;--grad:linear-gradient(135deg,#6C5CE7,#a29bfe,#fd79a8)}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.7;overflow-x:hidden}}
a{{color:inherit;text-decoration:none}}
header{{position:fixed;top:0;left:0;right:0;z-index:100;padding:14px 0;background:rgba(8,8,12,.88);backdrop-filter:blur(20px);border-bottom:1px solid var(--border)}}
.hi{{max-width:1200px;margin:0 auto;padding:0 24px;display:flex;justify-content:space-between;align-items:center}}
.logo{{font-size:1.2rem;font-weight:800;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.logo small{{font-size:.6rem;display:block;font-weight:400;color:var(--text2);-webkit-text-fill-color:var(--text2)}}
.back{{color:var(--text2);font-size:.85rem;padding:8px 16px;border-radius:8px;border:1px solid var(--border);transition:.3s}}
.back:hover{{border-color:var(--accent);color:var(--text)}}
.hero{{padding:140px 24px 60px;text-align:center}}
.hero h1{{font-size:clamp(1.8rem,4vw,3rem);font-weight:800;line-height:1.15;margin-bottom:16px;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.hero .sub{{max-width:600px;margin:0 auto;font-size:1.05rem;color:var(--text2);margin-bottom:12px}}
.hero .tag{{display:inline-block;background:var(--glow);border:1px solid var(--accent);padding:6px 18px;border-radius:20px;font-size:.8rem;color:var(--accent2)}}
.cta-row{{display:flex;gap:12px;justify-content:center;margin-top:28px;flex-wrap:wrap}}
.btn{{display:inline-flex;align-items:center;gap:8px;padding:14px 32px;border-radius:12px;font-size:.92rem;font-weight:700;border:none;cursor:pointer;transition:.3s}}
.btn-p{{background:var(--accent);color:#fff;box-shadow:0 4px 30px rgba(108,92,231,.3)}}
.btn-p:hover{{background:var(--accent2);transform:translateY(-2px)}}
.btn-w{{background:#25D366;color:#fff}}
section{{position:relative;z-index:1}}
.wrap{{max-width:1000px;margin:0 auto;padding:80px 24px}}
h2{{font-size:clamp(1.5rem,3vw,2.2rem);font-weight:800;margin-bottom:20px;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center}}
.grid3{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:28px}}
.card h3{{margin-bottom:8px;font-size:1.05rem}}
.card p{{font-size:.88rem;color:var(--text2)}}
.feature-list{{list-style:none;margin:20px 0}}
.feature-list li{{padding:10px 0;font-size:.9rem;color:var(--text2);border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px}}
.feature-list li:last-child{{border-bottom:none}}
.feature-list li::before{{content:"✓";color:var(--green);font-weight:700;flex-shrink:0}}
.steps{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:24px}}
.step{{text-align:center;padding:24px}}
.step-i{{width:56px;height:56px;background:var(--glow);border:1px solid var(--accent);border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:1.5rem;margin:0 auto 14px}}
.step-t{{font-weight:700;margin-bottom:6px;font-size:.95rem}}
.step-d{{font-size:.83rem;color:var(--text2)}}
.price-card{{background:var(--card);border:1px solid var(--border);border-radius:20px;padding:32px;text-align:center;position:relative}}
.price-card.f{{border-color:var(--accent)}}
.pop{{position:absolute;top:-10px;right:16px;background:var(--accent);color:#fff;padding:4px 14px;border-radius:20px;font-size:.65rem;font-weight:700}}
.pname{{font-size:1.1rem;font-weight:700;margin:8px 0}}
.pamount{{font-size:2.2rem;font-weight:800;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.pperiod{{font-size:.78rem;color:var(--text2)}}
.pfeat{{list-style:none;margin:16px 0;text-align:left}}
.pfeat li{{padding:5px 0;font-size:.83rem;color:var(--text2);display:flex;align-items:center;gap:8px}}
.pfeat li::before{{content:"✓";color:var(--green);font-weight:700}}
.pay-sec{{background:linear-gradient(135deg,rgba(108,92,231,.08),rgba(0,184,148,.05));border:1px solid var(--accent);border-radius:20px;padding:32px;margin-top:40px}}
.pay-sec h3{{text-align:center;margin-bottom:16px;font-size:1.3rem}}
.pay-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}}
.pay-card{{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:18px}}
.pay-card h4{{color:var(--accent);margin-bottom:6px;font-size:.9rem}}
.pay-card p{{font-size:.78rem;color:var(--text2);margin:2px 0}}
.rib{{font-family:'Courier New',monospace;background:var(--bg2);padding:8px;border-radius:6px;font-size:.72rem;margin:4px 0;word-break:break-all}}
.tcard{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:22px;margin-bottom:14px}}
.tstars{{color:#ffd700;font-size:.85rem;margin-bottom:8px}}
.ttext{{font-size:.85rem;color:var(--text2);margin-bottom:10px;font-style:italic}}
.tauth{{font-weight:700;font-size:.83rem}}
.trole{{font-size:.75rem;color:var(--text2)}}
.faq-item{{background:var(--card);border:1px solid var(--border);border-radius:12px;margin-bottom:8px;overflow:hidden}}
.faq-q{{width:100%;padding:16px 20px;background:none;border:none;color:var(--text);font-size:.88rem;font-weight:600;text-align:left;cursor:pointer;display:flex;justify-content:space-between;align-items:center}}
.faq-open .faq-a{{max-height:300px;padding:0 20px 16px}}
.faq-a{{max-height:0;overflow:hidden;transition:max-height .3s ease;font-size:.83rem;color:var(--text2)}}
.demo-box{{background:var(--bg2);border:1px solid var(--border);border-radius:16px;padding:20px;margin:20px 0}}
.chat-win{{background:var(--card);border-radius:12px;overflow:hidden;max-width:480px;margin:0 auto}}
.chat-h{{background:var(--accent);padding:10px 14px;font-weight:700;font-size:.85rem;display:flex;align-items:center;gap:8px;color:#fff}}
.chat-b{{padding:14px;max-height:250px;overflow-y:auto}}
.msg{{margin:8px 0;padding:8px 12px;border-radius:10px;font-size:.82rem;line-height:1.5}}
.msg.bot{{background:var(--bg2);border:1px solid var(--border)}}
.msg.user{{background:var(--accent);color:#fff;text-align:right}}
.final-cta{{text-align:center;padding:60px 24px}}
footer{{border-top:1px solid var(--border);padding:30px 24px;text-align:center;font-size:.75rem;color:var(--text2);position:relative;z-index:1}}
footer a{{color:var(--accent)}}
@media(max-width:768px){{.grid2{{grid-template-columns:1fr}}.hero{{padding:110px 24px 40px}}}}
</style>
</head>
<body>
<header><div class="hi">
<a href="https://ai.dominiqkmendy.com/" class="logo">IA Business Solutions<small>by Dominiqk Mendy</small></a>
<a href="https://ai.dominiqkmendy.com/" class="back">← Retour</a>
</div></header>

<section class="hero">
<div style="font-size:3rem;margin-bottom:12px">{emoji}</div>
<h1>{p['h1']}</h1>
<p class="sub">{p['h2']}</p>
<div class="tag">{p['tagline']}</div>
<div class="cta-row">
<a href="#tarifs" class="btn btn-p">Voir les tarifs ↓</a>
<a href="https://wa.me/212607798670?text=Bonjour%20Dominiqk,%20je%20souhaite%20en%20savoir%20plus%20sur%20{slug.replace('-','%20')}" target="_blank" class="btn btn-w">💬 WhatsApp</a>
</div>
</section>
"""

    # Demo section (for chatbot)
    if p.get("demo_bubbles"):
        html += '<section class="wrap"><div class="demo-box"><h3 style="text-align:center;margin-bottom:16px">Démo en direct</h3><div class="chat-win"><div class="chat-h">💬 Démo — Chatbot IA</div><div class="chat-b">'
        for role, text in p["demo_bubbles"]:
            html += f'<div class="msg {role}">{text}</div>'
        html += '</div></div></section>'

    # Features
    html += '<section class="wrap"><h2>Fonctionnalités</h2><div class="grid2"><ul class="feature-list">'
    for f in p["features"][:4]:
        html += f'<li>{f}</li>'
    html += '</ul><ul class="feature-list">'
    for f in p["features"][4:]:
        html += f'<li>{f}</li>'
    html += '</ul></div></section>'

    # Steps
    if p.get("steps"):
        html += '<section class="wrap"><h2>Comment ça marche</h2><div class="steps">'
        for icon, title, desc in p["steps"]:
            html += f'<div class="step"><div class="step-i">{icon}</div><div class="step-t">{title}</div><div class="step-d">{desc}</div></div>'
        html += '</div></section>'

    # Testimonials
    if p.get("testimonials"):
        html += '<section class="wrap"><h2>Ce qu\'en disent mes clients</h2>'
        for stars, text, auth, role in p["testimonials"]:
            html += f'<div class="tcard"><div class="tstars">{stars}</div><div class="ttext">"{text}"</div><div class="tauth">{auth}</div><div class="trole">{role}</div></div>'
        html += '</section>'

    # Pricing
    html += '<section class="wrap" id="tarifs"><h2>Tarifs</h2><div class="grid3">'
    for plan_id, name, amount, period, desc, featured in p["prices"]:
        feat_class = " f" if featured else ""
        pop = '<div class="pop">Populaire</div>' if featured else ""
        btn = "btn-p" if featured else "btn-p"
        html += f'<div class="price-card{feat_class}">{pop}<div class="pname">{name}</div><div class="pamount">{amount}</div><div class="pperiod">{period}</div><ul class="pfeat"><li>{desc}</li></ul><a href="#contact" class="btn {btn}" style="width:100%;justify-content:center">Choisir ce plan</a><a href="https://wa.me/212607798670?text=Bonjour%20je%20veux%20le%20plan%20{name}" target="_blank" class="btn btn-w" style="width:100%;justify-content:center">💬 WhatsApp</a></div>'
    html += '</div></section>'

    # Payment section
    html += """<div class="pay-sec">
<h3>💳 Informations de paiement</h3>
<p style="text-align:center;font-size:.85rem;color:var(--text2);margin-bottom:16px">Effectuez un virement vers l'un des comptes suivants. Activation sous 24h après réception.</p>
<div class="pay-grid">
<div class="pay-card">
<h4>Saham Bank (MAD)</h4>
<p>Titulaire : FARES ZINEB</p>
<p>Agence : MARRAKECH MAJORELLE</p>
<div class="rib">RIB : 022 450 0002200029051487 53<br>SWIFT : SGMBMAMC</div>
</div>
<div class="pay-card">
<h4>CIH Bank (MAD)</h4>
<p>Titulaire : ZINEB FARES</p>
<p>Agence : MARRAKECH REGENT</p>
<div class="rib">IBAN : MA64 2304 5053 3369 4214 0020 0092<br>SWIFT : CIHMMAMC</div>
</div>
</div>
<p style="text-align:center;margin-top:16px;font-size:.8rem;color:var(--text2)">Devises acceptées : EUR, USD, GBP, MAD, XOF | Frais à la charge de l'envoyeur</p>
</div>"""

    # FAQ
    if p.get("faq"):
        html += '<section class="wrap"><h2>FAQ</h2>'
        for q, a in p["faq"]:
            html += f'<div class="faq-item"><button class="faq-q">{q}</button><div class="faq-a">{a}</div></div>'
        html += '</section>'

    # Final CTA
    html += f"""<section class="final-cta">
<h2 style="font-size:clamp(1.5rem,3vw,2rem);font-weight:800;margin-bottom:16px;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">Prêt à démarrer ?</h2>
<p style="color:var(--text2);margin-bottom:24px">Choisissez votre plan et soyez opérationnel en moins de 24h.</p>
<div class="cta-row">
<a href="#tarifs" class="btn btn-p">Voir les tarifs ↑</a>
<a href="https://wa.me/212607798670?text=Bonjour%20Dominiqk,%20je%20souhaite%20d%C3%A9marrer%20avec%20{slug.replace('-','%20')}" target="_blank" class="btn btn-w">💬 WhatsApp</a>
</div>
</section>"""

    # Upsell: recommend complementary products
    upsell_map = {
        "chatbot-ia": [("agent-support", "🎧 Automatisez aussi votre support client"), ("assistant-seo", "✍️ Boostez votre contenu SEO")],
        "assistant-seo": [("chatbot-ia", "🤖 Ajoutez un chatbot à votre site"), ("landing-pages-ia", "🚀 Générez des landing pages qui convertissent")],
        "agent-support": [("chatbot-ia", "🤖 Ajoutez un chatbot WhatsApp"), ("resumeur-reunions", "📝 Automatisez vos comptes-rendus")],
        "analyse-contrats": [("traducteur-ia", "🌍 Traduisez vos contrats internationaux")],
        "videos-courtes-ia": [("assistant-seo", "✍️ Générez les scripts SEO automatiquement")],
        "analyste-donnees": [("agent-support", "🎧 Analysez vos données support")],
        "agent-recrutement": [("resumeur-reunions", "📝 Résumez vos entretiens automatiquement")],
        "traducteur-ia": [("assistant-seo", "✍️ Optimisez le SEO multilingue")],
        "landing-pages-ia": [("chatbot-ia", "🤖 Ajoutez un chatbot à vos landing pages"), ("assistant-seo", "✍️ Contenu SEO pour vos pages")],
        "resumeur-reunions": [("agent-recrutement", "👔 Automatisez aussi le tri des CV")],
    }
    
    upsells = upsell_map.get(slug, [])
    if upsells:
        html += '<section class="wrap"><h2>Complétez votre arsenal IA</h2><div class="grid2">'
        for uslug, utitle in upsells:
            if uslug in PRODUCTS:
                u = PRODUCTS[uslug]
                html += f'<div class="card"><div style="font-size:2rem;margin-bottom:8px">{u["emoji"]}</div><h3>{utitle}</h3><p>{u["description"][:100]}...</p><a href="/products/{uslug}/" class="btn btn-p" style="width:100%;justify-content:center;margin-top:12px">Découvrir →</a></div>'
        html += '</div></section>'

    html += """<footer>
<p>&copy; 2026 Dominiqk Mendy — IA Business Solutions | <a href="https://ai.dominiqkmendy.com">ai.dominiqkmendy.com</a> | <a href="mailto:ia@dominiqkmendy.com">ia@dominiqkmendy.com</a></p>
</footer>
<script>
document.querySelectorAll('.faq-q').forEach(btn=>{
btn.addEventListener('click',()=>{
btn.parentElement.classList.toggle('faq-open');
});
});
</script>
</body></html>"""

    return html


def main():
    """Generate all product pages"""
    os.makedirs(f"{OUTPUT_DIR}/products", exist_ok=True)
    
    # Generate each product page
    for slug, product in PRODUCTS.items():
        html = generate_product_page(slug, product)
        filepath = f"{OUTPUT_DIR}/products/{slug}.html"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ Generated: products/{slug}.html ({len(html)} bytes)")
    
    print(f"\n✅ All {len(PRODUCTS)} product pages generated!")

if __name__ == "__main__":
    main()
