import { useState, useEffect } from 'react';
import { User, Code2, Loader2, Trophy, Clock, Moon, Sun, Target, Activity, Star, CheckCircle2, XCircle, Trash2 } from 'lucide-react';
import axios from 'axios';

interface ProfileData {
  user: { id: number; name: string; email: string; preferences: string };
  snippets: any[];
  solved_count: number;
}

interface ProgressData {
  stats: {
    solved: number;
    attempting: number;
    total: number;
    easy: { solved: number; total: number };
    medium: { solved: number; total: number };
    hard: { solved: number; total: number };
  };
  recent_activity: any[];
}

export default function Profile() {
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [progress, setProgress] = useState<ProgressData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [profileRes, progressRes] = await Promise.all([
        axios.get('http://localhost:5000/api/profile', { withCredentials: true }),
        axios.get('http://localhost:5000/api/my_progress', { withCredentials: true })
      ]);
      setProfile(profileRes.data);
      setProgress(progressRes.data);
      setTheme(profileRes.data.user.preferences);
      if (profileRes.data.user.preferences === 'dark') {
        document.documentElement.classList.add('dark');
      }
    } catch (err) {
      setError('Failed to load profile data.');
    } finally {
      setLoading(false);
    }
  };

  const toggleTheme = async () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    try {
      await axios.post('http://localhost:5000/api/user/theme', { theme: newTheme }, { withCredentials: true });
      setTheme(newTheme);
      if (newTheme === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
    } catch (err) {
      console.error('Failed to update theme');
    }
  };

  const deleteSnippet = async (id: number) => {
    if (!window.confirm("Are you sure you want to delete this snippet?")) return;
    try {
      await axios.delete(`http://localhost:5000/delete_snippet/${id}`, { withCredentials: true });
      if (profile) {
        setProfile({
          ...profile,
          snippets: profile.snippets.filter(s => s.id !== id)
        });
      }
    } catch (err) {
      console.error("Failed to delete snippet", err);
    }
  };

  if (loading) return <div className="flex h-[calc(100vh-4rem)] items-center justify-center"><Loader2 className="w-12 h-12 animate-spin text-primary" /></div>;
  if (error || !profile || !progress) return <div className="text-center mt-20 text-destructive">{error}</div>;

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      
      {/* Banner / Header */}
      <div className="glass rounded-3xl overflow-hidden mb-12 relative">
        <div className="p-8 md:p-12 flex flex-col md:flex-row items-center gap-8 relative z-10">
          <div className="w-24 h-24 rounded-2xl bg-secondary border border-border flex items-center justify-center flex-shrink-0">
            <User className="w-10 h-10 text-foreground" />
          </div>
          
          <div className="flex-1 text-center md:text-left">
            <h1 className="text-4xl md:text-5xl font-bold text-foreground tracking-tight mb-2">
              {profile.user.name}
            </h1>
            <p className="text-muted-foreground text-lg flex items-center justify-center md:justify-start gap-2">
              {profile.user.email}
            </p>
          </div>

          <div className="flex gap-4">
            <button onClick={toggleTheme} className="p-3 bg-secondary hover:bg-secondary/80 border border-border rounded-xl text-foreground transition-all">
              {theme === 'dark' ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-8">
        
        {/* Left Column: Stats */}
        <div className="lg:col-span-1 space-y-8">
          
          {/* Main Stats Cards */}
          <div className="grid grid-cols-2 gap-4">
            <div className="glass p-6 rounded-2xl flex flex-col items-center justify-center text-center">
              <div className="p-3 bg-secondary text-foreground rounded-lg mb-3">
                <Trophy className="w-6 h-6" />
              </div>
              <h3 className="text-3xl font-bold">{progress.stats.solved}</h3>
              <p className="text-sm text-muted-foreground font-medium uppercase tracking-wide">Solved</p>
            </div>
            
            <div className="glass p-6 rounded-2xl flex flex-col items-center justify-center text-center">
              <div className="p-3 bg-secondary text-foreground rounded-lg mb-3">
                <Target className="w-6 h-6" />
              </div>
              <h3 className="text-3xl font-bold">{progress.stats.attempting}</h3>
              <p className="text-sm text-muted-foreground font-medium uppercase tracking-wide">Attempting</p>
            </div>
          </div>

          {/* Difficulty Progress */}
          <div className="glass p-6 rounded-2xl border border-border shadow-lg">
            <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
              <Star className="w-5 h-5 text-primary" /> Skill Breakdown
            </h3>
            
            <div className="space-y-5">
              {/* Easy */}
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-semibold text-foreground">Easy</span>
                  <span className="text-muted-foreground">{progress.stats.easy.solved} / {progress.stats.easy.total}</span>
                </div>
                <div className="h-2 bg-secondary rounded-full overflow-hidden">
                  <div className="h-full bg-foreground rounded-full transition-all duration-1000" style={{ width: `${progress.stats.easy.total ? (progress.stats.easy.solved / progress.stats.easy.total) * 100 : 0}%` }} />
                </div>
              </div>

              {/* Medium */}
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-semibold text-foreground">Medium</span>
                  <span className="text-muted-foreground">{progress.stats.medium.solved} / {progress.stats.medium.total}</span>
                </div>
                <div className="h-2 bg-secondary rounded-full overflow-hidden">
                  <div className="h-full bg-foreground rounded-full transition-all duration-1000" style={{ width: `${progress.stats.medium.total ? (progress.stats.medium.solved / progress.stats.medium.total) * 100 : 0}%` }} />
                </div>
              </div>

              {/* Hard */}
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-semibold text-foreground">Hard</span>
                  <span className="text-muted-foreground">{progress.stats.hard.solved} / {progress.stats.hard.total}</span>
                </div>
                <div className="h-2 bg-secondary rounded-full overflow-hidden">
                  <div className="h-full bg-foreground rounded-full transition-all duration-1000" style={{ width: `${progress.stats.hard.total ? (progress.stats.hard.solved / progress.stats.hard.total) * 100 : 0}%` }} />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Content */}
        <div className="lg:col-span-2 space-y-8">
          
          {/* Recent Activity */}
          <div className="glass p-6 rounded-2xl border border-border shadow-lg">
            <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
              <Activity className="w-5 h-5 text-primary" /> Recent Activity
            </h3>
            
            <div className="space-y-4">
              {progress.recent_activity.length === 0 ? (
                <div className="text-center p-6 text-muted-foreground border border-dashed border-border rounded-xl">
                  No activity yet. Start solving challenges!
                </div>
              ) : (
                progress.recent_activity.map((act, i) => (
                  <div key={i} className="flex items-center gap-4 p-4 rounded-xl bg-card border border-border hover:bg-secondary/50 transition-colors">
                    <div className={`p-2 rounded-lg bg-secondary text-foreground`}>
                      {act.solved ? <CheckCircle2 className="w-5 h-5" /> : <XCircle className="w-5 h-5" />}
                    </div>
                    <div className="flex-1">
                      <h4 className="font-semibold text-foreground">{act.challenge_title}</h4>
                      <p className="text-xs text-muted-foreground">
                        {act.solved ? 'Successfully solved' : `Attempted ${act.attempts} times`}
                      </p>
                    </div>
                    <div className="text-xs text-muted-foreground font-medium">
                      {new Date(act.updated_at).toLocaleDateString()}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Saved Snippets */}
          <div>
            <h3 className="text-xl font-bold mb-4 flex items-center gap-2 px-2">
              <Code2 className="w-5 h-5 text-primary" /> Saved Snippets
            </h3>

            <div className="grid gap-4">
              {profile.snippets.length === 0 ? (
                <div className="glass p-12 rounded-2xl text-center text-muted-foreground border-dashed border-border flex flex-col items-center">
                  <div className="w-16 h-16 bg-secondary rounded-full flex items-center justify-center mb-4">
                    <Code2 className="w-8 h-8 opacity-50" />
                  </div>
                  <p className="text-lg font-medium">No snippets saved</p>
                  <p className="text-sm mt-1">Go to the Workspace and save your AI-generated code!</p>
                </div>
              ) : (
                profile.snippets.map((snippet) => (
                  <div key={snippet.id} className="glass p-5 rounded-2xl group border border-border hover:border-primary/50 transition-all shadow-md min-w-0">
                    <div className="flex justify-between items-center mb-4">
                      <span className="px-3 py-1 bg-primary/10 text-primary text-xs font-bold rounded-full uppercase tracking-wider">
                        {snippet.language}
                      </span>
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-muted-foreground flex items-center gap-1 font-medium bg-secondary px-2 py-1 rounded-md">
                          <Clock className="w-3 h-3" />
                          Saved Snippet
                        </span>
                        <button 
                          onClick={() => deleteSnippet(snippet.id)}
                          className="p-1.5 text-muted-foreground hover:text-red-500 hover:bg-red-500/10 rounded-md transition-colors"
                          title="Delete snippet"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                    <pre className="bg-background p-4 rounded-xl overflow-x-auto text-sm font-mono border border-border shadow-inner text-foreground whitespace-pre-wrap word-break break-all">
                      <code>{typeof snippet.code === 'string' ? snippet.code.replace(/\\n/g, '\n') : snippet.code}</code>
                    </pre>
                    {snippet.explanation && (
                      <div className="mt-4 p-4 bg-primary/5 rounded-xl text-sm border border-primary/20 text-foreground">
                        {snippet.explanation}
                      </div>
                    )}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
        
      </div>
    </div>
  );
}
