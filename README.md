    import React, { useState, useRef, useEffect } from 'react';
    import { Upload, Download, X, File, Loader2, Mail, Phone } from 'lucide-react';
    
    interface FileData {
      id: string;
      name: string;
      size: number;
      type: string;
      data: string;
      timestamp: number;
      receiverEmail: string;
      receiverPhone: string;
      communicationMethod: 'email' | 'sms';
    }
    
    const FileTransferApp: React.FC = () => {
      const [mode, setMode] = useState<'send' | 'receive'>('send');
      const [files, setFiles] = useState<File[]>([]);
      const [isDragging, setIsDragging] = useState(false);
      const [isLoading, setIsLoading] = useState(false);
      const [storedFiles, setStoredFiles] = useState<FileData[]>([]);
      const [notification, setNotification] = useState<string>('');
      const [showModal, setShowModal] = useState(false);
      const [receiverEmail, setReceiverEmail] = useState('');
      const [receiverPhone, setReceiverPhone] = useState('');
      const [communicationMethod, setCommunicationMethod] = useState<'email' | 'sms'>('email');
      const [errors, setErrors] = useState<{email?: string; phone?: string}>({});
      const fileInputRef = useRef<HTMLInputElement>(null);
    
      useEffect(() => {
        loadStoredFiles();
      }, []);
    
      const loadStoredFiles = () => {
        const stored: FileData[] = [];
        for (let i = 0; i < localStorage.length; i++) {
          const key = localStorage.key(i);
          if (key?.startsWith('file_')) {
            try {
              const fileData = JSON.parse(localStorage.getItem(key) || '');
              stored.push(fileData);
            } catch (e) {
              console.error('Error loading file:', e);
            }
          }
        }
        setStoredFiles(stored.sort((a, b) => b.timestamp - a.timestamp));
      };
    
      const showNotification = (message: string) => {
        setNotification(message);
        setTimeout(() => setNotification(''), 3000);
      };
    
      const validateEmail = (email: string): boolean => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
      };
    
      const validatePhone = (phone: string): boolean => {
        const phoneRegex = /^[0-9]{10}$/;
        return phoneRegex.test(phone.replace(/[-\s()]/g, ''));
      };
    
      const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
      };
    
      const handleDragLeave = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
      };
    
      const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
        const droppedFiles = Array.from(e.dataTransfer.files);
        setFiles(prev => [...prev, ...droppedFiles]);
      };
    
      const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files) {
          const selectedFiles = Array.from(e.target.files);
          setFiles(prev => [...prev, ...selectedFiles]);
        }
      };
    
      const removeFile = (index: number) => {
        setFiles(prev => prev.filter((_, i) => i !== index));
      };
    
      const formatFileSize = (bytes: number): string => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
      };
    
      const handleUploadClick = () => {
        if (files.length === 0) {
          showNotification('Please select files to upload');
          return;
        }
        setShowModal(true);
        setErrors({});
      };
    
      const validateForm = (): boolean => {
        const newErrors: {email?: string; phone?: string} = {};
    
        if (!receiverEmail.trim()) {
          newErrors.email = 'Email is required';
        } else if (!validateEmail(receiverEmail)) {
          newErrors.email = 'Please enter a valid email address';
        }
    
        if (!receiverPhone.trim()) {
          newErrors.phone = 'Phone number is required';
        } else if (!validatePhone(receiverPhone)) {
          newErrors.phone = 'Please enter a valid 10-digit phone number';
        }
    
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
      };
    
      const uploadFiles = async () => {
        if (!validateForm()) {
          return;
        }
    
        setShowModal(false);
        setIsLoading(true);
    
        for (const file of files) {
          try {
            const reader = new FileReader();
            await new Promise((resolve, reject) => {
              reader.onload = () => {
                const fileData: FileData = {
                  id: `file_${Date.now()}_${Math.random()}`,
                  name: file.name,
                  size: file.size,
                  type: file.type,
                  data: reader.result as string,
                  timestamp: Date.now(),
                  receiverEmail,
                  receiverPhone,
                  communicationMethod
                };
                localStorage.setItem(fileData.id, JSON.stringify(fileData));
                resolve(null);
              };
              reader.onerror = reject;
              reader.readAsDataURL(file);
            });
          } catch (error) {
            console.error('Error uploading file:', error);
            showNotification('Error uploading some files');
          }
        }
    
        setIsLoading(false);
        showNotification(`${files.length} file(s) uploaded successfully via ${communicationMethod}!`);
        setFiles([]);
        setReceiverEmail('');
        setReceiverPhone('');
        setCommunicationMethod('email');
        loadStoredFiles();
      };
    
      const downloadFile = (fileData: FileData) => {
        const link = document.createElement('a');
        link.href = fileData.data;
        link.download = fileData.name;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        showNotification(`Downloading ${fileData.name}`);
      };
    
      const deleteStoredFile = (id: string) => {
        localStorage.removeItem(id);
        loadStoredFiles();
        showNotification('File deleted');
      };
    
      return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
          <div className="max-w-4xl mx-auto">
            <div className="bg-white rounded-lg shadow-xl overflow-hidden">
              <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-6">
                <h1 className="text-3xl font-bold text-white text-center">File Transfer</h1>
              </div>
    
              {notification && (
                <div className="bg-green-500 text-white px-6 py-3 text-center font-medium">
                  {notification}
                </div>
              )}
    
              <div className="flex border-b">
                <button
                  onClick={() => setMode('send')}
                  className={`flex-1 py-4 font-semibold transition-colors ${
                    mode === 'send'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  <Upload className="inline mr-2" size={20} />
                  Send Files
                </button>
                <button
                  onClick={() => setMode('receive')}
                  className={`flex-1 py-4 font-semibold transition-colors ${
                    mode === 'receive'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  <Download className="inline mr-2" size={20} />
                  Receive Files
                </button>
              </div>
    
              <div className="p-6">
                {isLoading && (
                  <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="bg-white rounded-lg p-8 flex flex-col items-center">
                      <Loader2 className="animate-spin text-blue-600 mb-4" size={48} />
                      <p className="text-xl font-semibold">Please wait...</p>
                      <p className="text-gray-600 mt-2">Processing your files</p>
                    </div>
                  </div>
                )}
    
                {showModal && (
                  <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
                    <div className="bg-white rounded-lg p-6 max-w-md w-full">
                      <h2 className="text-2xl font-bold mb-4">Receiver Details</h2>
                      
                      <div className="mb-4">
                        <label className="block text-sm font-semibold mb-2">
                          Receiver Email <span className="text-red-500">*</span>
                        </label>
                        <div className="relative">
                          <Mail className="absolute left-3 top-3 text-gray-400" size={20} />
                          <input
                            type="email"
                            value={receiverEmail}
                            onChange={(e) => setReceiverEmail(e.target.value)}
                            className={`w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                              errors.email ? 'border-red-500' : 'border-gray-300'
                            }`}
                            placeholder="example@email.com"
                          />
                        </div>
                        {errors.email && (
                          <p className="text-red-500 text-sm mt-1">{errors.email}</p>
                        )}
                      </div>
    
                      <div className="mb-4">
                        <label className="block text-sm font-semibold mb-2">
                          Receiver Phone <span className="text-red-500">*</span>
                        </label>
                        <div className="relative">
                          <Phone className="absolute left-3 top-3 text-gray-400" size={20} />
                          <input
                            type="tel"
                            value={receiverPhone}
                            onChange={(e) => setReceiverPhone(e.target.value)}
                            className={`w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 ${
                              errors.phone ? 'border-red-500' : 'border-gray-300'
                            }`}
                            placeholder="1234567890"
                          />
                        </div>
                        {errors.phone && (
                          <p className="text-red-500 text-sm mt-1">{errors.phone}</p>
                        )}
                      </div>
    
                      <div className="mb-6">
                        <label className="block text-sm font-semibold mb-3">
                          Communication Method <span className="text-red-500">*</span>
                        </label>
                        <div className="space-y-2">
                          <label className="flex items-center cursor-pointer">
                            <input
                              type="radio"
                              name="communicationMethod"
                              value="email"
                              checked={communicationMethod === 'email'}
                              onChange={(e) => setCommunicationMethod('email')}
                              className="w-4 h-4 text-blue-600 focus:ring-blue-500"
                            />
                            <Mail className="ml-3 mr-2 text-blue-600" size={18} />
                            <span className="text-gray-700">Email</span>
                          </label>
                          <label className="flex items-center cursor-pointer">
                            <input
                              type="radio"
                              name="communicationMethod"
                              value="sms"
                              checked={communicationMethod === 'sms'}
                              onChange={(e) => setCommunicationMethod('sms')}
                              className="w-4 h-4 text-blue-600 focus:ring-blue-500"
                            />
                            <Phone className="ml-3 mr-2 text-blue-600" size={18} />
                            <span className="text-gray-700">Phone SMS</span>
                          </label>
                        </div>
                      </div>
    
                      <div className="flex gap-3">
                        <button
                          onClick={() => setShowModal(false)}
                          className="flex-1 bg-gray-300 text-gray-700 py-2 rounded-lg font-semibold hover:bg-gray-400 transition-colors"
                        >
                          Cancel
                        </button>
                        <button
                          onClick={uploadFiles}
                          className="flex-1 bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                        >
                          Submit
                        </button>
                      </div>
                    </div>
                  </div>
                )}
    
                {mode === 'send' ? (
                  <div>
                    <div
                      onDragOver={handleDragOver}
                      onDragLeave={handleDragLeave}
                      onDrop={handleDrop}
                      className={`border-2 border-dashed rounded-lg p-12 text-center transition-colors cursor-pointer ${
                        isDragging
                          ? 'border-blue-600 bg-blue-50'
                          : 'border-gray-300 hover:border-blue-400'
                      }`}
                      onClick={() => fileInputRef.current?.click()}
                    >
                      <Upload className="mx-auto mb-4 text-gray-400" size={48} />
                      <p className="text-lg font-semibold text-gray-700 mb-2">
                        Drag & drop files here
                      </p>
                      <p className="text-gray-500 mb-4">or click to browse</p>
                      <input
                        ref={fileInputRef}
                        type="file"
                        multiple
                        onChange={handleFileSelect}
                        className="hidden"
                      />
                    </div>
    
                    {files.length > 0 && (
                      <div className="mt-6">
                        <h3 className="font-semibold text-lg mb-3">Selected Files ({files.length})</h3>
                        <div className="space-y-2 max-h-64 overflow-y-auto">
                          {files.map((file, index) => (
                            <div
                              key={index}
                              className="flex items-center justify-between bg-gray-50 p-3 rounded-lg"
                            >
                              <div className="flex items-center flex-1 min-w-0">
                                <File className="text-blue-600 mr-3 flex-shrink-0" size={24} />
                                <div className="min-w-0 flex-1">
                                  <p className="font-medium truncate">{file.name}</p>
                                  <p className="text-sm text-gray-500">{formatFileSize(file.size)}</p>
                                </div>
                              </div>
                              <button
                                onClick={() => removeFile(index)}
                                className="ml-3 text-red-500 hover:text-red-700 flex-shrink-0"
                              >
                                <X size={20} />
                              </button>
                            </div>
                          ))}
                        </div>
    
                        <button
                          onClick={handleUploadClick}
                          className="w-full mt-6 bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
                        >
                          Upload Files
                        </button>
                      </div>
                    )}
                  </div>
                ) : (
                  <div>
                    <h3 className="font-semibold text-lg mb-4">Stored Files ({storedFiles.length})</h3>
                    {storedFiles.length === 0 ? (
                      <div className="text-center py-12 text-gray-500">
                        <Download size={48} className="mx-auto mb-4 opacity-50" />
                        <p>No files available</p>
                      </div>
                    ) : (
                      <div className="space-y-2 max-h-96 overflow-y-auto">
                        {storedFiles.map((file) => (
                          <div
                            key={file.id}
                            className="bg-gray-50 p-4 rounded-lg hover:bg-gray-100 transition-colors"
                          >
                            <div className="flex items-center justify-between mb-2">
                              <div className="flex items-center flex-1 min-w-0">
                                <File className="text-blue-600 mr-3 flex-shrink-0" size={24} />
                                <div className="min-w-0 flex-1">
                                  <p className="font-medium truncate">{file.name}</p>
                                  <p className="text-sm text-gray-500">
                                    {formatFileSize(file.size)} • {new Date(file.timestamp).toLocaleString()}
                                  </p>
                                </div>
                              </div>
                              <div className="flex gap-2 ml-3">
                                <button
                                  onClick={() => downloadFile(file)}
                                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex-shrink-0"
                                >
                                  <Download size={18} />
                                </button>
                                <button
                                  onClick={() => deleteStoredFile(file.id)}
                                  className="bg-red-500 text-white px-4 py-2 rounded-lg hover:bg-red-600 transition-colors flex-shrink-0"
                                >
                                  <X size={18} />
                                </button>
                              </div>
                            </div>
                            <div className="flex gap-4 text-sm text-gray-600 mt-2 pt-2 border-t border-gray-200">
                              <span className="flex items-center">
                                <Mail size={14} className="mr-1" />
                                {file.receiverEmail}
                              </span>
                              <span className="flex items-center">
                                <Phone size={14} className="mr-1" />
                                {file.receiverPhone}
                              </span>
                              <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs font-semibold">
                                {file.communicationMethod.toUpperCase()}
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      );
    };
    
    export default FileTransferApp;
