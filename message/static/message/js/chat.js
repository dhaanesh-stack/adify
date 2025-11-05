document.addEventListener('alpine:init', () => {
  Alpine.data('chatComponent', () => ({
    content: '',
    csrf: document.querySelector('[name=csrfmiddlewaretoken]').value,
    lastMessageId: null,
    
    createMessageElement(msg, isOwn = false) {
      const template = document.getElementById('message-template');
      const clone = template.content.cloneNode(true);
      const bubble = clone.querySelector('.message-bubble');
      const wrapper = clone.querySelector('.flex');

      clone.querySelector('.message-text').textContent = msg.content;
      clone.querySelector('.meta-text').textContent = `${isOwn ? 'You' : msg.sender_name} • ${msg.timestamp}`;
      bubble.dataset.id = msg.id;

      if (!isOwn && msg.sender_name !== 'You') {
        wrapper.classList.remove('justify-end');
        wrapper.classList.add('justify-start');
        bubble.classList.remove('bg-indigo-500', 'text-white', 'rounded-tr-none');
        bubble.classList.add('bg-gray-300', 'rounded-tl-none');
      }

      return clone;
    },

    async sendMessage() {
      if (!this.content.trim()) return;

      const response = await fetch('', {
        method: 'POST',
        headers: {
          'X-CSRFToken': this.csrf,
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: new URLSearchParams({ content: this.content })
      });

      if (response.ok) {
        const data = await response.json();
        const clone = this.createMessageElement(data, true);

        this.$refs.chatBox.appendChild(clone);
        this.$refs.chatBox.scrollTop = this.$refs.chatBox.scrollHeight;
        this.content = '';
        this.lastMessageId = data.id;
      }
    },

    async fetchNewMessages() {
      try {
        const url = `${window.location.pathname}?poll=1&last_id=${this.lastMessageId || ''}`;
        const res = await fetch(url, {
          headers: { 'X-Requested-With': 'XMLHttpRequest' },
        });

        if (!res.ok) return;
        const data = await res.json();
        if (data.length === 0) return;

        data.forEach(msg => {
          const clone = this.createMessageElement(msg);
          this.$refs.chatBox.appendChild(clone);
        });


        this.lastMessageId = data[data.length - 1].id;
        this.$refs.chatBox.scrollTop = this.$refs.chatBox.scrollHeight;
      } catch (err) {
        console.error('Polling error:', err);
      }
    },

    initChat() {
      const chatBox = this.$refs.chatBox;
      chatBox.scrollTop = chatBox.scrollHeight;

      const noMsg = document.getElementById('no-messages');
      if (noMsg && chatBox.children.length > 0) {
        noMsg.style.display = 'none';
      }

      this.lastMessageId = chatBox.querySelector('.message-bubble:last-child')?.dataset.id || null;

      const poll = () => { 
        this.fetchNewMessages().finally(() => {
          setTimeout(poll, 3000); 
        }); 
      }; 
      poll();
    }
  }));
});
