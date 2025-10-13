Skip to content
Chat history

You said:
How to set oauth in react ts app and use cookies 
ChatGPT said:
Let’s go step-by-step 👇
You’ll learn how to set up OAuth (Google, GitHub, etc.) in a React + TypeScript app and use cookies to store the authentication token securely.

🧩 Overview
We’ll use this flow:

Frontend (React + TS) → Backend (Node/Express) → OAuth Provider (Google, GitHub)
Then:

Backend handles OAuth login and issues JWT

JWT is stored in a HTTP-only cookie

Frontend reads user info via an authenticated API

🏗 Step 1: Backend (Node.js + Express)
1. Install dependencies
        npm install express passport passport-google-oauth20 cookie-parser jsonwebtoken cors dotenv
2. Example backend structure

        backend/
        ├── server.ts
        ├── routes/
        │   └── auth.ts
        └── .env
3. .env

        GOOGLE_CLIENT_ID=your_google_client_id
        GOOGLE_CLIENT_SECRET=your_google_client_secret
        JWT_SECRET=super_secret_key
        CLIENT_URL=http://localhost:5173
        
4. server.ts

        import express from "express";
        import passport from "passport";
        import cookieParser from "cookie-parser";
        import session from "express-session";
        import cors from "cors";
        import dotenv from "dotenv";
        import "./strategies/google";
        
        dotenv.config();
        
        const app = express();
        app.use(cookieParser());
        app.use(
          cors({
            origin: process.env.CLIENT_URL,
            credentials: true,
          })
        );
        
        app.use(
          session({
            secret: process.env.JWT_SECRET!,
            resave: false,
            saveUninitialized: false,
          })
        );
        
        app.use(passport.initialize());
        app.use(passport.session());
        
        app.use("/auth", require("./routes/auth"));
        
        app.listen(4000, () => console.log("Server running on http://localhost:4000"));
        5. strategies/google.ts
        import passport from "passport";
        import { Strategy as GoogleStrategy } from "passport-google-oauth20";
        import jwt from "jsonwebtoken";
        import dotenv from "dotenv";
        
        dotenv.config();
        
        passport.use(
          new GoogleStrategy(
            {
              clientID: process.env.GOOGLE_CLIENT_ID!,
              clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
              callbackURL: "http://localhost:4000/auth/google/callback",
            },
            async (accessToken, refreshToken, profile, done) => {
              const user = {
                id: profile.id,
                name: profile.displayName,
                email: profile.emails?.[0].value,
              };
              done(null, user);
            }
          )
        );
        
        passport.serializeUser((user, done) => {
          done(null, user);
        });
        
        passport.deserializeUser((user: any, done) => {
          done(null, user);
        });
6. routes/auth.ts
 
        import express from "express";
        import passport from "passport";
        import jwt from "jsonwebtoken";

        const router = express.Router();
        
        // Step 1: Redirect to Google
        router.get("/google", passport.authenticate("google", { scope: ["profile", "email"] }));
        
        // Step 2: Google callback
        router.get(
          "/google/callback",
          passport.authenticate("google", { failureRedirect: "/" }),
          (req: any, res) => {
            const token = jwt.sign(req.user, process.env.JWT_SECRET!, { expiresIn: "1h" });
            res.cookie("token", token, {
              httpOnly: true,
              secure: false, // use true in production with HTTPS
              sameSite: "lax",
            });
            res.redirect(`${process.env.CLIENT_URL}/dashboard`);
          }
        );
        
        // Protected route example
        router.get("/me", (req, res) => {
          const token = req.cookies.token;
          if (!token) return res.status(401).json({ message: "No token" });
          try {
            const decoded = jwt.verify(token, process.env.JWT_SECRET!);
            res.json(decoded);
          } catch {
            res.status(401).json({ message: "Invalid token" });
          }
        });
        
        module.exports = router;
⚛️ Step 2: Frontend (React + TypeScript)
1. Install dependencies

        npm install axios react-router-dom
    
2. Setup AuthButton.tsx

        import React from "react";
        
        export const AuthButton: React.FC = () => {
          const handleLogin = () => {
            window.open("http://localhost:4000/auth/google", "_self");
          };
        
          return (
            <button
              onClick={handleLogin}
              className="bg-blue-500 text-white px-4 py-2 rounded-md"
            >
              Login with Google
            </button>
          );
        };

