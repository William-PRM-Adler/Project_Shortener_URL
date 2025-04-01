import { useState } from "react";
import "../styles/project_shortener_frontend.css";

export default function URL_Shortener() {
    const [LongURL, SetLongURL] = useState("");
    const [ShortURL, SetShortURL] = useState([]);

    const ShortenURL = async () => {
        if (!LongURL.trim()) return;
        const response = await fetch("http://127.0.0.1:8000/shorten_url", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ old_long_url: LongURL }),
        });
        if (response.ok) {
            const data = await response.json();
            SetShortURL([...ShortURL, data]);
            SetLongURL("");
        }
    };

    const DeleteURL = async (shortCode) => {
        const response = await fetch(`http://127.0.0.1:8000/delete_url/${shortCode}`, {
            method: "DELETE",
        });
        if (response.ok) {
            SetShortURL(ShortURL.filter((url) => url.new_short_url !== shortCode));
        }
    };

    return (
        <div className="container">
            <h1 className="title">URL Shortener</h1>

            <div className="input-group">
                <input
                    type="text"
                    placeholder="Enter URL:"
                    value={LongURL}
                    onChange={(e) => SetLongURL(e.target.value)}
                    className="input-box"
                />
                <button onClick={ShortenURL} className="shorten-btn">
                    Shorten
                </button>
            </div>

            <div className="url-list">
                {ShortURL.length > 0 && <h2 className="subtitle">New Short URL(s):</h2>}
                {ShortURL.map((url, index) => (
                    <div key={index} className="url-entry">
                        <a
                            href={`http://127.0.0.1:8000/short/${url.new_short_url}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="short-url"
                        >
                            {url.new_short_url}
                        </a>
                        <button
                            onClick={() => DeleteURL(url.new_short_url)}
                            className="delete-btn"
                        >
                            Delete
                        </button>
                    </div>
                ))}
            </div>
        </div>
    );
}
