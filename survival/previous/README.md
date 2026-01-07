To run the backend: python backend.py
To query the backend:
curl -XPOST -H "Content-type: application/json" http://localhost:5000/api/tasks -d '{"task":"mytask"}'
curl http://localhost:5000/api/tasks
curl -XDELETE -H "Content-type: application/json" http://localhost:5000/api/tasks -d '{"task":"mytask"}'

To run the frontend: REACT_APP_API_URL=http://localhost:5000 npm start
