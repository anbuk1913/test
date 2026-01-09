        import React, { useState, useEffect, useRef } from 'react';
        
        // Mock useTimer hook for demo
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
          onVerify = (otp) => console.log('Verify:', otp), 
          onResend = () => console.log('Resend OTP'), 
          expiryTime = 600,
          loading = false 
        }) => {
          const [otp, setOtp] = useState(['', '', '', '', '', '']);
          const { timeLeft, isActive, start, reset } = useTimer(expiryTime);
          const inputRefs = useRef([]);
        
          useEffect(() => {
            start(expiryTime);
          }, []);
        
          const formatTime = (seconds) => {
            const mins = Math.floor(seconds / 60);
            const secs = seconds % 60;
            return `${mins}:${secs.toString().padStart(2, '0')}`;
          };
        
          const handleChange = (index, value) => {
            if (value.length > 1) {
              value = value.slice(-1);
            }
            
            if (!/^\d*$/.test(value)) return;
        
            const newOtp = [...otp];
            newOtp[index] = value;
            setOtp(newOtp);
        
            if (value !== '' && index < 5) {
              inputRefs.current[index + 1]?.focus();
            }
          };
        
          const handleKeyDown = (index, e) => {
            if (e.key === 'Backspace' && !otp[index] && index > 0) {
              inputRefs.current[index - 1]?.focus();
            }
          };
        
          const handlePaste = (e) => {
            e.preventDefault();
            const pastedData = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6);
            const newOtp = [...otp];
            
            for (let i = 0; i < pastedData.length; i++) {
              newOtp[i] = pastedData[i];
            }
            
            setOtp(newOtp);
            
            if (pastedData.length < 6) {
              inputRefs.current[pastedData.length]?.focus();
            } else {
              inputRefs.current[5]?.focus();
            }
          };
        
          const handleSubmit = () => {
            const otpString = otp.join('');
            if (otpString.length === 6) {
              onVerify(otpString);
            }
          };
        
          const handleResend = () => {
            setOtp(['', '', '', '', '', '']);
            reset(expiryTime);
            onResend();
            inputRefs.current[0]?.focus();
          };
        
          const isComplete = otp.every(digit => digit !== '');
          const isExpired = timeLeft === 0;
        
          return (
            <div style={{
              minHeight: '100vh',
              background: 'linear-gradient(135deg, #04285b 0%, #00b3d0 100%)',
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              padding: '20px',
              fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
            }}>
              <div style={{
                maxWidth: '480px',
                width: '100%',
                background: 'white',
                borderRadius: '16px',
                boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
                overflow: 'hidden'
              }}>
                {/* Header */}
                <div style={{
                  background: 'linear-gradient(135deg, #04285b 0%, #00b3d0 100%)',
                  padding: '40px 30px',
                  textAlign: 'center'
                }}>
                  <div style={{
                    width: '80px',
                    height: '80px',
                    background: 'rgba(255, 255, 255, 0.2)',
                    borderRadius: '50%',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    margin: '0 auto 20px',
                    backdropFilter: 'blur(10px)'
                  }}>
                    <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                      <path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4" />
                    </svg>
                  </div>
                  <h2 style={{
                    color: 'white',
                    fontSize: '28px',
                    margin: '0 0 10px 0',
                    fontWeight: '600'
                  }}>
                    Verify Your Account
                  </h2>
                  <p style={{
                    color: 'rgba(255, 255, 255, 0.9)',
                    fontSize: '15px',
                    margin: 0
                  }}>
                    Enter the 6-digit code sent to your email
                  </p>
                </div>
        
                {/* Content */}
                <div style={{ padding: '40px 30px' }}>
                  {/* Timer */}
                  <div style={{
                    background: isExpired ? 'linear-gradient(135deg, rgba(220, 38, 38, 0.1) 0%, rgba(239, 68, 68, 0.1) 100%)' : 'linear-gradient(135deg, rgba(4, 40, 91, 0.05) 0%, rgba(0, 179, 208, 0.05) 100%)',
                    border: `2px solid ${isExpired ? '#ef4444' : '#00b3d0'}`,
                    borderRadius: '12px',
                    padding: '20px',
                    textAlign: 'center',
                    marginBottom: '30px'
                  }}>
                    <div style={{
                      fontSize: '14px',
                      color: isExpired ? '#dc2626' : '#04285b',
                      fontWeight: '600',
                      marginBottom: '8px',
                      textTransform: 'uppercase',
                      letterSpacing: '1px'
                    }}>
                      {isExpired ? '⚠️ Code Expired' : '⏱️ Time Remaining'}
                    </div>
                    <div style={{
                      fontSize: '36px',
                      fontWeight: 'bold',
                      color: isExpired ? '#dc2626' : '#04285b',
                      fontFamily: 'monospace'
                    }}>
                      {formatTime(timeLeft)}
                    </div>
                  </div>
        
                  {/* OTP Input */}
                  <div style={{
                    display: 'flex',
                    gap: '12px',
                    justifyContent: 'center',
                    marginBottom: '30px'
                  }}>
                    {otp.map((digit, index) => (
                      <input
                        key={index}
                        ref={el => inputRefs.current[index] = el}
                        type="text"
                        inputMode="numeric"
                        maxLength={1}
                        value={digit}
                        onChange={(e) => handleChange(index, e.target.value)}
                        onKeyDown={(e) => handleKeyDown(index, e)}
                        onPaste={handlePaste}
                        disabled={isExpired}
                        style={{
                          width: '56px',
                          height: '64px',
                          fontSize: '28px',
                          fontWeight: 'bold',
                          textAlign: 'center',
                          border: `2px solid ${isExpired ? '#e5e7eb' : digit ? '#00b3d0' : '#d1d5db'}`,
                          borderRadius: '12px',
                          outline: 'none',
                          transition: 'all 0.3s ease',
                          background: isExpired ? '#f9fafb' : 'white',
                          color: isExpired ? '#9ca3af' : '#04285b',
                          cursor: isExpired ? 'not-allowed' : 'text'
                        }}
                        onFocus={(e) => {
                          if (!isExpired) {
                            e.target.style.borderColor = '#04285b';
                            e.target.style.boxShadow = '0 0 0 3px rgba(0, 179, 208, 0.1)';
                          }
                        }}
                        onBlur={(e) => {
                          e.target.style.borderColor = digit ? '#00b3d0' : '#d1d5db';
                          e.target.style.boxShadow = 'none';
                        }}
                      />
                    ))}
                  </div>
        
                  {/* Submit Button */}
                  <button
                    onClick={handleSubmit}
                    disabled={!isComplete || isExpired || loading}
                    style={{
                      width: '100%',
                      padding: '16px',
                      fontSize: '16px',
                      fontWeight: '600',
                      color: 'white',
                      background: (!isComplete || isExpired || loading) ? '#cbd5e1' : 'linear-gradient(135deg, #04285b 0%, #00b3d0 100%)',
                      border: 'none',
                      borderRadius: '12px',
                      cursor: (!isComplete || isExpired || loading) ? 'not-allowed' : 'pointer',
                      transition: 'all 0.3s ease',
                      boxShadow: (!isComplete || isExpired || loading) ? 'none' : '0 4px 15px rgba(0, 179, 208, 0.3)',
                      marginBottom: '15px'
                    }}
                    onMouseEnter={(e) => {
                      if (isComplete && !isExpired && !loading) {
                        e.target.style.transform = 'translateY(-2px)';
                        e.target.style.boxShadow = '0 6px 20px rgba(0, 179, 208, 0.4)';
                      }
                    }}
                    onMouseLeave={(e) => {
                      e.target.style.transform = 'translateY(0)';
                      e.target.style.boxShadow = (!isComplete || isExpired || loading) ? 'none' : '0 4px 15px rgba(0, 179, 208, 0.3)';
                    }}
                  >
                    {loading ? (
                      <span style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px' }}>
                        <span style={{
                          width: '20px',
                          height: '20px',
                          border: '3px solid rgba(255,255,255,0.3)',
                          borderTop: '3px solid white',
                          borderRadius: '50%',
                          animation: 'spin 1s linear infinite'
                        }}></span>
                        Verifying...
                      </span>
                    ) : (
                      '✓ Verify OTP'
                    )}
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
                      color: loading ? '#9ca3af' : '#04285b',
                      background: 'transparent',
                      border: `2px solid ${loading ? '#e5e7eb' : '#04285b'}`,
                      borderRadius: '12px',
                      cursor: loading ? 'not-allowed' : 'pointer',
                      transition: 'all 0.3s ease'
                    }}
                    onMouseEnter={(e) => {
                      if (!loading) {
                        e.target.style.background = '#04285b';
                        e.target.style.color = 'white';
                      }
                    }}
                    onMouseLeave={(e) => {
                      e.target.style.background = 'transparent';
                      e.target.style.color = loading ? '#9ca3af' : '#04285b';
                    }}
                  >
                    🔄 Resend OTP
                  </button>
        
                  {/* Help Text */}
                  <div style={{
                    marginTop: '30px',
                    padding: '15px',
                    background: '#f8f9fa',
                    borderRadius: '8px',
                    fontSize: '13px',
                    color: '#6c757d',
                    lineHeight: '1.6',
                    textAlign: 'center'
                  }}>
                    Didn't receive the code? Check your spam folder or click resend to get a new code.
                  </div>
                </div>
              </div>
        
              <style>{`
                @keyframes spin {
                  to { transform: rotate(360deg); }
                }
              `}</style>
            </div>
          );
        };
        
        export default OTPVerification;
