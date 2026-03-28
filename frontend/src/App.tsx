import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from '@components/Layout'
import Dashboard from '@pages/Dashboard'
import ApiInventory from '@pages/ApiInventory'
import RiskAssessment from '@pages/RiskAssessment'
import Remediation from '@pages/Remediation'
import Analytics from '@pages/Analytics'
import ZombieDetection from '@pages/ZombieDetection'
import Settings from '@pages/Settings'
import Profile from '@pages/Profile'

function App() {
  return (
    <Router>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/inventory" element={<ApiInventory />} />
          <Route path="/risk-assessment" element={<RiskAssessment />} />
          <Route path="/zombie-detection" element={<ZombieDetection />} />
          <Route path="/remediation" element={<Remediation />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/profile" element={<Profile />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
