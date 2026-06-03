#!/usr/bin/env python3
"""
IA Business Solutions - Email Templates & Sequences
Templates d'emails automatises pour tout le pipeline client.
"""
from datetime import datetime

# ============================================================
# EMAIL DE BIENVENUE (apres achat + paiement confirme)
# ============================================================

EMAIL_BIENVENUE = """Bonjour {first_name},

Bienvenue chez IA Business Solutions ! 🎉

Votre commande a été confirmée et votre service est maintenant actif.

📋 RÉCAPITULATIF DE VOTRE COMMANDE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Produit : {product_name}
Plan : {plan_name}
Montant : {amount}€ / {period}
Référence : {reference}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 PROCHAINES ÉTAPES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Accédez à votre dashboard :
   → https://ai.dominiqkmendy.com/app/dashboard.html
   Email : {email}
   Mot de passe : {temp_password}

2. Configurez votre solution :
   Uploadez vos documents, personnalisez le bot,
   et copiez le code widget sur votre site.

3. Besoin d'aide ?
   → WhatsApp : https://wa.me/212607798670
   → Email : ia@dominiqkmendy.com
   → Support : https://ai.dominiqkmendy.com/app/dashboard.html

📧 Votre facture est en pièce jointe.

Merci pour votre confiance. On est là pour vous aider à automatiser votre entreprise.

Bien à toi,

Dominiqk Mendy
Fondateur — IA Business Solutions
+212 607 798 670
ia@dominiqkmendy.com
https://ai.dominiqkmendy.com
"""

# ============================================================
# EMAIL DE SUIVI J+3 (apres achat, verifier activation)
# ============================================================

EMAIL_SUIVI_J3 = """Bonjour {first_name},

Je voulais vérifier que tout se passe bien avec votre {product_name}. 🚀

Avez-vous réussi à accéder au dashboard ?
Avez-vous des questions sur la configuration ?

Pour rappel, votre dashboard :
→ https://ai.dominiqkmendy.com/app/dashboard.html

Si vous rencontrez le moindre problème, réponds-moi directement par WhatsApp :
→ https://wa.me/212607798670

J'ai aussi préparé un guide de démarrage rapide :
→ https://ai.dominiqkmendy.com/guide-demarrage.html

À dispo pour toute question.

Dominiqk Mendy
"""

# ============================================================
# EMAIL DE RELANCE PROSPECT (jour 3, pas de reponse)
# ============================================================

EMAIL_PROSPECT_RELANCE_J3 = """Bonjour {first_name},

Je me permets de revenir vers vous suite à mon message sur {original_subject}.

Le marché évolue vite. Dans le {sector}, les entreprises qui automatisent maintenant prendront une avance considérable dans les 6 prochains mois.

Si le timing n'est pas bon, pas de souci — je comprends. Mais si vous avez 15 minutes cette semaine, je suis disponible.

→ https://ai.dominiqkmendy.com

Bonne journée,

Dominiqk Mendy
Expert IA & Automatisation
+212 607 798 670
"""

# ============================================================
# EMAIL DERNIER PROSPECT (jour 7, dernier suivi)
# ============================================================

EMAIL_PROSPECT_DERNIER_J7 = """Bonjour {first_name},

Dernier message, promis 😄

Je sais que vous êtes occupé. Si l'IA n'est pas une priorité pour {company} en ce moment, parfait — gardez mon contact pour plus tard.

En attendant, voici un lien vers quelques résultats concrets :
→ https://ai.dominiqkmendy.com

Bonne continuation,

Dominiqk Mendy
"""

# ============================================================
# EMAIL UPGRADE (client gratuit depuis 14 jours)
# ============================================================

EMAIL_UPGRADE_14J = """Bonjour {first_name},

Cela fait 2 semaines que vous utilisez {product_name} en version gratuite. 🎯

J'espère que vous êtes satisfait ! Pour information, voici ce que vous ratez en restant en gratuit :

✗ Limite de {free_limit} messages/jour (vous l'avez probablement atteinte)
✗ Watermark "Propulsé par IA Business Solutions"
✗ Pas de support prioritaire
✗ Pas d'analytics avancés

Passez au plan Pro à seulement {pro_price}€/mois et débloquez tout :
→ https://ai.dominiqkmendy.com/checkout.html

Questions ? Réponds-moi directement.

Dominiqk Mendy
"""

# ============================================================
# EMAIL RENOUVELLEMENT (j-7 avant expiration abonnement)
# ============================================================

