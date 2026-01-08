    
    
    import { useState } from 'react';
    import { Copy, Check, ExternalLink, Link2 } from 'lucide-react';
    
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
        <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 p-4">
          <div className="bg-white rounded-2xl shadow-xl p-8 max-w-2xl w-full border border-gray-100">
            <div className="flex items-center gap-3 mb-6">
              <div className="bg-gradient-to-br from-blue-500 to-indigo-600 p-3 rounded-xl">
                <Link2 className="text-white" size={24} />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-800">Share Link</h2>
                <p className="text-sm text-gray-500">Copy and share this link with others</p>
              </div>
            </div>
            
            <div className="space-y-3">
              <div className="relative group">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-indigo-500 rounded-xl blur opacity-20 group-hover:opacity-30 transition-opacity"></div>
                <div className="relative flex items-center gap-3 bg-gray-50 border-2 border-gray-200 rounded-xl p-4 hover:border-blue-300 transition-all">
                  <div className="flex-1 overflow-hidden">
                    <a
                      href={link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:text-blue-700 font-medium flex items-center gap-2 group"
                    >
                      <span className="truncate">{link}</span>
                      <ExternalLink size={16} className="flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </a>
                  </div>
                  
                  <button
                    onClick={handleCopy}
                    className={`flex items-center gap-2 px-4 py-2.5 rounded-lg font-medium transition-all transform active:scale-95 flex-shrink-0 ${
                      copied
                        ? 'bg-green-500 text-white'
                        : 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white hover:from-blue-700 hover:to-indigo-700 shadow-md hover:shadow-lg'
                    }`}
                  >
                    {copied ? (
                      <>
                        <Check size={18} />
                        <span>Copied!</span>
                      </>
                    ) : (
                      <>
                        <Copy size={18} />
                        <span>Copy</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
    
              <div className="flex items-center justify-between text-xs text-gray-500 px-2">
                <span>Click the link to open in new tab</span>
                <span className="flex items-center gap-1">
                  {copied && (
                    <span className="text-green-600 font-medium animate-pulse">
                      ✓ Link copied to clipboard
                    </span>
                  )}
                </span>
              </div>
            </div>
          </div>
        </div>
      );
    }
