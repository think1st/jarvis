document.addEventListener("DOMContentLoaded", function () {
  const ttsSelect = document.getElementById("tts_engine");
  const voiceDropdown = document.getElementById("voice_id_container");

  function fetchVoices() {
    fetch("/voices")
      .then(res => res.json())
      .then(data => {
        const voiceId = document.getElementById("voice_id");
        voiceId.innerHTML = "";
        data.voices.forEach((voice, index) => {
          const option = document.createElement("option");
          option.value = index;
          option.text = `${voice.name} (${voice.language})`;
          voiceId.appendChild(option);
        });
      });
  }

  if (ttsSelect) {
    ttsSelect.addEventListener("change", () => {
      const engine = ttsSelect.value;
      if (engine === "espeak" || engine === "espeak-ng") {
        voiceDropdown.style.display = "block";
        fetchVoices();
      } else {
        voiceDropdown.style.display = "none";
      }
    });

    // Trigger once on load
    const initial = ttsSelect.value;
    if (initial === "espeak" || initial === "espeak-ng") {
      voiceDropdown.style.display = "block";
      fetchVoices();
    } else {
      voiceDropdown.style.display = "none";
    }
  }

  // Show toast on success messages (optional)
  const toast = document.getElementById("success-toast");
  if (toast) {
    setTimeout(() => {
      toast.style.opacity = 0;
    }, 3000);
  }
});
