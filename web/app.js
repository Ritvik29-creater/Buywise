// web/app.js — SmartShop Elite Client Logic

const API_BASE = window.location.origin;
let currentThreadId = null;
let isPendingApproval = false;
let displayedMessagesCount = 0;

// Elements
const chatViewport = document.getElementById('chat-viewport');
const chatInput = document.getElementById('chat-input');
const supervisorInput = document.getElementById('supervisor-text-input');
const inputLabel = document.getElementById('input-field-label');
const sendBtn = document.getElementById('send-button');
const modeBadge = document.getElementById('agent-mode-badge');
const sidebarMode = document.getElementById('sidebar-mode-text');
const sidebarThread = document.getElementById('sidebar-thread-id');
const cartContainer = document.getElementById('cart-container');
const cartCountBadge = document.getElementById('cart-count-badge');
const cartSummaryBox = document.getElementById('cart-summary-box');
const cartTotalAmount = document.getElementById('cart-total-amount');
const cartCheckoutBtn = document.getElementById('cart-checkout-button');
const approvalBanner = document.getElementById('approval-banner');
const approvalSummary = document.getElementById('approval-summary-text');
const approvalSeverity = document.getElementById('approval-severity-badge');
const approvalDetails = document.getElementById('approval-details-text');

// Initialize Session
async function initializeApp() {
  try {
    const res = await fetch(`${API_BASE}/api/new-session`);
    const data = await res.json();
    currentThreadId = data.thread_id;
    sidebarThread.textContent = `${currentThreadId.substring(0, 14)}...`;
    console.log(`Initialized SmartShop Session: ${currentThreadId}`);
  } catch (err) {
    console.error('Failed to initialize session:', err);
    appendErrorBubble('Could not connect to the backend agent server. Please ensure server.py is running.');
  }
}

// User Action Trigger
function triggerPrompt(text) {
  if (isPendingApproval) return;
  chatInput.value = text;
  handleUserSubmit();
}

// Send user or supervisor message
async function handleUserSubmit() {
  if (isPendingApproval) {
    const supervisorMsg = supervisorInput.value.trim();
    if (!supervisorMsg) return;
    submitSupervisorApproval(supervisorMsg);
  } else {
    const userMsg = chatInput.value.trim();
    if (!userMsg) return;
    
    // Clear input
    chatInput.value = '';
    
    // Remove welcome card if visible
    const welcomeCard = document.getElementById('welcome-card');
    if (welcomeCard) welcomeCard.remove();
    
    // Display user bubble
    appendUserBubble(userMsg);
    
    // Show thinking indicator
    const thinkingIndicator = showThinkingBubble();
    
    try {
      const response = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          thread_id: currentThreadId,
          message: userMsg
        })
      });
      
      const payload = await response.json();
      thinkingIndicator.remove();
      
      if (!response.ok) {
        throw new Error(payload.detail || 'Agent processing error');
      }
      
      renderAgentUpdates(payload);
    } catch (err) {
      thinkingIndicator.remove();
      appendErrorBubble(`Agent error: ${err.message}`);
    }
  }
}

// Submit Supervisor Decision (Human-in-the-Loop)
async function submitSupervisorApproval(decision) {
  supervisorInput.value = '';
  
  // Hide approval banner
  approvalBanner.classList.remove('active');
  isPendingApproval = false;
  
  // Reset input controls
  supervisorInput.style.display = 'none';
  chatInput.style.display = 'block';
  inputLabel.textContent = 'Your Message';
  
  // Display supervisor bubble
  appendSupervisorBubble(decision);
  const thinkingIndicator = showThinkingBubble();
  
  try {
    const response = await fetch(`${API_BASE}/api/supervisor`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        thread_id: currentThreadId,
        response: decision
      })
    });
    
    const payload = await response.json();
    thinkingIndicator.remove();
    
    if (!response.ok) {
      throw new Error(payload.detail || 'Supervisor resume error');
    }
    
    renderAgentUpdates(payload);
  } catch (err) {
    thinkingIndicator.remove();
    appendErrorBubble(`Supervisor resume error: ${err.message}`);
  }
}

// Render Graph State Output
function renderAgentUpdates(payload) {
  const allMessages = payload.messages || [];
  const freshMessages = allMessages.slice(displayedMessagesCount);
  displayedMessagesCount = allMessages.length;
  
  freshMessages.forEach(msg => {
    if (msg.role === 'assistant') {
      appendAssistantBubble(msg.content, payload.current_mode);
    } else if (msg.role === 'tool_call') {
      appendToolBubble(msg.tool_name, msg.content, 'CALLING');
    } else if (msg.role === 'tool_result') {
      appendToolBubble(msg.tool_name, msg.content, 'RESULT');
    }
  });
  
  // Update Mode
  updateAgentMode(payload.current_mode);
  
  // Update Cart
  updateCartSidebar(payload.cart || {});
  
  // Check for Human-in-the-loop interruption
  if (payload.pending_approval) {
    activateApprovalPanel(payload.pending_approval);
  }
}