EMAIL_RENOUVELLEMENT = """Bonjour {first_name},

Votre abonnement {product_name} ({plan_name}) expire dans 7 jours. ⏰

Pour éviter toute interruption de service, pensez à renouveler :
→ https://ai.dominiqkmendy.com/checkout.html

Vos informations de paiement :
RIB CIH Bank : MA64 2304 5053 3369 4214 0020 0092 (ZINEB FARES)
Montant : {amount}€

Envoyez la preuve à ia@dominiqkmendy.com ou par WhatsApp.

Merci pour votre confiance continue.

Dominiqk Mendy
"""

# ============================================================
# EMAIL SATISFACTION (j+30, demander temoignage)
# ============================================================

EMAIL_SATISFACTION = """Bonjour {first_name},

Cela fait un mois que vous utilisez {product_name}. 📊

J'aimerais avoir votre retour :
→ Êtes-vous satisfait du service ?
→ Qu'est-ce qui pourrait être amélioré ?
→ Seriez-vous prêt à laisser un témoignage ?

Un petit message de 2 minutes m'aiderait énormément :
→ https://wa.me/212607798670?text=Bonjour%20Dominiqk,%20voici%20mon%20retour%20sur%20{product_name}

Merci d'avance {first_name}.

Dominiqk Mendy
"""

# ============================================================
# EMAIL WIN-BACK (client inactif 60 jours)
# ============================================================

EMAIL_WINBACK = """Bonjour {first_name},

Cela fait un moment qu'on ne s'est pas parlé. J'espère que tout va bien de votre côté.

Je voulais vous informer des nouveautés depuis votre dernière visite :
→ 5 nouvelles solutions IA ajoutées
→ Dashboard client entièrement repensé
→ Tarifs revus à la baisse sur plusieurs produits

Vos données sont toujours là. Reprendre là où vous vous êtes arrêté prend 2 minutes :
→ https://ai.dominiqkmendy.com/app/dashboard.html

Si vous avez besoin d'aide, je suis là.

Dominiqk Mendy
"""

# ============================================================
# Sequences automatisees
# ============================================================

SEQUENCES = {
    "bienvenue_client": [
        {"delay": 0, "template": "bienvenue", "subject": "Bienvenue chez IA Business Solutions ! 🎉"},
        {"delay": 3, "template": "suivi_j3", "subject": "Comment ça va avec votre {product_name} ?"},
        {"delay": 14, "template": "upgrade", "subject": "Débloquez tout le potentiel de votre {product_name}"},
        {"delay": 30, "template": "satisfaction", "subject": "Votre retour compte ! 📊"},
        {"delay": 60, "template": "winback", "subject": "Vous nous manquez ! Voici les nouveautés"},
        {"delay": "renewal_7d", "template": "renouvellement", "subject": "Votre abonnement expire bientôt ⏰"},
    ],
    "prospect_froid": [
        {"delay": 0, "template": "prospect_initial", "subject": None},  # templates A/B/C du prospect.py
        {"delay": 3, "template": "prospect_relance_j3", "subject": "Re: {original_subject}"},
        {"delay": 7, "template": "prospect_dernier_j7", "subject": "Dernier message (puis je vous laisse tranquille)"},
    ]
}

# ============================================================
# Fonction de rendu
# ============================================================

TEMPLATES = {
    "bienvenue": EMAIL_BIENVENUE,
    "suivi_j3": EMAIL_SUIVI_J3,
    "prospect_relance_j3": EMAIL_PROSPECT_RELANCE_J3,
    "prospect_dernier_j7": EMAIL_PROSPECT_DERNIER_J7,
    "upgrade": EMAIL_UPGRADE_14J,
    "renouvellement": EMAIL_RENOUVELLEMENT,
    "satisfaction": EMAIL_SATISFACTION,
    "winback": EMAIL_WINBACK,
}

def render_email(template_name, **kwargs):
    """Render an email template with the given context"""
    template = TEMPLATES.get(template_name, "")
    return template.format(**kwargs)

if __name__ == "__main__":
    # Demo: render welcome email
    print("=" * 60)
    print("EMAIL DE BIENVENUE (demo)")
    print("=" * 60)
    print(render_email(
        "bienvenue",
        first_name="Jean",
        product_name="Chatbot IA — Pro",
        plan_name="Pro",
        amount="29",
        period="mois",
        reference="IA-20260603-JEA12",
        email="jean@example.com",
        temp_password="TempPass123!"
    ))
