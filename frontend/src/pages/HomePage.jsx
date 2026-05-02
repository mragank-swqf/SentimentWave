import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

function HomePage() {
  const [transcripts, setTranscripts] = useState([])
  const navigate = useNavigate()

  useEffect(() => {
    axios.get('http://localhost:8000/transcripts')
      .then(res => setTranscripts(res.data))
  }, [])

  return (
    <div style={{ padding: '2rem' }}>
      <h1>SentimentWave</h1>
      <p>Earnings Call Sentiment Analysis Platform</p>
      <button onClick={() => navigate('/upload')}>
        + Upload Transcript
      </button>

      <h2>Past Analyses</h2>
      <table border="1" cellPadding="8">
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Company</th>
            <th>Quarter</th>
            <th>Year</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {transcripts.map(t => (
            <tr key={t.id}>
              <td>{t.ticker}</td>
              <td>{t.company_name}</td>
              <td>Q{t.quarter}</td>
              <td>{t.year}</td>
              <td>
                <button onClick={() => navigate(`/analysis/${t.id}`)}>
                  View
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default HomePage