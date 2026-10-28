import httpx
import json
import time

def test_stream():
    client = httpx.Client(trust_env=False, timeout=40)
    url = "http://127.0.0.1:8501/api/stream?query=B0BS1QCFHX&market=US&provider=groq&model=openai/gpt-oss-120b"

    t0 = time.time()
    print("Connecting to SSE stream...")
    events_received = []

    with client.stream("GET", url) as response:
        assert response.status_code == 200
        print("HTTP Status 200 OK")
        buffer = ""
        for text in response.iter_text():
            buffer += text
            while "\n\n" in buffer:
                event_raw, buffer = buffer.split("\n\n", 1)
                event_raw = event_raw.strip()
                if event_raw.startswith("data: "):
                    payload = json.loads(event_raw[6:])
                    events_received.append(payload)
                    elapsed = round(time.time() - t0, 1)
                    print(f"[{elapsed}s] Event: {payload.get('type')} | Node: {payload.get('node')}")
                    if payload.get("type") == "done":
                        print("Done event received successfully!")
                        break
            if events_received and events_received[-1].get("type") == "done":
                break

    print("Total events received:", len(events_received))
    assert any(e.get("type") == "connected" for e in events_received), "Missing connected event"
    assert any(e.get("node") == "planner" for e in events_received), "Missing planner event"
    assert any(e.get("node") == "researcher" for e in events_received), "Missing researcher event"
    assert any(e.get("node") == "critic" for e in events_received), "Missing critic event"
    assert any(e.get("node") == "synthesizer" for e in events_received), "Missing synthesizer event"
    assert any(e.get("type") == "done" for e in events_received), "Missing done event"
    print(">>> ALL 5 NODES & SSE STREAM VERIFIED SUCCESSFULLY! <<<")

if __name__ == "__main__":
    test_stream()
