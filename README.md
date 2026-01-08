code

    # Client
    npm install react react-router-dom
    
Server

    npm install express cors crypto
    npm install -D @types/express @types/cors @types/node

link
    
    // ============================================
    // CLIENT SIDE CODE
    // ============================================
    
 src/types/index.ts
 
    export interface FileAccessResponse {
      success: boolean;
      email?: string;
      phone?: string;
      communicationType?: 'sms' | 'email';
    }
    
    export interface OTPSendResponse {
      success: boolean;
      message: string;
      expiryTime: number;
    }
    
    export interface OTPVerifyResponse {
      success: boolean;
      message: string;
      token: string;
    }
    
    export interface PasskeyVerifyResponse {
      success: boolean;
      message: string;
      fileUrl?: string;
    }
    
 src/services/api.ts
 
    const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api';
    
    export const securedFilesAPI = {
      checkAccess: async (id: string): Promise<FileAccessResponse> => {
        const res = await fetch(`${API_BASE_URL}/secured-files/${id}/check-access`);
        return res.json();
      },
    
      sendOTP: async (id: string, method: 'sms' | 'email'): Promise<OTPSendResponse> => {
        const res = await fetch(`${API_BASE_URL}/secured-files/${id}/send-otp`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ method })
        });
        return res.json();
      },
    
      verifyOTP: async (id: string, otp: string): Promise<OTPVerifyResponse> => {
        const res = await fetch(`${API_BASE_URL}/secured-files/${id}/verify-otp`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ otp })
        });
        return res.json();
      },
    
      verifyPasskey: async (id: string, passkey: string, token: string): Promise<PasskeyVerifyResponse> => {
        const res = await fetch(`${API_BASE_URL}/secured-files/${id}/verify-passkey`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({ passkey })
        });
        return res.json();
      }
    };
    
 src/hooks/useTimer.ts
 
    import { useState, useEffect, useRef } from 'react';
    
    export const useTimer = (initialTime: number) => {
      const [timeLeft, setTimeLeft] = useState(initialTime);
      const [isActive, setIsActive] = useState(false);
      const intervalRef = useRef<NodeJS.Timeout | null>(null);
    
      useEffect(() => {
        if (isActive && timeLeft > 0) {
          intervalRef.current = setInterval(() => {
            setTimeLeft(prev => {
              if (prev <= 1) {
                setIsActive(false);
                return 0;
              }
              return prev - 1;
            });
          }, 1000);
        }
    
        return () => {
          if (intervalRef.current) clearInterval(intervalRef.current);
        };
      }, [isActive, timeLeft]);
    
      const start = (time?: number) => {
        if (time) setTimeLeft(time);
        setIsActive(true);
      };
    
      const reset = (time: number) => {
        setTimeLeft(time);
        setIsActive(true);
      };
    
      const pause = () => setIsActive(false);
    
      return { timeLeft, isActive, start, reset, pause };
    };
    
 src/utils/mask.ts
 
    export const maskEmail = (email: string): string => {
      const [local, domain] = email.split('@');
      const masked = local.slice(0, 2) + '*'.repeat(local.length - 2);
      return `${masked}@${domain}`;
    };
    
    export const maskPhone = (phone: string): string => {
      return phone.slice(0, 2) + '*'.repeat(phone.length - 4) + phone.slice(-2);
    };
    
 src/components/OTPMethodSelection.tsx
 
    import React, { useState } from 'react';
    import styled from 'styled-components';
    
    interface Props {
      email: string;
      phone: string;
      defaultMethod: 'sms' | 'email';
      onSendOTP: (method: 'sms' | 'email') => void;
      loading: boolean;
    }
    
    export const OTPMethodSelection: React.FC<Props> = ({ 
      email, 
      phone, 
      defaultMethod, 
      onSendOTP,
      loading 
    }) => {
      const [method, setMethod] = useState<'sms' | 'email'>(defaultMethod);
    
      return (
        <StyledWrapper>
          <div className="otp-method-selection">
            <h2>Select OTP Delivery Method</h2>
            <div className="radio-input">
              <label className="label">
                <input
                  type="radio"
                  value="email"
                  checked={method === 'email'}
                  onChange={(e) => setMethod(e.target.value as 'email')}
                  name="otp-method"
                />
                <p className="text">Email: {email}</p>
              </label>
              <label className="label">
                <input
                  type="radio"
                  value="sms"
                  checked={method === 'sms'}
                  onChange={(e) => setMethod(e.target.value as 'sms')}
                  name="otp-method"
                />
                <p className="text">SMS: {phone}</p>
              </label>
            </div>
            <button 
              className="button"
              onClick={() => onSendOTP(method)} 
              disabled={loading}
            >
              {loading ? 'Sending...' : 'Send OTP'}
              <svg fill="currentColor" viewBox="0 0 24 24" className="icon">
                <path clipRule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm4.28 10.28a.75.75 0 000-1.06l-3-3a.75.75 0 10-1.06 1.06l1.72 1.72H8.25a.75.75 0 000 1.5h5.69l-1.72 1.72a.75.75 0 101.06 1.06l3-3z" fillRule="evenodd" />
              </svg>
            </button>
          </div>
        </StyledWrapper>
      );
    };
    
    const StyledWrapper = styled.div`
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    
      .otp-method-selection {
        padding: 40px;
        max-width: 450px;
        width: 100%;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.18);
      }
    
      @media (max-width: 768px) {
        .otp-method-selection {
          padding: 30px 20px;
          max-width: 100%;
        }
      }
    
      @media (max-width: 480px) {
        padding: 15px;
        
        .otp-method-selection {
          padding: 25px 15px;
        }
      }
    
      h2 {
        color: #1a1a1a;
        margin-bottom: 30px;
        font-size: 24px;
        text-align: center;
        font-weight: 600;
      }
    
      @media (max-width: 480px) {
        h2 {
          font-size: 20px;
          margin-bottom: 20px;
        }
      }
    
      .radio-input {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-bottom: 20px;
      }
    
      .radio-input * {
        box-sizing: border-box;
        padding: 0;
        margin: 0;
      }
    
      .radio-input label {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 0px 20px;
        width: 100%;
        cursor: pointer;
        height: 50px;
        position: relative;
      }
    
      @media (max-width: 480px) {
        .radio-input label {
          padding: 0px 15px;
          gap: 10px;
        }
    
        .radio-input .label .text {
          font-size: 13px;
        }
      }
    
      .radio-input label::before {
        position: absolute;
        content: "";
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 100%;
        height: 45px;
        z-index: -1;
        transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        border-radius: 10px;
        border: 2px solid transparent;
      }
    
      .radio-input label:hover::before {
        transition: all 0.2s ease;
        background-color: #f0f0f0;
      }
    
      .radio-input .label:has(input:checked)::before {
        background-color: #e8f0fe;
        border-color: #435dd8;
        height: 50px;
      }
    
      .radio-input .label .text {
        color: #1a1a1a;
        font-size: 14px;
      }
    
      .radio-input .label input[type="radio"] {
        background-color: #ffffff;
        appearance: none;
        width: 17px;
        height: 17px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 2px solid #d0d0d0;
      }
    
      .radio-input .label input[type="radio"]:checked {
        background-color: #435dd8;
        border-color: #435dd8;
        animation: pulse 0.7s forwards;
      }
    
      .radio-input .label input[type="radio"]:before {
        content: "";
        width: 6px;
        height: 6px;
        border-radius: 50%;
        transition: all 0.1s cubic-bezier(0.165, 0.84, 0.44, 1);
        background-color: #fff;
        transform: scale(0);
      }
    
      .radio-input .label input[type="radio"]:checked::before {
        transform: scale(1);
      }
    
      .button {
        position: relative;
        transition: all 0.3s ease-in-out;
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.2);
        padding-block: 0.5rem;
        padding-inline: 1.25rem;
        background-color: rgb(0 107 179);
        border-radius: 9999px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        color: #ffffff;
        gap: 10px;
        font-weight: bold;
        border: 3px solid #ffffff4d;
        outline: none;
        overflow: hidden;
        font-size: 15px;
        width: 100%;
      }
    
      .button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
      }
    
      .icon {
        width: 24px;
        height: 24px;
        transition: all 0.3s ease-in-out;
      }
    
      .button:hover:not(:disabled) {
        transform: scale(1.05);
        border-color: #fff9;
      }
    
      .button:hover:not(:disabled) .icon {
        transform: translate(4px);
      }
    
      .button:hover:not(:disabled)::before {
        animation: shine 1.5s ease-out infinite;
      }
    
      .button::before {
        content: "";
        position: absolute;
        width: 100px;
        height: 100%;
        background-image: linear-gradient(
          120deg,
          rgba(255, 255, 255, 0) 30%,
          rgba(255, 255, 255, 0.8),
          rgba(255, 255, 255, 0) 70%
        );
        top: 0;
        left: -100px;
        opacity: 0.6;
      }
    
      @keyframes shine {
        0% {
          left: -100px;
        }
        60% {
          left: 100%;
        }
        to {
          left: 100%;
        }
      }
    
      @keyframes pulse {
        0% {
          box-shadow: 0 0 0 0 rgba(67, 93, 216, 0.4);
        }
        70% {
          box-shadow: 0 0 0 8px rgba(67, 93, 216, 0);
        }
        100% {
          box-shadow: 0 0 0 0 rgba(67, 93, 216, 0);
        }
      }
    `;
    
    // Demo component to show usage
    const Demo = () => {
      const [loading, setLoading] = useState(false);
    
      const handleSendOTP = (method: 'sms' | 'email') => {
        setLoading(true);
        console.log(`Sending OTP via ${method}`);
        setTimeout(() => setLoading(false), 2000);
      };
    
      return (
        <OTPMethodSelection
          email="user@example.com"
          phone="+1 (555) 123-4567"
          defaultMethod="email"
          onSendOTP={handleSendOTP}
          loading={loading}
        />
      );
    };
    
    export default Demo;
    
 src/components/OTPVerification.tsx
 
    import React, { useState, useEffect } from 'react';
    import { useTimer } from '../hooks/useTimer';
    
    interface Props {
      onVerify: (otp: string) => void;
      onResend: () => void;
      expiryTime: number;
      loading: boolean;
    }
    
    export const OTPVerification: React.FC<Props> = ({ 
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
    
      return (
        <div className="otp-verification">
          <h2>Enter OTP</h2>
          <p>Time remaining: {timeLeft}s</p>
          <input
            type="text"
            maxLength={4}
            value={otp}
            onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
            placeholder="Enter 4-digit OTP"
            disabled={timeLeft === 0}
          />
          <button 
            onClick={() => onVerify(otp)} 
            disabled={otp.length !== 4 || timeLeft === 0 || loading}
          >
            {loading ? 'Verifying...' : 'Submit OTP'}
          </button>
          <button onClick={handleResend} disabled={loading}>
            Resend OTP
          </button>
        </div>
      );
    };
    
 src/components/PasskeyInput.tsx
 
    import React, { useState } from 'react';
    
    interface Props {
      onSubmit: (passkey: string) => void;
      loading: boolean;
    }
    
    export const PasskeyInput: React.FC<Props> = ({ onSubmit, loading }) => {
      const [passkey, setPasskey] = useState('');
    
      return (
        <div className="passkey-input">
          <h2>Enter 6-Digit Passkey</h2>
          <input
            type="password"
            maxLength={6}
            value={passkey}
            onChange={(e) => setPasskey(e.target.value.replace(/\D/g, ''))}
            placeholder="Enter 6-digit passkey"
          />
          <button 
            onClick={() => onSubmit(passkey)} 
            disabled={passkey.length !== 6 || loading}
          >
            {loading ? 'Verifying...' : 'Submit Passkey'}
          </button>
        </div>
      );
    };
    
 src/components/NotFound.tsx
 
    import React from 'react';
    
    export const NotFound: React.FC = () => {
      return (
        <div className="not-found">
          <h1>404</h1>
          <p>File not found or access denied</p>
        </div>
      );
    };
    
 src/app/SecuredFilePage.tsx
 
    import React, { useState, useEffect } from 'react';
    import { useParams } from 'react-router-dom';
    import { securedFilesAPI } from '../services/api';
    import { OTPMethodSelection } from '../components/OTPMethodSelection';
    import { OTPVerification } from '../components/OTPVerification';
    import { PasskeyInput } from '../components/PasskeyInput';
    import { NotFound } from '../components/NotFound';
    import { maskEmail, maskPhone } from '../utils/mask';
    
    type Stage = 'loading' | 'not-found' | 'otp-method' | 'otp-verify' | 'passkey' | 'success';
    
    export const SecuredFilePage: React.FC = () => {
      const { id } = useParams<{ id: string }>();
      const [stage, setStage] = useState<Stage>('loading');
      const [email, setEmail] = useState('');
      const [phone, setPhone] = useState('');
      const [communicationType, setCommunicationType] = useState<'sms' | 'email'>('email');
      const [expiryTime, setExpiryTime] = useState(75);
      const [token, setToken] = useState('');
      const [loading, setLoading] = useState(false);
    
      useEffect(() => {
        checkAccess();
      }, [id]);
    
      const checkAccess = async () => {
        if (!id) return;
        
        const data = await securedFilesAPI.checkAccess(id);
        
        if (!data.success) {
          setStage('not-found');
        } else {
          setEmail(maskEmail(data.email!));
          setPhone(maskPhone(data.phone!));
          setCommunicationType(data.communicationType!);
          setStage('otp-method');
        }
      };
    
      const handleSendOTP = async (method: 'sms' | 'email') => {
        if (!id) return;
        
        setLoading(true);
        const data = await securedFilesAPI.sendOTP(id, method);
        setLoading(false);
        
        if (data.success) {
          setExpiryTime(data.expiryTime);
          setStage('otp-verify');
        }
      };
    
      const handleVerifyOTP = async (otp: string) => {
        if (!id) return;
        
        setLoading(true);
        const data = await securedFilesAPI.verifyOTP(id, otp);
        setLoading(false);
        
        if (data.success) {
          setToken(data.token);
          setStage('passkey');
        } else {
          alert(data.message);
        }
      };
    
      const handleResendOTP = async () => {
        await handleSendOTP(communicationType);
      };
    
      const handleVerifyPasskey = async (passkey: string) => {
        if (!id) return;
        
        setLoading(true);
        const data = await securedFilesAPI.verifyPasskey(id, passkey, token);
        setLoading(false);
        
        if (data.success) {
          setStage('success');
          // Handle file download or display
          window.location.href = data.fileUrl!;
        } else {
          alert(data.message);
        }
      };
    
      if (stage === 'loading') return <div>Loading...</div>;
      if (stage === 'not-found') return <NotFound />;
    
      return (
        <div className="secured-file-page">
          {stage === 'otp-method' && (
            <OTPMethodSelection
              email={email}
              phone={phone}
              defaultMethod={communicationType}
              onSendOTP={handleSendOTP}
              loading={loading}
            />
          )}
          {stage === 'otp-verify' && (
            <OTPVerification
              onVerify={handleVerifyOTP}
              onResend={handleResendOTP}
              expiryTime={expiryTime}
              loading={loading}
            />
          )}
          {stage === 'passkey' && (
            <PasskeyInput
              onSubmit={handleVerifyPasskey}
              loading={loading}
            />
          )}
          {stage === 'success' && (
            <div>Access granted! Redirecting...</div>
          )}
        </div>
      );
    };
    
    // ============================================
    // SERVER SIDE CODE
    // ============================================
    
 src/entities/SecuredFile.ts
 
    export interface SecuredFile {
      id: string;
      email: string;
      phone: string;
      communicationType: 'sms' | 'email';
      passkey: string;
      fileUrl: string;
    }
    
    export interface OTPRecord {
      fileId: string;
      otp: string;
      expiryTime: Date;
      method: 'sms' | 'email';
    }
    
 src/config/database.ts
 
    import { SecuredFile, OTPRecord } from '../entities/SecuredFile';
    
    // Mock database
    export const filesDB: Map<string, SecuredFile> = new Map();
    export const otpDB: Map<string, OTPRecord> = new Map();
    
 src/helper/crypto.ts
 
    import crypto from 'crypto';
    
    export const generateOTP = (): string => {
      return Math.floor(1000 + Math.random() * 9000).toString();
    };
    
    export const generateToken = (): string => {
      return crypto.randomBytes(32).toString('hex');
    };
    
    export const hashPasskey = (passkey: string): string => {
      return crypto.createHash('sha256').update(passkey).digest('hex');
    };
    
 src/helper/notification.ts
 
    export const sendEmail = async (email: string, otp: string): Promise<boolean> => {
      // Implement email sending logic
      console.log(`Sending OTP ${otp} to email: ${email}`);
      return true;
    };
    
    export const sendSMS = async (phone: string, otp: string): Promise<boolean> => {
      // Implement SMS sending logic
      console.log(`Sending OTP ${otp} to phone: ${phone}`);
      return true;
    };
    
 src/middleware/auth.ts
 
    import { Request, Response, NextFunction } from 'express';
    
    export interface AuthRequest extends Request {
      token?: string;
    }
    
    export const verifyToken = (req: AuthRequest, res: Response, next: NextFunction) => {
      const token = req.headers.authorization?.replace('Bearer ', '');
      
      if (!token) {
        return res.status(401).json({ success: false, message: 'No token provided' });
      }
      
      req.token = token;
      next();
    };
    
 src/services/securedFileService.ts
 
    import { filesDB, otpDB } from '../config/database';
    import { generateOTP, generateToken, hashPasskey } from '../helper/crypto';
    import { sendEmail, sendSMS } from '../helper/notification';
    import { SecuredFile, OTPRecord } from '../entities/SecuredFile';
    
    export const securedFileService = {
      checkAccess: (id: string) => {
        const file = filesDB.get(id);
        
        if (!file) {
          return { success: false };
        }
        
        return {
          success: true,
          email: file.email,
          phone: file.phone,
          communicationType: file.communicationType
        };
      },
    
      sendOTP: async (id: string, method: 'sms' | 'email') => {
        const file = filesDB.get(id);
        
        if (!file) {
          return { success: false, message: 'File not found' };
        }
        
        const otp = generateOTP();
        const expiryTime = new Date(Date.now() + 75000); // 75 seconds
        
        otpDB.set(id, { fileId: id, otp, expiryTime, method });
        
        if (method === 'email') {
          await sendEmail(file.email, otp);
        } else {
          await sendSMS(file.phone, otp);
        }
        
        return { success: true, message: 'OTP sent', expiryTime: 75 };
      },
    
      verifyOTP: (id: string, otp: string) => {
        const record = otpDB.get(id);
        
        if (!record) {
          return { success: false, message: 'OTP not found' };
        }
        
        if (new Date() > record.expiryTime) {
          otpDB.delete(id);
          return { success: false, message: 'OTP expired' };
        }
        
        if (record.otp !== otp) {
          return { success: false, message: 'Invalid OTP' };
        }
        
        otpDB.delete(id);
        const token = generateToken();
        
        return { success: true, message: 'OTP verified', token };
      },
    
      verifyPasskey: (id: string, passkey: string) => {
        const file = filesDB.get(id);
        
        if (!file) {
          return { success: false, message: 'File not found' };
        }
        
        const hashedPasskey = hashPasskey(passkey);
        
        if (hashedPasskey !== file.passkey) {
          return { success: false, message: 'Invalid passkey' };
        }
        
        return { success: true, message: 'Access granted', fileUrl: file.fileUrl };
      }
    };
    
 src/controllers/securedFileController.ts
 
    import { Request, Response } from 'express';
    import { securedFileService } from '../services/securedFileService';
    import { AuthRequest } from '../middleware/auth';
    
    export const securedFileController = {
      checkAccess: (req: Request, res: Response) => {
        const { id } = req.params;
        const result = securedFileService.checkAccess(id);
        res.json(result);
      },
    
      sendOTP: async (req: Request, res: Response) => {
        const { id } = req.params;
        const { method } = req.body;
        const result = await securedFileService.sendOTP(id, method);
        res.json(result);
      },
    
      verifyOTP: (req: Request, res: Response) => {
        const { id } = req.params;
        const { otp } = req.body;
        const result = securedFileService.verifyOTP(id, otp);
        res.json(result);
      },
    
      verifyPasskey: (req: AuthRequest, res: Response) => {
        const { id } = req.params;
        const { passkey } = req.body;
        const result = securedFileService.verifyPasskey(id, passkey);
        res.json(result);
      }
    };
    
 src/routes/securedFileRoutes.ts
 
    import { Router } from 'express';
    import { securedFileController } from '../controllers/securedFileController';
    import { verifyToken } from '../middleware/auth';
    
    const router = Router();
    
    router.get('/:id/check-access', securedFileController.checkAccess);
    router.post('/:id/send-otp', securedFileController.sendOTP);
    router.post('/:id/verify-otp', securedFileController.verifyOTP);
    router.post('/:id/verify-passkey', verifyToken, securedFileController.verifyPasskey);
    
    export default router;
    
 src/server.ts

    import express from 'express';
    import cors from 'cors';
    import securedFileRoutes from './routes/securedFileRoutes';
    
    const app = express();
    const PORT = process.env.PORT || 3000;
    
    app.use(cors());
    app.use(express.json());
    
    app.use('/api/secured-files', securedFileRoutes);
    
    app.listen(PORT, () => {
      console.log(`Server running on port ${PORT}`);
    });
    
    export default app;


