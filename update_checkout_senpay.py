#!/usr/bin/env python3
"""
IA Business Solutions - Mise a jour Checkout avec SenePay + tarifs XOF
"""
import os, re

OUTPUT_DIR = "/home/dom/ia-boutique/dist"

# SenePay Merchant ID
SENPAY_MERCHANT_ID = "72"  # Maurice Olympio

# Tarifs XOF (1 EUR ≈ 655 XOF)
TARIFS_XOF = {
    # Chatbot
    "chatbot-free": {"name": "Chatbot IA — Gratuit", "xof": 0, "period": "mois", "desc": "10 messages/jour, watermark"},
    "chatbot-pro": {"name": "Chatbot IA — Pro", "xof": 19000, "period": "mois", "desc": "5,000 messages/mois, pas de watermark"},
    "chatbot-biz": {"name": "Chatbot IA — Business", "xof": 65000, "period": "mois", "desc": "50,000 messages, multi-langues"},
    # SEO
    "seo-starter": {"name": "Assistant SEO — Starter", "xof": 12500, "period": "mois", "desc": "10 articles/mois"},
    "seo-pro": {"name": "Assistant SEO — Pro", "xof": 32000, "period": "mois", "desc": "50 articles, export WP/Shopify"},
    "seo-biz": {"name": "Assistant SEO — Business", "xof": 65000, "period": "mois", "desc": "Articles illimités, API"},
    # Support
    "support-pro": {"name": "Agent Support — Starter", "xof": 65000, "period": "mois", "desc": "500 résolutions/mois"},
    "support-biz": {"name": "Agent Support — Pro", "xof": 196000, "period": "mois", "desc": "5,000 résolutions, multi-canal"},
    # Réunions
    "reunions-starter": {"name": "Résumeur Réunions — Starter", "xof": 6000, "period": "mois", "desc": "5 heures/mois"},
    "reunions-pro": {"name": "Résumeur Réunions — Pro", "xof": 19000, "period": "mois", "desc": "20 heures, Notion/Slack"},
    # Données
    "data-free": {"name": "Analyste Données — Gratuit", "xof": 0, "period": "mois", "desc": "100 requêtes/mois"},
    "data-pro": {"name": "Analyste Données — Pro", "xof": 32000, "period": "mois", "desc": "2,000 requêtes"},
    "data-biz": {"name": "Analyste Données — Business", "xof": 97500, "period": "mois", "desc": "Illimité, équipe, API"},
    # Contrats
    "contrats-unit": {"name": "Analyse Contrats — à l'unité", "xof": 6000, "unit": True, "desc": "1 document"},
    "contrats-pro": {"name": "Analyse Contrats — Pro", "xof": 19000, "period": "mois", "desc": "20 documents/mois"},
    # Vidéos
    "videos-starter": {"name": "Vidéos Courtes — Starter", "xof": 12500, "period": "mois", "desc": "5 vidéos/mois"},
    "videos-pro": {"name": "Vidéos Courtes — Pro", "xof": 32000, "period": "mois", "desc": "30 vidéos, publication auto"},
    # Recrutement
    "rh-unit": {"name": "Recrutement IA — à l'unité", "xof": 32000, "unit": True, "desc": "1 offre d'emploi"},
    "rh-pro": {"name": "Recrutement IA — Pro", "xof": 97500, "period": "mois", "desc": "Offres illimitées"},
    # Traducteur
    "trad-starter": {"name": "Traducteur IA — Starter", "xof": 12500, "period": "mois", "desc": "10,000 mots/mois"},
    "trad-pro": {"name": "Traducteur IA — Pro", "xof": 32000, "period": "mois", "desc": "50,000 mots, API"},
    # Landing Pages
    "landing-unit": {"name": "Landing Page — à l'unité", "xof": 19000, "unit": True, "desc": "1 page"},
    "landing-pro": {"name": "Landing Pages — Pro", "xof": 65000, "period": "mois", "desc": "10 pages/mois"},
}

