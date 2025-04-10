import { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./index.css";

function App() {
  const [prompt, setPrompt] = useState("");
  const [duration, setDuration] = useState(10); // seconds
  const [audioSrc, setAudioSrc] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showPlayer, setShowPlayer] = useState(false);
  const audioRef = useRef(null);
  const [visualizerData, setVisualizerData] = useState(Array(16).fill(20));
  const [savedTracks, setSavedTracks] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {
    if (!showPlayer) return;

    const interval = setInterval(() => {
      setVisualizerData(prev =>
        prev.map(() => Math.max(10, Math.random() * 80 + 10))
      );
    }, 150);

    return () => clearInterval(interval);
  }, [showPlayer]);

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError("Please describe your music.");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // 1. Send prompt & duration to backend
      const response = await axios.post("http://127.0.0.1:8000/generate_music", {
        prompt,
        duration
      });

      console.log("Backend response:", response.data);

      // 2. Download the generated audio
      const musicResponse = await axios.get("http://127.0.0.1:8000/api/download-music", {
        responseType: "blob"
      });

      const url = URL.createObjectURL(new Blob([musicResponse.data]));
      setAudioSrc(url);
      setShowPlayer(true);

      const newTrack = {
        id: Date.now(),
        prompt,
        audioUrl: url,
        date: new Date().toLocaleString()
      };
      setSavedTracks(prev => [newTrack, ...prev]);

    } catch (err) {
      setError("Something went wrong while generating the music.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const closePlayer = () => {
    setShowPlayer(false);
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
    }
  };

  const playSavedTrack = (track) => {
    setAudioSrc(track.audioUrl);
    setPrompt(track.prompt);
    setShowPlayer(true);
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className="music-app">
      <div className="three-d-background"></div>

      <div className="app-container">
        <button className="sidebar-toggle" onClick={toggleSidebar}>
          {sidebarOpen ? '◄' : '►'}
        </button>

        <div className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
          <h3>Your Tracks</h3>
          <div className="saved-tracks">
            {savedTracks.length > 0 ? (
              savedTracks.map(track => (
                <div
                  key={track.id}
                  className="track-item"
                  onClick={() => playSavedTrack(track)}
                >
                  <p className="track-prompt">{track.prompt}</p>
                  <p className="track-date">{track.date}</p>
                </div>
              ))
            ) : (
              <p className="empty-message">Your generated tracks will appear here</p>
            )}
          </div>
        </div>

        <div className="main-content">
          <div className="app-header">
            <h1>Create tracks with AI</h1>
            <p>Background music for any occasion</p>
          </div>

          <div className="generator-panel">
            <div className="input-section">
              <h2>Describe Your Music</h2>
              <textarea
                placeholder="Example: Ambient, soft sounding music I can study to"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                rows="3"
              />
              <button
                onClick={handleGenerate}
                disabled={loading}
                className={loading ? 'loading' : ''}
              >
                {loading ? 'Composing...' : 'Generate Music'}
              </button>
              {error && <p className="error">{error}</p>}
            </div>

            {showPlayer && (
              <div className="player-modal">
                <div className="modal-content">
                  <button className="close-btn" onClick={closePlayer}>×</button>
                  <h3>Your AI Composition</h3>

                  <div className="track-visualizer">
                    {visualizerData.map((height, i) => (
                      <div
                        key={i}
                        className="visualizer-bar"
                        style={{ height: `${height}%` }}
                      />
                    ))}
                  </div>

                  <div className="track-info">
                    <p className="prompt-preview">"{prompt}"</p>
                    <audio ref={audioRef} src={audioSrc} controls />
                    <a
                      href={audioSrc}
                      download="ai_music_composition.wav"
                      className="download-btn"
                    >
                      Download Composition
                    </a>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
