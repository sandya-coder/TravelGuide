const API_URL = "http://127.0.0.1:5000/generate-audio-guide";

const form = document.getElementById("guide-form");
const generateButton = document.getElementById("generate-btn");
const statusElement = document.getElementById("status");
const descriptionElement = document.getElementById("description");
const audioPlayer = document.getElementById("audio-player");
const audioControls = document.getElementById("audio-controls");

const playButton = document.getElementById("play-audio");
const pauseButton = document.getElementById("pause-audio");
const downloadButton = document.getElementById("download-audio");

const languageElement = document.getElementById("language");
const localeElement = document.getElementById("locale");
const voiceIdElement = document.getElementById("voiceId");

let currentAudioUrl = null;

// Suggest a matching locale when the language changes.
const suggestedLocales = {
  English: "en-US",
  Hindi: "hi-IN",
  Tamil: "ta-IN",
  Telugu: "te-IN"
};

languageElement.addEventListener("change", () => {
  localeElement.value = suggestedLocales[languageElement.value];
});

// Release the previous generated audio URL.
function clearPreviousAudio() {
  audioPlayer.pause();
  audioPlayer.removeAttribute("src");
  audioPlayer.load();

  if (currentAudioUrl) {
    URL.revokeObjectURL(currentAudioUrl);
    currentAudioUrl = null;
  }

  audioControls.hidden = true;
}

// Convert Base64 audio returned by the backend into an MP3 Blob.
function createAudioUrl(base64Audio, mimeType) {
  const binaryString = atob(base64Audio);
  const bytes = new Uint8Array(binaryString.length);

  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }

  const audioBlob = new Blob([bytes], {
    type: mimeType || "audio/mpeg"
  });

  return URL.createObjectURL(audioBlob);
}

// Generate a travel guide.
form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const place = document.getElementById("place").value.trim();
  const answerType = document.getElementById("answerType").value;
  const language = languageElement.value;
  const voiceId = voiceIdElement.value.trim();
  const locale = localeElement.value;

  if (!place || !voiceId) {
    statusElement.textContent =
      "Please enter a destination and a valid Murf voice ID.";
    return;
  }

  generateButton.disabled = true;
  generateButton.textContent = "Generating your travel story...";

  statusElement.textContent =
    "Generating your travel description and audio. Please wait.";

  clearPreviousAudio();

  descriptionElement.textContent = "Creating your travel story...";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        place,
        answerType,
        language,
        voiceId,
        locale
      })
    });

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.error || "Could not generate the guide.");
    }

    if (!result.description || !result.audioBase64) {
      throw new Error("The server did not return the description or audio.");
    }

    // Show the generated travel description.
    descriptionElement.textContent = result.description;

    // Convert returned Base64 audio into a playable MP3.
    currentAudioUrl = createAudioUrl(
      result.audioBase64,
      result.audioMimeType || "audio/mpeg"
    );

    audioPlayer.src = currentAudioUrl;
    audioPlayer.load();

    audioControls.hidden = false;

    statusElement.textContent =
      "Your travel guide is ready! Press Play to listen or download the MP3.";

  } catch (error) {
    descriptionElement.textContent =
      "Your travel story will appear here after successful generation.";

    statusElement.textContent =
      error.message || "Something went wrong. Please try again.";

    clearPreviousAudio();
  } finally {
    generateButton.disabled = false;
    generateButton.textContent = "✨ Generate my audio guide";
  }
});

// Play audio.
playButton.addEventListener("click", async () => {
  if (!audioPlayer.src) {
    statusElement.textContent = "Generate a travel guide first.";
    return;
  }

  try {
    await audioPlayer.play();
    statusElement.textContent = "Playing your travel guide.";
  } catch (error) {
    statusElement.textContent =
      "Unable to play the audio. Please try again.";
  }
});

// Pause audio.
pauseButton.addEventListener("click", () => {
  if (!audioPlayer.src) {
    statusElement.textContent = "Generate a travel guide first.";
    return;
  }

  audioPlayer.pause();
  statusElement.textContent = "Audio paused.";
});

// Download the generated MP3.
downloadButton.addEventListener("click", () => {
  if (!currentAudioUrl) {
    statusElement.textContent = "Generate a travel guide first.";
    return;
  }

  const link = document.createElement("a");
  link.href = currentAudioUrl;
  link.download = "travel-guide.mp3";

  document.body.appendChild(link);
  link.click();
  link.remove();

  statusElement.textContent = "Your MP3 download has started.";
});

// Release the generated URL when leaving the page.
window.addEventListener("beforeunload", () => {
  if (currentAudioUrl) {
    URL.revokeObjectURL(currentAudioUrl);
  }
});