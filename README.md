# 🎬 Video-to-Audio Application

A distributed microservices-based system where users can upload videos that are converted into audio files asynchronously.  
The app supports user authentication, background processing via message queues, and email notifications once conversion is complete.

---

## 🧠 System Overview

**Flow Summary:**

1. 🧍‍♂️ User registers or logs in via the **Auth Service**.
2. 💻 The **Frontend (React)** allows the user to upload a video file.
3. 🚪 The **Gateway Service** receives the upload request and stores the file in **MongoDB**.
4. 📬 The gateway sends a **message to RabbitMQ** to notify the **Converter Service**.
5. 🎧 The **Converter Service** converts the video to audio (e.g., MP3).
6. 📢 After conversion, another **message is sent to RabbitMQ**, triggering the **Email Service**.
7. ✉️ The **Email Service** sends a “Conversion Complete” notification to the user.
8. ⬇️ The user can download the converted audio file from the app.

---

## 🧩 Technology Stack

### ⚙️ Infrastructure

- **[Nginx](https://nginx.org/):** Reverse proxy that routes traffic between frontend and backend services.
- **[Docker Compose](https://www.docker.com):** Manages and orchestrates all microservices in containers.

### 🐍 Backend Services

#### 🔑 Auth Service (FastAPI)

- Handles **user registration, login**, and **JWT authentication**.
- Uses **PostgreSQL** for user data storage.
- Implements **SQLModel** for ORM and **Pydantic** for data validation.

#### 🚪 Gateway Service (FastAPI)

- Central API entry point for the frontend.
- Handles **video uploads** and stores them in **MongoDB**.
- Publishes messages to **RabbitMQ** for background processing.

#### 🎧 Converter Service (Python)

- Listens to **RabbitMQ** for conversion jobs.
- Fetches videos from MongoDB and converts them to MP3 using `moviepy` or `ffmpeg`.
- Publishes success messages back to RabbitMQ for notification.

#### ✉️ Email Service (Node)

- Listens to **RabbitMQ** for conversion completion messages.
- Sends **email notifications** via **Nodemailer**.

### 💾 Databases & Message Broker

- 🐘 **PostgreSQL:** Stores user credentials and authentication data.
- 🍃 **MongoDB:** Stores uploaded videos and converted audio files.
- 🐇 **RabbitMQ:** Handles asynchronous communication between microservices.

### 💻 Frontend

- **[React](https://react.dev):**
  - Clean UI for registration, login, upload, and download.
  - Communicates with backend services via **Nginx Gateway (http://localhost:8080)**.

## 🚀 Features

- 🔐 **JWT Authentication** and secure password hashing
- 🎥 **Video upload** and **audio conversion** pipeline
- 📨 Automatic **email notification** after conversion
- 💬 **Asynchronous communication** via RabbitMQ
- 🐳 **Fully containerized** using Docker Compose
- ⚙️ **Scalable architecture** – independent, modular microservices

---

## 🧭 Architecture Diagram

[![Diagram](docs/App_lifecycle.png.png)]

---

## 🏁 Quick Start

```bash
# 1️⃣ Clone the repository
git clone https://github.com/Sanjog-Pariyar/video-mp3-converter.git
cd video-mp3-converter

# 3️⃣ Run all services
docker compose up --build

# 4️⃣ Open in browser
http://localhost:8080
```
