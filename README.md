src/templates/otp-email.html

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OTP Verification</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #04285b 0%, #00b3d0 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .email-container {
                max-width: 600px;
                width: 100%;
                background: white;
                border-radius: 12px;
                box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
                overflow: hidden;
            }
            
            .header {
                background: linear-gradient(135deg, #04285b 0%, #00b3d0 100%);
                padding: 40px 30px;
                text-align: center;
            }
            
            .header h1 {
                color: white;
                font-size: 28px;
                margin-bottom: 10px;
            }
            
            .header p {
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
            }
            
            .content {
                padding: 40px 30px;
            }
            
            .greeting {
                color: #04285b;
                font-size: 18px;
                margin-bottom: 20px;
            }
            
            .message {
                color: #555;
                font-size: 15px;
                line-height: 1.6;
                margin-bottom: 30px;
            }
            
            .otp-section {
                background: linear-gradient(135deg, rgba(4, 40, 91, 0.05) 0%, rgba(0, 179, 208, 0.05) 100%);
                border: 2px dashed #00b3d0;
                border-radius: 8px;
                padding: 30px;
                text-align: center;
                margin-bottom: 30px;
            }
            
            .otp-label {
                color: #04285b;
                font-size: 14px;
                font-weight: 600;
                margin-bottom: 15px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .otp-code {
                font-size: 42px;
                font-weight: bold;
                color: #04285b;
                letter-spacing: 8px;
                margin-bottom: 20px;
                user-select: all;
            }
            
            .copy-button {
                background: linear-gradient(135deg, #04285b 0%, #00b3d0 100%);
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 6px;
                font-size: 15px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                box-shadow: 0 4px 15px rgba(0, 179, 208, 0.3);
            }
            
            .copy-button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 179, 208, 0.4);
            }
            
            .copy-button:active {
                transform: translateY(0);
            }
            
            .copy-button.copied {
                background: #10b981;
            }
            
            .validity {
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                border-radius: 4px;
                margin-bottom: 30px;
            }
            
            .validity p {
                color: #856404;
                font-size: 14px;
                margin: 0;
            }
            
            .warning {
                color: #666;
                font-size: 13px;
                line-height: 1.6;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 6px;
                margin-bottom: 20px;
            }
            
            .footer {
                background: #f8f9fa;
                padding: 25px 30px;
                text-align: center;
                border-top: 1px solid #e9ecef;
            }
            
            .footer p {
                color: #6c757d;
                font-size: 13px;
                margin-bottom: 10px;
            }
            
            .footer a {
                color: #00b3d0;
                text-decoration: none;
            }
            
            @media (max-width: 600px) {
                .header h1 {
                    font-size: 24px;
                }
                
                .otp-code {
                    font-size: 32px;
                    letter-spacing: 6px;
                }
                
                .content {
                    padding: 30px 20px;
                }
            }
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h1>Verification Code</h1>
                <p>Secure your account with OTP</p>
            </div>
            
            <div class="content">
                <div class="greeting">
                    Hello User,
                </div>
                
                <div class="message">
                    We received a request to verify your account. Please use the following One-Time Password (OTP) to complete your verification process.
                </div>
                
                <div class="otp-section">
                    <div class="otp-label">Your OTP Code</div>
                    <div class="otp-code" id="otpCode">123456</div>
                    <button class="copy-button" id="copyBtn" onclick="copyOTP()">
                        <span id="btnText">Copy Code</span>
                    </button>
                </div>
                
                <div class="validity">
                    <p>⏰ This code will expire in <strong>10 minutes</strong></p>
                </div>
                
                <div class="warning">
                    <strong>Security Notice:</strong><br>
                    • Never share this OTP with anyone<br>
                    • Our team will never ask for this code<br>
                    • If you didn't request this code, please ignore this email
                </div>
            </div>
            
            <div class="footer">
                <p>If you have any questions, contact us at <a href="mailto:support@example.com">support@example.com</a></p>
                <p>&copy; 2026 Your Company. All rights reserved.</p>
            </div>
        </div>
    
        <script>
            function copyOTP() {
                const otpText = document.getElementById('otpCode').textContent;
                const btn = document.getElementById('copyBtn');
                const btnText = document.getElementById('btnText');
                
                navigator.clipboard.writeText(otpText).then(() => {
                    btn.classList.add('copied');
                    btnText.textContent = '✓ Copied!';
                    
                    setTimeout(() => {
                        btn.classList.remove('copied');
                        btnText.textContent = 'Copy Code';
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy:', err);
                    btnText.textContent = 'Failed to copy';
                    setTimeout(() => {
                        btnText.textContent = 'Copy Code';
                    }, 2000);
                });
            }
        </script>
    </body>
    </html>




src/services/email.service.ts

    import nodemailer from 'nodemailer';
    import fs from 'fs';
    import path from 'path';
    
    export class EmailService {
      private transporter: nodemailer.Transporter;
    
      constructor() {
        this.transporter = nodemailer.createTransport({
          host: process.env.SMTP_HOST,
          port: parseInt(process.env.SMTP_PORT || '587'),
          secure: false,
          auth: {
            user: process.env.SMTP_USER,
            pass: process.env.SMTP_PASS,
          },
        });
      }
    
      async sendOTP(email: string, otp: string, expiryMinutes: number = 10) {
        const template = fs.readFileSync(
          path.join(__dirname, '../templates/otp-email.html'),
          'utf-8'
        );
    
        const html = template
          .replace('123456', otp)
          .replace('10 minutes', `${expiryMinutes} minutes`);
    
        await this.transporter.sendMail({
          from: process.env.EMAIL_FROM,
          to: email,
          subject: 'Your OTP Verification Code',
          html: html,
        });
      }
    }

src/services/otp.service.ts

    import crypto from 'crypto';
    
    export class OTPService {
      generateOTP(length: number = 6): string {
        return crypto.randomInt(0, Math.pow(10, length))
          .toString()
          .padStart(length, '0');
      }
    }

src/controllers/auth.controller.ts

    import { Request, Response } from 'express';
    import { EmailService } from '../services/email.service';
    import { OTPService } from '../services/otp.service';
    
    export class AuthController {
      private emailService = new EmailService();
      private otpService = new OTPService();
    
      async sendOTP(req: Request, res: Response) {
        try {
          const { email } = req.body;
          const otp = this.otpService.generateOTP();
          
          // Store OTP in cache/database with expiry
          // await redisClient.setex(`otp:${email}`, 600, otp);
          
          await this.emailService.sendOTP(email, otp);
          
          res.json({ success: true, message: 'OTP sent successfully' });
        } catch (error) {
          res.status(500).json({ success: false, error: 'Failed to send OTP' });
        }
      }
    }






    
