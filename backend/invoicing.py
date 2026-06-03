#!/usr/bin/env python3
"""
IA Business Solutions - Systeme de Facturation Automatique
Genere des factures PDF et les envoie par email au client + copie comptable (Zineb FARES).
"""
import os, json, subprocess
from datetime import datetime, timedelta
from typing import Dict, Optional

# ============================================================
# CONFIG
# ============================================================

# Zineb FARES - Comptable / Associee
COMPTABLE_EMAIL = "zineb@millenniumcapitalinvest.com"
SENDER_EMAIL = "ia@dominiqkmendy.com"
SENDER_NAME = "IA Business Solutions - Dominiqk Mendy"

# Informations bancaires pour les factures
PAYMENT_INFO = {
    "bank_1": {
        "bank": "Saham Bank",
        "titulaire": "FARES ZINEB",
        "agence": "MARRAKECH MAJORELLE",
        "rib": "022 450 0002200029051487 53",
        "swift": "SGMBMAMC",
        "devise": "MAD (accepte EUR, USD, GBP, XOF)"
    },
    "bank_2": {
        "bank": "CIH Bank",
        "titulaire": "ZINEB FARES",
        "agence": "MARRAKECH REGENT",
        "iban": "MA64 2304 5053 3369 4214 0020 0092",
        "rib": "230 450 5333694214002000 92",
        "swift": "CIHMMAMC",
        "devise": "MAD (accepte EUR, USD, GBP, XOF)"
    }
}

# Services et tarifs
SERVICES = {
    "agent-ia": {"name": "Agent IA Conversationnel", "price": 2500, "currency": "EUR", "delai": "7-14 jours"},
    "automatisation": {"name": "Automatisation IA Complete", "price": 3500, "currency": "EUR", "delai": "14-21 jours"},
    "predictif": {"name": "Analyse Predictive & BI IA", "price": 4500, "currency": "EUR", "delai": "14-21 jours"},
    "metier": {"name": "Agent IA Specialise Metier", "price": 5000, "currency": "EUR", "delai": "21-30 jours"},
    "api": {"name": "Integration API IA", "price": 1800, "currency": "EUR", "delai": "5-10 jours"},
    "formation": {"name": "Formation IA Enterprise", "price": 2000, "currency": "EUR", "delai": "Sur mesure"},
    "audit": {"name": "Audit IA Express", "price": 500, "currency": "EUR", "delai": "3-5 jours"},
}

# ============================================================
# FACTURE GENERATOR (HTML -> PDF)
# ============================================================

def generate_invoice_html(invoice_data: Dict) -> str:
    """Generate a professional HTML invoice"""
    num = invoice_data["numero"]
    date = invoice_data["date"]
    client = invoice_data["client"]
    service = invoice_data["service"]
    amount_ht = invoice_data["amount_ht"]
    tva = invoice_data.get("tva", 0)
    amount_ttc = invoice_data["amount_ttc"]
    currency = invoice_data.get("currency", "EUR")
    payment_method = invoice_data.get("payment_method", "Virement bancaire")
    due_date = invoice_data.get("due_date", "")
    
    # Payment instructions
    bank2 = PAYMENT_INFO["bank_2"]
    bank1 = PAYMENT_INFO["bank_1"]
    
    html = f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<style>
