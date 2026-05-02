import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

function UploadForm() {
  const [form, setForm] = useState({
    ticker: '', company_name: '', quarter: '', year: '', text: ''
  })
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState('')
  const navigate = useNavigate()

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async () => {
    setLoading(true)
    setStatus('Uploading transcript...')
    
    const uploadRes = await axios.post('http://localhost:8000/upload', {
      ...form,
      quarter: parseInt(form.quarter),
      year: parseInt(form.year)
    })
    
    const transcriptId = uploadRes.data.transcript_id
    setStatus('Running analysis... this may take a minute.')
    
    const analyzeRes = await axios.post(
      `http://localhost:8000/analyze/${transcriptId}`
    )
    
    setLoading(false)
    navigate(`/analysis/${analyzeRes.data.analysis_id}`)
  }

  return (
    <div style={{ padding: '2rem' }}>
      <h1>Upload Earnings Call</h1>

      <input name="ticker" placeholder="Ticker e.g. AAPL"
        onChange={handleChange} /><br/><br/>
      <input name="company_name" placeholder="Company Name"
        onChange={handleChange} /><br/><br/>
      <input name="quarter" placeholder="Quarter e.g. 1"
        onChange={handleChange} /><br/><br/>
      <input name="year" placeholder="Year e.g. 2024"
        onChange={handleChange} /><br/><br/>
      <textarea name="text" placeholder="Paste transcript here"
        rows={15} cols={60} onChange={handleChange} /><br/><br/>

      <button onClick={handleSubmit} disabled={loading}>
        {loading ? status : 'Analyze'}
      </button>
    </div>
  )
}

export default UploadForm