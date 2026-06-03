/**
 * IA Business Solutions — Chatbot API (Cloudflare Pages Function)
 * Endpoint: POST /api/chat
 * 
 * Receives: {messages, bot_id, session_id, visitor_email}
 * Calls OpenAI GPT-4o-mini
 * Tracks usage in KV storage
 * Free tier: 10 messages/day, then upgrade prompt
 * 
 * Environment variables (CF Pages secrets):
 *   OPENAI_API_KEY - OpenAI API key
 *   DASHBOARD_PASSWORD - Admin dashboard password
 *   BOT_MASTER_KEY - Master key for bot registration
 */

// CORS headers for cross-origin widget access
var HEADERS = {
  'Content-Type': 'application/json',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Max-Age': '86400'
};

// Handle CORS preflight
function handleOptions(request) {
  return new Response(null, {headers: HEADERS, status: 204});
}

// ── KV helpers ──
function getKV(kv, key) {
  return kv.get(key, {type: 'json'});
}
function setKV(kv, key, val, ttl) {
  var opts = {};
  if (ttl) opts.expirationTtl = ttl;
  return kv.put(key, JSON.stringify(val), opts);
}

// ── Usage tracking ──
// Key: "usage:{bot_id}:{YYYY-MM-DD}" -> {count, emails:[]}
function getTodayKey(botId) {
  var d = new Date();
  var tz = d.getTimezoneOffset() * 60000;
  var local = new Date(d.getTime() - tz);
  return 'usage:' + botId + ':' + local.toISOString().slice(0, 10);
}

async function getUsageCount(kv, botId) {
  var key = getTodayKey(botId);
  var data = await getKV(kv, key);
  return data ? data.count : 0;
}

async function incrementUsage(kv, botId, email) {
  var key = getTodayKey(botId);
  var data = await getKV(kv, key) || {count: 0, emails: []};
  data.count++;
  if (email && data.emails.indexOf(email) === -1) data.emails.push(email);
  // TTL: expire at midnight + 1h buffer = ~25h
  await setKV(kv, key, data, 90000);
  return data.count;
}

// ── Bot config from KV ──
async function getBotConfig(kv, botId) {
  var data = await getKV(kv, 'bot:' + botId);
  return data || null;
}

// ── Rate limit check ──
// Free: 10/day, Pro: 5000/month, Business: 50000/month
function checkLimit(plan, usageCount, planLimits) {
  var limit = planLimits[plan] || planLimits['free'];
  if (limit.type === 'daily') {
    return {
      allowed: usageCount < limit.count,
      remaining: Math.max(0, limit.count - usageCount),
      total: limit.count,
      period: 'jour'
    };
  }
  if (limit.type === 'monthly') {
    return {
      allowed: usageCount < limit.count,
      remaining: Math.max(0, limit.count - usageCount),
      total: limit.count,
      period: 'mois'
    };
  }
  return {allowed: true, remaining: -1, total: -1, period: ''};
}

var PLAN_LIMITS = {
  free: {count: 10, type: 'daily'},
  pro: {count: 5000, type: 'monthly'},
  business: {count: 50000, type: 'monthly'}
};

// ── OpenAI API call ──
async function callOpenAI(apiKey, systemPrompt, messages, language) {
  var langInstruction = language === 'en'
    ? 'Respond in English. '
    : language === 'ar'
    ? 'Respond in Arabic. '
    : 'Réponds en français. ';

  var openAIMessages = [{role: 'system', content: langInstruction + systemPrompt}];

  // Trim to last 20 messages to stay within token limits
  var recent = messages.slice(-20);
  for (var i = 0; i < recent.length; i++) {
    if (recent[i].role === 'user' || recent[i].role === 'assistant') {
      openAIMessages.push({role: recent[i].role, content: recent[i].content});
    }
  }

  var response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + apiKey
    },
    body: JSON.stringify({
      model: 'gpt-4o-mini',
      messages: openAIMessages,
      max_tokens: 500,
      temperature: 0.7,
      presence_penalty: 0.1
    })
  });

  if (!response.ok) {
    var errText = await response.text();
    console.error('OpenAI API error:', response.status, errText);
    throw new Error('OpenAI API error: ' + response.status);
  }

  var data = await response.json();
  return data.choices[0].message.content.trim();
}

// ── Bot master config (KV-stored, never hardcoded secrets) ──
// Each bot has: {id, name, plan, welcome_message, welcome_header, primary_color, system_prompt, knowledge_base, language, owner_email, created_at, active}
var DEFAULT_SYSTEM_PROMPT = "Tu es l'assistant virtuel de l'entreprise du client. Tu es professionnel, utile et concis. Réponds uniquement en français sauf si on te demande explicitement une autre langue. Si tu ne connais pas une réponse, suggère de contacter un humain.";

