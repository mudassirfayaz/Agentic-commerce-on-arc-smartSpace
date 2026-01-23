import { useState, useEffect, useRef, useMemo } from 'react'
import { Link } from 'react-router-dom'
import Chatbot from '../components/Chatbot/Chatbot'
import { ModelGallery, ModelSearch, ModelDetails } from '../components/Models'
import { getModels, getProviders, getCategories } from '../services/models'
import modelsData from '../data/models.json' // Fallback
import SmartSpaceIcon from '../components/SmartSpaceIcon'
import './LandingPage.css'

const LandingPage = () => {
  const [selectedLanguage, setSelectedLanguage] = useState('python')
  const [selectedFacility, setSelectedFacility] = useState('audio')
  const [selectedPlatform, setSelectedPlatform] = useState('openai')
  const [navScrolled, setNavScrolled] = useState(false)
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedProvider, setSelectedProvider] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('')
  const [selectedModel, setSelectedModel] = useState(null)
  const [allModels, setAllModels] = useState([])
  const [providers, setProviders] = useState([])
  const [categories, setCategories] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)
  const apiKey = 'smartspace234lkjpoij;lkjljasdfij234ljkls'
  
  const sectionRefs = useRef([])
  const cardRefs = useRef([])
  
  // Load models, providers, and categories on mount
  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true)
      setError(null)
      try {
        const [models, providersList, categoriesList] = await Promise.all([
          getModels(),
          getProviders(),
          getCategories()
        ])
        setAllModels(models)
        setProviders(providersList)
        setCategories(categoriesList)
      } catch (err) {
        console.error('Error loading model data:', err)
        setError('Failed to load models. Using cached data.')
        // Fallback to static data
        const staticModels = modelsData.models || []
        setAllModels(staticModels)
        setProviders([...new Set(staticModels.map(m => m.provider))].sort())
        setCategories([...new Set(staticModels.map(m => m.category))].sort())
      } finally {
        setIsLoading(false)
      }
    }
    loadData()
  }, [])
  
  // Check if any filters are active
  const hasActiveFilters = searchQuery || selectedProvider || selectedCategory

  // Filter models based on search and filters
  const filteredModels = useMemo(() => {
    // If no filters are active, return empty array
    if (!hasActiveFilters) {
      return []
    }
    
    let filtered = allModels
    
    // Search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(model =>
        model.name.toLowerCase().includes(query) ||
        model.provider.toLowerCase().includes(query) ||
        model.description.toLowerCase().includes(query) ||
        model.capabilities.some(cap => cap.toLowerCase().includes(query))
      )
    }
    
    // Provider filter
    if (selectedProvider) {
      filtered = filtered.filter(model => model.provider === selectedProvider)
    }
    
    // Category filter
    if (selectedCategory) {
      filtered = filtered.filter(model => model.category === selectedCategory)
    }
    
    return filtered
  }, [allModels, searchQuery, selectedProvider, selectedCategory, hasActiveFilters])
  
  const handleSearch = (query) => {
    setSearchQuery(query)
  }
  
  const handleFilterChange = ({ provider, category }) => {
    setSelectedProvider(provider)
    setSelectedCategory(category)
  }
  
  const handleModelClick = (model) => {
    setSelectedModel(model)
  }
  
  // Smooth scroll to models section
  const scrollToModels = () => {
    const modelsSection = document.getElementById('models')
    if (modelsSection) {
      modelsSection.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }

  const facilities = [
    { id: 'text', label: 'Text', endpoint: '/v1/text/completion' },
    { id: 'audio', label: 'Audio', endpoint: '/v1/audio/speech' },
    { id: 'images', label: 'Images', endpoint: '/v1/images/generate' },
    { id: 'embeddings', label: 'Embeddings', endpoint: '/v1/embeddings' },
    { id: 'vision', label: 'Vision', endpoint: '/v1/vision/analyze' }
  ]

  const platforms = [
    { id: 'openai', label: 'OpenAI', model: 'openai/tts-1' },
    { id: 'anthropic', label: 'Anthropic', model: 'anthropic/claude-3' },
    { id: 'google', label: 'Google', model: 'google/gemini-pro' },
    { id: 'cohere', label: 'Cohere', model: 'cohere/command' }
  ]

  // Scroll-triggered animations
  useEffect(() => {
    const handleScroll = () => {
      setNavScrolled(window.scrollY > 50)
      
      // Animate sections on scroll
      sectionRefs.current.forEach((section) => {
        if (section) {
          const rect = section.getBoundingClientRect()
          const isVisible = rect.top < window.innerHeight * 0.8 && rect.bottom > 0
          if (isVisible) {
            section.classList.add('visible')
          }
        }
      })
      
      // Animate cards on scroll
      cardRefs.current.forEach((card) => {
        if (card) {
          const rect = card.getBoundingClientRect()
          const isVisible = rect.top < window.innerHeight * 0.8 && rect.bottom > 0
          if (isVisible) {
            card.classList.add('visible')
          }
        }
      })
    }
    
    window.addEventListener('scroll', handleScroll)
    handleScroll() // Initial check
    
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const getCodeSnippet = () => {
    const facility = facilities.find(f => f.id === selectedFacility)
    const platform = platforms.find(p => p.id === selectedPlatform)
    const url = `https://smartspace.ai${facility.endpoint}`

    if (selectedLanguage === 'python') {
      return `# pip install requests
import requests

url = "${url}"
headers = {
    "Authorization": "Bearer ${apiKey}"
}
payload = {
    "model": "${platform.model}",
    "text": "Hello, world!",
    "voice": "nova"
}

response = requests.post(
    url,
    headers=headers,
    json=payload
)
print(response.json())`
    } else if (selectedLanguage === 'java') {
      return `import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import java.net.http.HttpRequest.BodyPublishers;
import java.net.http.HttpResponse.BodyHandlers;
import com.fasterxml.jackson.databind.ObjectMapper;

HttpClient client = HttpClient.newHttpClient();
ObjectMapper mapper = new ObjectMapper();

String url = "${url}";
String json = mapper.writeValueAsString(Map.of(
    "model", "${platform.model}",
    "text", "Hello, world!",
    "voice", "nova"
));

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create(url))
    .header("Authorization", "Bearer ${apiKey}")
    .header("Content-Type", "application/json")
    .POST(BodyPublishers.ofString(json))
    .build();

HttpResponse<String> response = client.send(request, BodyHandlers.ofString());
System.out.println(response.body());`
    } else if (selectedLanguage === 'javascript') {
      return `const fetch = require('node-fetch');

const url = "${url}";
const headers = {
    "Authorization": "Bearer ${apiKey}",
    "Content-Type": "application/json"
};
const payload = {
    model: "${platform.model}",
    text: "Hello, world!",
    voice: "nova"
};

fetch(url, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(payload)
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));`
    }
  }

  return (
    <div className="landing-page">
      {/* Navigation */}
      <nav className={`nav ${navScrolled ? 'scrolled' : ''}`}>
        <div className="nav-container">
          <Link to="/" className="nav-logo">
            <SmartSpaceIcon size={28} className="nav-logo-icon" />
            <span>SmartSpace</span>
          </Link>
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
          <div className="hero-content">
            <div className="code-snippet-container">
              <div className="code-snippet-card">
                <div className="code-header">
                  <div className="code-tabs">
                    <button 
                      className={`code-tab ${selectedLanguage === 'python' ? 'active' : ''}`}
                      onClick={() => setSelectedLanguage('python')}
                    >
                      Python
                    </button>
                    <button 
                      className={`code-tab ${selectedLanguage === 'java' ? 'active' : ''}`}
                      onClick={() => setSelectedLanguage('java')}
                    >
                      Java
                    </button>
                    <button 
                      className={`code-tab ${selectedLanguage === 'javascript' ? 'active' : ''}`}
                      onClick={() => setSelectedLanguage('javascript')}
                    >
                      JavaScript
                    </button>
                  </div>
                </div>
                <div className="code-selectors">
                  <div className="selector-group">
                    <label>Facility:</label>
                    <select 
                      value={selectedFacility} 
                      onChange={(e) => setSelectedFacility(e.target.value)}
                      className="code-select"
                    >
                      {facilities.map(f => (
                        <option key={f.id} value={f.id}>{f.label}</option>
                      ))}
                    </select>
                  </div>
                  <div className="selector-group">
                    <label>Platform:</label>
                    <select 
                      value={selectedPlatform} 
                      onChange={(e) => setSelectedPlatform(e.target.value)}
                      className="code-select"
                    >
                      {platforms.map(p => (
                        <option key={p.id} value={p.id}>{p.label}</option>
                      ))}
                    </select>
                  </div>
                </div>
                <pre className="code-block">
                  <code>{getCodeSnippet()}</code>
                </pre>
              </div>
            </div>
            <div className="hero-cta-section">
              <h1 className="hero-title">
                Autonomous Pay-Per-Use API Access<br />
                with USDC
              </h1>
              <p className="hero-subtitle">
                A secure gateway that allows users and AI agents to call paid APIs (OpenAI, Google, Gemini, etc.)<br />
                and pay instantly per request using USDC. No API keys needed. Transparent, controlled, and predictable billing.
              </p>
              <div className="api-key-display">
                <label>Your API Key:</label>
                <div className="api-key-value">{apiKey}</div>
              </div>
              <Link to="/signup" className="btn btn-primary btn-large btn-get-key">
                Get Your Key
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section 
        ref={(el) => (sectionRefs.current[0] = el)}
        className="section section-problem"
      >
        <div className="container">
          <h2 className="section-title">
            The Current State of AI API Access is Broken
          </h2>
          <p className="section-subtitle">
            Shared keys, unpredictable billing, and manual management create risk and overhead
          </p>
          
          <div className="problem-grid">
            <div 
              ref={(el) => (cardRefs.current[0] = el)}
              className="problem-card"
            >
              <h3>Shared API Keys</h3>
              <p>Sharing API keys across teams creates security risks. Revoking access means breaking production. Managing credentials becomes a nightmare.</p>
            </div>
            <div 
              ref={(el) => (cardRefs.current[1] = el)}
              className="problem-card"
            >
              <h3>Unpredictable Billing</h3>
              <p>Monthly bills surprise you. Hard to track exact usage per request. Finance teams struggle to audit costs. No per-request transparency.</p>
            </div>
            <div 
              ref={(el) => (cardRefs.current[2] = el)}
              className="problem-card"
            >
              <h3>Agent Limitations</h3>
              <p>AI agents cannot safely make paid API calls autonomously. Manual approvals break automation. No spending controls for autonomous systems.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Solution Section */}
      <section 
        ref={(el) => (sectionRefs.current[1] = el)}
        id="features" 
        className="section section-solution"
      >
        <div className="container">
          <h2 className="section-title">One Gateway. Unlimited Possibilities.</h2>
          <p className="section-subtitle">
            SmartSpace becomes your secure billing and control layer for autonomous API access
          </p>
          
          <div className="feature-grid">
            <div 
              ref={(el) => (cardRefs.current[3] = el)}
              className="feature-card"
            >
              <div className="feature-icon">⚡</div>
              <h3>Pay Per Request</h3>
              <p>Pay exactly what you use with instant USDC payments. No monthly commitments. Transparent pricing for every API call. Perfect for autonomous agents.</p>
            </div>
            <div 
              ref={(el) => (cardRefs.current[4] = el)}
              className="feature-card"
            >
              <div className="feature-icon">🔒</div>
              <h3>No API Keys Needed</h3>
              <p>Never expose your API keys. SmartSpace handles all authentication securely. Agents can make requests without credential management.</p>
            </div>
            <div 
              ref={(el) => (cardRefs.current[5] = el)}
              className="feature-card"
            >
              <div className="feature-icon">💰</div>
              <h3>Transparent Billing</h3>
              <p>See exactly what each request costs. Full transaction logs. Budget controls and spending policies. Enterprise-ready auditing.</p>
            </div>
            <div 
              ref={(el) => (cardRefs.current[6] = el)}
              className="feature-card"
            >
              <div className="feature-icon">🤖</div>
              <h3>Agent Ready</h3>
              <p>Autonomous agents can make API calls with built-in spending controls. SmartSpace evaluates, pays, and executes automatically.</p>
            </div>
            <div 
              ref={(el) => (cardRefs.current[7] = el)}
              className="feature-card"
            >
              <div className="feature-icon">📊</div>
              <h3>Usage Analytics</h3>
              <p>Track usage per request, per agent, per project. Real-time cost tracking. Detailed logs for every transaction.</p>
            </div>
            <div 
              ref={(el) => (cardRefs.current[8] = el)}
              className="feature-card"
            >
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
            Access {allModels.length > 0 ? allModels.length : '100'}+ AI models through one unified interface. No API keys needed.
          </p>
          
          {error && (
            <div className="model-error-message" style={{ color: '#BB4EEF', marginBottom: '20px', padding: '12px', background: 'rgba(187, 78, 239, 0.1)', borderRadius: '8px' }}>
              {error}
            </div>
          )}
          
          <ModelSearch
            onSearch={handleSearch}
            onFilterChange={handleFilterChange}
            providers={providers}
            categories={categories}
            disabled={isLoading}
          />
          
          {isLoading ? (
            <div className="model-loading" style={{ textAlign: 'center', padding: '60px 20px', color: '#F2F2F2' }}>
              <p>Loading models...</p>
            </div>
          ) : hasActiveFilters ? (
            <ModelGallery
              models={filteredModels}
              onModelClick={handleModelClick}
            />
          ) : (
            <div className="model-gallery-empty" style={{ textAlign: 'center', padding: '60px 20px', color: 'rgba(242, 242, 242, 0.7)' }}>
              <p style={{ fontSize: '16px', marginBottom: '8px' }}>Use the search bar or filters above to explore available models</p>
              <p style={{ fontSize: '14px', color: 'rgba(242, 242, 242, 0.5)' }}>Search by name, provider, or description • Filter by provider or category</p>
            </div>
          )}
        </div>
      </section>
      
      {selectedModel && (
        <ModelDetails
          model={selectedModel}
          onClose={() => setSelectedModel(null)}
        />
      )}

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
      <section 
        ref={(el) => (sectionRefs.current[2] = el)}
        id="faq" 
        className="section section-faq"
      >
        <div className="container">
          <h2 className="section-title">Frequently Asked Questions</h2>
          <div className="faq-grid">
            <div 
              ref={(el) => (cardRefs.current[9] = el)}
              className="faq-item"
            >
              <h3>How does USDC payment work?</h3>
              <p>You fund your SmartSpace wallet with USDC. Each API request is paid instantly from your balance. No monthly billing, no surprises. You only pay for what you use.</p>
            </div>
            <div 
              ref={(el) => (cardRefs.current[10] = el)}
              className="faq-item"
            >
              <h3>Do I need API keys from providers?</h3>
              <p>No! SmartSpace manages all API keys securely. You never expose credentials. Agents can make requests autonomously without key management.</p>
            </div>
            <div 
              ref={(el) => (cardRefs.current[11] = el)}
              className="faq-item"
            >
              <h3>Can AI agents use this autonomously?</h3>
              <p>Yes! Set budgets and spending rules per agent or project. Agents can make API calls automatically within those constraints. SmartSpace handles payment and execution.</p>
            </div>
            <div 
              ref={(el) => (cardRefs.current[12] = el)}
              className="faq-item"
            >
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

      {/* Chatbot Component */}
      <Chatbot />
    </div>
  )
}

export default LandingPage