// Update Active Agent Mode
function updateAgentMode(mode) {
  if (mode === 'customer_support') {
    modeBadge.textContent = 'Support Specialist';
    modeBadge.className = 'mode-badge support';
    sidebarMode.textContent = 'Support Agent';
  } else {
    modeBadge.textContent = 'Sales Representative';
    modeBadge.className = 'mode-badge sales';
    sidebarMode.textContent = 'Sales Agent';
  }
}

// Update Cart Display
function updateCartSidebar(cart) {
  const itemKeys = Object.keys(cart);
  let totalItemsCount = 0;
  let totalCost = 0.0;
  
  if (itemKeys.length === 0) {
    cartContainer.innerHTML = '<div class="cart-empty">Your shopping cart is empty.<br>Ask the sales agent to find and add products!</div>';
    cartSummaryBox.style.display = 'none';
    cartCheckoutBtn.style.display = 'none';
    cartCountBadge.textContent = '0';
    return;
  }
  
  let html = '';
  itemKeys.forEach(id => {
    const item = cart[id];
    const name = item.name || item.product_name || `Product #${id}`;
    const price = typeof item.price === 'number' ? item.price : parseFloat(item.price) || 0;
    const qty = item.quantity || 1;
    totalItemsCount += qty;
    totalCost += (price * qty);
    
    html += `
      <div class="cart-item">
        <div class="cart-item-info">
          <div class="cart-item-title" title="${escapeHtml(name)}">${escapeHtml(name)}</div>
          <div class="cart-item-price">$${price.toFixed(2)}</div>
        </div>
        <div class="cart-item-qty">x${qty}</div>
      </div>
    `;
  });
  
  cartContainer.innerHTML = html;
  cartCountBadge.textContent = totalItemsCount;
  cartTotalAmount.textContent = `$${totalCost.toFixed(2)}`;
  cartSummaryBox.style.display = 'flex';
  cartCheckoutBtn.style.display = 'inline-flex';
}

// Activate Supervisor Approval
function activateApprovalPanel(approvalInfo) {
  isPendingApproval = true;
  const severity = (approvalInfo.severity || 'high').toLowerCase();
  
  approvalSummary.textContent = approvalInfo.summary || 'Escalation requires management approval';
  approvalSeverity.textContent = severity.toUpperCase();
  approvalSeverity.className = `severity-pill severity-${severity}`;
  approvalDetails.textContent = approvalInfo.message || 'No additional details provided.';
  
  approvalBanner.classList.add('active');
  
  // Switch input focus
  chatInput.style.display = 'none';
  supervisorInput.style.display = 'block';
  supervisorInput.placeholder = 'Type approval decision (e.g., "Approved $50 store credit", "Deny refund")...';
  supervisorInput.focus();
  inputLabel.textContent = 'SUPERVISOR DECISION REQUIRED';
}

// Reset Chat Session
async function startFreshSession() {
  displayedMessagesCount = 0;
  isPendingApproval = false;
  approvalBanner.classList.remove('active');
  chatInput.style.display = 'block';
  supervisorInput.style.display = 'none';
  inputLabel.textContent = 'Your Message';
  
  chatViewport.innerHTML = `
    <div id="welcome-card">
      <span class="welcome-badge">AI-Powered Autonomous Retailer</span>
      <h2 class="welcome-title">Welcome to SmartShop Elite</h2>
      <p class="welcome-desc">Your autonomous retail concierge. I can explore our catalog via vector embeddings, compare technical specs, review customer sentiment, maintain your real-time shopping cart, and seamlessly coordinate with support.</p>
      
      <div class="prompts-container">
        <div class="prompt-chip" onclick="triggerPrompt('Compare Sony WH-1000XM5 and Bose QuietComfort Ultra headphones.')">
          <span class="chip-icon">🎧</span>
          <div>Compare Sony &amp; Bose Flagships</div>
        </div>
        <div class="prompt-chip" onclick="triggerPrompt('Find Apple MacBook and high-performance ultrabooks.')">
          <span class="chip-icon">💻</span>
          <div>MacBook &amp; Ultrabooks</div>
        </div>
        <div class="prompt-chip" onclick="triggerPrompt('Recommend top-rated home espresso machines.')">
          <span class="chip-icon">☕</span>
          <div>Espresso Coffee Machines</div>
        </div>
        <div class="prompt-chip" onclick="triggerPrompt('Find high-cushion running shoes with great reviews.')">
          <span class="chip-icon">👟</span>
          <div>Pro Running Shoes</div>
        </div>
        <div class="prompt-chip" onclick="triggerPrompt('Can you check what is in my cart?')">
          <span class="chip-icon">🛒</span>
          <div>View Shopping Cart</div>
        </div>
        <div class="prompt-chip" onclick="triggerPrompt('I want to track my recent orders.')">
          <span class="chip-icon">📦</span>
          <div>Track Recent Orders</div>
        </div>
      </div>
    </div>
  `;
  
  updateAgentMode('sales_rep');
  updateCartSidebar({});
  await initializeApp();
}

