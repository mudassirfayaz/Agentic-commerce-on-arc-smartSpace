import { useState, useEffect } from 'react'
import DashboardLayout from '../components/Dashboard/DashboardLayout'
import ApiKeySection from '../components/Dashboard/ApiKeySection'
import SimpleChatbot from '../components/Dashboard/SimpleChatbot'
import CodeExample from '../components/Dashboard/CodeExample'
import './Dashboard.css'

const Dashboard = () => {
  const [apiKey, setApiKey] = useState(null)
  const [selectedModel, setSelectedModel] = useState('ollama/qalb-urdu')
  const [requestText, setRequestText] = useState('')
  const [lastRequest, setLastRequest] = useState(null)

  // Fetch API key to share with components
  useEffect(() => {
    fetchApiKey()
  }, [])

  const fetchApiKey = async () => {
    try {
      const response = await fetch('/api/v1/api-keys', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      })

      if (response.ok) {
        const data = await response.json()
        setApiKey(data.api_key || data.key || null)
      }
    } catch (err) {
      console.error('Error fetching API key:', err)
    }
  }

  const handleRequestComplete = (request) => {
    setLastRequest(request)
    setSelectedModel(request.model)
    setRequestText(request.text)
  }

  return (
    <DashboardLayout>
      <ApiKeySection onApiKeyChange={setApiKey} />

      <div className="dashboard-main-content">
        <div className="dashboard-left">
          <SimpleChatbot
            apiKey={apiKey}
            onRequestComplete={handleRequestComplete}
            onModelChange={setSelectedModel}
            onTextChange={setRequestText}
          />
        </div>

        <div className="dashboard-right">
          <CodeExample
            apiKey={apiKey}
            selectedModel={selectedModel}
            requestText={requestText}
            lastRequest={lastRequest}
          />
        </div>
      </div>
    </DashboardLayout>
  )
}

export default Dashboard
