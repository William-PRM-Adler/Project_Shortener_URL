import {useState, useEffect} from "react";
import {Card, CardContent} from "@/components/ui/card";
import {Button} from "@/components/ui/button"
import {Input} from "@/components/ui/input";

export default function URL_Shortener() {
    const [LongURL, SetLongURL] = useState("");
    const [ShortURL, SetShortURL] = useState([]);
    const ShortenURL = async() => {
        if (!LongURL.trim()) return;
        const response = await fetch("http://127.0.0.1:8000/shorten_url", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({old_long_url: LongURL}),
        });
        if (response.ok) {
            const data = await response.json();
            SetShortURL([...ShortURL, data]);
            SetLongURL("");
        }
    };

    const DeleteURL = async (ShortURL) => {
        const response = await fetch("http://127.0.0.1:8000/delete_url/${ShortURL}", {
            method: "DELETE",
        });
        if (response.ok) {
            SetShortURL(ShortURL.filter((url) => url.new_short_url !== ShortURL));
        }
    };

    return (
        <div className = "flex flex-col items-center p-8">
            <h1 className = "text-2xl font-bold mb-4">URL Shortener</h1>
            <div className = "flex gap-2">
                <Input
                type = "text"
                placeholder = "Enter URL:"
                value = {LongURL}
                onChange = {(e) => SetLongURL(e.target.value)}
                />
                <Button onClick = {ShortenURL}>Shorten</Button>
            </div>
            <div className = "mt-6 w-full max-w-md">
                {ShortURL.length > 0 && <h2 className = "text-lg font-semibold mb-2">New Short URL:</h2>}
                {ShortURL.map((url, index) => (
                    <Card key = {index} className = "flex justify-between p-2 mb-2">
                        <a href = {"http://127.0.0.1:8000/short/${url.new_short_url}"} target = "_blank"></a>
                        <Button variant = "destructive" onClick = {() => DeleteURL(url.new_short_url)}></Button>
                    </Card>
                ))}
            </div>
        </div>
    )
}