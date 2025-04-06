# 🎼 Text-to-Music Generation App  
Generate unique music tracks from text prompts using AI — powered by **MusicGen**, with a clean **React frontend** and a fast, scalable **FastAPI backend**.

---

## 🚀 Project Overview

This project lets users **input a text prompt** and receive a **generated music clip** in seconds.

Built for both creativity and scalability, this full-stack app bridges **natural language processing** and **music generation** using modern tools and clean design.

---

## ✨ Features

- 🎤 Prompt-to-Music Generation via Meta’s **MusicGen**
- ⚡ Fast, async backend with **FastAPI**
- 🎧 Instant download of generated `.wav` files
- 🖼️ Sleek and responsive **React frontend**
- 🔁 Simple, repeatable prompt flow

---

## ⚙️ How It Works (Architecture)

```
User Input (Text Prompt)
      ↓
React Frontend (Input Form → Fetch)
      ↓
FastAPI Backend (Receives prompt, runs MusicGen)
      ↓
Music Generation via Audiocraft (Hugging Face / Local inference)
      ↓
Returns Audio → Allows Download in Frontend
```



---

## 🛠️ Installation

### 🔹 Backend Setup (FastAPI + MusicGen)

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

2. Install required packages:

```bash
pip install fastapi uvicorn torchaudio transformers
```

3. Run the backend server:

```bash
uvicorn app:app --reload
```

---

### 🔹 Frontend Setup (React)

1. Navigate to the `frontend` folder:

```bash
cd frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the React dev server:

```bash
npm start
```

---

## ▶️ Usage

- Enter a descriptive text prompt.
- Click “Generate Music”.
- Wait for the backend to process your request and return the audio.
- Download the `.wav` result!

---

## 💡 Examples of Prompts

- “Upbeat jazz with saxophone and soft piano”
- “Epic orchestral music for a movie trailer”
- “Rainy lofi background beat with guitar”

---

## 🤝 Credits & License

- 🎶 MusicGen by Meta (via [Audiocraft](https://github.com/facebookresearch/audiocraft))  
- 💻 React, FastAPI  
- 🛠️ Built by **Khushi Patil**  
- 📄 [MIT License](./LICENSE)

---

