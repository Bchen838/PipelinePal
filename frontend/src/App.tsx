import Login from './components/Login'
import Dashboard from './components/Dashboard'
import Register from './components/Register'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import ProtectedRoute from './components/ProtectedRoute'


function App() {
  
  return(
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Navigate to='/login' /> } />
        <Route path='/register' element={<Register />} />
        <Route path='/login' element={<Login />} />
        <Route path='/dashboard' element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } />
      </Routes>
    </BrowserRouter>
  )
}

export default App;