# File Transfer App - Folder Structure

## Project Structure
```
src/
├── app/
│   └── App.tsx
├── components/
│   ├── FileUploadZone.tsx
│   ├── FileList.tsx
│   ├── ReceiverModal.tsx
│   ├── StoredFilesList.tsx
│   ├── LoadingOverlay.tsx
│   ├── Notification.tsx
│   └── NotificationPanel.tsx
├── hooks/
│   ├── useFileStorage.ts
│   └── useNotification.ts
├── services/
│   ├── fileStorage.service.ts
│   └── api.service.ts
├── types/
│   └── index.ts
├── utils/
│   ├── validation.ts
│   └── formatters.ts
├── styles/
│   └── index.css
└── main.tsx
```

---

## File: `src/types/index.ts`

```typescript
export interface FileData {
  id: string;
  name: string;
  size: number;
  type: string;
  data: string;
  timestamp: number;
  receiverEmail: string;
  receiverPhone: string;
  communicationMethod: 'email' | 'sms';
  isNew?: boolean;
  uploadedBy?: string;
  fileUrl?: string;
}

export interface ReceiverDetails {
  email: string;
  phone: string;
  communicationMethod: 'email' | 'sms';
}

export interface ValidationErrors {
  email?: string;
  phone?: string;
}

export interface UploadResponse {
  success: boolean;
  message: string;
  files: Array<{
    id: string;
    name: string;
    size: number;
    url: string;
  }>;
}
```

---

## File: `src/utils/validation.ts`

```typescript
export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validatePhone = (phone: string): boolean => {
  const phoneRegex = /^[0-9]{10}$/;
  return phoneRegex.test(phone.replace(/[-\s()]/g, ''));
};

export const validateReceiverDetails = (
  email: string,
  phone: string
): { isValid: boolean; errors: { email?: string; phone?: string } } => {
  const errors: { email?: string; phone?: string } = {};

  if (!email.trim()) {
    errors.email = 'Email is required';
  } else if (!validateEmail(email)) {
    errors.email = 'Please enter a valid email address';
  }

  if (!phone.trim()) {
    errors.phone = 'Phone number is required';
  } else if (!validatePhone(phone)) {
    errors.phone = 'Please enter a valid 10-digit phone number';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};
```

---

## File: `src/utils/formatters.ts`

```typescript
export const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
};

export const formatDate = (timestamp: number): string => {
  return new Date(timestamp).toLocaleString();
};
```

---

## File: `src/services/api.service.ts`

```typescript
import { ReceiverDetails, UploadResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000/api';

export const apiService = {
  uploadFiles: async (
    files: File[],
    receiverDetails: ReceiverDetails
  ): Promise<UploadResponse> => {
    try {
      const formData = new FormData();

      // Append all files
      files.forEach((file) => {
        formData.append('files', file);
      });

      // Append receiver details
      formData.append('receiverEmail', receiverDetails.email);
      formData.append('receiverPhone', receiverDetails.phone);
      formData.append('communicationMethod', receiverDetails.communicationMethod);
      formData.append('timestamp', Date.now().toString());

      const response = await fetch(`${API_BASE_URL}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const data: UploadResponse = await response.json();
      return data;
    } catch (error) {
      console.error('Upload error:', error);
      throw error;
    }
  },

  getFiles: async (): Promise<any[]> => {
    try {
      const response = await fetch(`${API_BASE_URL}/files`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch files: ${response.statusText}`);
      }

      const data = await response.json();
      return data.files || [];
    } catch (error) {
      console.error('Fetch files error:', error);
      throw error;
    }
  },

  downloadFile: async (fileId: string): Promise<Blob> => {
    try {
      const response = await fetch(`${API_BASE_URL}/download/${fileId}`, {
        method: 'GET',
      });

      if (!response.ok) {
        throw new Error(`Download failed: ${response.statusText}`);
      }

      return await response.blob();
    } catch (error) {
      console.error('Download error:', error);
      throw error;
    }
  },

  deleteFile: async (fileId: string): Promise<void> => {
    try {
      const response = await fetch(`${API_BASE_URL}/files/${fileId}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error(`Delete failed: ${response.statusText}`);
      }
    } catch (error) {
      console.error('Delete error:', error);
      throw error;
    }
  },
};
```

---

## File: `src/services/fileStorage.service.ts`

```typescript
import { FileData } from '../types';

