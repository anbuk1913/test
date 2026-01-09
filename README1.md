        import React, { useState, useEffect } from 'react';
        
        // Mock hook for demonstration
        const useTimer = (initialTime) => {
          const [timeLeft, setTimeLeft] = useState(initialTime);
          const [isActive, setIsActive] = useState(false);
        
          useEffect(() => {
            let interval = null;
            if (isActive && timeLeft > 0) {
              interval = setInterval(() => {
                setTimeLeft(time => time - 1);
              }, 1000);
            } else if (timeLeft === 0) {
              setIsActive(false);
            }
            return () => clearInterval(interval);
          }, [isActive, timeLeft]);
        
          const start = (time) => {
            setTimeLeft(time);
            setIsActive(true);
          };
        
          const reset = (time) => {
            setTimeLeft(time);
            setIsActive(true);
          };
        
          return { timeLeft, isActive, start, reset };
        };
        
        const OTPVerification = ({ 
          onVerify, 
          onResend, 
          expiryTime,
          loading 
        }) => {
          const [otp, setOtp] = useState('');
          const { timeLeft, isActive, start, reset } = useTimer(expiryTime);
        
          useEffect(() => {
            start(expiryTime);
          }, []);
        
          const handleResend = () => {
            reset(75);
            onResend();
          };
        
          const formatTime = (seconds) => {
            const mins = Math.floor(seconds / 60);
            const secs = seconds % 60;
            return `${mins}:${secs.toString().padStart(2, '0')}`;
          };
        
          return (
            <div style={{
              minHeight: '100vh',
              background: 'linear-gradient(135deg, #04285b 0%, #00b3d0 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: '20px',
              fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
            }}>
              <div style={{
                background: 'white',
                borderRadius: '16px',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
                padding: '48px 40px',
                maxWidth: '480px',
                width: '100%'
              }}>
                {/* Header Icon */}
                <div style={{
                  width: '80px',
                  height: '80px',
                  background: 'linear-gradient(135deg, #04285b 0%, #00b3d0 100%)',
                  borderRadius: '50%',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 24px',
                  boxShadow: '0 8px 24px rgba(0, 179, 208, 0.3)'
                }}>
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                    <circle cx="12" cy="10" r="3"/>
                  </svg>
                </div>
        
                {/* Title */}
                <h2 style={{
                  color: '#04285b',
                  fontSize: '28px',
                  fontWeight: '700',
                  textAlign: 'center',
                  marginBottom: '12px'
                }}>
                  Enter OTP
                </h2>
        
                <p style={{
                  color: '#6b7280',
                  fontSize: '15px',
                  textAlign: 'center',
                  marginBottom: '32px'
                }}>
                  We've sent a verification code to your device
                </p>
        
                {/* Timer Display */}
                <div style={{
                  background: timeLeft <= 30 ? 'linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%)' : 'linear-gradient(135deg, rgba(4, 40, 91, 0.08) 0%, rgba(0, 179, 208, 0.08) 100%)',
                  border: `2px solid ${timeLeft <= 30 ? '#ef4444' : '#00b3d0'}`,
                  borderRadius: '12px',
                  padding: '20px',
                  marginBottom: '32px',
                  textAlign: 'center',
                  transition: 'all 0.3s ease'
                }}>
                  <div style={{
                    color: '#6b7280',
                    fontSize: '13px',
                    fontWeight: '600',
                    textTransform: 'uppercase',
                    letterSpacing: '1px',
                    marginBottom: '8px'
                  }}>
                    Time Remaining
                  </div>
                  <div style={{
                    fontSize: '36px',
                    fontWeight: '700',
                    color: timeLeft <= 30 ? '#ef4444' : '#04285b',
                    letterSpacing: '2px',
                    transition: 'color 0.3s ease'
                  }}>
                    {formatTime(timeLeft)}
                  </div>
                </div>
        
                {/* OTP Input */}
                <input
                  type="text"
                  maxLength={4}
                  value={otp}
                  onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
                  placeholder="Enter 4-digit OTP"
                  disabled={timeLeft === 0}
                  style={{
                    width: '100%',
                    padding: '18px',
                    fontSize: '24px',
                    textAlign: 'center',
                    letterSpacing: '12px',
                    border: '2px solid #e5e7eb',
                    borderRadius: '12px',
                    marginBottom: '24px',
                    outline: 'none',
                    fontWeight: '600',
                    color: '#04285b',
                    transition: 'all 0.3s ease',
                    opacity: timeLeft === 0 ? '0.5' : '1',
                    cursor: timeLeft === 0 ? 'not-allowed' : 'text'
                  }}
                  onFocus={(e) => {
                    if (timeLeft > 0) {
                      e.target.style.borderColor = '#00b3d0';
                      e.target.style.boxShadow = '0 0 0 3px rgba(0, 179, 208, 0.1)';
                    }
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = '#e5e7eb';
                    e.target.style.boxShadow = 'none';
                  }}
                />
        
                {/* Verify Button */}
                <button 
                  onClick={() => onVerify(otp)} 
                  disabled={otp.length !== 4 || timeLeft === 0 || loading}
                  style={{
                    width: '100%',
                    padding: '16px',
                    fontSize: '16px',
                    fontWeight: '600',
                    color: 'white',
                    background: (otp.length !== 4 || timeLeft === 0 || loading) 
                      ? '#9ca3af' 
                      : 'linear-gradient(135deg, #04285b 0%, #00b3d0 100%)',
                    border: 'none',
                    borderRadius: '12px',
                    cursor: (otp.length !== 4 || timeLeft === 0 || loading) ? 'not-allowed' : 'pointer',
                    transition: 'all 0.3s ease',
                    boxShadow: (otp.length !== 4 || timeLeft === 0 || loading) 
                      ? 'none' 
                      : '0 4px 15px rgba(0, 179, 208, 0.3)',
                    marginBottom: '16px'
                  }}
                  onMouseEnter={(e) => {
                    if (!(otp.length !== 4 || timeLeft === 0 || loading)) {
                      e.target.style.transform = 'translateY(-2px)';
                      e.target.style.boxShadow = '0 6px 20px rgba(0, 179, 208, 0.4)';
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (!(otp.length !== 4 || timeLeft === 0 || loading)) {
                      e.target.style.transform = 'translateY(0)';
                      e.target.style.boxShadow = '0 4px 15px rgba(0, 179, 208, 0.3)';
                    }
                  }}
                >
                  {loading ? (
                    <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}>
                      <span style={{
                        width: '16px',
                        height: '16px',
                        border: '2px solid white',
                        borderTop: '2px solid transparent',
                        borderRadius: '50%',
                        animation: 'spin 0.8s linear infinite'
                      }}></span>
                      Verifying...
                    </span>
                  ) : 'Verify OTP'}
                </button>
        
                {/* Resend Button */}
                <button 
                  onClick={handleResend} 
                  disabled={loading}
                  style={{
                    width: '100%',
                    padding: '16px',
                    fontSize: '15px',
                    fontWeight: '600',
                    color: '#00b3d0',
                    background: 'transparent',
                    border: '2px solid #00b3d0',
                    borderRadius: '12px',
                    cursor: loading ? 'not-allowed' : 'pointer',
                    transition: 'all 0.3s ease',
                    opacity: loading ? '0.5' : '1'
                  }}
                  onMouseEnter={(e) => {
                    if (!loading) {
                      e.target.style.background = 'rgba(0, 179, 208, 0.08)';
                      e.target.style.transform = 'translateY(-1px)';
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (!loading) {
                      e.target.style.background = 'transparent';
                      e.target.style.transform = 'translateY(0)';
                    }
                  }}
                >
                  Resend OTP
                </button>
        
                {/* Footer Message */}
                {timeLeft === 0 && (
                  <div style={{
                    marginTop: '24px',
                    padding: '16px',
                    background: '#fef2f2',
                    border: '1px solid #fecaca',
                    borderRadius: '8px',
                    color: '#991b1b',
                    fontSize: '14px',
                    textAlign: 'center'
                  }}>
                    ⚠️ OTP has expired. Please request a new code.
                  </div>
                )}
        
                <style>{`
                  @keyframes spin {
                    to { transform: rotate(360deg); }
                  }
                `}</style>
              </div>
            </div>
          );
        };
        
        // Demo wrapper
        export default function App() {
          const handleVerify = (otp) => {
            console.log('Verifying OTP:', otp);
            alert(`Verifying OTP: ${otp}`);
          };
        
          const handleResend = () => {
            console.log('Resending OTP');
            alert('OTP Resent!');
          };
        
          return (
            <OTPVerification
              onVerify={handleVerify}
              onResend={handleResend}
              expiryTime={75}
              loading={false}
            />
          );
        }
