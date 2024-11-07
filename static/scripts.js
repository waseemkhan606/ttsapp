async function convertToSpeech() {
  const text = document.getElementById('text-input').value;
  const lang = document.getElementById('voice-select').value;

  if (!text) {
    alert('Please enter text to convert.');
    return;
  }

  try {
    const response = await fetch('/convert', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ text, lang })
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Error converting text');
    }

    const data = await response.json();
    const audioPlayer = document.getElementById('audio-player');
    audioPlayer.src = data.audio_url;
    audioPlayer.style.display = 'block';
    adjustPlaybackSpeed();
    audioPlayer.play();

    const downloadBtn = document.getElementById('download-btn');
    downloadBtn.style.display = 'block';
    downloadBtn.onclick = () => {
      window.location.href = `/download/${data.audio_url.split('/').pop()}`;
    };
  } catch (error) {
    console.error('Error:', error);
    alert(`Error: ${error.message}`);
  }
}

function adjustPlaybackSpeed() {
  const audioPlayer = document.getElementById('audio-player');
  const speed = document.getElementById('speed-select').value;
  audioPlayer.playbackRate = parseFloat(speed);
}

document.getElementById('speed-select').addEventListener('change', adjustPlaybackSpeed);
