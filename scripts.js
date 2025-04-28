async function playSong(songTitle) {
    const response = await fetch('/play', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ song: songTitle })
    });
    const data = await response.json();
    const audio = new Audio(data.audio_url);
    audio.play();
}
