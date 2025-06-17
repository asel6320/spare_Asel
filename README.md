<img width="1426" alt="Снимок экрана 2025-06-17 в 3 20 39 AM" src="https://github.com/user-attachments/assets/ad0fa8a0-83b0-41e0-b3b8-2d6d81250fd7" /># 🛠 Spare_Asel – Django E-commerce Backend Platform

A **backend-focused**, multilingual vehicle parts platform built with Django and PostgreSQL. Includes a secure CRM system, admin analytics panel, dynamic cart & like systems, and multi-language support for users in Central Asia.

🌐 **Live Site:** [https://spare-asel-8.onrender.com](https://spare-asel-8.onrender.com)

---

![Django](https://img.shields.io/badge/Django-4.x-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%3E%3D13-blue)
![Docker](https://img.shields.io/badge/Docker-enabled-blue)
![Render](https://img.shields.io/badge/Deployed%20on-Render-success)
![i18n](https://img.shields.io/badge/Languages-RU%2C%20EN%2C%20KO-yellow)

---

## 📌 Key Features (Backend-Centered)

- 🔐 **Authentication & Authorization**  
  Only logged-in users can like products, post comments, and manage their cart.

- 🛒 **Dynamic Cart System**  
  Quantity and total prices update automatically using JavaScript + Django sessions.

- ❤️ **Like System**  
  Asynchronous like/unlike using JavaScript (no page reload).

- 💬 **Comment System**  
  Logged-in users can leave reviews under each part.

- 🌍 **Multilingual Support**  
  Interface available in Russian 🇷🇺, English 🇺🇸, and Korean 🇰🇷 (some translations in progress).

- 🧑‍💼 **CRM + Admin Panel**  
  Accessible only by superusers:
  - Manage orders, products, users
  - View analytics on sales and user activity

---

## 👤 Demo Credentials

### 🧑 Regular User (can like, comment, use cart)
- **Email:** `kkkk@gmail.com`  
- **Password:** `Askatai77!`

### 👑 Superuser (CRM + Admin Panel access)
- **Email:** `admin@gmail.com`  
- **Password:** `admin`  
- Access:  
  - CRM Dashboard → `/crm/`  
  - Admin Panel → `/admin/`

---

## 📸 Screenshots

> ⚠ Upload your images to `/screenshots/` and update these links accordingly.

### 🔐 Admin Login
<img width="1415" alt="Снимок экрана 2025-06-17 в 3 18 08 AM" src="https://github.com/user-attachments/assets/1cb4f106-0121-48dc-9b71-79d806071524" />


### 📊 CRM Dashboard
<img width="1437" alt="Снимок экрана 2025-06-17 в 3 18 44 AM" src="https://github.com/user-attachments/assets/02c53649-0d83-4bc5-8bc7-3e6dda2bda3f" />


### 🛒 Product Page with Like & Cart
<img width="1426" alt="Снимок экрана 2025-06-17 в 3 20 39 AM" src="https://github.com/user-attachments/assets/c100aa5f-4a97-4213-a8c9-a46f760660d7" />


### 🌐 Language Switching
<img width="1423" alt="Снимок экрана 2025-06-17 в 3 21 24 AM" src="https://github.com/user-attachments/assets/4219b446-676c-4dd6-8e9d-c755c6626867" />


---

## ⚙ Tech Stack

| Layer         | Technology                       |
|---------------|----------------------------------|
| Backend       | Django, Django REST Framework    |
| Database      | PostgreSQL                       |
| Deployment    | Docker, Render                   |
| Frontend      | HTML, CSS, JavaScript (Vanilla)  |
| Admin Tools   | Django Admin + Custom CRM        |
| Localization  | Django i18n (3 languages)        |

---

## 🗂 Project Structure

```
spare_Asel/
├── parts/         # Product logic, filters, cart, likes & comments
├── crm/           # CRM dashboard for admins
├── users/         # Authentication logic
├── static/        # CSS, JS, images
├── templates/     # HTML (multilingual)
├── locale/        # Translation files
├── Dockerfile
└── requirements.txt
```

---

## 🚀 Getting Started Locally

### 1. Clone the repo
```bash
git clone https://github.com/asel6320/spare_Asel.git
cd spare_Asel
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `.env` file (example)
```env
SECRET_KEY=your_secret
DEBUG=True
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
```

### 5. Migrate and run
```bash
python manage.py migrate
python manage.py runserver
```

Or using Docker:
```bash
docker build -t spare_asel .
docker run -p 8000:8000 spare_asel
```

---

## 🛠 Admin Access on Render

If you cannot access the Render shell, create a superuser like this:

### Option: Auto-create via code (in `urls.py` temporarily)
```python
from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin12345')
```

Then visit `/admin/`, log in, and **delete this code immediately for security.**

---

## ⚠ Known Limitations

- 🖥 **Desktop-Only UI**: Mobile responsiveness under development  
- 🌐 **Translation Bugs**: Some language strings missing or inconsistent  
- 🔐 **Admin/CRM Access**: Only visible to superusers


---

> ✅ This project showcases complete backend architecture: authentication, business logic, multilingual support, admin analytics, and real deployment — built from scratch and production-ready.



