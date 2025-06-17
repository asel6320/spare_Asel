# 🛠 Spare_Asel – Django E-commerce Backend Platform

A **backend-focused**, multilingual vehicle parts platform built with Django and PostgreSQL. The project includes a secure CRM system, admin analytics panel, dynamic cart and like systems, and multilingual support for users across Central Asia.

🚀 **Live Site:** [https://spare-asel-8.onrender.com](https://spare-asel-8.onrender.com)

---

![Django](https://img.shields.io/badge/Django-4.x-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%3E%3D13-blue)
![Docker](https://img.shields.io/badge/Docker-enabled-blue)
![Render](https://img.shields.io/badge/Deployed%20on-Render-success)
![i18n](https://img.shields.io/badge/Languages-RU%2C%20EN%2C%20KO-yellow)

---

## 📌 Highlights

### ✅ Backend-Centered Features
- 🔐 **Authenticated Routes**: Only logged-in users can like, comment, or add to cart
- ❤️ **AJAX-Based Likes**: Like/unlike products with no page reload
- 🛒 **Dynamic Cart System**: Automatically updates quantity & total price
- 💬 **Comments System**: Authenticated users can comment on parts
- 🌍 **i18n Multilingual Support**: Russian 🇷🇺, English 🇺🇸, Korean 🇰🇷
- 🧑‍💼 **Admin CRM Dashboard**: Order, user, and product management + visual analytics
- ⚙️ **Deployed via Docker on Render**

---

## 👤 Regular User Demo

🔗 [Login Page](https://spare-asel-8.onrender.com/login/)  
Credentials:
- **Email:** `kkkk@gmail.com`  
- **Password:** `Askatai77!`

You can:
- Like products
- Add items to the cart
- See automatic price & quantity updates
- Switch between languages
- Leave product reviews/comments

---

⚙ Tech Stack
Layer	Technology
Backend	Django, Django REST Framework
Database	PostgreSQL
Deployment	Docker, Render
Frontend	HTML, CSS, JavaScript (vanilla)
Admin Tools	Django Admin + Custom CRM
Localization	Django i18n (3 languages)

🗂 Project Structure
bash
Copy
Edit
spare_Asel/
├── parts/         # Product logic, filters, cart, likes
├── crm/           # CRM dashboard for superusers
├── users/         # User registration and login
├── static/        # CSS, JS, images
├── templates/     # HTML templates (multi-language)
├── locale/        # Translation files
├── Dockerfile
└── requirements.txt

1. Clone the repo

git clone https://github.com/asel6320/spare_Asel.git
cd spare_Asel

2. Install dependencies

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. Configure .env

SECRET_KEY=your_secret
DEBUG=True
DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost

4. Run migrations and start

python manage.py migrate
python manage.py runserver

Or use Docker:

docker build -t spare_asel .
docker run -p 8000:8000 spare_asel

⚠ Known Limitations
🖥 Responsive Design: Optimized for desktop; mobile support under development
🌐 Translation Issues: Some i18n text errors are being resolved
🔐 Admin & CRM Access: Must create superuser (instructions above)



