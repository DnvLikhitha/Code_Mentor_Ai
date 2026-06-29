import { Link, useNavigate } from 'react-router-dom';
import { Code2, LogOut, User, Layout } from 'lucide-react';
import axios from 'axios';

interface NavbarProps {
  isAuthenticated: boolean;
  setIsAuthenticated: (val: boolean) => void;
}

export default function Navbar({ isAuthenticated, setIsAuthenticated }: NavbarProps) {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await axios.post('http://localhost:5000/logout', {}, { withCredentials: true });
      setIsAuthenticated(false);
      navigate('/');
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <nav className="sticky top-0 z-50 w-full glass border-b border-border/50">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-2 group">
          <div className="p-2 bg-primary/20 rounded-lg group-hover:bg-primary/30 transition-colors">
            <Code2 className="w-6 h-6 text-primary" />
          </div>
          <span className="font-bold text-xl tracking-tight text-foreground">
            CodeMentor AI
          </span>
        </Link>

        <div className="flex items-center space-x-4">
          {isAuthenticated ? (
            <>
              <Link to="/editor" className="text-sm font-medium hover:text-primary transition-colors flex items-center gap-1">
                <Layout className="w-4 h-4" /> Workspace
              </Link>
              <Link to="/challenges" className="text-sm font-medium hover:text-primary transition-colors flex items-center gap-1">
                <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="8" r="7"></circle><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline></svg> Challenges
              </Link>
              <Link to="/profile" className="text-sm font-medium hover:text-primary transition-colors flex items-center gap-1">
                <User className="w-4 h-4" /> Profile
              </Link>
              <button 
                onClick={handleLogout}
                className="text-sm font-medium text-destructive hover:text-destructive/80 transition-colors flex items-center gap-1"
              >
                <LogOut className="w-4 h-4" /> Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="text-sm font-medium hover:text-primary transition-colors">
                Login
              </Link>
              <Link to="/register" className="px-4 py-2 text-sm font-medium bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-all shadow-lg hover:shadow-primary/25">
                Get Started
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
