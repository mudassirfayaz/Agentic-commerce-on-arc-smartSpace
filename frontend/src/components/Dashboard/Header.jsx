import './Header.css'

const Header = ({ title = 'Dashboard' }) => {
  return (
    <header className="dashboard-header">
      <div className="header-content">
        <h1 className="header-title">{title}</h1>
        <div className="header-actions">
          <div className="wallet-balance">
            <span className="balance-label">USDC Balance</span>
            <span className="balance-amount">$0.00</span>
          </div>
          <button className="btn btn-primary btn-sm">Fund Wallet</button>
        </div>
      </div>
    </header>
  )
}

export default Header

