import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Auth from './pages/Auth';
import Profile from './pages/Profile';
import Challenges from './pages/Challenges';
import ChallengeDetail from './pages/ChallengeDetail';
import Editor from './pages/Editor';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const isNewSession = !sessionStorage.getItem('session_active');
    
    if (isNewSession) {
      // Force logout on the backend because they just opened a new tab/window
      axios.post(`${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/logout`, {}, { withCredentials: true })
        .finally(() => {
          sessionStorage.setItem('session_active', 'true');
          setIsAuthenticated(false);
          setLoading(false);
        });
    } else {
      // Normal auth check
      axios.get(`${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/auth/me`, { withCredentials: true })
        .then(response => {
          if (response.data.authenticated) {
            setIsAuthenticated(true);
          }
        })
        .catch(() => {
          setIsAuthenticated(false);
        })
        .finally(() => {
          setLoading(false);
        });
    }
  }, []);

  if (loading) {
    return <div className="h-screen w-screen flex items-center justify-center bg-background text-foreground">Loading...</div>;
  }

  return (
    <Router>
      <div className="min-h-screen bg-background text-foreground selection:bg-primary/30">
        <Navbar isAuthenticated={isAuthenticated} setIsAuthenticated={setIsAuthenticated} />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={!isAuthenticated ? <Auth setIsAuthenticated={setIsAuthenticated} isLogin={true} /> : <Navigate to="/profile" />} />
          <Route path="/register" element={!isAuthenticated ? <Auth setIsAuthenticated={setIsAuthenticated} isLogin={false} /> : <Navigate to="/profile" />} />
          <Route path="/profile" element={isAuthenticated ? <Profile /> : <Navigate to="/login" />} />
          <Route path="/challenges" element={isAuthenticated ? <Challenges /> : <Navigate to="/login" />} />
          <Route path="/challenge/:id" element={isAuthenticated ? <ChallengeDetail /> : <Navigate to="/login" />} />
          <Route path="/editor" element={isAuthenticated ? <Editor /> : <Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}
