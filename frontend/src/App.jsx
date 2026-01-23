import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import LandingPage from './pages/LandingPage'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Dashboard from './pages/Dashboard'
import Projects from './pages/Projects'
import Agents from './pages/Agents'
import Usage from './pages/Usage'
import Billing from './pages/Billing'
import ApiKeys from './pages/ApiKeys'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/dashboard/projects" element={<Projects />} />
        <Route path="/dashboard/agents" element={<Agents />} />
        <Route path="/dashboard/usage" element={<Usage />} />
        <Route path="/dashboard/billing" element={<Billing />} />
        <Route path="/dashboard/api-keys" element={<ApiKeys />} />
      </Routes>
    </Router>
  )
}

export default App