@page {{ size: A4; margin: 2cm; }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #333; font-size: 14px; line-height: 1.6; }}
.invoice-box {{ max-width: 800px; margin: 0 auto; }}
.header {{ display: flex; justify-content: space-between; margin-bottom: 40px; }}
.logo {{ font-size: 24px; font-weight: 700; color: #6C5CE7; }}
.logo small {{ display: block; font-size: 11px; color: #999; font-weight: 400; }}
.invoice-title {{ font-size: 28px; font-weight: 300; color: #999; text-align: right; }}
.meta {{ display: flex; justify-content: space-between; margin-bottom: 30px; }}
.meta-box {{ width: 45%; }}
.meta-label {{ font-size: 11px; color: #999; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }}
table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
th {{ background: #f8f9fa; text-align: left; padding: 12px; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; color: #666; border-bottom: 2px solid #ddd; }}
td {{ padding: 12px; border-bottom: 1px solid #eee; }}
.text-right {{ text-align: right; }}
.total-row {{ font-weight: 700; font-size: 18px; background: #f0f0ff; }}
.payment {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin-top: 30px; }}
.payment h3 {{ color: #6C5CE7; margin-bottom: 12px; }}
.rib {{ font-family: 'Courier New', monospace; background: #fff; padding: 8px; border-radius: 4px; margin: 4px 0; font-size: 12px; }}
.footer {{ text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #999; }}
</style></head><body>
<div class="invoice-box">
<div class="header">
<div>
<div class="logo">IA Business Solutions<small>by Dominiqk Mendy</small></div>
<div style="margin-top:16px;font-size:13px;color:#666">
Dominique Maurice Olympio Mendy<br>
Millennium Capital Invest LLC<br>
Marrakech, Maroc<br>
contact@ia.dominiqkmendy.com<br>
+212 607 798 670
</div>
</div>
<div>
<div class="invoice-title">FACTURE</div>
<div style="text-align:right;font-size:13px;color:#666;margin-top:8px">
<strong>N° :</strong> {num}<br>
<strong>Date :</strong> {date}<br>
<strong>Echeance :</strong> {due_date}<br>
</div>
</div>
</div>

<div class="meta">
<div class="meta-box">
<div class="meta-label">Facture a</div>
<div style="font-size:14px">
<strong>{client.get('name', '')}</strong><br>
{client.get('company', '')}<br>
{client.get('address', '')}<br>
{client.get('email', '')}<br>
{client.get('country', '')}<br>
</div>
</div>
<div class="meta-box">
<div class="meta-label">Details projet</div>
<div style="font-size:14px">
<strong>Service :</strong> {service.get('name', '')}<br>
<strong>Delai de livraison :</strong> {service.get('delai', '')}<br>
<strong>Methode de paiement :</strong> {payment_method}<br>
</div>
</div>
</div>

<table>
<tr><th>Description</th><th>Quantite</th><th class="text-right">Prix unitaire</th><th class="text-right">Total</th></tr>
<tr>
<td><strong>{service.get('name', '')}</strong><br><span style="color:#999;font-size:12px">{service.get('description', '')}</span></td>
<td>1</td>
<td class="text-right">{amount_ht:,.2f} {currency}</td>
<td class="text-right">{amount_ht:,.2f} {currency}</td>
</tr>
<tr><td colspan="3" class="text-right">Sous-total HT</td><td class="text-right">{amount_ht:,.2f} {currency}</td></tr>
<tr><td colspan="3" class="text-right">TVA ({invoice_data.get('tva_rate', '0')}%)</td><td class="text-right">{tva:,.2f} {currency}</td></tr>
<tr class="total-row"><td colspan="3" class="text-right">TOTAL TTC</td><td class="text-right">{amount_ttc:,.2f} {currency}</td></tr>
</table>

<div class="payment">
<h3>Instructions de paiement</h3>
<p>Pour regler cette facture, effectuez un virement bancaire vers l'un des comptes suivants :</p>
<p><strong>Devises acceptees :</strong> EUR, USD, GBP, MAD, XOF - Frais de transfert a la charge de l'envoyeur.</p>

<p><strong>Option 1 — Saham Bank (MAD)</strong></p>
<div class="rib">
Titulaire : {bank1['titulaire']} | Agence : {bank1['agence']}<br>
RIB : {bank1['rib']} | SWIFT : {bank1['swift']}
</div>

<p><strong>Option 2 — CIH Bank (MAD) [Recommande]</strong></p>
<div class="rib">
Titulaire : {bank2['titulaire']} | Agence : {bank2['agence']}<br>
IBAN : {bank2['iban']}<br>
RIB : {bank2['rib']} | BIC/SWIFT : {bank2['swift']}
</div>

<p style="margin-top:16px;font-size:12px;color:#666">
Merci de mentionner le numero de facture <strong>{num}</strong> dans le motif du virement.<br>
Un accusé de reception sera envoye automatiquement et le projet demarrera sous 48h.
</p>
</div>

<div class="footer">
<p>Millennium Capital Invest LLC | IA Business Solutions<br>
Facture generee automatiquement le {date}<br>
Pour toute question : ia@dominiqkmendy.com | +212 607 798 670</p>
</div>
</div></body></html>"""
    return html

def create_invoice(client_email, service_key, custom_price=None):
    """Create a full invoice for a sale"""
    service = SERVICES.get(service_key, {"name": service_key, "price": 0, "currency": "EUR", "delai": "Sur mesure"})
    price = custom_price or service.get("price", 0)
    currency = service.get("currency", "EUR")
    
    # Calculate amounts
    tva_rate = 0  # Exo de TVA pour les services export / micro-entreprise
    amount_ht = price
    tva = price * tva_rate / 100 if tva_rate else 0
    amount_ttc = amount_ht + tva
    
    # Invoice number
    now = datetime.now()
    invoice_num = f"IA-{now.strftime('%Y%m%d')}-{client_email[:3].upper()}{now.strftime('%H%M')}"
    
    invoice_data = {
        "numero": invoice_num,
        "date": now.strftime("%d/%m/%Y"),
        "due_date": (now + timedelta(days=15)).strftime("%d/%m/%Y"),
        "client": client_email,
        "service": service,
        "amount_ht": amount_ht,
        "tva_rate": tva_rate,
        "tva": tva,
        "amount_ttc": amount_ttc,
        "currency": currency,
        "payment_method": "Virement bancaire"
    }
    
    # Generate HTML
    html_content = generate_invoice_html(invoice_data)
    
    # Save to file
    invoice_dir = os.path.expanduser(f"~/.hermes/ia-boutique/invoices/{now.strftime('%Y-%m')}")
    os.makedirs(invoice_dir, exist_ok=True)
    
    html_path = os.path.join(invoice_dir, f"{invoice_num}.html")
    pdf_path = os.path.join(invoice_dir, f"{invoice_num}.pdf")
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Convert to PDF using wkhtmltopdf or weasyprint
    try:
        subprocess.run(["wkhtmltopdf", "--page-size", "A4", html_path, pdf_path], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        try:
            import weasyprint
            weasyprint.HTML(string=html_content).write_pdf(pdf_path)
        except ImportError:
            print("PDF generation not available, HTML saved")
            pdf_path = None
    
    # Save invoice record
    record_file = os.path.join(invoice_dir, "invoices.json")
    records = []
    if os.path.exists(record_file):
        with open(record_file) as f:
            records = json.load(f)
    records.append(invoice_data)
    with open(record_file, "w") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    
    print(f"Facture creee: {invoice_num}")
    print(f"  Montant: {amount_ttc:,.2f} {currency}")
    print(f"  HTML: {html_path}")
    print(f"  PDF: {pdf_path}")
    
    return {
        "invoice_num": invoice_num,
        "html_path": html_path,
        "pdf_path": pdf_path,
        "data": invoice_data
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["create", "list"])
    parser.add_argument("--email", help="Client email")
    parser.add_argument("--service", help="Service key")
    parser.add_argument("--price", type=float, help="Custom price")
    parser.add_argument("--month", help="Month to list (YYYY-MM)")
    args = parser.parse_args()
    
    if args.action == "create" and args.email and args.service:
        create_invoice(args.email, args.service, args.price)
    elif args.action == "list":
        month = args.month or datetime.now().strftime("%Y-%m")
        record_file = os.path.expanduser(f"~/.hermes/ia-boutique/invoices/{month}/invoices.json")
        if os.path.exists(record_file):
            with open(record_file) as f:
                records = json.load(f)
            total = sum(r["amount_ttc"] for r in records)
            print(f"Factures {month}: {len(records)} | Total: {total:,.2f} EUR")
            for r in records:
                print(f"  {r['numero']}: {r['amount_ttc']:,.2f} {r['currency']} - {r['service']['name']}")
        else:
            print(f"Aucune facture pour {month}")
