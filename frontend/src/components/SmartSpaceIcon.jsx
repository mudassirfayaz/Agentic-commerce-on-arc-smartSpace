const SmartSpaceIcon = ({ size = 24, className = '' }) => {
  // Generate unique ID for gradients to avoid conflicts
  const gradientId = `smartspaceGradient-${Math.random().toString(36).substr(2, 9)}`
  
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      {/* Main network/space icon with interconnected nodes */}
      <defs>
        <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#BB4EEF" />
          <stop offset="100%" stopColor="#A03DD9" />
        </linearGradient>
      </defs>
      
      {/* Central hub */}
      <circle cx="16" cy="16" r="4" fill={`url(#${gradientId})`} />
      
      {/* Outer nodes */}
      <circle cx="8" cy="8" r="2.5" fill="#BB4EEF" opacity="0.8" />
      <circle cx="24" cy="8" r="2.5" fill="#BB4EEF" opacity="0.8" />
      <circle cx="8" cy="24" r="2.5" fill="#BB4EEF" opacity="0.8" />
      <circle cx="24" cy="24" r="2.5" fill="#BB4EEF" opacity="0.8" />
      
      {/* Connection lines */}
      <line x1="16" y1="16" x2="8" y2="8" stroke={`url(#${gradientId})`} strokeWidth="1.5" opacity="0.6" />
      <line x1="16" y1="16" x2="24" y2="8" stroke={`url(#${gradientId})`} strokeWidth="1.5" opacity="0.6" />
      <line x1="16" y1="16" x2="8" y2="24" stroke={`url(#${gradientId})`} strokeWidth="1.5" opacity="0.6" />
      <line x1="16" y1="16" x2="24" y2="24" stroke={`url(#${gradientId})`} strokeWidth="1.5" opacity="0.6" />
      
      {/* Additional connecting lines between outer nodes */}
      <line x1="8" y1="8" x2="24" y2="8" stroke="#BB4EEF" strokeWidth="1" opacity="0.3" />
      <line x1="8" y1="24" x2="24" y2="24" stroke="#BB4EEF" strokeWidth="1" opacity="0.3" />
      <line x1="8" y1="8" x2="8" y2="24" stroke="#BB4EEF" strokeWidth="1" opacity="0.3" />
      <line x1="24" y1="8" x2="24" y2="24" stroke="#BB4EEF" strokeWidth="1" opacity="0.3" />
    </svg>
  )
}

export default SmartSpaceIcon

