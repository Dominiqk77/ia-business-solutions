/**
 * IA Business Solutions — Chatbot Widget v1.0
 * Widget JS 1-clic pour chatbot IA clé en main
 * 
 * Usage: <script src="https://ai.dominiqkmendy.com/widget/chatbot-widget.js" data-bot-id="CLIENT_ID" data-theme="dark"></script>
 * 
 * Aucun secret/token client — toutes les clés API sont côté serveur (CF Pages env vars)
 */
(function(){
  'use strict';

  // ── Configuration depuis les data-attributes ──
  var scriptTag = document.currentScript || (function(){var s=document.querySelectorAll('script[src*="chatbot-widget"]');return s[s.length-1];})();
  var BOT_ID = scriptTag.getAttribute('data-bot-id') || '';
  var THEME = scriptTag.getAttribute('data-theme') || 'dark';
  var API_BASE = 'https://ai.dominiqkmendy.com';

  // ── Validate bot_id ──
  if(!BOT_ID){
    console.warn('[ChatbotWidget] data-bot-id manquant. Le widget ne sera pas initialisé.');
    return;
  }

  // ── Free tier limit ──
  var FREE_LIMIT = 10;
  var sessionMsgCount = 0;
  var visitorEmail = '';
  var emailCollected = false;
  var sessionId = 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2,9);

  // ── CSS injection ──
  var isDark = THEME === 'dark';
  var colors = {
    bg: isDark ? '#12121c' : '#ffffff',
    bg2: isDark ? '#1a1a2e' : '#f5f5f7',
    header: isDark ? '#6C5CE7' : '#6C5CE7',
    text: isDark ? '#e8e8f0' : '#1a1a2e',
    text2: isDark ? '#9090a8' : '#6b6b80',
    border: isDark ? '#1e1e2e' : '#e0e0e8',
    accent: '#6C5CE7',
    accent2: '#a29bfe',
    userMsg: isDark ? '#6C5CE7' : '#6C5CE7',
    botMsg: isDark ? '#1e1e2e' : '#f0f0f5',
    inputBg: isDark ? '#0e0e14' : '#ffffff',
    white: '#ffffff',
    green: '#00b894',
    shadow: '0 8px 40px rgba(0,0,0,0.3)'
  };

  var css = `
  .cbw-reset{all:unset;box-sizing:border-box}
  .cbw-reset *{box-sizing:border-box;margin:0;padding:0}
  @keyframes cbw-bounce{0%,100%{transform:scale(1)}50%{transform:scale(1.1)}}
  @keyframes cbw-slideUp{from{opacity:0;transform:translateY(20px) scale(0.95)}to{opacity:1;transform:translateY(0) scale(1)}}
  @keyframes cbw-fadeIn{from{opacity:0}to{opacity:1}}
  @keyframes cbw-typing{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-4px)}}
  .cbw-fab{position:fixed;bottom:24px;right:24px;z-index:99999;width:60px;height:60px;border-radius:50%;background:${colors.accent};border:none;cursor:pointer;box-shadow:0 4px 24px rgba(108,92,231,.4);display:flex;align-items:center;justify-content:center;transition:all .3s;font-size:28px;animation:cbw-bounce 2s infinite}
  .cbw-fab:hover{transform:scale(1.1);box-shadow:0 6px 32px rgba(108,92,231,.5)}
  .cbw-fab.hidden{display:none}
  .cbw-window{position:fixed;bottom:24px;right:24px;z-index:99999;width:380px;height:560px;max-height:80vh;border-radius:20px;overflow:hidden;box-shadow:${colors.shadow};font-family:'Segoe UI',system-ui,-apple-system,sans-serif;display:flex;flex-direction:column;animation:cbw-slideUp .3s ease;transition:all .3s}
  .cbw-window.cbw-light{background:${colors.bg};border:1px solid ${colors.border}}
  .cbw-window.cbw-dark{background:${colors.bg};border:1px solid ${colors.border}}
  .cbw-window.cbw-minimized{height:60px!important;overflow:hidden}
  .cbw-window.cbw-closed{display:none}
  .cbw-header{padding:16px 18px;display:flex;align-items:center;justify-content:space-between;background:${colors.header};color:${colors.white};cursor:pointer;user-select:none}
  .cbw-header-left{display:flex;align-items:center;gap:10px}
  .cbw-avatar{width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.2);display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0}
  .cbw-title-text{font-size:.95rem;font-weight:700}
  .cbw-subtitle{font-size:.7rem;opacity:.8;font-weight:400}
  .cbw-header-btns{display:flex;gap:4px}
  .cbw-hdr-btn{background:rgba(255,255,255,.15);border:none;color:${colors.white};width:28px;height:28px;border-radius:50%;cursor:pointer;font-size:14px;display:flex;align-items:center;justify-content:center;transition:.2s}
  .cbw-hdr-btn:hover{background:rgba(255,255,255,.3)}
  .cbw-messages{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:10px;min:0}
  .cbw-messages::-webkit-scrollbar{width:4px}
  .cbw-messages::-webkit-scrollbar-track{background:transparent}
  .cbw-messages::-webkit-scrollbar-thumb{background:${colors.border};border-radius:4px}
  .cbw-msg{display:flex;gap:8px;max-width:85%;animation:cbw-fadeIn .3s ease}
  .cbw-msg{align-self:flex-end}
  .cbw-msg-bot{align-self:flex-start}
  .cbw-msg-avatar{width:28px;height:28px;border-radius:50%;font-size:14px;display:flex;align-items:center;justify-content:center;flex-shrink:0;margin-top:4px}
  .cbw-msg-bot .cbw-msg-avatar{background:${colors.header};color:#fff}
  .cbw-msg-user .cbw-msg-avatar{background:${colors.accent};color:#fff;order:2}
  .cbw-msg-bubble{padding:10px 14px;border-radius:16px;font-size:.85rem;line-height:1.5;word-wrap:break-word}
  .cbw-msg-bot .cbw-msg-bubble{background:${colors.botMsg};color:${colors.text};border-bottom-left-radius:4px}
  .cbw-msg-user .cbw-msg-bubble;background:${colors.userMsg};color:#fff;border-bottom-right-radius:4px;order:1;margin-right:8px}
  .cbw-typing{display:flex;gap:4px;padding:12px 16px;background:${colors.botMsg};border-radius:16px;border-bottom-left-radius:4px;width:52px;align-self:flex-start}
  .cbw-typing span{width:7px;height:7px;border-radius:50%;background:${colors.accent};display:inline-block}
  .cbw-typing span:nth-child(1){animation:cbw-typing .6s .0s infinite}
  .cbw-typing span:nth-child(2){animation:cbw-typing .6s .15s infinite}
  .cbw-typing span:nth-child(3){animation:cbw-typing .6s .3s infinite}
  .cbw-email-collect{padding:20px;text-align:center;animation:cbw-fadeIn .3s ease}
  .cbw-email-collect h3{font-size:1rem;color:${colors.text};margin-bottom:6px}
  .cbw-email-collect p{font-size:.78rem;color:${colors.text2};margin-bottom:16px}
  .cbw-email-input{width:100%;padding:11px 14px;border:1px solid ${colors.border};border-radius:10px;background:${colors.inputBg};color:${colors.text};font-size:.85rem;font-family:inherit;margin-bottom:10px;outline:none;transition:.2s}
  .cbw-email-input:focus{border-color:${colors.accent};box-shadow:0 0 0 3px rgba(108,92,231,.1)}
  .cbw-email-btn{width:100%;padding:11px;border:none;border-radius:10px;background:${colors.accent};color:#fff;font-size:.88rem;font-weight:700;cursor:pointer;transition:.2s;font-family:inherit}
  .cbw-email-btn:hover{background:${colors.accent2}}
  .cbw-email-btn:disabled{opacity:.6;cursor:not-allowed}
  .cbw-error-msg{font-size:.75rem;color:#ff6b6b;margin-top:8px;display:none}
  .cbw-input-area{padding:12px 14px;border-top:1px solid ${colors.border};display:flex;gap:8px;align-items:center;background:${colors.bg}}
  .cbw-input{flex:1;padding:10px 14px;border:1px solid ${colors.border};border-radius:22px;background:${colors.inputBg};color:${colors.text};font-size:.85rem;font-family:inherit;outline:none;transition:.2s}
  .cbw-input:focus{border-color:${colors.accent};box-shadow:0 0 0 3px rgba(108,92,231,.1)}
  .cbw-input::placeholder{color:${colors.text2}}
  .cbw-send{width:40px;height:40px;border-radius:50%;border:none;background:${colors.accent};color:#fff;font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:.2s}
  .cbw-send:hover{background:${colors.accent2}}
  .cbw-send:disabled{opacity:.4;cursor:not-allowed}
  .cbw-upgrade{padding:10px 14px;text-align:center;background:linear-gradient(135deg,rgba(108,92,231,.08),rgba(253,121,168,.05));border-top:1px solid ${colors.border}}
  .cbw-upgrade a{font-size:.78rem;color:${colors.accent2};text-decoration:none;font-weight:600}
  .cbw-upgrade a:hover{text-decoration:underline}
  .cbw-counter{font-size:.68rem;color:${colors.text2};text-align:center;padding:4px}
  .cbw-reached .cbw-input-area{display:none}
  @media(max-width:440px){.cbw-window{width:calc(100% - 24px);right:12px;bottom:12px;height:70vh;max-height:70vh}}
  `;

  var styleEl = document.createElement('style');
  styleEl.textContent = css;
  document.head.appendChild(styleEl);

  // ── DOM Construction ──
  var container = document.createElement('div');
  container.className = 'cbw-reset';
  document.body.appendChild(container);

  // FAB button
  var fab = document.createElement('button');
  fab.className = 'cbw-fab';
  fab.innerHTML = '💬';
  fab.setAttribute('aria-label', 'Ouvrir le chat');
  container.appendChild(fab);

  // Chat window
  var win = document.createElement('div');
  win.className = 'cbw-window cbw-' + (isDark?'dark':'light') + ' cbw-closed';
  container.appendChild(win);

  // Header
  var header = document.createElement('div');
  header.className = 'cbw-header';
  header.innerHTML = '<div class="cbw-header-left"><div class="cbw-avatar">🤖</div><div><div class="cbw-title-text">Assistant IA</div><div class="cbw-subtitle"></div></div></div>';
  var hdrBtns = document.createElement('div');
  hdrBtns.className = 'cbw-header-btns';
  var btnMin = document.createElement('button');
  btnMin.className = 'cbw-hdr-btn';
  btnMin.innerHTML = '−';
  btnMin.setAttribute('aria-label', 'Minimiser');
  var btnClose = document.createElement('button');
  btnClose.className = 'cbw-hdr-btn';
  btnClose.innerHTML = '×';
  btnClose.setAttribute('aria-label', 'Fermer');
  hdrBtns.appendChild(btnMin);
  hdrBtns.appendChild(btnClose);
  header.appendChild(hdrBtns);
  win.appendChild(header);

  // Messages area
  var msgsDiv = document.createElement('div');
  msgsDiv.className = 'cbw-messages';
  win.appendChild(msgsDiv);

  // Email collection area
  var emailDiv = document.createElement('div');
  emailDiv.className = 'cbw-email-collect';
  emailDiv.style.display = 'none';
  emailDiv.innerHTML = '<h3>👋 Bonjour !</h3><p>Pour commencer, entrez votre email. C\'est gratuit !</p><input type="email" class="cbw-email-input" placeholder="votre@email.com" required><button class="cbw-email-btn">Démarrer la conversation →</button><div class="cbw-error-msg">Veuillez entrer un email valide.</div>';
  win.appendChild(emailDiv);

  // Input area
  var inputArea = document.createElement('div');
  inputArea.className = 'cbw-input-area';
  inputArea.style.display = 'none';
  var textInput = document.createElement('input');
  textInput.type = 'text';
  textInput.className = 'cbw-input';
  textInput.placeholder = 'Tapez votre message...';
  var sendBtn = document.createElement('button');
  sendBtn.className = 'cbw-send';
  sendBtn.innerHTML = '➤';
  sendBtn.disabled = true;
  inputArea.appendChild(textArea=textInput);
  inputArea.appendChild(sendBtn);
  win.appendChild(inputArea);

  // Message counter
  var counterDiv = document.createElement('div');
  counterDiv.className = 'cbw-counter';
  counterDiv.style.display = 'none';
  win.appendChild(counterDiv);

  // Upgrade banner
  var upgradeDiv = document.createElement('div');
  upgradeDiv.className = 'cbw-upgrade';
  upgradeDiv.style.display = 'none';
  upgradeDiv.innerHTML = '<a href="https://ai.dominiqkmendy.com/#tarifs" target="_blank">⚡ Passez en Pro pour des réponses illimitées</a>';
  win.appendChild(upgradeDiv);

  // ── State ──
  var isOpen = false;
  var isMinimized = false;
  var messages = [];
  var isWaitingForReply = false;

  // ── Subtitle text from bot config ──
  fetch(API_BASE + '/api/bot-config?id=' + encodeURIComponent(BOT_ID))
    .then(function(r){ return r.json(); })
    .then(function(cfg){
      if(cfg && cfg.welcome_header){
        header.querySelector('.cbw-subtitle').textContent = cfg.welcome_header;
      } else {
        header.querySelector('.cbw-subtitle').textContent = 'En ligne • Répond instantanément';
      }
      if(cfg && cfg.welcome_message){
        addBotMsg(cfg.welcome_message);
      }
      if(cfg && cfg.primary_color){
        applyColor(cfg.primary_color);
      }
    })
    .catch(function(){
      header.querySelector('.cbw-subtitle').textContent = 'En ligne • Répond instantanément';
    });

  function applyColor(hex){
    colors.accent = hex;
    // Update key elements dynamically
    fab.style.background = hex;
    sendBtn.style.background = hex;
    header.style.background = hex;
  }

  // ── Event Handlers ──
  fab.addEventListener('click', openChat);
  btnClose.addEventListener('click', closeChat);
  btnMin.addEventListener('click', toggleMinimize);

  header.addEventListener('click', function(e){
    if(e.target === header || e.target.closest('.cbw-header-left')){
      if(isMinimized) toggleMinimize();
    }
  });

  // Email collection
  var emailInput = emailDiv.querySelector('.cbw-email-input');
  var emailBtn = emailDiv.querySelector('.cbw-email-btn');
  var emailError = emailDiv.querySelector('.cbw-error-msg');

  emailBtn.addEventListener('click', startChat);
  emailInput.addEventListener('keypress', function(e){ if(e.key==='Enter') startChat(); });

  function startChat(){
    var email = emailInput.value.trim().toLowerCase();
    if(!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){
      emailError.style.display = 'block';
      return;
    }
    visitorEmail = email;
    emailCollected = true;
    emailDiv.style.display = 'none';
    inputArea.style.display = 'flex';
    counterDiv.style.display = 'block';
    textInput.focus();
    updateCounter();
    // Store lead
    fetch(API_BASE + '/api/lead', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email: email, bot_id: BOT_ID, source: window.location.href})
    }).catch(function(){});
  }

  // Message sending
  sendBtn.addEventListener('click', sendMsg);
  textInput.addEventListener('keypress', function(e){ if(e.key==='Enter' && !e.shiftKey){ e.preventDefault(); sendMsg(); } });
  textInput.addEventListener('input', function(){ sendBtn.disabled = textInput.value.trim().length === 0 || isWaitingForReply; });

  function sendMsg(){
    if(isWaitingForReply) return;
    var txt = textInput.value.trim();
    if(!txt) return;

    // Check free tier limit
    if(sessionMsgCount >= FREE_LIMIT && !visitorEmail){
      showUpgradePrompt();
      return;
    }

    textInput.value = '';
    sendBtn.disabled = true;
    sessionMsgCount++;
    updateCounter();

    addUserMsg(txt);
    addTyping();
    isWaitingForReply = true;

    fetch(API_BASE + '/api/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        messages: messages,
        bot_id: BOT_ID,
        session_id: sessionId,
        visitor_email: visitorEmail
      })
    })
    .then(function(r){ return r.json(); })
    .then(function(data){
      removeTyping();
      isWaitingForReply = false;
      sendBtn.disabled = false;

      if(data.limit_reached){
        showUpgradePrompt();
        addBotMsg("Vous avez atteint la limite de " + FREE_LIMIT + " messages/jour du plan gratuit. 🎯\\n\\nPassez au <strong>Pro à 29€/mois</strong> pour des réponses illimitées !\\n\\n👉 <a href='https://ai.dominiqkmendy.com/#tarifs' target='_blank' style='color:#6C58E7'>Voir les plans</a>");
      } else if(data.error){
        addBotMsg("Désolé, une erreur s'est produite. Veuillez réessayer.");
        console.error('[ChatbotWidget]', data.error);
      } else if(data.reply){
        addBotMsg(data.reply);
        if(data.nearing_limit){
          upgradeDiv.style.display = 'block';
        }
        if(data.show_upgrade){
          showUpgradePrompt();
        }
      }
    })
    .catch(function(err){
      removeTyping();
      isWaitingForReply = false;
      sendBtn.disabled = false;
      addBotMsg("Désolé, le service est temporairement indisponible. Veuillez réessayer dans un instant.");
      console.error('[ChatbotWidget] API error:', err);
    });
  }

  // ── DOM helpers ──
  function addUserMsg(text){
    var m = {role:'user', content:text};
    messages.push(m);
    renderMsg('user', text);
    scrollBottom();
  }

  function addBotMsg(text){
    var m = {role:'assistant', content:text};
    messages.push(m);
    renderMsg('bot', text);
    scrollBottom();
  }

  function renderMsg(type, text){
    var d = document.createElement('div');
    d.className = 'cbw-msg cbw-msg-' + type;
    var avatar = document.createElement('div');
    avatar.className = 'cbw-msg-avatar';
    avatar.textContent = type === 'bot' ? '🤖' : '👤';
    var bubble = document.createElement('div');
    bubble.className = 'cbw-msg-bubble';
    bubble.innerHTML = formatText(text);
    d.appendChild(avatar);
    d.appendChild(bubble);
    msgsDiv.appendChild(d);
  }

  function formatText(t){
    // Basic formatting: line breaks + bold + links
    return t
      .replace(/&/g,'&amp;')
      .replace(/</g,'&lt;')
      .replace(/>/g,'&gt;')
      .replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>')
      .replace(/\n/g,'<br>')
      .replace(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g,'<a href="$2" target="_blank" style="color:#6C5CE7;text-decoration:underline">$1</a>')
      .replace(/(https?:\/\/[^\s<]+)/g,'<a href="$1" target="_blank" style="color:#6C5CE7;text-decoration:underline">$1</a>');
  }

  function addTyping(){
    var d = document.createElement('div');
    d.className = 'cbw-typing';
    d.id = 'cbw-typing';
    d.innerHTML = '<span></span><span></span><span></span>';
    msgsDiv.appendChild(d);
    scrollBottom();
  }

  function removeTyping(){
    var t = document.getElementById('cbw-typing');
    if(t) t.remove();
  }

  function scrollBottom(){
    requestAnimationFrame(function(){
      msgsDiv.scrollTop = msgsDiv.scrollHeight;
    });
  }

  function updateCounter(){
    if(visitorEmail){
      var remaining = Math.max(0, FREE_LIMIT - sessionMsgCount);
      if(remaining <= 3 && remaining > 0){
        counterDiv.textContent = remaining + ' message(s) gratuit(s) restant(s)';
        counterDiv.style.color = '#ffd700';
      } else if(remaining === 0){
        counterDiv.textContent = 'Limite atteinte — Passez en Pro';
        counterDiv.style.color = '#ff6b6b';
      } else {
        counterDiv.textContent = '';
      }
    }
  }

  function showUpgradePrompt(){
    upgradeDiv.style.display = 'block';
    win.classList.add('cbw-reached');
  }

  // ── Window controls ──
  function openChat(){
    if(isOpen) return;
    isOpen = true;
    fab.classList.add('hidden');
    win.classList.remove('cbw-closed');
    emailDiv.style.display = emailCollected ? 'none' : 'block';
    inputArea.style.display = emailCollected ? 'flex' : 'none';
    counterDiv.style.display = emailCollected ? 'block' : 'none';
    if(emailCollected) textInput.focus();
  }

  function closeChat(){
    isOpen = false;
    isMinimized = false;
    fab.classList.remove('hidden');
    win.classList.add('cbw-closed');
    win.classList.remove('cbw-minimized');
  }

  function toggleMinimize(){
    isMinimized = !isMinimized;
    win.classList.toggle('cbw-minimized', isMinimized);
    btnMin.innerHTML = isMinimized ? '+' : '−';
  }

})();
