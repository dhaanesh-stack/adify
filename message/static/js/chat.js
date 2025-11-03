  const form = document.getElementById('message-form');
  const chatBox = document.getElementById('chat-box');
  const input = document.getElementById('message-input');
  const noMsg = document.getElementById('no-messages');
  const msgTemplate = document.getElementById('message-template');

  chatBox.scrollTop = chatBox.scrollHeight;

  if (noMsg && chatBox.children.length > 0) {
    noMsg.style.display = 'none';
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const content = input.value.trim();
    if (!content) return;

    const response = await fetch('', {
      method: 'POST',
      headers: {
        'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
        'X-Requested-With': 'XMLHttpRequest',
      },
      body: new URLSearchParams({ 'content': content })
    });

    if (response.ok) {
      const data = await response.json();

      if (noMsg && noMsg.style.display !== 'none') {
        noMsg.style.display = 'none';
      }

      const msgClone = msgTemplate.content.cloneNode(true);
      msgClone.querySelector('.message-text').textContent = data.content;
      msgClone.querySelector('.meta-text').textContent = `You • ${data.timestamp}`;

      chatBox.appendChild(msgClone);
      chatBox.scrollTop = chatBox.scrollHeight;
      input.value = '';
      input.focus();
    }
  });