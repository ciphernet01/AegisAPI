import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from '@components/Layout'
import Dashboard from '@pages/Dashboard'
import ApiInventory from '@pages/ApiInventory'
import RiskAssessment from '@pages/RiskAssessment'
import Remediations from '@pages/Remediations'
import Settings from '@pages/Settings'

function App() {
  return (
    <Router>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/inventory" element={<ApiInventory />} />
          <Route path="/risk-assessment" element={<RiskAssessment />} />
          <Route path="/remediations" element={<Remediations />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
