/* GitHub Pages serves static files only, so there is no server to post to.
   The form composes the message and hands it to WhatsApp instead: no third
   party ever sees it, and it lands where messages actually get read. */
(function () {
  var WHATSAPP = '972522057074';        // 052-205-7074 in international form

  var form = document.getElementById('contactForm');
  if (!form) return;
  var hint = document.getElementById('hint');
  var btn = form.querySelector('button');

  function say(msg, bad) {
    hint.textContent = msg;
    hint.style.color = bad ? '#e8736b' : '';
  }
  say('Opens WhatsApp with your message ready to send.');

  var EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    var f = new FormData(form);
    if ((f.get('company') || '').trim()) return;      // honeypot: a bot filled it

    var name = (f.get('name') || '').trim();
    var mail = (f.get('email') || '').trim();
    var subj = (f.get('subject') || '').trim();
    var body = (f.get('message') || '').trim();

    if (!name || !subj || !body) {
      say('Please fill in your name, a subject and a message.', true);
      return;
    }
    if (mail && !EMAIL_RE.test(mail)) {
      say('That email address does not look right.', true);
      return;
    }

    var lines = [
      subj,
      '',
      body,
      '',
      '— ' + name + (mail ? ' (' + mail + ')' : ''),
      'via elyotam.github.io'
    ];
    var url = 'https://wa.me/' + WHATSAPP + '?text=' +
              encodeURIComponent(lines.join('\n'));

    var win = window.open(url, '_blank', 'noopener');
    if (win) {
      say('WhatsApp is opening with your message.');
    } else {
      // Pop-up blocked: navigate in place rather than failing silently.
      say('Opening WhatsApp...');
      location.href = url;
    }
    btn.blur();
  });
})();