export const fileStorageService = {
  saveFile: (fileData: FileData): void => {
    const dataToSave = { ...fileData, isNew: true };
    localStorage.setItem(fileData.id, JSON.stringify(dataToSave));
  },

  getFile: (id: string): FileData | null => {
    const data = localStorage.getItem(id);
    return data ? JSON.parse(data) : null;
  },

  getAllFiles: (): FileData[] => {
    const files: FileData[] = [];
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key?.startsWith('file_')) {
        try {
          const fileData = JSON.parse(localStorage.getItem(key) || '');
          files.push(fileData);
        } catch (e) {
          console.error('Error loading file:', e);
        }
      }
    }
    return files.sort((a, b) => b.timestamp - a.timestamp);
  },

  getNewFiles: (): FileData[] => {
    return fileStorageService.getAllFiles().filter(file => file.isNew);
  },

  markFileAsRead: (id: string): void => {
    const file = fileStorageService.getFile(id);
    if (file) {
      file.isNew = false;
      localStorage.setItem(id, JSON.stringify(file));
    }
  },

  markAllFilesAsRead: (): void => {
    const files = fileStorageService.getAllFiles();
    files.forEach(file => {
      if (file.isNew) {
        file.isNew = false;
        localStorage.setItem(file.id, JSON.stringify(file));
      }
    });
  },

  deleteFile: (id: string): void => {
    localStorage.removeItem(id);
  },

  readFileAsBase64: (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result as string);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }
};
```

---

## File: `src/hooks/useNotification.ts`

```typescript
import { useState, useCallback } from 'react';

export const useNotification = () => {
  const [notification, setNotification] = useState<string>('');

  const showNotification = useCallback((message: string) => {
    setNotification(message);
    setTimeout(() => setNotification(''), 3000);
  }, []);

  return { notification, showNotification };
};
```

---

## File: `src/hooks/useFileStorage.ts`

```typescript
import { useState, useEffect, useCallback } from 'react';
import { FileData, ReceiverDetails } from '../types';
import { fileStorageService } from '../services/fileStorage.service';
import { apiService } from '../services/api.service';

