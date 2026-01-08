http://localhost:3881/profile/TX/45ffd741-307b-4c6b-a61f-b707a5dad89d?action=invite&token=7bac2794bbedfd49725ed57b6b3539a5


Sodium-Native
    
    const sodium = require('sodium-native');
    const fs = require('fs').promises;
    const path = require('path');
    
    const SALT_LENGTH = sodium.crypto_pwhash_SALTBYTES; // 16 bytes
    const KEY_LENGTH = sodium.crypto_secretbox_KEYBYTES; // 32 bytes
    const NONCE_LENGTH = sodium.crypto_secretbox_NONCEBYTES; // 24 bytes
    
    function deriveKey(password, salt) {
      const key = Buffer.allocUnsafe(KEY_LENGTH);
      const passwordBuffer = Buffer.from(password);
      
      sodium.crypto_pwhash(
        key,
        passwordBuffer,
        salt,
        sodium.crypto_pwhash_OPSLIMIT_INTERACTIVE,
        sodium.crypto_pwhash_MEMLIMIT_INTERACTIVE,
        sodium.crypto_pwhash_ALG_ARGON2ID13
      );
      
      return key;
    }
    
    /**
     * Encrypts a file
     * @param {string} inputPath - Path to the file to encrypt
     * @param {string} outputPath - Path where encrypted file will be saved
     * @param {string} password - Password for encryption
     */
    async function encryptFile(inputPath, outputPath, password) {
      try {
        // Read the file
        const data = await fs.readFile(inputPath);
        
        // Generate random salt and nonce
        const salt = Buffer.allocUnsafe(SALT_LENGTH);
        const nonce = Buffer.allocUnsafe(NONCE_LENGTH);
        sodium.randombytes_buf(salt);
        sodium.randombytes_buf(nonce);
        
        // Derive key from password
        const key = deriveKey(password, salt);
        
        // Prepare buffer for encrypted data (includes MAC tag)
        const encrypted = Buffer.allocUnsafe(data.length + sodium.crypto_secretbox_MACBYTES);
        
        // Encrypt the data using secretbox (XSalsa20 + Poly1305)
        sodium.crypto_secretbox_easy(encrypted, data, nonce, key);
        
        // Combine salt + nonce + encrypted data
        const output = Buffer.concat([salt, nonce, encrypted]);
        
        // Write to output file
        await fs.writeFile(outputPath, output);
        
        console.log(`✓ File encrypted successfully: ${outputPath}`);
        return true;
      } catch (error) {
        console.error('Encryption error:', error.message);
        throw error;
      }
    }
    
    /**
     * Decrypts a file
     * @param {string} inputPath - Path to the encrypted file
     * @param {string} outputPath - Path where decrypted file will be saved
     * @param {string} password - Password for decryption
     */
    async function decryptFile(inputPath, outputPath, password) {
      try {
        // Read the encrypted file
        const data = await fs.readFile(inputPath);
        
        // Extract components
        const salt = data.slice(0, SALT_LENGTH);
        const nonce = data.slice(SALT_LENGTH, SALT_LENGTH + NONCE_LENGTH);
        const encrypted = data.slice(SALT_LENGTH + NONCE_LENGTH);
        
        // Derive key from password
        const key = deriveKey(password, salt);
        
        // Prepare buffer for decrypted data
        const decrypted = Buffer.allocUnsafe(encrypted.length - sodium.crypto_secretbox_MACBYTES);
        
        // Decrypt the data
        const result = sodium.crypto_secretbox_open_easy(decrypted, encrypted, nonce, key);
        
        if (!result) {
          throw new Error('Invalid password or corrupted file');
        }
        
        // Write to output file
        await fs.writeFile(outputPath, decrypted);
        
        console.log(`✓ File decrypted successfully: ${outputPath}`);
        return true;
      } catch (error) {
        console.error('Decryption error:', error.message);
        throw error;
      }
    }
    
    /**
     * Encrypts a file in place (overwrites original)
     */
    async function encryptFileInPlace(filePath, password) {
      const tempPath = `${filePath}.tmp`;
      await encryptFile(filePath, tempPath, password);
      await fs.rename(tempPath, filePath);
    }
    
    /**
     * Decrypts a file in place (overwrites original)
     */
    async function decryptFileInPlace(filePath, password) {
      const tempPath = `${filePath}.tmp`;
      await decryptFile(filePath, tempPath, password);
      await fs.rename(tempPath, filePath);
    }
    
    // Example usage
    async function main() {
      const password = 'your-secure-password-here';
      
      // Example 1: Encrypt a file
      await encryptFile(
        './769af862af4724e348bd90fda8fdea5f.webp',
        './encrypted.enc',
        password
      );
      
      // Example 2: Decrypt a file
      await decryptFile(
        './encrypted.enc',
        './img.png',
        password
      );
      
      // Example 3: Encrypt in place
      // await encryptFileInPlace('./myfile.txt', password);
      
      // Example 4: Decrypt in place
      // await decryptFileInPlace('./myfile.txt', password);
    }
    
    // Uncomment to run examples
    main().catch(console.error);
    
    // Export functions
    module.exports = {
      encryptFile,
      decryptFile,
      encryptFileInPlace,
      decryptFileInPlace
    };
