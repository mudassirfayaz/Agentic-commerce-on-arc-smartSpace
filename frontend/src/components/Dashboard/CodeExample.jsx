import { useState } from 'react'
import './CodeExample.css'

const CodeExample = ({ apiKey, selectedModel, requestText, lastRequest }) => {
  const [activeTab, setActiveTab] = useState('python')
  const [copySuccess, setCopySuccess] = useState({})

  // Mask API key by default
  const displayApiKey = apiKey ? (apiKey.length > 8 ? `${apiKey.substring(0, 4)}${'•'.repeat(apiKey.length - 8)}${apiKey.substring(apiKey.length - 4)}` : '••••••••') : 'YOUR_API_KEY'
  const fullApiKey = apiKey || 'YOUR_API_KEY'
  const model = selectedModel || 'ollama/qalb-urdu'
  const text = requestText || 'Hello, world!'

  const handleCopy = async (code, language) => {
    try {
      await navigator.clipboard.writeText(code)
      setCopySuccess({ [language]: true })
      setTimeout(() => {
        setCopySuccess({ ...copySuccess, [language]: false })
      }, 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  const generatePythonCode = () => {
    return `import requests

url = "https://smartspace.ai/v1/text/completion"
headers = {
    "Authorization": "Bearer ${fullApiKey}"
}
payload = {
    "model": "${model}",
    "text": "${text}"
}

response = requests.post(url, headers=headers, json=payload)
print(response.json())`
  }

  const generateJavaScriptCode = () => {
    return `const response = await fetch('https://smartspace.ai/v1/text/completion', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ${fullApiKey}'
  },
  body: JSON.stringify({
    model: '${model}',
    text: '${text}'
  })
});

const data = await response.json();
console.log(data);`
  }

  const generateCurlCode = () => {
    return `curl -X POST https://smartspace.ai/v1/text/completion \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer ${fullApiKey}" \\
  -d '{
    "model": "${model}",
    "text": "${text}"
  }'`
  }

  const codeExamples = {
    python: generatePythonCode(),
    javascript: generateJavaScriptCode(),
    curl: generateCurlCode(),
  }

  return (
    <div className="code-example">
      <div className="code-example-header">
        <h3>Code Examples</h3>
        <p className="code-example-subtitle">Copy and use in your application</p>
      </div>

      <div className="code-tabs">
        <button
          className={`code-tab ${activeTab === 'python' ? 'active' : ''}`}
          onClick={() => setActiveTab('python')}
        >
          Python
        </button>
        <button
          className={`code-tab ${activeTab === 'javascript' ? 'active' : ''}`}
          onClick={() => setActiveTab('javascript')}
        >
          JavaScript
        </button>
        <button
          className={`code-tab ${activeTab === 'curl' ? 'active' : ''}`}
          onClick={() => setActiveTab('curl')}
        >
          cURL
        </button>
      </div>

      <div className="code-block-container">
        <div className="code-block-header">
          <span className="code-language">{activeTab}</span>
          <button
            className="copy-button"
            onClick={() => handleCopy(codeExamples[activeTab], activeTab)}
            aria-label={`Copy ${activeTab} code`}
          >
            {copySuccess[activeTab] ? '✓ Copied!' : 'Copy'}
          </button>
        </div>
        <pre className="code-block">
          <code>{codeExamples[activeTab]}</code>
        </pre>
      </div>

      {!apiKey && (
        <div className="code-warning">
          ⚠️ Generate an API key to see your actual key in the examples
        </div>
      )}

      {lastRequest && (
        <div className="code-note">
          <strong>Last Request:</strong> Model: {lastRequest.model}, Status: {lastRequest.status}
        </div>
      )}
    </div>
  )
}

export default CodeExample

