    import { useState } from 'react';
    
    export default function LinkWithCopy() {
      const [copied, setCopied] = useState(false);
      const link = "https://example.com/your-link-here";
    
      const handleCopy = async () => {
        try {
          await navigator.clipboard.writeText(link);
          setCopied(true);
          setTimeout(() => setCopied(false), 2000);
        } catch (err) {
          console.error('Failed to copy:', err);
        }
      };
    
      return (
        <>
          <style>{`
            @keyframes letterShow {
              0% {
                transform: translateY(50%);
                opacity: 0;
                filter: blur(20px);
              }
              20% {
                transform: translateY(70%);
                opacity: 1;
              }
              50% {
                transform: translateY(-15%);
                opacity: 1;
                filter: blur(0);
              }
              100% {
                transform: translateY(0);
                opacity: 1;
              }
            }
    
            @keyframes letterHide {
              0% {
                transform: translateY(0);
                opacity: 1;
              }
              100% {
                transform: translateY(-70%);
                opacity: 0;
                filter: blur(3px);
              }
            }
    
            @keyframes bump {
              20% {
                stroke-dasharray: 3;
                stroke-dashoffset: 3;
              }
              30% {
                stroke-dasharray: 5;
                stroke-dashoffset: 3;
              }
              30.1% {
                stroke-dasharray: 3;
                stroke-dashoffset: 6;
              }
              75% {
                stroke-dasharray: 3;
                stroke-dashoffset: 3;
              }
              100% {
                stroke-dasharray: 3;
                stroke-dashoffset: 3;
              }
            }
    
            @keyframes beat {
              0% {
                transform: scale(1);
              }
              50% {
                transform: scale(1.1);
              }
              100% {
                transform: scale(1);
              }
            }
    
            .copy-button-animated {
              cursor: pointer;
              background: linear-gradient(to bottom, #6e3bff, #7e51ff);
              color: #ffffff;
              border: 1px solid #af93ff;
              border-radius: 8px;
              position: relative;
              font-family: Arial, Helvetica, sans-serif;
              text-shadow: 0 2px 0 rgba(0, 0, 0, 0.25);
              box-shadow: 0 8px 10px -4px #503b89, 0 0 0 2px #562cce;
              font-size: 25px;
            }
    
            .copy-button-animated:active .button-content {
              box-shadow: inset -1px 12px 8px -5px rgba(71, 0, 137, 0.4), inset 0px -3px 8px 0px #d190ff;
            }
    
            .button-content {
              pointer-events: none;
              display: flex;
              align-items: center;
              justify-content: center;
              position: relative;
              height: 100%;
              width: 100%;
              padding: 4px;
              gap: 16px;
              border-radius: 7px;
              font-weight: 600;
              transition: all 0.3s ease;
            }
    
            .button-content::before {
              content: "";
              inset: 0;
              position: absolute;
              width: 80%;
              top: 45%;
              bottom: 35%;
              opacity: 0.7;
              margin: auto;
              background: linear-gradient(to bottom, transparent, #a78bfa);
              filter: brightness(1.3) blur(5px);
            }
    
            .button-letters {
              transition: all 0.3s ease;
              display: flex;
              align-items: center;
              justify-content: center;
              padding: 4px;
            }
    
            .button-letters span {
              display: block;
              color: transparent;
              position: relative;
              left: 6px;
              animation: letterShow 1.2s ease backwards;
            }
    
            .button-letters span:nth-child(1) { animation-delay: 0.03s; }
            .button-letters span:nth-child(2) { animation-delay: 0.06s; }
            .button-letters span:nth-child(3) { animation-delay: 0.09s; }
            .button-letters span:nth-child(4) { animation-delay: 0.12s; }
            .button-letters span:nth-child(5) { animation-delay: 0.15s; margin-left: 5px; }
            .button-letters span:nth-child(6) { animation-delay: 0.18s; margin-left: 1px; }
            .button-letters span:nth-child(7) { animation-delay: 0.21s; }
            .button-letters span:nth-child(8) { animation-delay: 0.24s; }
    
            .button-letters span::before,
            .button-letters span::after {
              content: attr(data-label);
              position: absolute;
              color: #ffffff;
              text-shadow: -1px 1px 2px #8b5cf6;
              left: 0;
            }
    
            .button-letters span::before {
              opacity: 0;
              transform: translateY(-100%);
            }
    
            .copy-button-animated:hover .button-letters span::before {
              animation: letterShow 0.7s ease;
            }
    
            .copy-button-animated:hover .button-letters span:nth-child(1)::before { animation-delay: 0.03s; }
            .copy-button-animated:hover .button-letters span:nth-child(2)::before { animation-delay: 0.06s; }
            .copy-button-animated:hover .button-letters span:nth-child(3)::before { animation-delay: 0.09s; }
            .copy-button-animated:hover .button-letters span:nth-child(4)::before { animation-delay: 0.12s; }
            .copy-button-animated:hover .button-letters span:nth-child(5)::before { animation-delay: 0.15s; }
            .copy-button-animated:hover .button-letters span:nth-child(6)::before { animation-delay: 0.18s; }
            .copy-button-animated:hover .button-letters span:nth-child(7)::before { animation-delay: 0.21s; }
            .copy-button-animated:hover .button-letters span:nth-child(8)::before { animation-delay: 0.24s; }
    
            .copy-button-animated:hover .button-letters span::after {
              opacity: 1;
              animation: letterHide 0.7s ease;
            }
    
            .copy-button-animated:hover .button-letters span:nth-child(1)::after { animation-delay: 0.03s; }
            .copy-button-animated:hover .button-letters span:nth-child(2)::after { animation-delay: 0.06s; }
            .copy-button-animated:hover .button-letters span:nth-child(3)::after { animation-delay: 0.09s; }
            .copy-button-animated:hover .button-letters span:nth-child(4)::after { animation-delay: 0.12s; }
            .copy-button-animated:hover .button-letters span:nth-child(5)::after { animation-delay: 0.15s; }
            .copy-button-animated:hover .button-letters span:nth-child(6)::after { animation-delay: 0.18s; }
            .copy-button-animated:hover .button-letters span:nth-child(7)::after { animation-delay: 0.21s; }
            .copy-button-animated:hover .button-letters span:nth-child(8)::after { animation-delay: 0.24s; }
    
            .icon-container {
              display: flex;
              align-items: center;
              justify-content: center;
              padding: 8px 10px;
              background-color: #ffffff;
              border-radius: 50%;
              box-shadow: inset 0 -2px 4px 0 #c6c6c6, 0 3px 6px rgba(0, 0, 0, 0.25);
              text-align: center;
              z-index: 10;
            }
    
            .icon-container svg {
              width: 25px;
              height: 30px;
              stroke: #592cd6;
              margin-top: -2px;
              z-index: 4;
              transform: rotate(180deg);
            }
    
            .icon-container svg path.bm {
              stroke-dasharray: 3;
              stroke-dashoffset: 3;
              stroke-width: 1px;
              transform: translateX(-23px) translateY(16px) scale(2) rotate(-44deg);
            }
    
            .copied .icon-container svg path.bm {
              animation: bump 1s ease forwards;
            }
    
            .copied .icon-container svg {
              animation: beat 1s ease-in-out forwards;
            }
          `}</style>
    
          <div className="flex items-center justify-center min-h-screen p-4" style={{
            background: 'url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48cGF0dGVybiBpZD0iZ3JpZCIgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiBwYXR0ZXJuVW5pdHM9InVzZXJTcGFjZU9uVXNlIj48cGF0aCBkPSJNIDQwIDAgTCAwIDAgMCA0MCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJyZ2JhKDIwMCwyMDAsMjAwLDAuMykiIHN0cm9rZS13aWR0aD0iMSIvPjwvcGF0dGVybj48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNncmlkKSIvPjwvc3ZnPg==), linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            backdropFilter: 'blur(10px)'
          }}>
            <div className="relative">
              <div className="absolute inset-0 bg-white/10 backdrop-blur-xl rounded-3xl" style={{ filter: 'blur(20px)' }}></div>
              
              <div className="relative bg-white/20 backdrop-blur-md rounded-3xl shadow-2xl p-8 max-w-2xl w-full border border-white/30">
                <div className="mb-6">
                  <h2 className="text-3xl font-bold text-white mb-2" style={{ textShadow: '0 2px 10px rgba(0,0,0,0.3)' }}>Share Your Link</h2>
                  <p className="text-white/80">Copy and share this link with others</p>
                </div>
    
                <div className="bg-white/30 backdrop-blur-sm border border-white/40 rounded-xl p-4 mb-6">
                  <a
                    href={link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-white font-medium hover:text-white/80 transition-colors block truncate"
                    style={{ textShadow: '0 1px 2px rgba(0,0,0,0.2)' }}
                  >
                    {link}
                  </a>
                </div>
    
                <div className="flex justify-center">
                  <button
                    className={`copy-button-animated ${copied ? 'copied' : ''}`}
                    onClick={handleCopy}
                  >
                    <div className="button-content">
                      <span className="button-letters">
                        <span data-label="C">C</span>
                        <span data-label="o">o</span>
                        <span data-label="p">p</span>
                        <span data-label="y">y</span>
                        <span data-label="L">L</span>
                        <span data-label="i">i</span>
                        <span data-label="n">n</span>
                        <span data-label="k">k</span>
                      </span>
                      <div className="icon-container">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="1.6" fill="none">
                          <path className="bm" d="M12.0017 6V4M8.14886 7.40371L6.86328 5.87162M15.864 7.40367L17.1496 5.87158" />
                          <path d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244" strokeLinejoin="round" strokeLinecap="round" className="link" />
                        </svg>
                      </div>
                    </div>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </>
      );
    }
