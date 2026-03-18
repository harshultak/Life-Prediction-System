document.getElementById("chatForm").onsubmit = async function (e) {
    e.preventDefault();

    const formData = new FormData(this);

    const res = await fetch("/chatbot/chat", {
        method: "POST",
        body: formData
    });

    const data = await res.json();
    document.getElementById("response").innerText = data.reply;
};
