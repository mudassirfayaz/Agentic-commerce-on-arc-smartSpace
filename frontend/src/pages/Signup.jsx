import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'
import SmartSpaceIcon from '../components/SmartSpaceIcon'
import './Auth.css'

const Signup = () => {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const navigate = useNavigate()

  const handleSubmit = (e) => {
    e.preventDefault()
    // TODO: Implement actual registration
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
          <h1>Create Account</h1>
          <p className="auth-subtitle">Start using SmartSpace today</p>
          
          <form onSubmit={handleSubmit} className="auth-form">
            <div className="form-group">
              <label htmlFor="name">Full Name</label>
              <input
                type="text"
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="John Doe"
                required
              />
            </div>
            
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
                placeholder="Create a strong password"
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="confirmPassword">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm your password"
                required
              />
            </div>
            
            <div className="form-options">
              <label className="checkbox-label">
                <input type="checkbox" required />
                I agree to the <Link to="#" className="link">Terms of Service</Link> and <Link to="#" className="link">Privacy Policy</Link>
              </label>
            </div>
            
            <button type="submit" className="btn btn-primary btn-block">
              Create Account
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
            Already have an account? <Link to="/login" className="link">Sign in</Link>
          </p>
        </div>
        
        <p className="auth-back">
          <Link to="/" className="link">← Back to home</Link>
        </p>
      </div>
    </div>
  )
}

export default Signup

