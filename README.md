Project Structure

        local-gemma-chat-sql/
        ├─ src/
        │  ├─ index.ts        # Express entry point
        │  ├─ chat.ts         # Chatbot logic
        │  ├─ db.ts           # SQL connection
        │  └─ entity/
        │       └─ Chat.ts    # Chat entity
        ├─ package.json
        ├─ tsconfig.json
        └─ .env               # MYSQL credentials

Step 1: Install Dependencies

        npm init -y
        npm install express cors dotenv typeorm mysql2 reflect-metadata @langchain/community langchain
        npm install --save-dev @types/express ts-node typescript

Step 2: Environment Variables – .env

        DB_HOST=localhost
        DB_PORT=3306
        DB_USER=root
        DB_PASSWORD=yourpassword
        DB_NAME=gemma_chat
        
        Step 3: Database Connection – src/db.ts
        import { DataSource } from "typeorm";
        import dotenv from "dotenv";
        import { Chat } from "./entity/Chat";
        
        dotenv.config();
        
        export const AppDataSource = new DataSource({
          type: "mysql",
          host: process.env.DB_HOST,
          port: parseInt(process.env.DB_PORT || "3306"),
          username: process.env.DB_USER,
          password: process.env.DB_PASSWORD,
          database: process.env.DB_NAME,
          entities: [Chat],
          synchronize: true, // Auto create table
          logging: false,
        });
        
        export async function connectDB() {
          await AppDataSource.initialize();
          console.log("MySQL connected");
        }

Step 4: Chat Entity – src/entity/Chat.ts

        import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from "typeorm";
        
        @Entity()
        export class Chat {
          @PrimaryGeneratedColumn()
          id!: number;
        
          @Column()
          userId!: string;
        
          @Column({ type: "enum", enum: ["user", "bot"] })
          role!: "user" | "bot";
        
          @Column("text")
          message!: string;
        
          @CreateDateColumn()
          createdAt!: Date;
        }

Step 5: Chatbot Logic – src/chat.ts

        import { Ollama } from "@langchain/community/llms/ollama";
        import { ConversationChain } from "langchain/chains";
        import { BufferMemory } from "langchain/memory";
        import { AppDataSource } from "./db";
        import { Chat } from "./entity/Chat";
        
        const model = new Ollama({ model: "gemma3:4b" });
        
        // Map to store per-user conversation chains
        const userChains: Record<string, ConversationChain> = {};
        
        async function loadUserMemory(userId: string) {
          const messages = await AppDataSource.getRepository(Chat).find({
            where: { userId },
            order: { createdAt: "ASC" },
          });
        
          return messages.map((m) => ({
            role: m.role === "user" ? "human" : "ai",
            content: m.message,
          }));
        }
        
        export async function getUserChatbot(userId: string) {
          if (!userChains[userId]) {
            const memory = new BufferMemory({ returnMessages: true });
            const pastMessages = await loadUserMemory(userId);
            memory.chatHistory = pastMessages;
        
            userChains[userId] = new ConversationChain({ llm: model, memory });
          }
          return userChains[userId];
        }
        
        export async function getResponse(userId: string, message: string) {
          const chatbot = await getUserChatbot(userId);
          const res = await chatbot.call({ input: message });
        
          // Save user and bot messages to SQL
          const repo = AppDataSource.getRepository(Chat);
          await repo.save({ userId, role: "user", message });
          await repo.save({ userId, role: "bot", message: res.response });
        
          return res.response;
        }

Step 6: Express Server – src/index.ts

        import express from "express";
        import cors from "cors";
        import dotenv from "dotenv";
        import { connectDB } from "./db";
        import { getResponse } from "./chat";
        
        dotenv.config();
        const app = express();
        app.use(cors());
        app.use(express.json());
        
        const PORT = 4000;
        
        // Connect to MySQL
        connectDB();
        
        // Health check
        app.get("/", (req, res) => res.send("Gemma 3 Chatbot Server with SQL is running!"));
        
        // Chat endpoint
        app.post("/chat", async (req, res) => {
          try {
            const { userId, message } = req.body;
            if (!userId || !message)
              return res.status(400).json({ error: "userId and message are required" });
        
            const response = await getResponse(userId, message);
            res.json({ response });
          } catch (error: any) {
            console.error(error);
            res.status(500).json({ error: "Something went wrong" });
          }
        });
        
        app.listen(PORT, () => {
          console.log(`Server running on http://localhost:${PORT}`);
        });

Step 7: Run the Server

        npx ts-node src/index.ts
