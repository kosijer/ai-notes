document.addEventListener("DOMContentLoaded", function () {
  const summaryElement = document.getElementById("summary");
  const sentimentElement = document.getElementById("sentiment-status");
  const categoryInput = document.getElementById("category");
  const titleInput = document.querySelector('input[name="title"]');
  const contentInput = document.getElementById("content");
  const buttons = document.querySelectorAll(".button-container button");

  function updateSentimentStyle(sentiment) {
    sentimentElement.className = "sentiment"; // Reset class

    switch (sentiment) {
      case "positive":
        sentimentElement.classList.add("positive");
        break;
      case "negative":
        sentimentElement.classList.add("negative");
        break;
      case "neutral":
        sentimentElement.classList.add("neutral");
        break;
      default:
        sentimentElement.classList.add("unknown");
    }
  }

  function resetSearch() {
    document.querySelector('input[name="query"]').value = "";
    document.getElementById("search-form").submit();
  }

  function toggleButtonState() {
    const title = titleInput.value.trim();
    const content = contentInput.value.trim();
    const category = categoryInput.value.trim();

    buttons.forEach((button) => {
      button.disabled = !(title && content && category);
    });
  }

  async function categorizeNote() {
    const content = contentInput.value.trim();
    if (content.length > 5) {
      const response = await fetch("/categorize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content }),
      });
      const data = await response.json();
      categoryInput.value = data.category;
      toggleButtonState(); // Call after updating the category
    }
  }

  async function summarizeNote() {
    const content = contentInput.value;

    // Display loading text
    summaryElement.innerText = "Loading...";

    try {
      const response = await fetch("/summarize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content }),
      });

      const data = await response.json();

      // Clear the loading text and append the summary
      summaryElement.innerHTML = ""; // Clear existing content
      const spanElement = document.createElement("span");
      spanElement.innerText = data.summary;
      summaryElement.appendChild(spanElement);

      // Update hidden input with the summary
      document.querySelector('input[name="summary"]').value = data.summary;
    } catch (error) {
      // Handle errors and update the UI accordingly
      summaryElement.innerText = "Error fetching summary.";
      console.error("Error fetching summary:", error);
    }
  }

  async function analyzeSentiment() {
    const content = contentInput.value;

    // Set loading status
    sentimentElement.innerText = "Loading...";

    try {
      const response = await fetch("/sentiment", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content }),
      });

      const data = await response.json();
      if (response.ok) {
        sentimentElement.innerText = data.sentiment;
        updateSentimentStyle(data.sentiment.toLowerCase());
        document.querySelector('input[name="sentiment"]').value =
          data.sentiment;
      } else {
        sentimentElement.innerText = "Error: Unable to determine sentiment.";
      }
    } catch (error) {
      sentimentElement.innerText = "Error: Unable to connect to server.";
    }
  }

  // Expose functions to the global scope for inline HTML usage
  window.summarizeNote = summarizeNote;
  window.analyzeSentiment = analyzeSentiment;
  window.categorizeNote = categorizeNote;
  window.resetSearch = resetSearch;

  // Attach event listeners to input fields
  titleInput.addEventListener("input", toggleButtonState);
  contentInput.addEventListener("input", toggleButtonState);
  categoryInput.addEventListener("input", toggleButtonState);

  // Initial check on page load
  toggleButtonState();
});
