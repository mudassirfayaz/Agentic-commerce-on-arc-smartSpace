import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import SmartSpaceIcon from '../components/SmartSpaceIcon'
import './Auth.css'

const Login = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const navigate = useNavigate()

  const handleSubmit = (e) => {
    e.preventDefault()
    // TODO: Implement actual authentication
    // For now, just redirect to dashboard
    navigate('/dashboard')
  }

  return (
    <div className="auth-page">
      <div className="auth-container">
        <Link to="/" className="auth-logo">
          <SmartSpaceIcon size={32} className="auth-logo-icon" />
          <span>SmartSpace</span>
        </Link>
        
        <div className="auth-card">
          <h1>Welcome Back</h1>
          <p className="auth-subtitle">Sign in to your SmartSpace account</p>
          
          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="password">Password</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter your password"
                required
              />
            </div>
            
            <div className="form-options">
              <label className="checkbox-label">
                <input type="checkbox" />
                Remember me
              </label>
              <Link to="#" className="link">Forgot password?</Link>
            </div>
            
            <button type="submit" className="btn btn-primary btn-block">
              Sign In
            </button>
          </form>
          
          <div className="auth-divider">
            <span>Or continue with</span>
          </div>
          
          <div className="auth-social">
            <button className="btn btn-outline btn-block">
              Connect Wallet
            </button>
          </div>
          
          <p className="auth-footer">
            Don't have an account? <Link to="/signup" className="link">Sign up</Link>
          </p>
        </div>
        
        <p className="auth-back">
          <Link to="/" className="link">← Back to home</Link>
        </p>
      </div>
    </div>
  )
}

export default Login

