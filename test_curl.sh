curl -X POST http://localhost:8080/chat \
     -H "Content-Type: application/json" \
     -d '{"thread_id": "thread_oqfCnPxWXQyJzqB5CErB02CS", "message": "Hello there!"}'


curl -X POST https://flask-openai-probe.onrender.com/chat \
     -H "Content-Type: application/json" \
     -d '{"thread_id": "thread_C8Z6l2Munb51gaa4acvx5Ti8", "message": "Kas saaksid anada ka terviselehele linke, et ma saaks ise edasi veebis lugeda?"}'
