/**
 * IA Business Solutions - Chatbot Widget v2.0
 * Widget JS 1-clic UNIVERSEL - Compatible tous frameworks
 * 
 * Usage: <script src="https://ai.dominiqkmendy.com/widget/chatbot-widget.js" data-bot-id="CLIENT_ID" data-theme="dark"></script>
 * 
 * Detection automatique du site et configuration contextuelle.
 * Aucun secret/token cote client.
 */
(function(){
  'use strict';
  
  // ── Detection du site ──
  var hostname = window.location.hostname;
  var sitePresets = {
    'sene-pay.com': { botId: 'SENEPAY_LEAD', theme: 'light', color: '#F59E0B', greeting: 'Bonjour ! Je suis l\'assistant SenePay. Je peux vous aider avec nos solutions IA.' },
    'mafacturepro.sn': { botId: 'MAFACTUREPRO_LEAD', theme: 'dark', color: '#C7772E', greeting: 'Bonjour ! Je suis l\'assistant MaFacturePro. Découvrez nos solutions IA pour votre entreprise.' },
    'senadmin.com': { botId: 'SENADMIN_LEAD', theme: 'dark', color: '#6C5CE7', greeting: 'Bonjour ! Assistant SenAdmin. Besoin d\'automatiser vos processus ?' }
  };
  
  var preset = null;
  for (var d in sitePresets) { if (hostname.indexOf(d) !== -1) { preset = sitePresets[d]; break; } }
  
  // ── Configuration ──
  var scriptTag = document.currentScript || (function(){var s=document.querySelectorAll('script[src*="chatbot-widget"]');return s[s.length-1];})();
  var BOT_ID = (preset ? preset.botId : null) || scriptTag.getAttribute('data-bot-id') || '';
  var THEME = (preset ? preset.theme : null) || scriptTag.getAttribute('data-theme') || 'dark';
  var API_BASE = 'https://ai.dominiqkmendy.com';
  var FREE_LIMIT = 10;
  var sessionMsgCount = 0;
  var visitorEmail = '';
  var emailCollected = false;
  var sessionId = 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2,9);
  var widgetOpen = false;
  
  if (!BOT_ID) { console.warn('[ChatbotWidget] data-bot-id manquant'); return; }
  
  // ── Thème couleurs ──
  var isDark = THEME === 'dark';
  var colors = {
    bg: isDark ? '#12121c' : '#ffffff',
    bg2: isDark ? '#1a1a2e' : '#f5f5f7',
    header: (preset ? preset.color : null) || '#6C5CE7',
    text: isDark ? '#e8e8f0' : '#1a1a2e',
    text2: isDark ? '#9090a8' : '#6b6b80',
    border: isDark ? '#1e1e2e' : '#e0e0e8',
    accent: (preset ? preset.color : null) || '#6C5CE7',
    userMsg: isDark ? '#6C5CE7' : '#6C5CE7',
    botMsg: isDark ? '#1e1e2e' : '#f0f0f5',
    inputBg: isDark ? '#0e0e14' : '#ffffff'
  };
  
  // ── CSS ──
  var css = `
  #ia-chatbot *{box-sizing:border-box;margin:0;padding:0;font-family:'Segoe UI',system-ui,sans-serif}
  #ia-chatbot-launcher{position:fixed;bottom:24px;right:24px;z-index:99999;width:56px;height:56px;border-radius:50%;background:${colors.accent};color:#fff;border:none;cursor:pointer;box-shadow:0 4px 20px rgba(0,0,0,.3);display:flex;align-items:center;justify-content:center;font-size:24px;transition:.3s}
  #ia-chatbot-launcher:hover{transform:scale(1.1)}
  #ia-chatbot{position:fixed;bottom:90px;right:24px;z-index:99999;width:380px;height:520px;background:${colors.bg};border:1px solid ${colors.border};border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,.4);display:none;flex-direction:column;overflow:hidden}
  #ia-chatbot.open{display:flex}
  .ia-cb-header{background:${colors.header};color:#fff;padding:16px 20px;display:flex;align-items:center;gap:10px;flex-shrink:0}
  .ia-cb-header .title{font-weight:700;font-size:.95rem;flex:1}
  .ia-cb-header .close-btn{background:rgba(255,255,255,.2);border:none;color:#fff;width:28px;height:28px;border-radius:50%;cursor:pointer;font-size:14px;display:flex;align-items:center;justify-content:center}
  .ia-cb-messages{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:10px}
  .ia-cb-msg{padding:10px 14px;border-radius:14px;font-size:.85rem;line-height:1.5;max-width:85%}
  .ia-cb-msg.bot{background:${colors.botMsg};color:${colors.text};border:1px solid ${colors.border};align-self:flex-start}
  .ia-cb-msg.user{background:${colors.accent};color:#fff;align-self:flex-end}
  .ia-cb-msg.error{background:#e74c3c20;color:#e74c3c;border:1px solid #e74c3c40;align-self:flex-start}
  .ia-cb-msg.upgrade{background:linear-gradient(135deg,rgba(108,92,231,.1),rgba(0,184,148,.05));border:1px solid ${colors.accent};color:${colors.text};align-self:flex-start;text-align:center}
  .ia-cb-msg.upgrade a{color:${colors.accent};font-weight:700}
  .ia-cb-typing{padding:10px 14px;color:${colors.text2};font-size:.8rem;font-style:italic}
  .ia-cb-input{border-top:1px solid ${colors.border};padding:12px;display:flex;gap:8px;flex-shrink:0;background:${colors.bg2}}
  .ia-cb-input input{flex:1;padding:10px 14px;border:1px solid ${colors.border};border-radius:10px;background:${colors.inputBg};color:${colors.text};font-size:.85rem;outline:none}
  .ia-cb-input input:focus{border-color:${colors.accent}}
  .ia-cb-input button{background:${colors.accent};color:#fff;border:none;padding:10px 16px;border-radius:10px;cursor:pointer;font-weight:700;font-size:.8rem;white-space:nowrap}
  .ia-cb-email-collect{padding:16px;text-align:center}
  .ia-cb-email-collect input{width:100%;margin:8px 0;padding:10px 14px;border:1px solid ${colors.border};border-radius:10px;background:${colors.inputBg};color:${colors.text};font-size:.85rem;outline:none}
  .ia-cb-email-collect button{width:100%;padding:10px;background:${colors.accent};color:#fff;border:none;border-radius:10px;cursor:pointer;font-weight:700}
  .ia-cb-footer{text-align:center;padding:6px;font-size:.65rem;color:${colors.text2};border-top:1px solid ${colors.border}}
  .ia-cb-footer a{color:${colors.accent}}
  @media(max-width:480px){
    #ia-chatbot{width:calc(100% - 32px);right:16px;bottom:80px;height:70vh}
    #ia-chatbot-launcher{bottom:16px;right:16px}
  }
  `;
  
  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);
  
  // ── HTML ──
  var launcher = document.createElement('button');
  launcher.id = 'ia-chatbot-launcher';
  launcher.innerHTML = '💬';
  launcher.title = 'Assistant IA';
  launcher.onclick = toggleWidget;
  document.body.appendChild(launcher);
  
  var widget = document.createElement('div');
  widget.id = 'ia-chatbot';
  widget.innerHTML = `
    <div class="ia-cb-header">
      <span class="title">🤖 Assistant IA</span>
      <button class="close-btn" onclick="document.getElementById('ia-chatbot').classList.remove('open');widgetOpen=false">✕</button>
    </div>
    <div class="ia-cb-messages" id="iaCbMsgs"></div>
    <div class="ia-cb-input">
      <input type="text" id="iaCbInput" placeholder="Tapez votre message..." onkeydown="if(event.key==='Enter'){iaSendMessage()}">
      <button onclick="iaSendMessage()">Envoyer</button>
    </div>
    <div class="ia-cb-footer">Propulsé par <a href="${API_BASE}" target="_blank">IA Business Solutions</a></div>
  `;
  document.body.appendChild(widget);
  
  // Exposer les fonctions globalement
  window.iaSendMessage = sendMessage;
  
  function toggleWidget() {
    widgetOpen = !widgetOpen;
    widget.classList.toggle('open', widgetOpen);
    if (widgetOpen && !emailCollected) {
      requestEmail();
    } else if (widgetOpen && emailCollected) {
      showMessage('bot', (preset ? preset.greeting : 'Bonjour ! Comment puis-je vous aider ?'));
    }
  }
  
  // Close button
  widget.querySelector('.close-btn').onclick = function() {
    widget.classList.remove('open');
    widgetOpen = false;
  };
  
  function requestEmail() {
    var msgs = document.getElementById('iaCbMsgs');
    msgs.innerHTML = '';
    var emailDiv = document.createElement('div');
    emailDiv.className = 'ia-cb-email-collect';
    emailDiv.innerHTML = `
      <div style="font-weight:700;margin-bottom:8px;color:${colors.text}">👋 Bienvenue !</div>
      <div style="font-size:.85rem;color:${colors.text2};margin-bottom:12px">Pour commencer, entrez votre email. C'est gratuit.</div>
      <input type="email" id="iaCbEmailInput" placeholder="votre@email.com" onkeydown="if(event.key==='Enter'){iaCollectEmail()}">
      <button onclick="iaCollectEmail()">Commencer →</button>
    `;
    msgs.appendChild(emailDiv);
  }
  
  window.iaCollectEmail = function() {
    var email = document.getElementById('iaCbEmailInput').value.trim();
    if (!email || email.indexOf('@') === -1) { alert('Email invalide'); return; }
    visitorEmail = email;
    emailCollected = true;
    
    // Stocker le lead
    fetch(API_BASE + '/api/leads', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email: email, bot_id: BOT_ID, source: hostname, ts: Date.now()})
    }).catch(function(){});
    
    var msgs = document.getElementById('iaCbMsgs');
    msgs.innerHTML = '';
    showMessage('bot', (preset ? preset.greeting : 'Bonjour ! Comment puis-je vous aider aujourd\'hui ?'));
  };
  
  function showMessage(role, text, extraClass) {
    var msgs = document.getElementById('iaCbMsgs');
    var msg = document.createElement('div');
    msg.className = 'ia-cb-msg ' + role + (extraClass ? ' ' + extraClass : '');
    msg.textContent = text;
    msgs.appendChild(msg);
    msgs.scrollTop = msgs.scrollHeight;
  }
  
  function showTyping() {
    var msgs = document.getElementById('iaCbMsgs');
    var typing = document.createElement('div');
    typing.className = 'ia-cb-typing';
    typing.id = 'iaCbTyping';
    typing.textContent = 'L\'IA écrit...';
    msgs.appendChild(typing);
    msgs.scrollTop = msgs.scrollHeight;
  }
  
  function hideTyping() {
    var t = document.getElementById('iaCbTyping');
    if (t) t.remove();
  }
  
  function sendMessage() {
    var input = document.getElementById('iaCbInput');
    var text = input.value.trim();
    if (!text) return;
    input.value = '';
    
    showMessage('user', text);
    sessionMsgCount++;
    
    if (sessionMsgCount > FREE_LIMIT) {
      showMessage('bot', 'Vous avez atteint la limite gratuite de ' + FREE_LIMIT + ' messages. Passez au Pro pour continuer !', 'upgrade');
      var upgradeLink = document.createElement('div');
      upgradeLink.style.marginTop = '8px';
      upgradeLink.innerHTML = '<a href="' + API_BASE + '/#tarifs" target="_blank" style="color:' + colors.accent + ';font-weight:700">Voir les plans →</a>';
      document.getElementById('iaCbMsgs').appendChild(upgradeLink);
      return;
    }
    
    showTyping();
    
    // Messages specifiques au site
    var siteResponses = {
      'sene-pay': {
        'paiement': 'SenePay accepte Orange Money, Wave et Free Money. Intégration en 5 minutes. 1.8% flat. Voulez-vous un devis ?',
        'tarif': 'Nos tarifs commencent à 1.8% par transaction. Pas de frais cachés. Pas de frais d\'inscription.',
        'intégration': 'L\'intégration prend 5 minutes. API REST, plugins WordPress et Shopify disponibles. Documentation : https://docs.sene-pay.com'
      },
      'mafacturepro': {
        'facture': 'MaFacturePro génère des factures électroniques conformes aux normes sénégalaises. Dès 29€/mois.',
        'dgi': 'Nos factures sont 100% conformes aux exigences de la DGI Sénégal. Export PDF, envoi automatique, archivage.'
      }
    };
    
    // Chercher une reponse specifique
    var lowerText = text.toLowerCase();
    var responded = false;
    for (var site in siteResponses) {
      if (hostname.indexOf(site) !== -1) {
        for (var keyword in siteResponses[site]) {
          if (lowerText.indexOf(keyword) !== -1) {
            setTimeout(function(response) {
              hideTyping();
              showMessage('bot', response);
            }, 800, siteResponses[site][keyword]);
            responded = true;
            break;
          }
        }
      }
    }
    
    if (!responded) {
      // Appeler l'API IA
      fetch(API_BASE + '/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          messages: [{role: 'user', content: text}],
          bot_id: BOT_ID,
          session_id: sessionId,
          visitor_email: visitorEmail
        })
      })
      .then(function(r) { return r.json(); })
      .then(function(data) {
        hideTyping();
        if (data.limit_reached) {
          showMessage('bot', 'Limite gratuite atteinte. Passez au Pro !', 'upgrade');
        } else if (data.reply) {
          showMessage('bot', data.reply);
        } else if (data.error) {
          showMessage('bot', 'Erreur temporaire. Réessayez ou contactez-nous sur WhatsApp.', 'error');
        }
      })
      .catch(function() {
        hideTyping();
        showMessage('bot', 'Je suis temporairement indisponible. Contactez-nous sur WhatsApp : https://wa.me/212607798670', 'error');
      });
    }
  }
  
  // Auto-open apres 30s si pas encore interacte
  setTimeout(function() {
    if (!widgetOpen && !emailCollected) {
      launcher.style.animation = 'ia-pulse 2s infinite';
    }
  }, 30000);
  
  // Ajouter animation pulse
  var animStyle = document.createElement('style');
  animStyle.textContent = '@keyframes ia-pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.15)}}';
  document.head.appendChild(animStyle);
  
})();
