📁 Folder Structure
frontend/

        ├── src/
        │   ├── api/
        │   │   └── authAPI.ts
        │   ├── components/
        │   │   ├── AuthButton.tsx
        │   │   └── LogoutButton.tsx
        │   ├── hooks/
        │   │   └── useAuth.ts
        │   ├── App.tsx
        │   └── main.tsx
        ├── tsconfig.json
        ├── package.json
        └── vite.config.ts

🔘 components/AuthButton.tsx

        import React from "react";
        
        const AuthButton: React.FC = () => {
          const handleLogin = () => {
            // Opens the backend OAuth route
            window.open("http://localhost:4000/auth/google", "_self");
          };
        
          return (
            <button onClick={handleLogin} style={{ padding: "10px", margin: "10px" }}>
              Login with Google
            </button>
          );
        };
        
        export default AuthButton;

🔘 components/LogoutButton.tsx

        import React from "react";
        import axios from "axios";
        
        const LogoutButton: React.FC<{ onLogout: () => void }> = ({ onLogout }) => {
          const handleLogout = async () => {
            await axios.get("http://localhost:4000/auth/logout", { withCredentials: true });
            onLogout();
          };
        
          return (
            <button onClick={handleLogout} style={{ padding: "10px", margin: "10px" }}>
              Logout
            </button>
          );
        };
        
        export default LogoutButton;

🌐 api/authAPI.ts

        import axios from "axios";
        
        const api = axios.create({
          baseURL: "http://localhost:4000",
          withCredentials: true,
        });
        
        export const getUser = async () => {
          try {
            const res = await api.get("/auth/me");
            return res.data;
          } catch (err) {
            return null;
          }
        };

🪝 hooks/useAuth.ts

        import { useState, useEffect } from "react";
        import { getUser } from "../api/authAPI";
        
        export const useAuth = () => {
          const [user, setUser] = useState<any>(null);
          const [loading, setLoading] = useState(true);
        
          useEffect(() => {
            getUser().then((data) => {
              setUser(data);
              setLoading(false);
            });
          }, []);
        
          return { user, setUser, loading };
        };

🚀 App.tsx

        import React from "react";
        import AuthButton from "./components/AuthButton";
        import LogoutButton from "./components/LogoutButton";
        import { useAuth } from "./hooks/useAuth";
        
        const App: React.FC = () => {
          const { user, setUser, loading } = useAuth();
        
          if (loading) return <p>Loading...</p>;
        
          return (
            <div style={{ textAlign: "center", marginTop: "50px" }}>
              {!user ? (
                <AuthButton />
              ) : (
                <div>
                  <h2>Welcome, {user.name}</h2>
                  <p>Email: {user.email}</p>
                  <LogoutButton onLogout={() => setUser(null)} />
                </div>
              )}
            </div>
          );
        };
        
        export default App;
        
        🔹 main.tsx
        import React from "react";
        import ReactDOM from "react-dom/client";
        import App from "./App";
        
        ReactDOM.createRoot(document.getElementById("root")!).render(
          <React.StrictMode>
            <App />
          </React.StrictMode>
        );

⚡ Notes

Backend routes expected:

GET /auth/google → redirect to Google login

GET /auth/google/callback → exchange code, set cookie, redirect

GET /auth/me → return user from JWT cookie

GET /auth/logout → clear cookie

Axios withCredentials: true is important for cookies.

You can expand with React Router, context, or loading spinners later.



Flow:

1️⃣ User clicks "Login with Google"
2️⃣ Frontend redirects to Google OAuth URL
3️⃣ Google sends code to backend
4️⃣ Backend exchanges code for access token + user info
5️⃣ Backend creates JWT & sets in HTTP-only cookie

⚙️ Key Library (Backend)

Just install:

npm install google-auth-library jsonwebtoken axios cookie-parser

🔁 Minimal Code Flow (No Passport)
🛑 Backend – Create Google URL (No Passport)

        import express from "express";
        import axios from "axios";
        import jwt from "jsonwebtoken";
        import cookieParser from "cookie-parser";
        import dotenv from "dotenv";
        
        dotenv.config();
        const app = express();
        app.use(cookieParser());
        
        const GOOGLE_CLIENT_ID = process.env.GOOGLE_CLIENT_ID!;
        const GOOGLE_CLIENT_SECRET = process.env.GOOGLE_CLIENT_SECRET!;
        const REDIRECT_URL = "http://localhost:4000/auth/google/callback";
        const FRONTEND_URL = "http://localhost:5173";
        
        app.get("/auth/google", (req, res) => {
          const url =
            `https://accounts.google.com/o/oauth2/v2/auth?` +
            `client_id=${GOOGLE_CLIENT_ID}&` +
            `redirect_uri=${REDIRECT_URL}&` +
            `response_type=code&` +
            `scope=profile email`;
        
          res.redirect(url);
        });
        
        app.get("/auth/google/callback", async (req, res) => {
          const code = req.query.code as string;
        
          const tokenRes = await axios.post(
            `https://oauth2.googleapis.com/token`,
            {
              code,
              client_id: GOOGLE_CLIENT_ID,
              client_secret: GOOGLE_CLIENT_SECRET,
              redirect_uri: REDIRECT_URL,
              grant_type: "authorization_code",
            }
          );
        
          const { access_token } = tokenRes.data;
        
          const userRes = await axios.get(
            `https://www.googleapis.com/oauth2/v2/userinfo`,
            {
              headers: { Authorization: `Bearer ${access_token}` },
            }
          );
        
          const user = userRes.data;
        
          const jwtToken = jwt.sign(user, process.env.JWT_SECRET!, { expiresIn: "1h" });
        
          res.cookie("token", jwtToken, {
            httpOnly: true,
          });
        
          res.redirect(`${FRONTEND_URL}/dashboard`);
        });
        
        app.get("/auth/me", (req, res) => {
          const token = req.cookies.token;
          if (!token) return res.json(null);
        
          try {
            const decoded = jwt.verify(token, process.env.JWT_SECRET!);
            res.json(decoded);
          } catch (err) {
            res.json(null);
          }
        });

        app.listen(4000, () => console.log("Server running"));

🎯 Why Use This (Over Passport)?
Feature	Passport	Custom OAuth
Simplicity	Heavy setup	Lightweight
Control	Limited	Full control
Login Logic	Hidden	Transparent
Best for	Legacy apps	Modern SPA (React/Vue)
🧠 Frontend → Same Code You Already Saw

Use same AuthButton, getUser, useAuth.
