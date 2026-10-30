const extractButton = document.getElementById("extract-page");
const pageStatus = document.getElementById("page-status");
const errorMessage = document.getElementById("error-message");
const askButton = document.getElementById("ask-ai");
const questionInput = document.getElementById("question");
const answerElement = document.getElementById("answer");

let pageContent = "";


extractButton.addEventListener("click", async () => {
  errorMessage.hidden = true;
  askButton.disabled = true;
  extractButton.disabled = true;
  pageStatus.textContent = "Reading webpage...";

  try {
    const [tab] = await chrome.tabs.query({
      active: true,
      currentWindow: true,
    });

    if (!tab?.id) {
      throw new Error("No active tab found.");
    }

    const results = await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: () => document.body?.innerText ?? "",
    });

    const extractedText = (results[0]?.result ?? "").trim();

    if (!extractedText) {
      throw new Error("No readable webpage text found.");
    }

    const maxCharacters = 12000;
    pageContent = extractedText.slice(0, maxCharacters);

    const wasTruncated = extractedText.length > maxCharacters;

    pageStatus.textContent = wasTruncated
      ? `Page content extracted (${maxCharacters.toLocaleString()} characters; truncated).`
      : `Page content extracted (${pageContent.length.toLocaleString()} characters).`;

  
    askButton.disabled = false;
  } catch (error) {
    pageContent = "";
    pageStatus.textContent = "Could not extract webpage content.";
    errorMessage.textContent = "Open a regular webpage and try again.";
    errorMessage.hidden = false;

    console.error("Page extraction failed:", error);
  } finally {
    extractButton.disabled = false;
  }
});


askButton.addEventListener("click", async () => {
  const question = questionInput.value.trim();

  if (!pageContent || !question) {
    errorMessage.textContent = "Read a webpage and enter a question first.";
    errorMessage.hidden = false;
    return;
  }

  askButton.disabled = true;
  errorMessage.hidden = true;
  answerElement.textContent = "Thinking...";

  try {
    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: question,
        page_content: pageContent,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || `Request failed (${response.status}).`);
    }

    answerElement.textContent = data.answer;
  } catch (error) {
    answerElement.textContent = "Unable to generate an answer.";
    errorMessage.textContent =
      "Check that the backend is running and try again.";
    errorMessage.hidden = false;

    console.error("AI request failed:", error);
  } finally {
    askButton.disabled = false;
  }
});
function updateAskButton() {
  askButton.disabled = !pageContent || !questionInput.value.trim();
}


questionInput.addEventListener("input", updateAskButton);

document.querySelectorAll("[data-prompt]").forEach((button) => {
  button.addEventListener("click", () => {
    questionInput.value = button.dataset.prompt;

    updateAskButton();
    questionInput.focus();
  });
});