def generate_senpay_button(product_id, product_name, amount_xof):
    """Generate SenePay payment button HTML"""
    if amount_xof == 0:
        return f'<a href="#" class="btn btn-p" style="width:100%;justify-content:center" onclick="startFreeTrial(\'{product_id}\')">🧪 Essai gratuit 7 jours</a>'
    
    return f"""
    <form action="https://sene-pay.com/payment/{SENPAY_MERCHANT_ID}" method="POST" target="_blank">
        <input type="hidden" name="product_id" value="{product_id}">
        <input type="hidden" name="product_name" value="{product_name}">
        <input type="hidden" name="amount" value="{amount_xof}">
        <input type="hidden" name="currency" value="XOF">
        <button type="submit" class="btn btn-p" style="width:100%;justify-content:center">💳 Payer {amount_xof:,} XOF via SenePay</button>
    </form>
    <p style="text-align:center;font-size:.75rem;color:var(--text2);margin-top:8px">ou virement (voir RIB ci-dessous)</p>
    """

# Generate the checkout page with XOF prices and SenePay
checkout_html = '''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Commander — IA Business Solutions | Paiement SenePay</title>
<meta name="description" content="Commandez votre solution IA. Paiement securise via SenePay ou virement. Activation sous 24h.">
<link rel="canonical" href="https://ai.dominiqkmendy.com/checkout.html">
<style>
:root{--bg:#08080c;--bg2:#0e0e14;--card:#12121c;--border:#1e1e2e;--accent:#6C5CE7;--accent2:#a29bfe;--glow:rgba(108,92,231,.15);--green:#00b894;--text:#e8e8f0;--text2:#9090a8;--grad:linear-gradient(135deg,#6C5CE7,#a29bfe,#fd79a8)}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);line-height:1.7}
a{color:inherit;text-decoration:none}
header{padding:14px 0;background:rgba(8,8,12,.88);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:100}
.hi{max-width:1200px;margin:0 auto;padding:0 24px;display:flex;justify-content:space-between;align-items:center}
.logo{font-size:1.2rem;font-weight:800;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.logo small{font-size:.6rem;display:block;font-weight:400;color:var(--text2);-webkit-text-fill-color:var(--text2)}
.back{color:var(--text2);font-size:.85rem;padding:8px 16px;border-radius:8px;border:1px solid var(--border)}
section{position:relative;z-index:1}
.wrap{max-width:800px;margin:0 auto;padding:60px 24px 80px}
h1{font-size:clamp(1.6rem,3.5vw,2.4rem);font-weight:800;text-align:center;margin-bottom:8px;background:var(--grad);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.sub{text-align:center;color:var(--text2);margin-bottom:40px;font-size:.95rem}
label{display:block;font-size:.85rem;font-weight:600;margin:16px 0 6px}
input,textarea,select{width:100%;padding:12px 16px;border:1px solid var(--border);border-radius:10px;background:var(--bg);color:var(--text);font-size:.9rem;font-family:inherit;transition:.3s}
input:focus,textarea:focus,select:focus{outline:none;border-color(--accent)}
textarea{min-height:80px;resize:vertical}
.form-row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.card{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:24px;margin-bottom:20px}
.card h3{margin-bottom:16px;font-size:1.1rem}
.summary-row{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--border);font-size:.9rem}
.summary-row:last-child{border-bottom:none;font-weight:700;font-size:1.1rem;color:var(--accent)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;padding:14px 32px;border-radius:10px;font-size:.92rem;font-weight:700;border:none;cursor:pointer;transition:.3s;width:100%}
.btn-p{background:var(--accent);color:#fff}
.btn-p:hover{background:var(--accent2)}
.btn-s{background:#C7772E;color:#fff}
.btn-s:hover{background:#e8a04b}
.btn-w{background:#25D366;color:#fff;margin-top:8px}
.btn-w:hover{background:#1da851}
.pay-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin:20px 0}
.pay-card{background:var(--bg);border:1px solid var(--border);border-radius:12px;padding:16px}
.pay-card h4{color:var(--accent);margin-bottom:6px;font-size:.88rem}
.pay-card p{font-size:.76rem;color:var(--text2);margin:2px 0}
.rib{font-family:'Courier New',monospace;background:var(--bg2);padding:8px;border-radius:6px;font-size:.7rem;margin:4px 0;word-break:break-all}
.trust{display:flex;gap:16px;justify-content:center;margin:24px 0;flex-wrap:wrap}
.trust-item{display:flex;align-items:center;gap:6px;font-size:.78rem;color:var(--text2)}
.step-indicator{display:flex;justify-content:center;gap:8px;margin-bottom:32px}
.step-dot{width:32px;height:32px;border-radius:50%;background:var(--border);color:var(--text2);display:flex;align-items:center;justify-content:center;font-size:.8rem;font-weight:700}
.step-dot.active{background:var(--accent);color:#fff}
.step-dot.done{background:var(--green);color:#fff}
.crypto-banner{background:linear-gradient(135deg,rgba(199,119,46,.1),rgba(0,184,148,.05));border:1px solid #C7772E;border-radius:16px;padding:20px;text-align:center;margin-bottom:24px}
footer{border-top:1px solid var(--border);padding:36px 24px;text-align:center;font-size:.78rem;color:var(--text2)}
footer a{color:var(--accent)}
.hidden{display:none}
@media(max-width:768px){.form-row{grid-template-columns:1fr}.pay-grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<header><div class="hi">
<a href="https://ai.dominiqkmendy.com/" class="logo">IA Business Solutions<small>by Dominiqk Mendy</small></a>
<a href="https://ai.dominiqkmendy.com/" class="back">← Retour</a>
</div></header>

<section class="wrap">
<h1>Commander votre solution IA</h1>
<p class="sub">Paiement sécurisé via SenePay ou virement. Activation sous 24h. Essai gratuit 7 jours.</p>

<div class="crypto-banner">
🚀 <strong>Offre de lancement :</strong> -20% sur tous les abonnements la première année ! Code : <strong>LAUNCH20</strong>
</div>

<div class="step-indicator">
<div class="step-dot active" id="s1">1</div>
<div style="width:40px;height:2px;background:var(--border);align-self:center"></div>
<div class="step-dot" id="s2">2</div>
<div style="width:40px;height:2px;background:var(--border);align-self:center"></div>
<div class="step-dot" id="s3">3</div>
</div>

<!-- ÉTAPE 1 -->
<div id="step1">
<div class="card">
<h3>1. Choisissez votre solution</h3>
<label for="product">Solution IA *</label>
<select id="product" required onchange="updateSummary()">
<option value="">-- Choisir --</option>
<optgroup label="🗣️ Communication">
<option value="chatbot-free|0|Chatbot IA Gratuit">🤖 Chatbot IA — Gratuit (0 XOF, essai 7j)</option>
<option value="chatbot-pro|19000|Chatbot IA Pro">🤖 Chatbot IA — Pro (19,000 XOF/mois)</option>
<option value="chatbot-biz|65000|Chatbot IA Business">🤖 Chatbot IA — Business (65,000 XOF/mois)</option>
<option value="support-pro|65000|Agent Support Starter">🎧 Agent Support — Starter (65,000 XOF/mois)</option>
<option value="support-biz|196000|Agent Support Pro">🎧 Agent Support — Pro (196,000 XOF/mois)</option>
<option value="reunions-starter|6000|Résumeur Réunions Starter">📝 Résumeur Réunions — Starter (6,000 XOF/mois)</option>
<option value="reunions-pro|19000|Résumeur Réunions Pro">📝 Résumeur Réunions — Pro (19,000 XOF/mois)</option>
</optgroup>
<optgroup label="📈 Marketing & Contenu">
<option value="seo-starter|12500|Assistant SEO Starter">✍️ Assistant SEO — Starter (12,500 XOF/mois)</option>
<option value="seo-pro|32000|Assistant SEO Pro">✍️ Assistant SEO — Pro (32,000 XOF/mois)</option>
<option value="seo-biz|65000|Assistant SEO Business">✍️ Assistant SEO — Business (65,000 XOF/mois)</option>
<option value="videos-starter|12500|Vidéos Courtes Starter">🎬 Vidéos Courtes — Starter (12,500 XOF/mois)</option>
<option value="videos-pro|32000|Vidéos Courtes Pro">🎬 Vidéos Courtes — Pro (32,000 XOF/mois)</option>
<option value="landing-unit|19000|Landing Page unitaire">🚀 Landing Page — à l'unité (19,000 XOF)</option>
<option value="landing-pro|65000|Landing Pages Pro">🚀 Landing Pages — Pro (65,000 XOF/mois)</option>
</optgroup>
<optgroup label="⚙️ Opérations">
<option value="data-free|0|Analyste Données Gratuit">📊 Analyste Données — Gratuit (100 requêtes/mois)</option>
<option value="data-pro|32000|Analyste Données Pro">📊 Analyste Données — Pro (32,000 XOF/mois)</option>
<option value="data-biz|97500|Analyste Données Business">📊 Analyste Données — Business (97,500 XOF/mois)</option>
<option value="contrats-unit|6000|Analyse Contrats unitaire">⚖️ Analyse Contrats — à l'unité (6,000 XOF)</option>
<option value="contrats-pro|19000|Analyse Contrats Pro">⚖️ Analyse Contrats — Pro (19,000 XOF/mois)</option>
<option value="trad-starter|12500|Traducteur IA Starter">🌍 Traducteur IA — Starter (12,500 XOF/mois)</option>
<option value="trad-pro|32000|Traducteur IA Pro">🌍 Traducteur IA — Pro (32,000 XOF/mois)</option>
</optgroup>
<optgroup label="👥 Ressources Humaines">
<option value="rh-unit|32000|Recrutement IA unitaire">👔 Recrutement IA — à l'unité (32,000 XOF)</option>
<option value="rh-pro|97500|Recrutement IA Pro">👔 Recrutement IA — Pro (97,500 XOF/mois)</option>
</optgroup>
</select>

<div id="qtyContainer" style="display:none">
<label for="quantity" id="qtyLabel">Quantité</label>
<input type="number" id="quantity" value="1" min="1" max="100" onchange="updateSummary()">
</div>
</div>

<!-- Cross-sell -->
<div class="card" style="background:linear-gradient(135deg,rgba(199,119,46,.05),rgba(0,184,148,.03));border:1px solid #C7772E">
<h3>🔗 Complétez avec l'écosystème Millennium</h3>
<p style="font-size:.85rem;color:var(--text2);margin-bottom:12px">Nos solutions fonctionnent ensemble :</p>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px">
<a href="https://www.sene-pay.com" target="_blank" style="background:var(--bg);padding:14px;border-radius:10px;display:flex;align-items:center;gap:10px">
<div style="font-size:1.5rem">💳</div><div><div style="font-weight:700;font-size:.85rem">SenePay</div><div style="font-size:.75rem;color:var(--text2)">Paiements en ligne</div></div>
</a>
<a href="https://mafacturepro.sn" target="_blank" style="background:var(--bg);padding:14px;border-radius:10px;display:flex;align-items:center;gap:10px">
<div style="font-size:1.5rem">📄</div><div><div style="font-weight:700;font-size:.85rem">MaFacturePro</div><div style="font-size:.75rem;color:var(--text2)">Facturation électronique</div></div>
</a>
</div>
</div>

<div style="text-align:center;margin-top:24px">
<button class="btn btn-p" onclick="goStep(2)" style="width:auto;padding:12px 40px">Continuer →</button>
</div>
</div>

<!-- ÉTAPE 2 -->
<div id="step2" class="hidden">
<div class="card">
<h3>2. Vos coordonnées</h3>
<div class="form-row">
<div><label for="firstName">Prénom *</label><input type="text" id="firstName" required></div>
<div><label for="lastName">Nom *</label><input type="text" id="lastName" required></div>
</div>
<label for="email">Email professionnel *</label><input type="email" id="email" required placeholder="vous@entreprise.com">
<label for="company">Entreprise</label><input type="text" id="company" placeholder="Nom de votre entreprise">
<label for="phone">Téléphone / WhatsApp</label><input type="tel" id="phone" placeholder="+221 77 XXX XXXX">
<label for="message">Message (optionnel)</label><textarea id="message" rows="3" placeholder="Décrivez brièvement votre besoin..."></textarea>
</div>

<div class="card">
<h3>Résumé de votre commande</h3>
<div id="summaryBox"><p style="color:var(--text2);font-size:.85rem">Sélectionnez un produit.</p></div>
</div>

<div style="display:flex;gap:12px;justify-content:center;margin-top:24px">
<button class="btn" onclick="goStep(1)" style="width:auto;padding:12px 30px;background:var(--border)">← Retour</button>
<button class="btn btn-p" onclick="goStep(3)" style="width:auto;padding:12px 40px">Continuer →</button>
</div>
</div>

<!-- ÉTAPE 3: PAIEMENT -->
<div id="step3" class="hidden">
<div class="card">
<h3>3. Payez via SenePay</h3>
<p style="font-size:.85rem;color:var(--text2);margin-bottom:16px">Paiement sécurisé par SenePay — le leader des paiements en Afrique de l'Ouest.</p>
<div id="paySenpay">
<!-- SenePay button generated by JS -->
</div>
<div style="text-align:center;margin-top:16px;font-size:.8rem;color:var(--text2)">
Paiement par carte, Mobile Money, Wave, Orange Money
</div>
</div>

<div class="card">
<h3>Ou par virement bancaire</h3>
<div class="pay-grid">
<div class="pay-card">
<h4>Saham Bank (MAD)</h4><p>Titulaire : FARES ZINEB</p><p>Agence : MARRAKECH MAJORELLE</p>
<div class="rib">RIB : 022 450 0002200029051487 53<br>SWIFT : SGMBMAMC</div>
</div>
<div class="pay-card">
<h4>CIH Bank (MAD)</h4><p>Titulaire : ZINEB FARES</p><p>Agence : MARRAKECH REGENT</p>
<div class="rib">IBAN : MA64 2304 5053 3369 4214 0020 0092<br>SWIFT : CIHMMAMC</div>
</div>
</div>
<p style="font-size:.8rem;color:var(--text2);margin-top:12px">Devises : EUR, USD, GBP, MAD, XOF. Frais à la charge de l'envoyeur.</p>
</div>

<div class="trust">
<div class="trust-item">🔒 Paiement sécurisé</div>
<div class="trust-item">⚡ Activation sous 24h</div>
<div class="trust-item">📧 Confirmation par email</div>
<div class="trust-item">💰 Satisfait ou remboursé 7j</div>
</div>

<div style="text-align:center;margin-top:24px">
<a id="whatsappProof" href="https://wa.me/212607798670" target="_blank" class="btn btn-w" style="font-size:1.05rem;padding:16px 40px">💬 Envoyer la preuve de paiement →</a>
</div>

<div style="text-align:center;margin-top:16px">
<button class="btn" onclick="goStep(2)" style="width:auto;padding:10px 30px;background:transparent;border:1px solid var(--border);color:var(--text2)">← Retour</button>
</div>
</div>

</section>

<footer>
<p>© 2026 Dominiqk Mendy — Millennium Capital Invest LLC | <a href="https://ai.dominiqkmendy.com">ia.dominiqkmendy.com</a> | Paiement sécurisé par SenePay</p>
</footer>

<script>
var senpayMerchant="''' + SENPAY_MERCHANT_ID + '''";
var currentProduct=null;
function goStep(n){
document.getElementById('step1').classList.toggle('hidden',n!==1);
document.getElementById('step2').classList.toggle('hidden',n!==2);
document.getElementById('step3').classList.toggle('hidden',n!==3);
for(var i=1;i<=3;i++){
var d=document.getElementById('s');
if(d){d.classList.remove('active','done');if(i<n)d.classList.add('done');if(i===n)d.classList.add('active');}
}
window.scrollTo({top:0,behavior:'smooth'});
}
function updateSummary(){
var sel=document.getElementById('product');
var opt=sel.options[sel.selectedIndex];
if(!opt.value)return;
var parts=opt.value.split('|');
var id=parts[0],price=parseInt(parts[1]),name=parts[2];
currentProduct={id:id,price:price,name:name};
var qtyInput=document.getElementById('quantity');
var qtyContainer=document.getElementById('qtyContainer');
var isUnit=id.includes('unit');
if(isUnit){qtyContainer.style.display='block';}else{qtyContainer.style.display='none';}
var qty=parseInt(qtyInput.value)||1;
var total=price*qty;
var discount=total*0.20;
var finalTotal=total-discount;
var html='<div class="summary-row"><span>Produit</span><span>'+name+'</span></div>';
if(isUnit)html+='<div class="summary-row"><span>Quantité</span><span>'+qty+'</span></div>';
html+='<div class="summary-row"><span>Sous-total</span><span>'+total.toLocaleString()+' XOF</span></div>';
html+='<div class="summary-row" style="color:var(--green)"><span>Remise LAUNCH20 (-20%)</span><span>-'+discount.toLocaleString()+' XOF</span></div>';
html+='<div class="summary-row"><span>Total</span><span>'+finalTotal.toLocaleString()+' XOF</span></div>';
html+='<div class="summary-row"><span>Activation</span><span>Sous 24h</span></div>';
document.getElementById('summaryBox').innerHTML=html;
var senpayBtn=document.getElementById('paySenpay');
if(finalTotal===0){
senpayBtn.innerHTML='<a href="#" class="btn btn-p" style="width:100%" onclick="startFreeTrial(\\''+id+'\\')">🧪 Lancer l\\'essai gratuit 7 jours</a>';
}else{
senpayBtn.innerHTML='<form action="https://sene-pay.com/payment/'+senpayMerchant+'" method="POST" target="_blank"><input type="hidden" name="product_id" value="'+id+'"><input type="hidden" name="product_name" value="'+name+'"><input type="hidden" name="amount" value="'+finalTotal+'"><input type="hidden" name="currency" value="XOF"><button type="submit" class="btn btn-s" style="width:100%">💳 Payer '+finalTotal.toLocaleString()+' XOF via SenePay</button></form><p style="text-align:center;font-size:.75rem;color:var(--text2);margin-top:8px">Carte, Mobile Money, Wave, Orange Money</p>';
}
var waLink='https://wa.me/212607798670?text=Bonjour%20Dominiqk,%20j%27ai%20pay%C3%A9%20'+finalTotal.toLocaleString()+'%20XOF%20pour%20'+encodeURIComponent(name)+'.%20Voici%20la%20preuve.';
document.getElementById('whatsappProof').href=waLink;
}
function startFreeTrial(productId){
alert('Essai gratuit activé ! Vous recevrez vos accès par email dans 5 minutes.\\n\\nPlan : '+productId+'\\nDurée : 7 jours\\nAucun paiement requis.');
}
</script>
</body></html>'''

with open(f"{OUTPUT_DIR}/checkout.html", "w", encoding="utf-8") as f:
    f.write(checkout_html)
print(f"✅ Checkout updated: {len(checkout_html)} bytes")
