import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Layout from '@components/Layout'
import ProtectedRoute from '@components/ProtectedRoute'
import Dashboard from '@pages/Dashboard'
import ApiInventory from '@pages/ApiInventory'
import RiskAssessment from '@pages/RiskAssessment'
import Remediations from '@pages/Remediations'
import Settings from '@pages/Settings'
import Login from '@pages/Login'
import Profile from '@pages/Profile'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          element={(
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          )}
        >
          <Route path="/" element={<Dashboard />} />
          <Route path="/inventory" element={<ApiInventory />} />
          <Route path="/risk-assessment" element={<RiskAssessment />} />
          <Route path="/remediations" element={<Remediations />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/profile" element={<Profile />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  )
}

export default App