// ── DOM HELPER FUNCTIONS ──
function appendUserBubble(text) {
  const bubble = document.createElement('div');
  bubble.className = 'message-bubble user';
  bubble.textContent = text;
  chatViewport.appendChild(bubble);
  scrollToBottom();
}

function appendAssistantBubble(text, mode) {
  const bubble = document.createElement('div');
  const isSupport = mode === 'customer_support';
  bubble.className = `message-bubble assistant ${isSupport ? 'support' : 'sales'}`;
  
  const roleName = isSupport ? 'Customer Support Agent' : 'Sales Representative';
  bubble.innerHTML = `
    <div class="bubble-header">${roleName}</div>
    <div class="bubble-body">${formatMarkdownLike(text)}</div>
  `;
  chatViewport.appendChild(bubble);
  scrollToBottom();
}

function appendToolBubble(toolName, content, stateTag) {
  const wrap = document.createElement('div');
  wrap.className = 'tool-collapsible';
  
  wrap.innerHTML = `
    <div class="tool-header" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'none' ? 'block' : 'none'">
      <span>⚡ TOOL [${stateTag}]: ${escapeHtml(toolName)}</span>
      <span style="font-size:0.7rem;opacity:0.7">▼ Details</span>
    </div>
    <div class="tool-details" style="display:none">
      <pre>${escapeHtml(content)}</pre>
    </div>
  `;
  chatViewport.appendChild(wrap);
  scrollToBottom();
}

function appendSupervisorBubble(decision) {
  const bubble = document.createElement('div');
  bubble.className = 'message-bubble supervisor';
  bubble.innerHTML = `
    <div class="supervisor-header">Supervisor Approval Resolution</div>
    <div style="font-size:0.9rem;color:#f8fafc">${escapeHtml(decision)}</div>
  `;
  chatViewport.appendChild(bubble);
  scrollToBottom();
}

function appendErrorBubble(message) {
  const bubble = document.createElement('div');
  bubble.className = 'message-bubble error';
  bubble.textContent = message;
  chatViewport.appendChild(bubble);
  scrollToBottom();
}

function showThinkingBubble() {
  const bubble = document.createElement('div');
  bubble.className = 'thinking-bubble';
  bubble.innerHTML = `
    <span>Agent Reasoning</span>
    <div class="dot-pulse">
      <span></span>
      <span></span>
      <span></span>
    </div>
  `;
  chatViewport.appendChild(bubble);
  scrollToBottom();
  return bubble;
}

function scrollToBottom() {
  chatViewport.scrollTop = chatViewport.scrollHeight;
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function formatMarkdownLike(str) {
  let safe = escapeHtml(str);
  // Headers
  safe = safe.replace(/^#### (.*?)$/gm, '<h5 style="margin:8px 0 4px;font-size:0.95rem;font-weight:700;color:#c7d2fe;">$1</h5>');
  safe = safe.replace(/^### (.*?)$/gm, '<h4 style="margin:10px 0 6px;font-size:1.05rem;font-weight:700;color:#818cf8;">$1</h4>');
  safe = safe.replace(/^## (.*?)$/gm, '<h3 style="margin:12px 0 8px;font-size:1.15rem;font-weight:700;color:#a5b4fc;">$1</h3>');
  safe = safe.replace(/^# (.*?)$/gm, '<h2 style="margin:14px 0 10px;font-size:1.25rem;font-weight:800;color:#fff;">$1</h2>');
  // Bold
  safe = safe.replace(/\*\*(.*?)\*\*/g, '<strong style="color:#f1f5f9;font-weight:600;">$1</strong>');
  // Bullet lists
  safe = safe.replace(/^\s*[\*\-]\s+(.*?)$/gm, '<div style="margin:4px 0 4px 12px;line-height:1.5;">• $1</div>');
  // Horizontal rules
  safe = safe.replace(/^---$/gm, '<hr style="border:none;border-top:1px solid rgba(255,255,255,0.12);margin:12px 0;"/>');
  // Newlines to br
  safe = safe.replace(/\n\n+/g, '<br/>');
  safe = safe.replace(/\n/g, '<br/>');
  return safe;
}

// Event Listeners
chatInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') handleUserSubmit();
});

supervisorInput.addEventListener('keydown', e => {
  if (e.key === 'Enter') handleUserSubmit();
});

sendBtn.addEventListener('click', handleUserSubmit);

// Start
initializeApp();