3. Use cookies with Axios
By default, Axios doesn’t send cookies — you need to enable it:

        import axios from "axios";
        
        axios.defaults.withCredentials = true;
        
        export const getUser = async () => {
          const res = await axios.get("http://localhost:4000/auth/me");
          return res.data;
        };

🍪 Step 3: How cookies work here
✅ httpOnly: frontend cannot access token via JS → safer
✅ secure: cookie only sent over HTTPS
✅ sameSite: reduces CSRF risk
✅ Browser automatically attaches cookie on requests to your backend

🧠 Optional: Logout

      router.get("/logout", (req, res) => {
        res.clearCookie("token");
        res.json({ message: "Logged out" });
      });

Frontend:

    const logout = async () => {
    await axios.get("http://localhost:4000/auth/logout", { withCredentials: true });
    window.location.href = "/";
    };

✅ Summary
Step	Task	Tool
1	Setup OAuth Strategy	passport-google-oauth20
2	Issue JWT	jsonwebtoken
3	Store token in cookie	res.cookie()
4	Access protected route	Axios with withCredentials
5	Logout by clearing cookie	res.clearCookie()
Would you like me to show you the same setup but using GitHub OAuth instead of Google (or both)?



📁 Recommended Folder Structure (React + TS)

                frontend/
                ├── src/
                │   ├── api/
                │   │   └── authAPI.ts
                │   │
                │   ├── components/
                │   │   ├── buttons/
                │   │   │   └── AuthButton.tsx
                │   │   ├── Navbar.tsx
                │   │   └── Loader.tsx
                │   │
                │   ├── context/
                │   │   └── AuthContext.tsx
                │   │
                │   ├── hooks/
                │   │   └── useAuth.ts
                │   │
                │   ├── pages/
                │   │   ├── Home.tsx
                │   │   ├── Dashboard.tsx
                │   │   └── NotFound.tsx
                │   │
                │   ├── routes/
                │   │   └── PrivateRoute.tsx
                │   │
                │   ├── utils/
                │   │   └── axiosConfig.ts
                │   │
                │   ├── App.tsx
                │   ├── main.tsx
                │   └── vite-env.d.ts
                │
                ├── public/
                │   └── favicon.ico
                │
                ├── tsconfig.json
                ├── package.json
                └── vite.config.ts

🗂 Folder Purpose Explained
Folder	Purpose
api/	        Central place to call backend (/auth/me, /logout)
components/	Reusable UI components (buttons, layouts)
context/	Global auth state (user, login, logout)
hooks/	        Custom hooks like useAuth, useFetch
pages/	        Page screens (Home, Dashboard, Login)
routes/	        Protected Routes (PrivateRoute)
utils/	        Utility functions, axios configuration

🔐 Auth with Context Example

context/AuthContext.tsx

        import React, { createContext, useState, useEffect } from "react";
        import { getUser } from "../api/authAPI";
        
        interface User {
          name: string;
          email: string;
        }
        
        interface AuthContextType {
          user: User | null;
          loading: boolean;
        }
        
        export const AuthContext = createContext<AuthContextType>({
          user: null,
          loading: true,
        });
        
        export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
          const [user, setUser] = useState<User | null>(null);
          const [loading, setLoading] = useState(true);
        
          useEffect(() => {
            getUser().then(setUser).finally(() => setLoading(false));
          }, []);
        
          return (
            <AuthContext.Provider value={{ user, loading }}>
              {children}
            </AuthContext.Provider>
          );
        };

⚙️ Axios Cookie Config

utils/axiosConfig.ts

        import axios from "axios";
        
        const api = axios.create({
          baseURL: "http://localhost:4000",
          withCredentials: true,
        });
        
        export default api;
        
        🧭 Protected Route
        
        routes/PrivateRoute.tsx
        
        import { Navigate } from "react-router-dom";
        import { useAuth } from "../hooks/useAuth";
        
        export const PrivateRoute = ({ children }: any) => {
          const { user, loading } = useAuth();
          if (loading) return <div>Loading...</div>;
          return user ? children : <Navigate to="/" />;
        };
        
        🚀 Usage Example in App.tsx
        <Routes>
          <Route path="/" element={<Home />} />
          <Route
            path="/dashboard"
            element={
              <PrivateRoute>
                <Dashboard />
              </PrivateRoute>
            }
          />
        </Routes>
