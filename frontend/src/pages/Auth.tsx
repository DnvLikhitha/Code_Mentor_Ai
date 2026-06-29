import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Code2, ArrowRight } from 'lucide-react';
import axios from 'axios';

interface AuthProps {
  setIsAuthenticated: (val: boolean) => void;
  isLogin?: boolean;
}

export default function Auth({ setIsAuthenticated, isLogin = true }: AuthProps) {
  const navigate = useNavigate();
  const [isLoginMode, setIsLoginMode] = useState(isLogin);
  const [formData, setFormData] = useState({ name: '', email: '', password: '', confirm: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const endpoint = isLoginMode ? `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/login` : `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/register`;
      const response = await axios.post(endpoint, formData, { withCredentials: true });
      
      if (response.data.success) {
        if (isLoginMode) {
          setIsAuthenticated(true);
          navigate('/profile');
        } else {
          // If registered successfully, switch to login mode
          setIsLoginMode(true);
          setFormData({ ...formData, password: '', confirm: '' });
          alert("Registration successful! Please login.");
        }
      }
    } catch (err: any) {
      setError(err.response?.data?.error || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-[100px] pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/20 rounded-full blur-[100px] pointer-events-none" />

      <div className="max-w-md w-full space-y-8 glass p-10 rounded-2xl relative z-10 animate-in fade-in zoom-in duration-500">
        <div>
          <div className="mx-auto w-12 h-12 bg-primary/20 rounded-xl flex items-center justify-center">
            <Code2 className="w-8 h-8 text-primary" />
          </div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-foreground">
            {isLoginMode ? 'Welcome back' : 'Create an account'}
          </h2>
          <p className="mt-2 text-center text-sm text-muted-foreground">
            {isLoginMode ? "Don't have an account? " : "Already have an account? "}
            <button 
              onClick={() => { setIsLoginMode(!isLoginMode); setError(''); }} 
              className="font-medium text-primary hover:text-primary/80 transition-colors"
            >
              {isLoginMode ? 'Sign up' : 'Sign in'}
            </button>
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-destructive/10 border border-destructive/20 text-destructive text-sm rounded-lg p-3 text-center">
              {error}
            </div>
          )}
          
          <div className="space-y-4">
            {!isLoginMode && (
              <div>
                <label className="text-sm font-medium">Name</label>
                <input
                  name="name"
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full mt-1 px-4 py-2 bg-background border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all"
                  placeholder="John Doe"
                />
              </div>
            )}
            <div>
              <label className="text-sm font-medium">Email address</label>
              <input
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                className="w-full mt-1 px-4 py-2 bg-background border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all"
                placeholder="you@example.com"
              />
            </div>
            <div>
              <label className="text-sm font-medium">Password</label>
              <input
                name="password"
                type="password"
                required
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                className="w-full mt-1 px-4 py-2 bg-background border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all"
                placeholder="••••••••"
              />
            </div>
            {!isLoginMode && (
              <div>
                <label className="text-sm font-medium">Confirm Password</label>
                <input
                  name="confirm"
                  type="password"
                  required
                  value={formData.confirm}
                  onChange={(e) => setFormData({...formData, confirm: e.target.value})}
                  className="w-full mt-1 px-4 py-2 bg-background border border-border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all"
                  placeholder="••••••••"
                />
              </div>
            )}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full group relative flex justify-center items-center gap-2 py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-primary-foreground bg-primary hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all disabled:opacity-50"
          >
            {loading ? 'Processing...' : (isLoginMode ? 'Sign in' : 'Sign up')}
            {!loading && <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />}
          </button>
        </form>
      </div>
    </div>
  );
}
