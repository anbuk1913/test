code

    await sendSecureFileLinkEmail({
      recipientEmail: 'user@example.com',
      secureLink: 'https://your-secure-link.com/file/abc123'
    });

link
    
    SMTP_HOST=smtp.gmail.com
    SMTP_PORT=587
    SMTP_USER=your-email@gmail.com
    SMTP_PASS=your-app-password
    
    npm install nodemailer

new
    
    npm install --save-dev @types/nodemailer


code
    
    import nodemailer from 'nodemailer';
    
    interface SecureFileEmailData {
      recipientEmail: string;
      secureLink: string;
    }
    
    // Simple email template
    function generateSecureFileEmailTemplate(secureLink: string): string {
      return `
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Secure File Shared</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background-color: #f4f4f4; padding: 20px;">
        <tr>
          <td align="center">
            <table width="600" cellpadding="0" cellspacing="0" style="background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
              
              <!-- Header -->
              <tr>
                <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center;">
                  <h1 style="color: #ffffff; margin: 0; font-size: 24px;">🔒 Secure File Shared</h1>
                </td>
              </tr>
              
              <!-- Body Content -->
              <tr>
                <td style="padding: 40px 30px;">
                  <p style="color: #333333; font-size: 16px; line-height: 1.6; margin: 0 0 20px 0;">
                    Hello,
                  </p>
                  
                  <p style="color: #333333; font-size: 16px; line-height: 1.6; margin: 0 0 30px 0;">
                    A secure file has been shared with you. Click the button below to access it.
                  </p>
                  
                  <!-- CTA Button -->
                  <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
                    <tr>
                      <td align="center">
                        <a href="${secureLink}" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; text-decoration: none; padding: 14px 40px; border-radius: 6px; font-size: 16px; font-weight: bold;">
                          Access Secure File
                        </a>
                      </td>
                    </tr>
                  </table>
                  
                  <p style="color: #666666; font-size: 14px; line-height: 1.6; margin: 30px 0 0 0;">
                    If you did not expect this file, please ignore this email.
                  </p>
                </td>
              </tr>
              
              <!-- Footer -->
              <tr>
                <td style="background-color: #f8f9fa; padding: 20px 30px; text-align: center; border-top: 1px solid #e9ecef;">
                  <p style="margin: 0; color: #999999; font-size: 12px;">
                    This is an automated message. Please do not reply to this email.
                  </p>
                </td>
              </tr>
              
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
      `;
    }
    
    // Configure email transporter
    function createEmailTransporter() {
      return nodemailer.createTransport({
        host: process.env.SMTP_HOST || 'smtp.gmail.com',
        port: parseInt(process.env.SMTP_PORT || '587'),
        secure: false,
        auth: {
          user: process.env.SMTP_USER,
          pass: process.env.SMTP_PASS,
        },
      });
    }
    
    // Send secure file link email
    async function sendSecureFileLinkEmail(data: SecureFileEmailData): Promise<void> {
      try {
        const transporter = createEmailTransporter();
        
        const mailOptions = {
          from: process.env.SMTP_USER,
          to: data.recipientEmail,
          subject: '🔒 Secure File Shared',
          html: generateSecureFileEmailTemplate(data.secureLink),
          text: `A secure file has been shared with you. Access it here: ${data.secureLink}`,
        };
    
        const info = await transporter.sendMail(mailOptions);
        console.log('Email sent successfully:', info.messageId);
      } catch (error) {
        console.error('Error sending email:', error);
        throw error;
      }
    }
    
    // Example usage
    async function example() {
      await sendSecureFileLinkEmail({
        recipientEmail: 'recipient@example.com',
        secureLink: 'https://secure.yourapp.com/files/abc123xyz',
      });
    }
    
    // Uncomment to run
    // example().catch(console.error);
    
    export { sendSecureFileLinkEmail, SecureFileEmailData };
