document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('loveForm');
  const messageBox = document.getElementById('responseMessage');

  form.addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
      const response = await fetch('/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      if (!response.ok) throw new Error("Server error");

      const result = await response.json();

      messageBox.innerHTML = `
        Link created! 👉 
        <a href="/love/${result.id}" target="_blank">
          Send this to your crush
        </a>`;
    } catch (err) {
      console.error("JS Error:", err);
      messageBox.innerHTML = "Something went wrong 😢";
    }
  });
});
