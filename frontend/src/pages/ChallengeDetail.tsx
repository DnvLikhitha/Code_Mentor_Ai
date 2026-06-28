import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Code2, ArrowLeft, Play, CheckCircle2, XCircle, Loader2 } from 'lucide-react';
import axios from 'axios';

interface ChallengeData {
  challenge: {
    id: number;
    title: string;
    description: string;
    difficulty: string;
    starter_codes: Record<string, string>;
  };
  progress: {
    attempts: number;
    solved: boolean;
    last_code: string | null;
    last_feedback: string | null;
  };
}

export default function ChallengeDetail() {
  const { id } = useParams();
  const [data, setData] = useState<ChallengeData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState<string | null>(null);
  const [solved, setSolved] = useState(false);

  useEffect(() => {
    fetchChallenge();
  }, [id]);

  const fetchChallenge = async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/challenge/${id}`, { withCredentials: true });
      setData(response.data);
      setSolved(response.data.progress.solved);
      setFeedback(response.data.progress.last_feedback);
      
      if (response.data.progress.last_code) {
        setCode(response.data.progress.last_code);
      } else {
        setCode(response.data.challenge.starter_codes['python'] || '');
      }
    } catch (err) {
      setError('Failed to load challenge details.');
    } finally {
      setLoading(false);
    }
  };

  const handleLanguageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newLang = e.target.value;
    setLanguage(newLang);
    if (data && !data.progress.last_code) {
      setCode(data.challenge.starter_codes[newLang] || '');
    }
  };

  const handleSubmit = async () => {
    if (!code.trim()) return;
    setSubmitting(true);
    setFeedback(null);

    try {
      const response = await axios.post(`http://localhost:5000/api/challenge/${id}`, 
        { code, language },
        { withCredentials: true }
      );
      setFeedback(response.data.feedback);
      setSolved(response.data.solved);
    } catch (err: any) {
      setFeedback('Error: Failed to submit solution. ' + (err.response?.data?.error || ''));
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="flex h-[calc(100vh-4rem)] items-center justify-center"><Loader2 className="w-8 h-8 animate-spin text-primary" /></div>;
  if (error || !data) return <div className="text-center mt-20 text-destructive">{error}</div>;

  const isSuccess = feedback?.includes('ALL PASS') || solved;

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      <Link to="/challenges" className="inline-flex items-center text-sm font-medium text-muted-foreground hover:text-primary transition-colors mb-6">
        <ArrowLeft className="w-4 h-4 mr-2" /> Back to Challenges
      </Link>

      <div className="grid lg:grid-cols-2 gap-8">
        
        {/* Left Column: Description & Feedback */}
        <div className="space-y-6">
          <div className="glass p-8 rounded-2xl">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h1 className="text-3xl font-bold mb-2">{data.challenge.title}</h1>
                <span className={`px-3 py-1 text-xs font-semibold rounded-full border uppercase tracking-wider ${
                  data.challenge.difficulty === 'easy' ? 'text-green-500 border-green-500/20 bg-green-500/10' :
                  data.challenge.difficulty === 'medium' ? 'text-yellow-500 border-yellow-500/20 bg-yellow-500/10' :
                  'text-red-500 border-red-500/20 bg-red-500/10'
                }`}>
                  {data.challenge.difficulty}
                </span>
              </div>
              {solved && (
                <div className="flex items-center gap-2 text-green-500 bg-green-500/10 px-4 py-2 rounded-xl border border-green-500/20">
                  <CheckCircle2 className="w-5 h-5" />
                  <span className="font-bold">Solved</span>
                </div>
              )}
            </div>
            
            <div className="prose prose-invert max-w-none">
              <div dangerouslySetInnerHTML={{ __html: data.challenge.description }} />
            </div>
          </div>

          {feedback && (
            <div className={`glass p-6 rounded-2xl border ${isSuccess ? 'border-green-500/50 bg-green-500/5' : 'border-red-500/50 bg-red-500/5'} animate-in fade-in slide-in-from-bottom-4`}>
              <h3 className={`text-lg font-bold flex items-center gap-2 mb-4 ${isSuccess ? 'text-green-500' : 'text-red-500'}`}>
                {isSuccess ? <CheckCircle2 className="w-5 h-5" /> : <XCircle className="w-5 h-5" />}
                Test Results
              </h3>
              <pre className="whitespace-pre-wrap font-mono text-sm leading-relaxed text-muted-foreground overflow-x-auto">
                {feedback}
              </pre>
            </div>
          )}
        </div>

        {/* Right Column: Code Editor */}
        <div className="space-y-4">
          <div className="glass rounded-2xl overflow-hidden flex flex-col h-[600px] border border-border shadow-2xl">
            
            <div className="flex items-center justify-between px-4 py-3 bg-secondary/50 border-b border-border">
              <div className="flex items-center gap-2 text-muted-foreground">
                <Code2 className="w-5 h-5" />
                <span className="font-medium text-sm">Solution Code</span>
              </div>
              <select
                value={language}
                onChange={handleLanguageChange}
                className="bg-background border border-border text-sm rounded-lg px-3 py-1.5 focus:ring-2 focus:ring-primary outline-none"
              >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="cpp">C++</option>
                <option value="java">Java</option>
                <option value="csharp">C#</option>
              </select>
            </div>

            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="flex-1 w-full bg-background/50 p-6 font-mono text-sm resize-none outline-none focus:bg-background/80 transition-colors"
              spellCheck={false}
              placeholder="Write your solution here..."
            />

            <div className="p-4 bg-secondary/50 border-t border-border flex justify-end">
              <button
                onClick={handleSubmit}
                disabled={submitting}
                className="group relative flex items-center gap-2 px-6 py-2.5 bg-primary text-primary-foreground font-semibold rounded-xl hover:bg-primary/90 transition-all focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-50"
              >
                {submitting ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Play className="w-4 h-4 group-hover:scale-110 transition-transform" fill="currentColor" />
                )}
                {submitting ? 'Running Tests...' : 'Run Tests'}
              </button>
            </div>

          </div>
        </div>

      </div>
    </div>
  );
}
