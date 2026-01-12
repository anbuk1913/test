        import React, { useState } from 'react';
        
        interface Props {
          onSubmit: (passkey: string) => void;
          loading: boolean;
        }
        
        export const PasskeyInput: React.FC<Props> = ({ onSubmit, loading }) => {
          const [passkey, setPasskey] = useState('');
        
          const handleSubmit = (e: React.FormEvent) => {
            e.preventDefault();
            if (passkey.length === 6) {
              onSubmit(passkey);
            }
          };
        
          return (
            <div className="min-h-screen flex items-center justify-center p-4" style={{ background: 'linear-gradient(135deg, #04285b 0%, #00b3d0 100%)' }}>
              <div className="w-full max-w-md">
                <div className="bg-white rounded-2xl shadow-2xl p-8">
                  {/* Header */}
                  <div className="text-center mb-8">
                    <div className="inline-flex items-center justify-center w-16 h-16 rounded-full mb-4" style={{ background: 'linear-gradient(135deg, #04285b 0%, #00b3d0 100%)' }}>
                      <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                      </svg>
                    </div>
                    <h2 className="text-3xl font-bold mb-2" style={{ color: '#04285b' }}>
                      Secure Access
                    </h2>
                    <p className="text-gray-600">
                      Enter your 6-character passkey to continue
                    </p>
                  </div>
        
                  {/* Input Form */}
                  <div className="space-y-6">
                    <div>
                      <label className="block text-sm font-medium mb-2" style={{ color: '#04285b' }}>
                        Passkey
                      </label>
                      <div className="relative">
                        <input
                          type="password"
                          maxLength={6}
                          value={passkey}
                          onChange={(e) => setPasskey(e.target.value.replace(/[^a-zA-Z]/g, '').toUpperCase())}
                          placeholder="******"
                          disabled={loading}
                          className="w-full px-4 py-3 text-center text-2xl font-bold tracking-widest border-2 rounded-lg focus:outline-none focus:ring-2 transition-all duration-200"
                          style={{
                            borderColor: passkey.length === 6 ? '#00b3d0' : '#e5e7eb',
                            color: '#04285b'
                          }}
                          onFocus={(e) => e.target.style.borderColor = '#00b3d0'}
                          onBlur={(e) => {
                            if (passkey.length !== 6) e.target.style.borderColor = '#e5e7eb';
                          }}
                        />
                        {passkey.length > 0 && (
                          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                            <span className="text-sm font-medium" style={{ color: passkey.length === 6 ? '#00b3d0' : '#9ca3af' }}>
                              {passkey.length}/6
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
        
                    <button
                      onClick={handleSubmit}
                      disabled={passkey.length !== 6 || loading}
                      className="w-full py-3 px-4 rounded-lg font-semibold text-white transition-all duration-200 transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none shadow-lg"
                      style={{
                        background: passkey.length === 6 && !loading ? 'linear-gradient(135deg, #04285b 0%, #00b3d0 100%)' : '#cbd5e1'
                      }}
                    >
                      {loading ? (
                        <span className="flex items-center justify-center">
                          <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Verifying...
                        </span>
                      ) : (
                        'Submit Passkey'
                      )}
                    </button>
                  </div>
        
                  {/* Footer */}
                  <div className="mt-6 text-center">
                    <p className="text-sm text-gray-500">
                      Need help? <a href="#" className="font-medium hover:underline" style={{ color: '#00b3d0' }}>Contact support</a>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          );
        };
        
        // Demo wrapper
        export default function App() {
          const [loading, setLoading] = useState(false);
        
          const handleSubmit = (passkey: string) => {
            setLoading(true);
            setTimeout(() => {
              alert(`Passkey submitted: ${passkey}`);
              setLoading(false);
            }, 2000);
          };
        
          return <PasskeyInput onSubmit={handleSubmit} loading={loading} />;
        }
