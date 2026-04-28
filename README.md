# 🚀 Personal Tracker Pro

An elegant, mobile-friendly tracking application built with **FastAPI**, **PostgreSQL**, and **SortableJS**. Track items, increment usage with precise timestamps, and organize your lists with drag-and-drop functionality.

## ✨ Features

* **Elegant UI:** Clean, minimalist design using Tailwind CSS.
* **Dynamic Lists:** Create, view, and delete multiple tracking lists.
* **Precise Data:** Every "+" click saves a high-precision timestamp in PostgreSQL for future behavioral analysis.
* **Drag & Drop:** Reorder your tracking items effortlessly.
* **Dockerized:** One-command setup for database and API.
* **Cloud Ready:** Easily shareable via Ngrok or Cloudflare Tunnels.

## 🛠️ Tech Stack

- **Backend:** Python / FastAPI
- **Database:** PostgreSQL
- **Frontend:** JavaScript / Tailwind CSS / SortableJS
- **Orchestration:** Docker Compose

## 🚀 Getting Started

### 1. Prerequisites
- Docker and Docker Compose installed.
- (Optional) Ngrok for sharing.

### 2. Installation
Clone this repository and navigate to the project folder:
```bash
docker-compose up --build