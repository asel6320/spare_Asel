function shareProduct(productUrl) {
        const modifiedUrl = productUrl.replace("127.0.0.1", "localhost");

        navigator.clipboard.writeText(modifiedUrl)
            .then(() => {
                const notification = document.getElementById("copy-notification");
                notification.classList.remove("d-none");
                setTimeout(() => notification.classList.add("d-none"), 2000);
            })
            .catch(err => {
                console.error("Ошибка копирования ссылки:", err);
            });
    }