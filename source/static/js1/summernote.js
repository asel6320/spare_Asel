document.addEventListener("DOMContentLoaded", () => {
    const editButton = document.getElementById("edit");
    const saveButton = document.getElementById("save");
    const newsContent = document.getElementById("news-content");
    const editUrl = newsContent.dataset.editUrl;

    const edit = () => {
        $('.click2edit').summernote({
            focus: true,
            height: 300,
            lang: 'ru-RU',
            toolbar: [
                ['style', ['bold', 'italic', 'underline', 'clear']],
                ['font', ['strikethrough', 'superscript', 'subscript']],
                ['fontsize', ['fontsize']],
                ['color', ['color']],
                ['para', ['ul', 'ol', 'paragraph']],
                ['table', ['table']],
                ['insert', ['link', 'picture', 'video']],
                ['view', ['fullscreen', 'codeview', 'help']]
            ]
        });
        editButton.style.display = "none";
        saveButton.style.display = "block";
    };

    const save = async () => {
        const markup = $('.click2edit').summernote('code');
        $('.click2edit').summernote('destroy');

        try {
            const response = await fetch( editUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({ full_text: markup })
            });

            const data = await response.json();
            if (response.ok) {
                alert("Сохранено успешно!");
            } else {
                alert(`Ошибка: ${data.message}`);
            }
        } catch (error) {
            alert(`Ошибка сети: ${error}`);
        }

        editButton.style.display = "block";
        saveButton.style.display = "none";
    };

    editButton.addEventListener("click", edit);
    saveButton.addEventListener("click", save);
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrfToken = document.getElementById("csrf_token").value;

