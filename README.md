# ⚡️ Swift Reply AI

> AI Conversations, Reimagined.**
> A production-ready, highly polished AI customer support platform built for modern startups and SMEs.

![Swift Reply](https://img.shields.io/badge/Status-Active-success) ![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B) ![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange)

Swift Reply is an intelligent, autonomous business assistant capable of understanding customer inquiries, handling FAQs, explaining services, and automatically capturing lead information (Name, Email, Phone) directly within a beautiful, glassmorphic chat interface.

---

## ✨ Features

- **🧠 Advanced AI Engine:** Powered by the cutting-edge Google `gemini-flash-latest` model for ultra-fast, intelligent, and context-aware responses.
- **🎨 Luxury UI/UX:** Built with custom CSS to bypass standard Streamlit limitations. Features glassmorphism, floating ambient orbs, and neon gradient styling to simulate a billion-dollar SaaS aesthetic.
- **🎯 Dynamic Context Injection:** The AI adapts its entire persona instantly based on the Business Name, Industry, and FAQs you provide in the sidebar.
- **📈 Automated Lead Generation:** Uses NLP keyword detection to naturally interrupt the chat flow and capture customer contact details when they express purchasing intent.
- **💾 Local Database Logging:** All leads are securely saved to a local, serverless SQLite database.
- **📊 Admin Dashboard:** Features a togglable view to display all captured leads in a clean Pandas dataframe.

---

## 🛠️ Technology Stack

- **Frontend:** Streamlit, Vanilla CSS3, HTML5
- **Backend Language:** Python 3.10+
- **AI Integration:** Google GenAI SDK (`google-genai`)
- **Database:** SQLite (`sqlite3`)
- **Data Visualization:** Pandas

---

## 🚀 Quickstart Guide (Run Locally)

Follow these steps to run Swift Reply on your local machine.

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/SwiftReply.git
cd SwiftReply