export const useFileStorage = () => {
  const [storedFiles, setStoredFiles] = useState<FileData[]>([]);
  const [newFilesCount, setNewFilesCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  const loadFiles = useCallback(() => {
    const files = fileStorageService.getAllFiles();
    setStoredFiles(files);
    setNewFilesCount(files.filter(f => f.isNew).length);
  }, []);

  useEffect(() => {
    loadFiles();
  }, [loadFiles]);

  const uploadFiles = async (
    files: File[],
    receiverDetails: ReceiverDetails
  ): Promise<void> => {
    setIsLoading(true);
    setUploadProgress(0);

    try {
      // Call backend API
      const response = await apiService.uploadFiles(files, receiverDetails);

      if (response.success) {
        // Save to localStorage with backend response data
        response.files.forEach((uploadedFile) => {
          const fileData: FileData = {
            id: uploadedFile.id,
            name: uploadedFile.name,
            size: uploadedFile.size,
            type: files.find(f => f.name === uploadedFile.name)?.type || '',
            data: uploadedFile.url,
            timestamp: Date.now(),
            receiverEmail: receiverDetails.email,
            receiverPhone: receiverDetails.phone,
            communicationMethod: receiverDetails.communicationMethod,
            isNew: true,
            fileUrl: uploadedFile.url
          };
          fileStorageService.saveFile(fileData);
        });

        setUploadProgress(100);
        loadFiles();
      } else {
        throw new Error(response.message || 'Upload failed');
      }
    } catch (error) {
      console.error('Upload failed:', error);
      throw error;
    } finally {
      setIsLoading(false);
      setUploadProgress(0);
    }
  };

  const deleteFile = useCallback(async (id: string) => {
    try {
      setIsLoading(true);
      // Delete from backend
      await apiService.deleteFile(id);
      // Delete from localStorage
      fileStorageService.deleteFile(id);
      loadFiles();
    } catch (error) {
      console.error('Delete failed:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, [loadFiles]);

  const downloadFile = useCallback(async (fileData: FileData) => {
    try {
      if (fileData.fileUrl) {
        // Download from backend URL
        const blob = await apiService.downloadFile(fileData.id);
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = fileData.name;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
      } else {
        // Fallback to base64 data
        const link = document.createElement('a');
        link.href = fileData.data;
        link.download = fileData.name;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }
    } catch (error) {
      console.error('Download failed:', error);
      throw error;
    }
  }, []);

  const markAsRead = useCallback((id: string) => {
    fileStorageService.markFileAsRead(id);
    loadFiles();
  }, [loadFiles]);

  const markAllAsRead = useCallback(() => {
    fileStorageService.markAllFilesAsRead();
    loadFiles();
  }, [loadFiles]);

  const syncWithBackend = useCallback(async () => {
    try {
      setIsLoading(true);
      const backendFiles = await apiService.getFiles();
      
      // Merge backend files with local storage
      backendFiles.forEach((file: any) => {
        const existingFile = fileStorageService.getFile(file.id);
        if (!existingFile) {
          const fileData: FileData = {
            id: file.id,
            name: file.name,
            size: file.size,
            type: file.type || '',
            data: file.url,
            timestamp: file.timestamp,
            receiverEmail: file.receiverEmail,
            receiverPhone: file.receiverPhone,
            communicationMethod: file.communicationMethod,
            isNew: true,
            fileUrl: file.url
          };
          fileStorageService.saveFile(fileData);
        }
      });
      
      loadFiles();
    } catch (error) {
      console.error('Sync failed:', error);
    } finally {
      setIsLoading(false);
    }
  }, [loadFiles]);

  return {
    storedFiles,
    newFilesCount,
    isLoading,
    uploadProgress,
    uploadFiles,
    deleteFile,
    downloadFile,
    markAsRead,
    markAllAsRead,
    syncWithBackend
  };
};
```

---

## File: `src/components/NotificationPanel.tsx`

```typescript
import React from 'react';
import { X, Download, Mail, Phone, FileIcon, ExternalLink } from 'lucide-react';
import { FileData } from '../types';
import { formatFileSize, formatDate } from '../utils/formatters';

interface NotificationPanelProps {
  isOpen: boolean;
  newFiles: FileData[];
  onClose: () => void;
  onDownload: (file: FileData) => void;
  onMarkAsRead: (id: string) => void;
  onMarkAllAsRead: () => void;
}

export const NotificationPanel: React.FC<NotificationPanelProps> = ({
  isOpen,
  newFiles,
  onClose,
  onDownload,
  onMarkAsRead,
  onMarkAllAsRead
}) => {
  if (!isOpen) return null;

  const handleDownload = (file: FileData) => {
    onDownload(file);
    onMarkAsRead(file.id);
  };

  return (
    <>
      <div 
        className="fixed inset-0 bg-black bg-opacity-30 z-40"
        onClick={onClose}
      />
      <div className="fixed right-0 top-0 h-full w-full max-w-md bg-white shadow-2xl z-50 flex flex-col">
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-4 flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-white">Notifications</h2>
            <p className="text-blue-100 text-sm">{newFiles.length} new file{newFiles.length !== 1 ? 's' : ''}</p>
          </div>
          <button
            onClick={onClose}
            className="text-white hover:bg-white hover:bg-opacity-20 p-2 rounded-lg transition-colors"
          >
            <X size={24} />
          </button>
        </div>

        {newFiles.length > 0 && (
          <div className="p-4 border-b bg-gray-50">
            <button
              onClick={onMarkAllAsRead}
              className="text-blue-600 hover:text-blue-800 font-semibold text-sm"
            >
              Mark all as read
            </button>
          </div>
        )}

        <div className="flex-1 overflow-y-auto p-4">
          {newFiles.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <FileIcon size={48} className="mx-auto mb-4 opacity-50" />
              <p>No new notifications</p>
            </div>
          ) : (
            <div className="space-y-3">
              {newFiles.map((file) => (
                <div
                  key={file.id}
                  className="bg-blue-50 border border-blue-200 rounded-lg p-4 hover:bg-blue-100 transition-colors"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-start flex-1 min-w-0">
                      <FileIcon className="text-blue-600 mr-3 flex-shrink-0 mt-1" size={20} />
                      <div className="min-w-0 flex-1">
                        <p className="font-semibold text-gray-900 truncate">{file.name}</p>
                        <p className="text-sm text-gray-600 mt-1">
                          {formatFileSize(file.size)}
                        </p>
                        <p className="text-xs text-gray-500 mt-1">
                          {formatDate(file.timestamp)}
                        </p>
                      </div>
                    </div>
                    <span className="ml-2 w-2 h-2 bg-blue-600 rounded-full flex-shrink-0 mt-2"></span>
                  </div>

                  <div className="mt-3 pt-3 border-t border-blue-200">
                    <div className="space-y-1 mb-3">
                      <div className="flex items-center text-sm text-gray-700">
                        <Mail size={14} className="mr-2 text-blue-600" />
                        <span className="truncate">{file.receiverEmail}</span>
                      </div>
                      <div className="flex items-center text-sm text-gray-700">
                        <Phone size={14} className="mr-2 text-blue-600" />
                        <span>{file.receiverPhone}</span>
                      </div>
                      <div className="flex items-center text-sm">
                        <span className="px-2 py-1 bg-blue-600 text-white rounded text-xs font-semibold">
                          {file.communicationMethod.toUpperCase()}
                        </span>
                      </div>
                    </div>

                    <div className="flex gap-2">
                      <button
                        onClick={() => handleDownload(file)}
                        className="flex-1 bg-blue-600 text-white px-3 py-2 rounded-lg hover:bg-blue-700 transition-colors text-sm font-semibold flex items-center justify-center"
                      >
                        <Download size={16} className="mr-2" />
                        Download
                      </button>
                      <button
                        onClick={() => onMarkAsRead(file.id)}
                        className="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-100 transition-colors text-sm"
                      >
                        <X size={16} />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
};
```

---

## File: `src/components/Notification.tsx`

```typescript
import React from 'react';

interface NotificationProps {
  message: string;
}

export const Notification: React.FC<NotificationProps> = ({ message }) => {
  if (!message) return null;

  return (
    <div className="bg-green-500 text-white px-6 py-3 text-center font-medium">
      {message}
    </div>
  );
};
```

---

## File: `src/components/LoadingOverlay.tsx`

```typescript
import React from 'react';
import { Loader2 } from 'lucide-react';

interface LoadingOverlayProps {
  isLoading: boolean;
}

export const LoadingOverlay: React.FC<LoadingOverlayProps> = ({ isLoading }) => {
  if (!isLoading) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-8 flex flex-col items-center">
        <Loader2 className="animate-spin text-blue-600 mb-4" size={48} />
        <p className="text-xl font-semibold">Please wait...</p>
        <p className="text-gray-600 mt-2">Processing your files</p>
      </div>
    </div>
  );
};
```

---

## File: `src/components/FileUploadZone.tsx`

```typescript
import React, { useRef, useState } from 'react';
import { Upload } from 'lucide-react';

interface FileUploadZoneProps {
  onFilesSelected: (files: File[]) => void;
}

export const FileUploadZone: React.FC<FileUploadZoneProps> = ({ onFilesSelected }) => {
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

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
    onFilesSelected(droppedFiles);
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const selectedFiles = Array.from(e.target.files);
      onFilesSelected(selectedFiles);
    }
  };

  return (
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
  );
};
```

---

## File: `src/components/FileList.tsx`

```typescript
import React from 'react';
import { File, X } from 'lucide-react';
import { formatFileSize } from '../utils/formatters';

interface FileListProps {
  files: File[];
  onRemove: (index: number) => void;
  onUpload: () => void;
}

export const FileList: React.FC<FileListProps> = ({ files, onRemove, onUpload }) => {
  if (files.length === 0) return null;

  return (
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
              onClick={() => onRemove(index)}
              className="ml-3 text-red-500 hover:text-red-700 flex-shrink-0"
            >
              <X size={20} />
            </button>
          </div>
        ))}
      </div>

      <button
        onClick={onUpload}
        className="w-full mt-6 bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
      >
        Upload Files
      </button>
    </div>
  );
};
```

---

## File: `src/components/ReceiverModal.tsx`

```typescript
import React, { useState } from 'react';
import { Mail, Phone } from 'lucide-react';
import { ReceiverDetails, ValidationErrors } from '../types';
import { validateReceiverDetails } from '../utils/validation';

interface ReceiverModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (details: ReceiverDetails) => void;
}

export const ReceiverModal: React.FC<ReceiverModalProps> = ({
  isOpen,
  onClose,
  onSubmit
}) => {
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [communicationMethod, setCommunicationMethod] = useState<'email' | 'sms'>('email');
  const [errors, setErrors] = useState<ValidationErrors>({});

  if (!isOpen) return null;

  const handleSubmit = () => {
    const validation = validateReceiverDetails(email, phone);
    
    if (!validation.isValid) {
      setErrors(validation.errors);
      return;
    }

    onSubmit({ email, phone, communicationMethod });
    setEmail('');
    setPhone('');
    setCommunicationMethod('email');
    setErrors({});
  };

  return (
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
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
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
                onChange={() => setCommunicationMethod('email')}
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
                onChange={() => setCommunicationMethod('sms')}
                className="w-4 h-4 text-blue-600 focus:ring-blue-500"
              />
              <Phone className="ml-3 mr-2 text-blue-600" size={18} />
              <span className="text-gray-700">Phone SMS</span>
            </label>
          </div>
        </div>

        <div className="flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 bg-gray-300 text-gray-700 py-2 rounded-lg font-semibold hover:bg-gray-400 transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleSubmit}
            className="flex-1 bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            Submit
          </button>
        </div>
      </div>
    </div>
  );
};
```

---

## File: `src/components/StoredFilesList.tsx`

```typescript
import React from 'react';
import { File, Download, X, Mail, Phone } from 'lucide-react';
import { FileData } from '../types';
import { formatFileSize, formatDate } from '../utils/formatters';

interface StoredFilesListProps {
  files: FileData[];
  onDownload: (file: FileData) => void;
  onDelete: (id: string) => void;
}

export const StoredFilesList: React.FC<StoredFilesListProps> = ({
  files,
  onDownload,
  onDelete
}) => {
  if (files.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <Download size={48} className="mx-auto mb-4 opacity-50" />
        <p>No files available</p>
      </div>
    );
  }

  return (
    <div className="space-y-2 max-h-96 overflow-y-auto">
      {files.map((file) => (
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
                  {formatFileSize(file.size)} • {formatDate(file.timestamp)}
                </p>
              </div>
            </div>
            <div className="flex gap-2 ml-3">
              <button
                onClick={() => onDownload(file)}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors flex-shrink-0"
              >
                <Download size={18} />
              </button>
              <button
                onClick={() => onDelete(file.id)}
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
  );
};
```

---

## File: `src/app/App.tsx`

```typescript
import React, { useState, useEffect } from 'react';
import { Upload, Download, Bell, RefreshCw } from 'lucide-react';
import { FileUploadZone } from '../components/FileUploadZone';
import { FileList } from '../components/FileList';
import { ReceiverModal } from '../components/ReceiverModal';
import { StoredFilesList } from '../components/StoredFilesList';
import { LoadingOverlay } from '../components/LoadingOverlay';
import { Notification } from '../components/Notification';
import { NotificationPanel } from '../components/NotificationPanel';
import { useFileStorage } from '../hooks/useFileStorage';
import { useNotification } from '../hooks/useNotification';
import { ReceiverDetails } from '../types';

const App: React.FC = () => {
  const [mode, setMode] = useState<'send' | 'receive'>('send');
  const [files, setFiles] = useState<File[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [showNotificationPanel, setShowNotificationPanel] = useState(false);

  const { 
    storedFiles, 
    newFilesCount, 
    isLoading, 
    uploadFiles, 
    deleteFile, 
    downloadFile,
    markAsRead,
    markAllAsRead,
    syncWithBackend
  } = useFileStorage();
  const { notification, showNotification } = useNotification();

  const newFiles = storedFiles.filter(file => file.isNew);

  // Sync with backend on mount
  useEffect(() => {
    syncWithBackend();
  }, [syncWithBackend]);

  const handleFilesSelected = (newFiles: File[]) => {
    setFiles(prev => [...prev, ...newFiles]);
  };

  const handleRemoveFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleUploadClick = () => {
    if (files.length === 0) {
      showNotification('Please select files to upload');
      return;
    }
    setShowModal(true);
  };

  const handleSubmitReceiverDetails = async (details: ReceiverDetails) => {
    setShowModal(false);
    
    try {
      await uploadFiles(files, details);
      showNotification(`${files.length} file(s) uploaded successfully via ${details.communicationMethod}!`);
      setFiles([]);
    } catch (error) {
      showNotification('Upload failed. Please try again.');
      console.error('Upload error:', error);
    }
  };

  const handleDownload = async (file: any) => {
    try {
      await downloadFile(file);
      showNotification(`Downloading ${file.name}`);
    } catch (error) {
      showNotification('Download failed. Please try again.');
      console.error('Download error:', error);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteFile(id);
      showNotification('File deleted');
    } catch (error) {
      showNotification('Delete failed. Please try again.');
      console.error('Delete error:', error);
    }
  };

  const handleNotificationDownload = async (file: any) => {
    try {
      await downloadFile(file);
      showNotification(`Downloading ${file.name}`);
    } catch (error) {
      showNotification('Download failed. Please try again.');
      console.error('Download error:', error);
    }
  };

  const handleRefresh = async () => {
    try {
      await syncWithBackend();
      showNotification('Files synced successfully');
    } catch (error) {
      showNotification('Sync failed. Please try again.');
      console.error('Sync error:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-xl overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 p-6 relative">
            <h1 className="text-3xl font-bold text-white text-center">File Transfer</h1>
            
            <div className="absolute right-6 top-1/2 -translate-y-1/2 flex gap-2">
              <button
                onClick={handleRefresh}
                className="text-white hover:bg-white hover:bg-opacity-20 p-2 rounded-lg transition-colors"
                title="Sync with server"
              >
                <RefreshCw size={24} />
              </button>
              
              <button
                onClick={() => setShowNotificationPanel(true)}
                className="text-white hover:bg-white hover:bg-opacity-20 p-2 rounded-lg transition-colors relative"
              >
                <Bell size={24} />
                {newFilesCount > 0 && (
                  <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">
                    {newFilesCount > 9 ? '9+' : newFilesCount}
                  </span>
                )}
              </button>
            </div>
          </div>

          <Notification message={notification} />

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
            <LoadingOverlay isLoading={isLoading} />

            <ReceiverModal
              isOpen={showModal}
              onClose={() => setShowModal(false)}
              onSubmit={handleSubmitReceiverDetails}
            />

            <NotificationPanel
              isOpen={showNotificationPanel}
              newFiles={newFiles}
              onClose={() => setShowNotificationPanel(false)}
              onDownload={handleNotificationDownload}
              onMarkAsRead={markAsRead}
              onMarkAllAsRead={markAllAsRead}
            />

            {mode === 'send' ? (
              <div>
                <FileUploadZone onFilesSelected={handleFilesSelected} />
                <FileList
                  files={files}
                  onRemove={handleRemoveFile}
                  onUpload={handleUploadClick}
                />
              </div>
            ) : (
              <div>
                <h3 className="font-semibold text-lg mb-4">
                  Stored Files ({storedFiles.length})
                </h3>
                <StoredFilesList
                  files={storedFiles}
                  onDownload={handleDownload}
                  onDelete={handleDelete}
                />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
```

---

## File: `src/main.tsx`

```typescript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './app/App';
import './styles/index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

---

## File: `src/styles/index.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}
```

---

## Additional Configuration Files

### `vite.config.ts`

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': '/src'
    }
  }
});
```

### `tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

### `package.json`

```json
{
  "name": "file-transfer-app",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "lucide-react": "^0.263.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.2.2",
    "vite": "^5.0.8"
  }
}
```

---

## Installation & Running

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

This structure follows React best practices with clear separation of concerns, making the codebase maintainable and scalable!

---

# Backend Server Implementation

## Backend Structure
```
backend/
├── src/
│   ├── controllers/
│   │   └── fileController.ts
│   ├── routes/
│   │   └── fileRoutes.ts
│   ├── middleware/
│   │   └── upload.ts
│   ├── config/
│   │   └── db.ts
│   └── server.ts
├── uploads/
├── package.json
└── tsconfig.json
```

---

## File: `backend/src/server.ts`

```typescript
import express from 'express';
import cors from 'cors';
import path from 'path';
import fileRoutes from './routes/fileRoutes';

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve uploaded files statically
app.use('/uploads', express.static(path.join(__dirname, '../uploads')));

// Routes
app.use('/api', fileRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', message: 'Server is running' });
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

export default app;
```

---

## File: `backend/src/middleware/upload.ts`

```typescript
import multer from 'multer';
import path from 'path';
import fs from 'fs';

// Ensure uploads directory exists
const uploadsDir = path.join(__dirname, '../../uploads');
if (!fs.existsSync(uploadsDir)) {
  fs.mkdirSync(uploadsDir, { recursive: true });
}

// Configure storage
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, uploadsDir);
  },
  filename: (req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
    cb(null, uniqueSuffix + '-' + file.originalname);
  }
});

// File filter
const fileFilter = (req: any, file: Express.Multer.File, cb: any) => {
  // Accept all files for now, add restrictions as needed
  cb(null, true);
};

// Configure multer
export const upload = multer({
  storage: storage,
  fileFilter: fileFilter,
  limits: {
    fileSize: 50 * 1024 * 1024, // 50MB limit
  }
});
```

---

## File: `backend/src/controllers/fileController.ts`

```typescript
import { Request, Response } from 'express';
import path from 'path';
import fs from 'fs';

// In-memory database (replace with real database in production)
interface FileRecord {
  id: string;
  name: string;
  originalName: string;
  size: number;
  type: string;
  url: string;
  timestamp: number;
  receiverEmail: string;
  receiverPhone: string;
  communicationMethod: string;
}

const filesDB: FileRecord[] = [];

export const uploadFiles = async (req: Request, res: Response) => {
  try {
    const files = req.files as Express.Multer.File[];
    const { receiverEmail, receiverPhone, communicationMethod, timestamp } = req.body;

    if (!files || files.length === 0) {
      return res.status(400).json({
        success: false,
        message: 'No files uploaded'
      });
    }

    if (!receiverEmail || !receiverPhone || !communicationMethod) {
      return res.status(400).json({
        success: false,
        message: 'Missing required fields'
      });
    }

    const uploadedFiles = files.map(file => {
      const fileRecord: FileRecord = {
        id: `file_${Date.now()}_${Math.random()}`,
        name: file.filename,
        originalName: file.originalname,
        size: file.size,
        type: file.mimetype,
        url: `${req.protocol}://${req.get('host')}/uploads/${file.filename}`,
        timestamp: parseInt(timestamp) || Date.now(),
        receiverEmail,
        receiverPhone,
        communicationMethod
      };

      filesDB.push(fileRecord);
      return fileRecord;
    });

    // Here you would typically:
    // 1. Save file metadata to database
    // 2. Send notification email/SMS to receiver
    // 3. Generate download links

    console.log(`Files uploaded for ${receiverEmail} via ${communicationMethod}`);

    res.status(200).json({
      success: true,
      message: `${files.length} file(s) uploaded successfully`,
      files: uploadedFiles.map(f => ({
        id: f.id,
        name: f.originalName,
        size: f.size,
        url: f.url
      }))
    });
  } catch (error) {
    console.error('Upload error:', error);
    res.status(500).json({
      success: false,
      message: 'Upload failed',
      error: error instanceof Error ? error.message : 'Unknown error'
    });
  }
};

export const getFiles = async (req: Request, res: Response) => {
  try {
    res.status(200).json({
      success: true,
      files: filesDB.map(file => ({
        id: file.id,
        name: file.originalName,
        size: file.size,
        type: file.type,
        url: file.url,
        timestamp: file.timestamp,
        receiverEmail: file.receiverEmail,
        receiverPhone: file.receiverPhone,
        communicationMethod: file.communicationMethod
      }))
    });
  } catch (error) {
    console.error('Get files error:', error);
    res.status(500).json({
      success: false,
      message: 'Failed to fetch files',
      error: error instanceof Error ? error.message : 'Unknown error'
    });
  }
};

export const downloadFile = async (req: Request, res: Response) => {
  try {
    const { fileId } = req.params;
    const file = filesDB.find(f => f.id === fileId);

    if (!file) {
      return res.status(404).json({
        success: false,
        message: 'File not found'
      });
    }

    const filePath = path.join(__dirname, '../../uploads', file.name);

    if (!fs.existsSync(filePath)) {
      return res.status(404).json({
        success: false,
        message: 'File not found on server'
      });
    }

    res.download(filePath, file.originalName);
  } catch (error) {
    console.error('Download error:', error);
    res.status(500).json({
      success: false,
      message: 'Download failed',
      error: error instanceof Error ? error.message : 'Unknown error'
    });
  }
};

export const deleteFile = async (req: Request, res: Response) => {
  try {
    const { fileId } = req.params;
    const fileIndex = filesDB.findIndex(f => f.id === fileId);

    if (fileIndex === -1) {
      return res.status(404).json({
        success: false,
        message: 'File not found'
      });
    }

    const file = filesDB[fileIndex];
    const filePath = path.join(__dirname, '../../uploads', file.name);

    // Delete file from filesystem
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
    }

    // Remove from database
    filesDB.splice(fileIndex, 1);

    res.status(200).json({
      success: true,
      message: 'File deleted successfully'
    });
  } catch (error) {
    console.error('Delete error:', error);
    res.status(500).json({
      success: false,
      message: 'Delete failed',
      error: error instanceof Error ? error.message : 'Unknown error'
    });
  }
};
```

---

## File: `backend/src/routes/fileRoutes.ts`

```typescript
import express from 'express';
import { upload } from '../middleware/upload';
import {
  uploadFiles,
  getFiles,
  downloadFile,
  deleteFile
} from '../controllers/fileController';

const router = express.Router();

// Upload files
router.post('/upload', upload.array('files', 10), uploadFiles);

// Get all files
router.get('/files', getFiles);

// Download file
router.get('/download/:fileId', downloadFile);

// Delete file
router.delete('/files/:fileId', deleteFile);

export default router;
```

---

## File: `backend/package.json`

```json
{
  "name": "file-transfer-backend",
  "version": "1.0.0",
  "description": "Backend API for file transfer application",
  "main": "dist/server.js",
  "scripts": {
    "dev": "ts-node-dev --respawn --transpile-only src/server.ts",
    "build": "tsc",
    "start": "node dist/server.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "cors": "^2.8.5",
    "multer": "^1.4.5-lts.1"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/cors": "^2.8.17",
    "@types/multer": "^1.4.11",
    "@types/node": "^20.10.0",
    "ts-node-dev": "^2.0.0",
    "typescript": "^5.3.3"
  }
}
```

---

## File: `backend/tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "moduleResolution": "node"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules"]
}
```

---

## Setup Instructions

### Frontend Setup
```bash
# Install dependencies
npm install

# Create .env file
echo "VITE_API_BASE_URL=http://localhost:3000/api" > .env

# Run development server
npm run dev
```

### Backend Setup
```bash
cd backend

# Install dependencies
npm install

# Run development server
npm run dev
```

The backend will run on `http://localhost:3000` and handle all file uploads, downloads, and deletions!