// ── Main handler ──
export async function onRequestPost(context) {
  var env = context.env;

  try {
    var body = await context.request.json();
    var botId = body.bot_id || '';
    var messages = body.messages || [];
    var sessionId = body.session_id || '';
    var visitorEmail = body.visitor_email || '';

    if (!botId) {
      return jsonResponse({error: 'bot_id requis'}, 400);
    }
    if (!messages || messages.length === 0) {
      return jsonResponse({error: 'messages requis'}, 400);
    }

    // Get bot config from KV
    var botConfig = await getKV(env.CHATBOT_KV, 'bot:' + botId);
    if (!botConfig || !botConfig.active) {
      return jsonResponse({error: 'Bot non trouvé ou inactif'}, 404);
    }

    var plan = botConfig.plan || 'free';

    // Check limits
    var usageCount = 0;
    var limit;

    if (plan === 'free') {
      usageCount = await getUsageCount(env.CHATBOT_KV, botId);
      limit = checkLimit('free', usageCount, PLAN_LIMITS);

      if (!limit.allowed) {
        return jsonResponse({
          limit_reached: true,
          reply: null,
          show_upgrade: true,
          plan: plan,
          upgrade_url: 'https://ai.dominiqkmendy.com/#tarifs'
        });
      }
    } else {
      // Pro/Business: check monthly usage
      var monthKey = 'monthly_usage:' + botId + ':' + new Date().toISOString().slice(0, 7);
      var monthData = await getKV(env.CHATBOT_KV, monthKey);
      usageCount = monthData ? monthData.count : 0;
      limit = checkLimit(plan, usageCount, PLAN_LIMITS);

      if (!limit.allowed) {
        return jsonResponse({
          limit_reached: true,
          reply: null,
          show_upgrade: true,
          plan: plan
        });
      }
    }

    // Build system prompt
    var systemPrompt = botConfig.system_prompt || DEFAULT_SYSTEM_PROMPT;

    // Append knowledge base if available
    if (botConfig.knowledge_base && botConfig.knowledge_base.length > 0) {
      systemPrompt += '\n\n--- BASE DE CONNAISSANCES ---\n' + botConfig.knowledge_base;
    }

    // Append company info
    if (botConfig.company_name) {
      systemPrompt += '\n\nNom de l\'entreprise: ' + botConfig.company_name;
    }
    if (botConfig.company_description) {
      systemPrompt += '\nDescription: ' + botConfig.company_description;
    }

    // Call OpenAI
    var reply = await callOpenAI(
      env.OPENAI_API_KEY,
      systemPrompt,
      messages,
      botConfig.language || 'fr'
    );

    // Increment usage
    await incrementUsage(env.CHATBOT_KV, botId, visitorEmail);

    if (plan !== 'free') {
      var monthKey2 = 'monthly_usage:' + botId + ':' + new Date().toISOString().slice(0, 7);
      var monthData2 = await getKV(env.CHATBOT_KV, monthKey2);
      if (!monthData2) monthData2 = {count: 0};
      monthData2.count++;
      await setKV(env.CHATBOT_KV, monthKey2, monthData2, 2592000); // 30 days
    }

    // Store conversation log (last 30 days)
    var convKey = 'conv:' + botId + ':' + sessionId;
    var convData = await getKV(env.CHATBOT_KV, convKey) || {messages: [], created_at: Date.now()};
    convData.messages.push({
      user: messages[messages.length - 1].content,
      assistant: reply,
      ts: Date.now()
    });
    // Keep last 50 exchanges
    if (convData.messages.length > 50) convData.messages = convData.messages.slice(-50);
    await setKV(env.CHATBOT_KV, convKey, convData, 2592000);

    return jsonResponse({
      reply: reply,
      plan: plan,
      usage: usageCount + 1,
      limit_total: limit.total,
      limit_remaining: Math.max(0, limit.remaining - 1),
      limit_period: limit.period,
      nearing_limit: (limit.remaining - 1) <= 2 && plan === 'free',
      show_upgrade: false
    });

  } catch (err) {
    console.error('Chat API error:', err);
    return jsonResponse({error: 'Erreur serveur: ' + err.message}, 500);
  }
}

// OPTIONS handler for CORS
export function onRequestOptions() {
  return handleOptions();
}

function jsonResponse(data, status) {
  status = status || 200;
  return new Response(JSON.stringify(data), {
    status: status,
    headers: HEADERS
  });
}
