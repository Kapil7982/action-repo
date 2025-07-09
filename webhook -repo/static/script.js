function formatEvent(event) {
    const { event_type, author, from_branch, to_branch, timestamp } = event;
    const date = new Date(timestamp).toUTCString();
  
    if (event_type === "push") {
      return `${author} pushed to ${to_branch} on ${date}`;
    }
    if (event_type === "pull_request") {
      return `${author} submitted a pull request from ${from_branch} to ${to_branch} on ${date}`;
    }
    if (event_type === "merge") {
      return `${author} merged branch ${from_branch} to ${to_branch} on ${date}`;
    }
    return "";
  }
  
  function fetchEvents() {
    fetch('/events')
      .then(res => res.json())
      .then(data => {
        const container = document.getElementById("events");
        container.innerHTML = '';
        data.forEach(event => {
          const div = document.createElement("div");
          div.className = "event";
          div.innerText = formatEvent(event);
          container.appendChild(div);
        });
      });
  }
  
  setInterval(fetchEvents, 15000);
  window.onload = fetchEvents;
  