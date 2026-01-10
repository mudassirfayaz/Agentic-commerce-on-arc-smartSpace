import { Link } from 'react-router-dom'
import './LandingPage.css'

const LandingPage = () => {
  return (
    <div className="landing-page">
      {/* Navigation */}
      <nav className="nav">
        <div className="nav-container">
          <div className="nav-logo">SmartSpace</div>
          <div className="nav-links">
            <a href="#features">Features</a>
            <a href="#how-it-works">How It Works</a>
            <a href="#models">Models</a>
            <a href="#pricing">Pricing</a>
            <a href="#faq">FAQ</a>
            <Link to="/login" className="nav-link-btn">Login</Link>
            <Link to="/signup" className="nav-link-btn primary">Sign Up</Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero">
        <div className="container">
          <h1 className="hero-title">
            Autonomous Pay-Per-Use API Access<br />
            with USDC
          </h1>
          <p className="hero-subtitle">
            A secure gateway that allows users and AI agents to call paid APIs (OpenAI, Google, Gemini, etc.)<br />
            and pay instantly per request using USDC. No API keys needed. Transparent, controlled, and predictable billing.
          </p>
          <div className="hero-cta">
            <Link to="/signup" className="btn btn-primary btn-large">
              Get Started
            </Link>
            <Link to="/login" className="btn btn-secondary btn-large">
              Sign In
            </Link>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="section section-problem">
        <div className="container">
          <h2 className="section-title">
            The Current State of AI API Access is Broken
          </h2>
          <p className="section-subtitle">
            Shared keys, unpredictable billing, and manual management create risk and overhead
          </p>
          
          <div className="problem-grid">
            <div className="problem-card">
              <h3>Shared API Keys</h3>
              <p>Sharing API keys across teams creates security risks. Revoking access means breaking production. Managing credentials becomes a nightmare.</p>
            </div>
            <div className="problem-card">
              <h3>Unpredictable Billing</h3>
              <p>Monthly bills surprise you. Hard to track exact usage per request. Finance teams struggle to audit costs. No per-request transparency.</p>
            </div>
            <div className="problem-card">
              <h3>Agent Limitations</h3>
              <p>AI agents cannot safely make paid API calls autonomously. Manual approvals break automation. No spending controls for autonomous systems.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Solution Section */}
      <section id="features" className="section section-solution">
        <div className="container">
          <h2 className="section-title">One Gateway. Unlimited Possibilities.</h2>
          <p className="section-subtitle">
            SmartSpace becomes your secure billing and control layer for autonomous API access
          </p>
          
          <div className="feature-grid">
            <div className="feature-card">
              <div className="feature-icon">⚡</div>
              <h3>Pay Per Request</h3>
              <p>Pay exactly what you use with instant USDC payments. No monthly commitments. Transparent pricing for every API call. Perfect for autonomous agents.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔒</div>
              <h3>No API Keys Needed</h3>
              <p>Never expose your API keys. SmartSpace handles all authentication securely. Agents can make requests without credential management.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">💰</div>
              <h3>Transparent Billing</h3>
              <p>See exactly what each request costs. Full transaction logs. Budget controls and spending policies. Enterprise-ready auditing.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>Agent Ready</h3>
              <p>Autonomous agents can make API calls with built-in spending controls. SmartSpace evaluates, pays, and executes automatically.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3>Usage Analytics</h3>
              <p>Track usage per request, per agent, per project. Real-time cost tracking. Detailed logs for every transaction.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔄</div>
              <h3>Unified Interface</h3>
              <p>Access 100+ AI models through one consistent API. OpenAI, Anthropic, Google, and more. Switch providers instantly.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Models Section */}
      <section id="models" className="section section-models">
        <div className="container">
          <h2 className="section-title">Supported AI Models</h2>
          <p className="section-subtitle">
            Access 100+ AI models through one unified interface. No API keys needed.
          </p>
          
          <div className="feature-grid">
            <div className="feature-card">
              <div className="feature-icon">🤖</div>
              <h3>OpenAI</h3>
              <p>GPT-4, GPT-3.5 Turbo, DALL-E, Whisper, and more. Access all OpenAI models with instant USDC payments.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🧠</div>
              <h3>Anthropic</h3>
              <p>Claude 3 Opus, Sonnet, Haiku, and Claude 2. Enterprise-grade AI models with transparent per-request billing.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🔮</div>
              <h3>Google</h3>
              <p>Gemini Pro, PaLM, Vertex AI, and more. Google's latest AI models available through SmartSpace.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">⚡</div>
              <h3>Other Providers</h3>
              <p>Access models from Cohere, Hugging Face, Stability AI, and more. One API for all your AI needs.</p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="section section-how-it-works">
        <div className="container">
          <h2 className="section-title">How SmartSpace Works</h2>
          <p className="section-subtitle">
            From request to result in seconds. Transparent, secure, and automated.
          </p>
          <div className="flow-steps">
            <div className="flow-step">
              <div className="step-number">1</div>
              <h3>Request Task</h3>
              <p>User or agent requests a task through SmartSpace API gateway</p>
            </div>
            <div className="flow-arrow">→</div>
            <div className="flow-step">
              <div className="step-number">2</div>
              <h3>Check & Pay</h3>
              <p>SmartSpace checks price and spending policies, pays required amount in USDC instantly</p>
            </div>
            <div className="flow-arrow">→</div>
            <div className="flow-step">
              <div className="step-number">3</div>
              <h3>Execute API</h3>
              <p>SmartSpace calls the external API using secure internal keys (no key exposure)</p>
            </div>
            <div className="flow-arrow">→</div>
            <div className="flow-step">
              <div className="step-number">4</div>
              <h3>Return Results</h3>
              <p>Result + full usage metrics + payment log + transaction receipt is returned</p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="section section-pricing">
        <div className="container">
          <h2 className="section-title">Simple, Transparent Pricing</h2>
          <p className="section-subtitle">
            Pay exactly what the API provider charges. We only add a small platform fee.
          </p>
          
          <div className="pricing-grid">
            <div className="pricing-card">
              <h3>Starter</h3>
              <div className="price">Free</div>
              <p className="price-subtitle">+ 2% platform fee on API costs</p>
              <ul className="pricing-features">
                <li>100 requests per day</li>
                <li>Access to all 100+ models</li>
                <li>USDC payment integration</li>
                <li>Basic usage logs</li>
                <li>Standard support</li>
              </ul>
              <Link to="/signup" className="btn btn-outline btn-block">
                Get Started
              </Link>
            </div>
            
            <div className="pricing-card featured">
              <div className="badge">Most Popular</div>
              <h3>Pro</h3>
              <div className="price">$9<span>/month</span></div>
              <p className="price-subtitle">+ 1% platform fee on API costs</p>
              <ul className="pricing-features">
                <li>All Starter features, plus:</li>
                <li>10,000 requests per day</li>
                <li>Budget controls & spending rules</li>
                <li>Automatic provider fallback</li>
                <li>Advanced analytics</li>
                <li>Priority support</li>
              </ul>
              <Link to="/signup" className="btn btn-primary btn-block">
                Get Started
              </Link>
            </div>
            
            <div className="pricing-card">
              <h3>Enterprise</h3>
              <div className="price">$99<span>/month</span></div>
              <p className="price-subtitle">+ 0.5% platform fee on API costs</p>
              <ul className="pricing-features">
                <li>All Pro features, plus:</li>
                <li>1,000,000 requests per day</li>
                <li>SLA guarantees</li>
                <li>Dedicated support team</li>
                <li>Custom integrations</li>
                <li>White-label options</li>
              </ul>
              <Link to="/signup" className="btn btn-outline btn-block">
                Contact Sales
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section id="faq" className="section section-faq">
        <div className="container">
          <h2 className="section-title">Frequently Asked Questions</h2>
          <div className="faq-grid">
            <div className="faq-item">
              <h3>How does USDC payment work?</h3>
              <p>You fund your SmartSpace wallet with USDC. Each API request is paid instantly from your balance. No monthly billing, no surprises. You only pay for what you use.</p>
            </div>
            <div className="faq-item">
              <h3>Do I need API keys from providers?</h3>
              <p>No! SmartSpace manages all API keys securely. You never expose credentials. Agents can make requests autonomously without key management.</p>
            </div>
            <div className="faq-item">
              <h3>Can AI agents use this autonomously?</h3>
              <p>Yes! Set budgets and spending rules per agent or project. Agents can make API calls automatically within those constraints. SmartSpace handles payment and execution.</p>
            </div>
            <div className="faq-item">
              <h3>How transparent is the billing?</h3>
              <p>Every request includes a full receipt: API used, tokens consumed, cost in USDC, timestamp, and agent/project ID. Perfect for finance audits.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section section-cta">
        <div className="container">
          <h2 className="section-title">Ready to Get Started?</h2>
          <p className="section-subtitle">
            Join developers building autonomous AI systems with transparent, secure API access.
          </p>
          <div className="cta-buttons">
            <Link to="/signup" className="btn btn-primary btn-large">
              Get Your API Key
            </Link>
            <Link to="/login" className="btn btn-secondary btn-large">
              Sign In
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container">
          <div className="footer-content">
            <div className="footer-brand">
              <h3>SmartSpace</h3>
              <p>Pay-per-use API access with USDC</p>
            </div>
            <div className="footer-links">
              <div className="footer-column">
                <h4>Product</h4>
                <a href="#features">Features</a>
                <a href="#how-it-works">How It Works</a>
                <a href="#models">Models</a>
                <a href="#pricing">Pricing</a>
                <a href="#faq">FAQ</a>
              </div>
              <div className="footer-column">
                <h4>Company</h4>
                <a href="#">About</a>
                <a href="#">Blog</a>
                <a href="#">Contact</a>
              </div>
              <div className="footer-column">
                <h4>Legal</h4>
                <a href="#">Terms of Service</a>
                <a href="#">Privacy Policy</a>
              </div>
            </div>
          </div>
          <div className="footer-bottom">
            <p>© 2025 SmartSpace. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage

